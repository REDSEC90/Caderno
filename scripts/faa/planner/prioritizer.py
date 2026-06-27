"""Planejador de ações corretivas"""
from typing import List, Dict

def generate_plan(issues: Dict) -> List[Dict]:
    """Converte issues em plano de ação ordenado por prioridade"""
    
    tasks = []
    
    # Críticos primeiro
    for issue in issues["critical"]:
        tasks.append({
            "priority": 1,
            "type": issue["type"],
            "file": issue["file"],
            "action": issue["action"] or "Corrigir problema crítico",
            "severity": "CRITICAL"
        })
    
    # Warnings depois
    for issue in issues["warnings"]:
        tasks.append({
            "priority": 2,
            "type": issue["type"],
            "file": issue["file"],
            "action": issue["action"] or "Corrigir aviso",
            "severity": "WARNING"
        })
    
    # Ordena por prioridade
    tasks.sort(key=lambda t: t["priority"])
    
    return tasks

def generate_roadmap(tasks: List[Dict]) -> Dict:
    """Gera roadmap estruturado"""
    
    return {
        "total_tasks": len(tasks),
        "critical_tasks": len([t for t in tasks if t["severity"] == "CRITICAL"]),
        "tasks": tasks[:10],  # Top 10
        "status": "BLOCKED" if any(t["severity"] == "CRITICAL" for t in tasks) else "READY"
    }
