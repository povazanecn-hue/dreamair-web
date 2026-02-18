from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, Field


# ============== Chat Models ==============
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    response: str


# ============== Reservation Models ==============
class ReservationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class ReservationType(str, Enum):
    INSPECTION = "inspection"  # Obhliadka
    INSTALLATION = "installation"  # Montáž
    SERVICE = "service"  # Servis


class ReservationRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str
    phone: str = Field(..., min_length=9, max_length=20)
    address: str = Field(..., min_length=5, max_length=200)
    reservation_type: ReservationType = ReservationType.INSPECTION
    preferred_date: str  # ISO format date
    preferred_time: str  # e.g. "09:00-12:00"
    message: Optional[str] = None
    selected_products: Optional[List[str]] = None


class Reservation(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    address: str
    reservation_type: ReservationType
    preferred_date: str
    preferred_time: str
    message: Optional[str]
    selected_products: Optional[List[str]]
    status: ReservationStatus
    created_at: str
    updated_at: str
    admin_note: Optional[str] = None


class ReservationUpdate(BaseModel):
    status: Optional[ReservationStatus] = None
    admin_note: Optional[str] = None


# In-memory storage (pre produkciu použi databázu)
reservations_db: Dict[str, Reservation] = {}


SMARTAIR_SYSTEM_PROMPT = """Si Smartesko, priateľský AI asistent spoločnosti SmartAir - profesionálnej firmy na klimatizácie a vzduchotechniku v Bratislave.

## O SmartAir:
- Sídlo: Bratislava, Slovensko
- Telefón: +421 915 033 440
- Služby: projektovanie, certifikovaná montáž, záručný a pozáručný servis, diagnostika, čistenie a dezinfekcia klimatizácií

## Produkty a značky:
- Klimatizácie: Daikin, Samsung, Midea, Vivax, Inventor, TCL
- Tepelné čerpadlá pre úsporu energie
- Rekuperácie a vzduchotechnika
- Čističky vzduchu a odvlhčovače
- Chladiace zariadenia pre gastro

## Výhody SmartAir:
- Montáž možná do 48 hodín
- Cena montáže je súčasťou ponuky
- Služby pre domácnosti aj firmy
- Profesionálny tím certifikovaných technikov

## Ako odpovedať:
1. Buď priateľský a používaj slovenčinu
2. Odpovedaj stručne ale výstižne (max 2-3 vety)
3. Pri otázkach o cenách odporúčaj kontaktovať nás pre presnú ponuku
4. Pri technických otázkach poskytni základné info a ponúkni konzultáciu
5. Vždy ponúkni možnosť zavolať na +421 915 033 440 alebo využiť online formulár
6. Nehovor že si AI alebo chatbot - si Smartesko, asistent SmartAir"""


def _load_config() -> Dict[str, Any]:
    """Load config.json from repo root and expand env placeholders like ${VAR}.

    Returns an empty dict if the file is missing or invalid.
    """
    try:
        repo_root = Path(__file__).resolve().parents[1]
        cfg_path = repo_root / "config.json"
        raw = cfg_path.read_text(encoding="utf-8")
        expanded = os.path.expandvars(raw)
        return json.loads(expanded)
    except FileNotFoundError:
        return {}
    except Exception:
        # Keep the app resilient even if config is malformed
        return {}


config = _load_config()

cors_origins: List[str] = config.get("cors_origins", ["*"])

app = FastAPI(title="SmartAir API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "SmartAir API"}


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Smartesko AI chat endpoint using Gemini."""
    api_key = config.get("gemini_api_key", "")

    if not api_key or api_key.startswith("${"):
        raise HTTPException(status_code=500, detail="Gemini API key not configured")

    # Build conversation for Gemini
    contents = []

    # Add history if provided
    if request.history:
        for msg in request.history:
            role = "user" if msg.role == "user" else "model"
            contents.append({"role": role, "parts": [{"text": msg.content}]})

    # Add current message
    contents.append({"role": "user", "parts": [{"text": request.message}]})

    # Gemini API request
    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    payload = {
        "contents": contents,
        "systemInstruction": {"parts": [{"text": SMARTAIR_SYSTEM_PROMPT}]},
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 500,
            "topP": 0.9
        }
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(gemini_url, json=payload)
            resp.raise_for_status()
            data = resp.json()

            # Extract response text
            response_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return ChatResponse(response=response_text)

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=502, detail=f"Gemini API error: {e.response.status_code}")
        except (KeyError, IndexError):
            raise HTTPException(status_code=502, detail="Invalid response from Gemini API")
        except httpx.RequestError as e:
            raise HTTPException(status_code=502, detail=f"Connection error: {str(e)}")


# ============== Reservation Endpoints ==============

@app.post("/reservations", response_model=Reservation)
async def create_reservation(request: ReservationRequest) -> Reservation:
    """Vytvorí novú rezerváciu obhliadky."""
    reservation_id = str(uuid.uuid4())[:8]
    now = datetime.now().isoformat()

    reservation = Reservation(
        id=reservation_id,
        name=request.name,
        email=request.email,
        phone=request.phone,
        address=request.address,
        reservation_type=request.reservation_type,
        preferred_date=request.preferred_date,
        preferred_time=request.preferred_time,
        message=request.message,
        selected_products=request.selected_products,
        status=ReservationStatus.PENDING,
        created_at=now,
        updated_at=now,
    )

    reservations_db[reservation_id] = reservation
    return reservation


@app.get("/reservations", response_model=List[Reservation])
async def list_reservations(
    status: Optional[ReservationStatus] = None,
    limit: int = Query(default=50, le=100),
) -> List[Reservation]:
    """Zoznam všetkých rezervácií (pre admin)."""
    reservations = list(reservations_db.values())

    if status:
        reservations = [r for r in reservations if r.status == status]

    # Sort by created_at descending
    reservations.sort(key=lambda r: r.created_at, reverse=True)
    return reservations[:limit]


@app.get("/reservations/{reservation_id}", response_model=Reservation)
async def get_reservation(reservation_id: str) -> Reservation:
    """Získaj detail rezervácie."""
    if reservation_id not in reservations_db:
        raise HTTPException(status_code=404, detail="Rezervácia nenájdená")
    return reservations_db[reservation_id]


@app.patch("/reservations/{reservation_id}", response_model=Reservation)
async def update_reservation(
    reservation_id: str, update: ReservationUpdate
) -> Reservation:
    """Aktualizuj stav rezervácie (schváliť/zamietnuť)."""
    if reservation_id not in reservations_db:
        raise HTTPException(status_code=404, detail="Rezervácia nenájdená")

    reservation = reservations_db[reservation_id]

    if update.status:
        reservation.status = update.status
    if update.admin_note is not None:
        reservation.admin_note = update.admin_note

    reservation.updated_at = datetime.now().isoformat()
    reservations_db[reservation_id] = reservation
    return reservation


@app.delete("/reservations/{reservation_id}")
async def delete_reservation(reservation_id: str) -> Dict[str, str]:
    """Vymaž rezerváciu."""
    if reservation_id not in reservations_db:
        raise HTTPException(status_code=404, detail="Rezervácia nenájdená")
    del reservations_db[reservation_id]
    return {"message": "Rezervácia vymazaná"}


# ============== Admin Panel ==============

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel() -> str:
    """Admin panel pre správu rezervácií."""
    return """
<!DOCTYPE html>
<html lang="sk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartAir Admin - Rezervácie</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            min-height: 100vh;
        }
        .header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 { font-size: 24px; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .filters {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .filter-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }
        .filter-btn.active { background: #3b82f6; color: white; }
        .filter-btn:not(.active) { background: white; color: #333; }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .stat-card h3 { font-size: 32px; color: #3b82f6; }
        .stat-card p { color: #666; font-size: 14px; }
        .reservations { display: flex; flex-direction: column; gap: 16px; }
        .reservation-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 16px;
            align-items: start;
        }
        .reservation-info h3 { margin-bottom: 8px; color: #1a1a2e; }
        .reservation-info p { color: #666; margin: 4px 0; font-size: 14px; }
        .reservation-info .label { font-weight: 600; color: #333; }
        .status-badge {
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .status-pending { background: #fef3c7; color: #92400e; }
        .status-approved { background: #d1fae5; color: #065f46; }
        .status-rejected { background: #fee2e2; color: #991b1b; }
        .status-completed { background: #dbeafe; color: #1e40af; }
        .actions { display: flex; gap: 8px; flex-wrap: wrap; }
        .btn {
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.2s;
        }
        .btn-approve { background: #10b981; color: white; }
        .btn-reject { background: #ef4444; color: white; }
        .btn-complete { background: #3b82f6; color: white; }
        .btn:hover { opacity: 0.9; transform: translateY(-1px); }
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #666;
        }
        .type-badge {
            display: inline-block;
            padding: 4px 8px;
            background: #e5e7eb;
            border-radius: 4px;
            font-size: 12px;
            margin-left: 8px;
        }
        @media (max-width: 768px) {
            .reservation-card { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏠 SmartAir Admin</h1>
        <span id="refresh-time">Posledná aktualizácia: -</span>
    </div>

    <div class="container">
        <div class="stats">
            <div class="stat-card">
                <h3 id="stat-pending">0</h3>
                <p>Čakajúce</p>
            </div>
            <div class="stat-card">
                <h3 id="stat-approved">0</h3>
                <p>Schválené</p>
            </div>
            <div class="stat-card">
                <h3 id="stat-completed">0</h3>
                <p>Dokončené</p>
            </div>
            <div class="stat-card">
                <h3 id="stat-total">0</h3>
                <p>Celkom</p>
            </div>
        </div>

        <div class="filters">
            <button class="filter-btn active" data-status="">Všetky</button>
            <button class="filter-btn" data-status="pending">Čakajúce</button>
            <button class="filter-btn" data-status="approved">Schválené</button>
            <button class="filter-btn" data-status="rejected">Zamietnuté</button>
            <button class="filter-btn" data-status="completed">Dokončené</button>
        </div>

        <div class="reservations" id="reservations-list">
            <div class="empty-state">Načítavam rezervácie...</div>
        </div>
    </div>

    <script>
        const API_BASE = window.location.origin;
        let currentFilter = '';

        const typeLabels = {
            'inspection': 'Obhliadka',
            'installation': 'Montáž',
            'service': 'Servis'
        };

        async function loadReservations() {
            try {
                const url = currentFilter
                    ? `${API_BASE}/reservations?status=${currentFilter}`
                    : `${API_BASE}/reservations`;

                const resp = await fetch(url);
                const data = await resp.json();

                renderReservations(data);
                updateStats(data);
                document.getElementById('refresh-time').textContent =
                    `Posledná aktualizácia: ${new Date().toLocaleTimeString('sk')}`;
            } catch (err) {
                console.error('Error loading reservations:', err);
            }
        }

        function updateStats(reservations) {
            const pending = reservations.filter(r => r.status === 'pending').length;
            const approved = reservations.filter(r => r.status === 'approved').length;
            const completed = reservations.filter(r => r.status === 'completed').length;

            document.getElementById('stat-pending').textContent = pending;
            document.getElementById('stat-approved').textContent = approved;
            document.getElementById('stat-completed').textContent = completed;
            document.getElementById('stat-total').textContent = reservations.length;
        }

        function renderReservations(reservations) {
            const container = document.getElementById('reservations-list');

            if (reservations.length === 0) {
                container.innerHTML = '<div class="empty-state">Žiadne rezervácie</div>';
                return;
            }

            container.innerHTML = reservations.map(r => `
                <div class="reservation-card">
                    <div class="reservation-info">
                        <h3>
                            ${r.name}
                            <span class="type-badge">${typeLabels[r.reservation_type] || r.reservation_type}</span>
                        </h3>
                        <p><span class="label">📅 Termín:</span> ${r.preferred_date} (${r.preferred_time})</p>
                        <p><span class="label">📍 Adresa:</span> ${r.address}</p>
                        <p><span class="label">📞 Telefón:</span> <a href="tel:${r.phone}">${r.phone}</a></p>
                        <p><span class="label">✉️ Email:</span> <a href="mailto:${r.email}">${r.email}</a></p>
                        ${r.selected_products && r.selected_products.length ? `<p><span class="label">🧾 Produkty:</span> ${r.selected_products.join(', ')}</p>` : ''}
                        ${r.message ? `<p><span class="label">💬 Správa:</span> ${r.message}</p>` : ''}
                        ${r.admin_note ? `<p><span class="label">📝 Poznámka:</span> ${r.admin_note}</p>` : ''}
                        <p style="color:#999; font-size:12px; margin-top:8px;">ID: ${r.id} | Vytvorené: ${new Date(r.created_at).toLocaleString('sk')}</p>
                    </div>
                    <div>
                        <span class="status-badge status-${r.status}">${r.status}</span>
                        <div class="actions" style="margin-top:12px;">
                            ${r.status === 'pending' ? `
                                <button class="btn btn-approve" onclick="updateStatus('${r.id}', 'approved')">✓ Schváliť</button>
                                <button class="btn btn-reject" onclick="updateStatus('${r.id}', 'rejected')">✗ Zamietnuť</button>
                            ` : ''}
                            ${r.status === 'approved' ? `
                                <button class="btn btn-complete" onclick="updateStatus('${r.id}', 'completed')">✓ Dokončené</button>
                            ` : ''}
                        </div>
                    </div>
                </div>
            `).join('');
        }

        async function updateStatus(id, status) {
            try {
                await fetch(`${API_BASE}/reservations/${id}`, {
                    method: 'PATCH',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ status })
                });
                loadReservations();
            } catch (err) {
                alert('Chyba pri aktualizácii');
            }
        }

        // Filter buttons
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                currentFilter = btn.dataset.status;
                loadReservations();
            });
        });

        // Initial load and auto-refresh
        loadReservations();
        setInterval(loadReservations, 30000);
    </script>
</body>
</html>
"""
