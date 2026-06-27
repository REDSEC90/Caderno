"""Motor de roadmap — converte issues em tarefas executáveis"""
from typing import List, Dict
from dataclasses import dataclass, asdict
from enum import Enum

class Area(Enum):
    DOCS = "docs"
    DADOS = "dados"
    SCRIPTS = "scripts"
    ARQUITETURA = "arquitetura"

class TipoTask(Enum):
    CREATE = "create"
    FIX = "fix"
    IMPROVE = "improve"
    REFACTOR = "refactor"

class Impacto(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class Task:
    id: str
    area: str
    tipo: str
    prioridade: int
    impacto: str
    descricao: str
    resultado_esperado: str
    dependencias: List[str] = None
    
    def __post_init__(self):
        if self.dependencias is None:
            self.dependencias = []

@dataclass
class Epic:
    id: str
    nome: str
    descricao: str
    tasks: List[Task]

def classify_area(file_path: str) -> Area:
    """Classifica área baseado no path"""
    if "docs/" in file_path:
        return Area.DOCS
    elif "dados/" in file_path:
        return Area.DADOS
    elif "scripts/" in file_path:
        return Area.SCRIPTS
    return Area.ARQUITETURA

def classify_impact(severity: str, file_path: str) -> Impacto:
    """Classifica impacto baseado em severidade e arquivo"""
    if severity == "critical":
        return Impacto.HIGH
    
    # Arquivos de domínio/glossário = alto impacto
    if "glossario" in file_path or "dominio" in file_path:
        return Impacto.HIGH
    
    # Catálogos e templates = médio
    if "catalogo" in file_path or "template" in file_path:
        return Impacto.MEDIUM
    
    return Impacto.LOW

def issue_to_task(issue: Dict, task_id: int) -> Task:
    """Converte um issue em task executável"""
    area = classify_area(issue["file"])
    impacto = classify_impact(issue.get("severity", "warning"), issue["file"])
    
    # Prioridade baseada em severidade e impacto
    prioridade = 100 if issue.get("severity") == "critical" else 50
    if impacto == Impacto.HIGH:
        prioridade += 30
    
    # Tipo baseado no tipo de issue
    tipo = TipoTask.FIX
    if "ausente" in issue.get("message", "").lower():
        tipo = TipoTask.CREATE
    elif "versioned_naming" in issue.get("type", ""):
        tipo = TipoTask.FIX
    
    return Task(
        id=f"TASK-{task_id:03d}",
        area=area.value,
        tipo=tipo.value,
        prioridade=prioridade,
        impacto=impacto.value,
        descricao=issue.get("action", issue.get("message", "Corrigir problema")),
        resultado_esperado=f"Arquivo {issue['file']} conforme com padrões"
    )

def group_into_epics(tasks: List[Task]) -> List[Epic]:
    """Agrupa tasks em epics por área"""
    epics_map = {}
    
    for task in tasks:
        area = task.area
        if area not in epics_map:
            epics_map[area] = {
                "id": f"EPIC-{area.upper()}",
                "nome": f"Consolidação {area}",
                "descricao": f"Garantir consistência e completude da área {area}",
                "tasks": []
            }
        epics_map[area]["tasks"].append(task)
    
    return [Epic(**data) for data in epics_map.values()]

def generate_roadmap(issues: Dict) -> Dict:
    """Gera roadmap completo a partir de issues"""
    
    # Converter todos issues em tasks
    all_tasks = []
    task_counter = 1
    
    # Críticos primeiro
    for issue in issues.get("critical", []):
        all_tasks.append(issue_to_task(issue, task_counter))
        task_counter += 1
    
    # Warnings depois
    for issue in issues.get("warnings", []):
        all_tasks.append(issue_to_task(issue, task_counter))
        task_counter += 1
    
    # Ordenar por prioridade
    all_tasks.sort(key=lambda t: t.prioridade, reverse=True)
    
    # Agrupar em epics
    epics = group_into_epics(all_tasks)
    
    # Calcular métricas
    total_high_impact = len([t for t in all_tasks if t.impacto == "high"])
    total_critical = len([t for t in all_tasks if t.prioridade >= 90])
    
    return {
        "total_tasks": len(all_tasks),
        "total_epics": len(epics),
        "high_impact_tasks": total_high_impact,
        "critical_tasks": total_critical,
        "epics": [
            {
                "id": epic.id,
                "nome": epic.nome,
                "descricao": epic.descricao,
                "total_tasks": len(epic.tasks),
                "tasks": [asdict(t) for t in epic.tasks[:5]]  # Top 5 por epic
            }
            for epic in epics
        ],
        "execution_order": [asdict(t) for t in all_tasks[:10]]  # Top 10 global
    }
