# FAA v2 — Guia de extensão

## Arquitetura extensível

O FAA v2 foi projetado para ser estendido sem modificar o core.

---

## 1. Adicionar novas regras

### Exemplo simples

```python
# plugins/my_rules.py
from core.rules import Rule, Severity

def check_my_condition(node):
    """Retorna True se válido, False se inválido"""
    return node.path.name.startswith("valid-")

MY_RULES = [
    Rule(
        "my_custom_rule",
        Severity.WARNING,
        check_my_condition,
        "Renomear com prefixo valid-"
    )
]
```

### Ativar regra

```python
# core/rules.py
from plugins.my_rules import MY_RULES

RULES.extend(MY_RULES)
```

---

## 2. Adicionar novo engine de análise

### Estrutura

```python
# engines/semantic_engine.py
from typing import List, Dict
from core.scanner import FileNode

def analyze_semantics(nodes: List[FileNode]) -> Dict:
    """Analisa conteúdo semântico dos documentos"""
    
    semantic_issues = []
    
    for node in nodes:
        if node.category == "documentation":
            content = node.path.read_text()
            
            # Análise customizada
            if "TODO" in content:
                semantic_issues.append({
                    "file": node.relative,
                    "type": "incomplete",
                    "line": content.count("\n", 0, content.find("TODO"))
                })
    
    return {
        "total_analyzed": len([n for n in nodes if n.category == "documentation"]),
        "issues_found": len(semantic_issues),
        "issues": semantic_issues
    }
```

### Integrar no orquestrador

```python
# core/orchestrator.py
from engines.semantic_engine import analyze_semantics

class FAA:
    def run(self):
        # ... código existente ...
        
        # Adicionar análise semântica
        semantic = analyze_semantics(self.nodes)
        self.state["semantic"] = semantic
```

---

## 3. Adicionar novos comandos CLI

### Comando personalizado

```python
# cli/analyze.py
def cmd_analyze(args):
    """Comando customizado de análise"""
    from core.orchestrator import FAA
    
    faa = FAA()
    state = faa.run()
    
    # Análise customizada
    print(f"Análise profunda de {state['metrics']['total_files']} arquivos...")
```

### Registrar no CLI principal

```python
# faa (CLI principal)
def main():
    # ... código existente ...
    
    # Adicionar subcommand
    p_analyze = subparsers.add_parser("analyze", help="Análise customizada")
    
    # Dispatch
    commands["analyze"] = cmd_analyze
```

---

## 4. Adicionar métricas customizadas

### Métrica personalizada

```python
# metrics/custom_metrics.py
def compute_complexity(nodes):
    """Calcula complexidade do sistema"""
    
    total_lines = 0
    
    for node in nodes:
        if node.path.suffix == ".md":
            total_lines += len(node.path.read_text().splitlines())
    
    return {
        "total_lines": total_lines,
        "complexity_score": total_lines / 1000  # Exemplo
    }
```

### Integrar

```python
# metrics/coverage.py
from metrics.custom_metrics import compute_complexity

def compute_metrics(nodes, issues, structure):
    # ... código existente ...
    
    complexity = compute_complexity(nodes)
    
    return {
        # ... existentes ...
        "complexity": complexity
    }
```

---

## 5. Criar formatadores de saída customizados

### Saída HTML

```python
# observability/report_html.py
def generate_html(state: Dict) -> str:
    """Gera relatório HTML"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head><title>FAA Report</title></head>
    <body>
        <h1>FAA v2 Report</h1>
        <p>Score: {state['metrics']['score']}</p>
        <p>Decision: {state['metrics']['decision']}</p>
    </body>
    </html>
    """
    
    return html

def save_html_report(state: Dict, path: Path):
    html = generate_html(state)
    path.write_text(html, encoding="utf-8")
```

### Usar no CLI

```bash
./faa validate --format html --output report.html
```

---

## 6. Integrar com sistemas externos

### Exemplo: enviar para API

```python
# plugins/api_integration.py
import requests
import json

def send_to_api(state: Dict, api_url: str):
    """Envia estado para API externa"""
    
    payload = {
        "project": "SOE-CCG",
        "score": state["metrics"]["score"],
        "decision": state["metrics"]["decision"],
        "issues": state["issues"]["counts"]
    }
    
    response = requests.post(api_url, json=payload)
    return response.status_code == 200
```

### Uso

```python
# Após auditoria
faa = FAA()
state = faa.run()

from plugins.api_integration import send_to_api
send_to_api(state, "https://monitoring.example.com/faa")
```

---

## 7. Adicionar validadores de conteúdo

### Validador semântico

```python
# validators/content_validator.py
def validate_markdown_structure(node):
    """Valida estrutura de markdown"""
    
    if node.path.suffix != ".md":
        return True
    
    content = node.path.read_text()
    
    # Deve ter título H1
    if not content.startswith("# "):
        return False
    
    # Deve ter ao menos 100 caracteres
    if len(content) < 100:
        return False
    
    return True
```

### Criar regra

```python
Rule(
    "markdown_structure",
    Severity.WARNING,
    validate_markdown_structure,
    "Adicionar título H1 e conteúdo mínimo"
)
```

---

## 8. Pipeline de CI/CD

### GitHub Actions

```yaml
# .github/workflows/faa.yml
name: FAA Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Run FAA v2
        run: |
          cd scripts/faa
          ./faa validate --snapshot
      
      - name: Upload state
        uses: actions/upload-artifact@v3
        with:
          name: faa-state
          path: docs/99-referencias/faa-state.json
      
      - name: Check decision
        run: |
          DECISION=$(python3 -c "import json; print(json.load(open('docs/99-referencias/faa-state.json'))['metrics']['decision'])")
          if [ "$DECISION" = "BLOCKED" ]; then
            echo "❌ Sistema bloqueado por problemas críticos"
            exit 1
          fi
```

---

## 9. Hooks e callbacks

### Sistema de hooks

```python
# core/hooks.py
class HookManager:
    def __init__(self):
        self.hooks = {
            "before_scan": [],
            "after_scan": [],
            "before_validate": [],
            "after_validate": []
        }
    
    def register(self, event: str, callback):
        self.hooks[event].append(callback)
    
    def trigger(self, event: str, *args, **kwargs):
        for callback in self.hooks.get(event, []):
            callback(*args, **kwargs)

# Uso
hooks = HookManager()

hooks.register("after_validate", lambda state: print(f"Score: {state['metrics']['score']}"))
```

---

## 10. Plugins completos

### Estrutura de plugin

```python
# plugins/my_plugin/
#   __init__.py
#   rules.py
#   analyzer.py
#   metrics.py

# plugins/my_plugin/__init__.py
from .rules import PLUGIN_RULES
from .analyzer import analyze
from .metrics import compute_metrics

class MyPlugin:
    name = "my_plugin"
    version = "1.0"
    
    def install(self, faa):
        """Instala plugin no FAA"""
        faa.add_rules(PLUGIN_RULES)
        faa.add_analyzer(analyze)
        faa.add_metrics(compute_metrics)
```

---

## Boas práticas

1. **Isolamento**: mantenha extensões em `plugins/`
2. **Testes**: crie testes em `tests/test_my_extension.py`
3. **Documentação**: documente suas extensões
4. **Versionamento**: use versionamento semântico
5. **Compatibilidade**: evite modificar o core

---

## Exemplos prontos

- `plugins/custom_rules.py` — regras customizadas
- `tests/test_basic.py` — testes de exemplo

---

**O FAA v2 é sua plataforma de governança — estenda conforme necessário.**
