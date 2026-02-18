# SmartAir

Minimal FastAPI backend with deployment scripts and tests.

## Development Setup

### Prerequisites

- Python 3.11+ (recommended: Python 3.12 or 3.13)
- VS Code with recommended extensions (will be suggested on first open)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/povazanecn-hue/SmartAir.git
   cd SmartAir
   ```

2. **Create and activate virtual environment:**

   **Windows (PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Open in VS Code:**
   ```bash
   code .
   ```
   - Install recommended extensions when prompted
   - Select Python interpreter: `.venv/Scripts/python.exe` (Windows) or `.venv/bin/python` (Unix)

## Run Locally

- **Start API:** `python -m uvicorn app.main:app --reload --port 8000`
- **Run tests:** `python -m pytest -q`

## VS Code Features

### Tasks (Ctrl+Shift+P → "Tasks: Run Task")
- **Install Dependencies** - Install all Python packages
- **Tests: Pytest** - Run tests (default test task)
- **Tests: Pytest (verbose)** - Run tests with detailed output
- **API: Start (uvicorn)** - Start the development server

### Debug Configurations (F5)
- **Python: FastAPI (uvicorn)** - Debug the API server with breakpoints
- **Python: Current File** - Debug the currently open Python file
- **Python: Pytest** - Debug tests with breakpoints
- **PowerShell: Launch Current File** - Run PowerShell scripts

### Keyboard Shortcuts
- `F5` - Start debugging
- `Ctrl+Shift+B` - Run build task
- `Ctrl+Shift+P` - Command palette

## Project Structure

```
SmartAir/
├── app/
│   └── main.py          # FastAPI application
├── tests/
│   └── test_health.py   # API tests
├── deploy/              # VPS deployment scripts
├── .vscode/             # VS Code configuration
├── config.json          # Runtime configuration (uses ${ENV_VARS})
└── requirements.txt     # Python dependencies
```

## Deployment (VPS)

- See `deploy/README.md` and `deploy/vps_bootstrap.sh`
- Nginx proxies `api.smartair.space`; static files under `/var/www/smartair` for `images.smartair.space`

## Notes

- Config uses env-first, with `config.json` as fallback (expands ${VARS})
- Line endings: `.gitattributes` enforces LF for shell scripts
