"""Testes básicos do FAA v2"""
import sys
from pathlib import Path

# Setup path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.scanner import scan_tree, _classify
from core.rules import Rule, Severity, validate_node
from issues.detector import detect_issues, classify_issues
from planner.prioritizer import generate_plan

def test_scanner():
    """Testa scanner básico"""
    root = Path(__file__).parent.parent.parent.parent
    nodes = scan_tree(root)
    
    assert len(nodes) > 0, "Scanner não encontrou arquivos"
    
    # Verifica categorização
    categories = {n.category for n in nodes}
    assert "documentation" in categories or "data" in categories or "other" in categories
    
    print("✅ Scanner: OK")

def test_rules():
    """Testa motor de regras"""
    from dataclasses import dataclass
    
    @dataclass
    class MockNode:
        path: Path
        relative: str
        category: str
        is_versioned: bool
        has_frontmatter: bool
    
    # Node sem versão em docs
    node = MockNode(
        path=Path("docs/test.md"),
        relative="docs/test.md",
        category="documentation",
        is_versioned=False,
        has_frontmatter=False
    )
    
    rule = Rule(
        "test_versioned",
        Severity.WARNING,
        lambda n: n.is_versioned if n.category == "documentation" else True,
        "Adicionar versão"
    )
    
    issue = rule.validate(node)
    assert issue is not None, "Regra deveria detectar problema"
    assert issue.severity == Severity.WARNING
    
    print("✅ Rules: OK")

def test_planner():
    """Testa geração de plano"""
    issues = {
        "critical": [
            {"type": "test", "severity": "critical", "file": "foo.md", "action": "Corrigir"}
        ],
        "warnings": [
            {"type": "test2", "severity": "warning", "file": "bar.md", "action": "Ajustar"}
        ],
        "counts": {"critical": 1, "warnings": 1}
    }
    
    tasks = generate_plan(issues)
    
    assert len(tasks) == 2, "Deveria gerar 2 tarefas"
    assert tasks[0]["priority"] == 1, "Crítico deveria ser prioridade 1"
    assert tasks[1]["priority"] == 2, "Warning deveria ser prioridade 2"
    
    print("✅ Planner: OK")

def test_full_pipeline():
    """Testa pipeline completo"""
    from core.orchestrator import FAA
    
    faa = FAA()
    state = faa.run(save_snapshot_flag=False)
    
    assert "metrics" in state
    assert "structure" in state
    assert "issues" in state
    assert "plan" in state
    
    assert state["metrics"]["score"] >= 0
    assert state["metrics"]["score"] <= 100
    
    print("✅ Pipeline: OK")

if __name__ == "__main__":
    test_scanner()
    test_rules()
    test_planner()
    test_full_pipeline()
    
    print("\n🎉 Todos os testes passaram!")
