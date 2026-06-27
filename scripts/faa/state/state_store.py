"""Gerenciador de estado do sistema"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

def save_state(state: Dict, path: Path) -> None:
    """Persiste estado em JSON"""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    snapshot = {
        "version": "2.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        **state
    }
    
    with open(path, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, ensure_ascii=False)

def load_state(path: Path) -> Dict | None:
    """Carrega último estado"""
    if not path.exists():
        return None
    
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_snapshot(state: Dict, snapshot_dir: Path) -> None:
    """Salva snapshot com timestamp"""
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    snapshot_path = snapshot_dir / f"faa-snapshot-{timestamp}.json"
    
    with open(snapshot_path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
