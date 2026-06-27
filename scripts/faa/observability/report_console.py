"""Saída visual para console"""
from typing import Dict

def print_status(state: Dict) -> None:
    """Exibe status unificado"""
    m = state["metrics"]
    s = state["structure"]
    i = state["issues"]
    
    print("\n╔═══════════════════════════════════════╗")
    print("║   FAA v2 — STATUS ARQUITETURAL        ║")
    print("╚═══════════════════════════════════════╝\n")
    
    # Score
    score_icon = "✅" if m["score"] >= 80 else "⚠️" if m["score"] >= 50 else "❌"
    print(f"{score_icon} Score Global: {m['score']:.1f}/100")
    print(f"   Decisão: {m['decision']}")
    print(f"   Integridade: {m['integrity']:.1f}%")
    print(f"   Saúde: {m['health']}\n")
    
    # Cobertura
    print("📊 Cobertura:")
    print(f"   Documentação: {m['coverage']['documentation']} arquivos")
    print(f"   Dados: {m['coverage']['data']} registros")
    print(f"   Esquemas: {m['coverage']['schema']} schemas\n")
    
    # Issues
    print("🔍 Issues:")
    print(f"   Críticos: {i['counts']['critical']}")
    print(f"   Avisos: {i['counts']['warnings']}")
    print(f"   Info: {i['counts']['info']}\n")
    
    # Problemas estruturais
    if s["missing_critical_files"]:
        print("❌ Arquivos críticos ausentes:")
        for f in s["missing_critical_files"][:3]:
            print(f"   - {f}")
        if len(s["missing_critical_files"]) > 3:
            print(f"   ... e mais {len(s['missing_critical_files']) - 3}")
        print()
    
    # Plano
    if state["plan"]["tasks"]:
        print(f"📋 Próximas ações ({state['plan']['total_tasks']} total):")
        for i, task in enumerate(state["plan"]["tasks"][:5], 1):
            icon = "🔴" if task["severity"] == "CRITICAL" else "🟡"
            print(f"   {i}. {icon} {task['action']}")
            print(f"      → {task['file']}")
        print()

def print_issues(state: Dict, critical_only: bool = False) -> None:
    """Lista todos os issues"""
    issues = state["issues"]
    
    print("\n═══ FAA v2 — ISSUES DETECTADOS ═══\n")
    
    if critical_only:
        items = issues["critical"]
        print(f"🔴 CRÍTICOS ({len(items)}):\n")
    else:
        items = issues["critical"] + issues["warnings"]
        print(f"Total: {issues['counts']['critical']} críticos, {issues['counts']['warnings']} avisos\n")
    
    for issue in items:
        severity_icon = "🔴" if issue["severity"] == "critical" else "🟡"
        print(f"{severity_icon} [{issue['type']}] {issue['file']}")
        print(f"   ↳ Ação: {issue['action']}")
        print()

def print_plan(state: Dict) -> None:
    """Exibe roadmap completo"""
    plan = state["plan"]
    
    print("\n═══ FAA v2 — PLANO DE AÇÃO ═══\n")
    print(f"Status: {plan['status']}")
    print(f"Total de tarefas: {plan['total_tasks']}")
    print(f"Críticas: {plan['critical_tasks']}\n")
    
    for i, task in enumerate(plan["tasks"], 1):
        icon = "🔴" if task["severity"] == "CRITICAL" else "🟡"
        print(f"{i}. {icon} [{task['type']}]")
        print(f"   Arquivo: {task['file']}")
        print(f"   Ação: {task['action']}\n")

def print_roadmap(state: Dict) -> None:
    """Exibe roadmap estruturado em epics"""
    roadmap = state.get("roadmap", {})
    
    if not roadmap:
        print("\n⚠️  Roadmap estruturado não disponível\n")
        return
    
    print("\n╔═══════════════════════════════════════════╗")
    print("║   FAA v2 — ROADMAP ESTRUTURADO            ║")
    print("╚═══════════════════════════════════════════╝\n")
    
    print(f"📊 Total: {roadmap['total_tasks']} tasks | {roadmap['total_epics']} epics")
    print(f"🔴 Críticas: {roadmap['critical_tasks']}")
    print(f"⚠️  Alto impacto: {roadmap['high_impact_tasks']}\n")
    
    # Ordem de execução global
    print("═══ ORDEM DE EXECUÇÃO RECOMENDADA ═══\n")
    for i, task in enumerate(roadmap.get("execution_order", [])[:10], 1):
        icon = "🔴" if task["prioridade"] >= 90 else "🟡"
        print(f"{i}. {icon} [{task['area']}] {task['tipo'].upper()}")
        print(f"   Prioridade: {task['prioridade']} | Impacto: {task['impacto']}")
        print(f"   → {task['descricao']}")
        print(f"   ✓ {task['resultado_esperado']}\n")
    
    # Epics organizados
    print("\n═══ ORGANIZAÇÃO POR ÉPICOS ═══\n")
    for epic in roadmap.get("epics", []):
        print(f"📦 {epic['nome']} ({epic['total_tasks']} tasks)")
        print(f"   {epic['descricao']}\n")
