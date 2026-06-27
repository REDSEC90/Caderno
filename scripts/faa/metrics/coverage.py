"""Métricas do sistema"""
from typing import List, Dict

def compute_metrics(nodes: List, issues: Dict, structure: Dict) -> Dict:
    """Calcula métricas globais do sistema"""
    
    total = len(nodes)
    total_issues = issues["counts"]["critical"] + issues["counts"]["warnings"]
    
    # Score global (100 - % de problemas)
    score = max(0, 100 - (total_issues / max(total, 1) * 100)) if total > 0 else 0
    
    # Integridade estrutural
    integrity = 100.0
    if structure["missing_critical_files"]:
        integrity -= len(structure["missing_critical_files"]) * 20
    if structure["missing_dirs"]:
        integrity -= len(structure["missing_dirs"]) * 10
    
    integrity = max(0, integrity)
    
    # Decisão arquitetural
    if issues["counts"]["critical"] > 0:
        decision = "BLOCKED"
    elif issues["counts"]["warnings"] > 5:
        decision = "DEGRADED"
    else:
        decision = "APPROVED"
    
    return {
        "score": round(score, 2),
        "integrity": round(integrity, 2),
        "decision": decision,
        "total_files": total,
        "health": structure["health"],
        "coverage": {
            "documentation": structure["files_by_category"].get("documentation", 0),
            "data": structure["files_by_category"].get("data", 0),
            "schema": structure["files_by_category"].get("schema", 0)
        }
    }
