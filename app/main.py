from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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
