"""Analisador de estrutura arquitetural"""
from pathlib import Path
from typing import Dict, List
from core.scanner import FileNode

def analyze_structure(nodes: List[FileNode], root: Path) -> Dict:
    """Analisa estrutura do sistema"""
    
    structure = {
        "documentation": 0,
        "data": 0,
        "schema": 0,
        "automation": 0,
        "other": 0
    }
    
    for node in nodes:
        structure[node.category] = structure.get(node.category, 0) + 1
    
    # Verifica diretórios obrigatórios
    from config import CONFIG
    missing_dirs = []
    for d in CONFIG.dirs_required:
        if not (root / d).exists():
            missing_dirs.append(d)
    
    # Verifica arquivos críticos
    missing_files = []
    for f in CONFIG.critical_files:
        if not (root / f).exists():
            missing_files.append(f)
    
    return {
        "files_by_category": structure,
        "total_files": len(nodes),
        "missing_dirs": missing_dirs,
        "missing_critical_files": missing_files,
        "health": "CRITICAL" if missing_files else ("WARNING" if missing_dirs else "OK")
    }
