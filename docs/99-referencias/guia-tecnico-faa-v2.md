# 🔧 Guia Técnico — FAA v2 + SOE-CCG

> Para desenvolvedores que vão manter/evoluir o sistema

---

## 🎯 O que foi feito

Implementamos **FAA v2** (Framework de Auditoria Arquitetural) e o usamos para consolidar SOE-CCG de v0.5 para v1.

**Resultado:** Score +7.3, Integridade +20%, 30 arquivos consolidados, 0 problemas críticos.

---

## 🧠 Arquitetura FAA v2

### Pipeline de execução

```
COLLECT → CLASSIFY → ANALYZE → VALIDATE → DETECT → PLAN → MEASURE → PERSIST → REPORT
```

### Módulos principais

```python
faa/
├── core/
│   ├── scanner.py       # Escaneia e classifica arquivos
│   ├── rules.py         # Motor de regras (extensível)
│   └── orchestrator.py  # Coordena pipeline
│
├── engines/
│   └── structure_engine.py  # Análise estrutural
│
├── issues/
│   └── detector.py      # Detecta problemas
│
├── planner/
│   └── prioritizer.py   # Gera roadmap
│
├── metrics/
│   └── coverage.py      # Calcula métricas
│
├── state/
│   └── state_store.py   # Persistência JSON
│
└── observability/
    └── report_console.py  # Saída visual
```

---

## ⚙️ Como usar

### 1. Status do sistema

```bash
./scripts/faa.sh status
```

Retorna:
- Score global (0-100)
- Decisão (APPROVED/DEGRADED/BLOCKED)
- Integridade estrutural
- Issues por severidade
- Próximas ações prioritárias

### 2. Auditoria completa

```bash
./scripts/faa.sh validate
```

Executa:
1. Scanner (classifica arquivos)
2. Estrutura (valida diretórios obrigatórios)
3. Regras (valida contra 2 regras ativas)
4. Issues (detecta problemas)
5. Planner (gera roadmap)
6. Métricas (calcula score)
7. State (persiste JSON)

### 3. Criar snapshot histórico

```bash
./scripts/faa.sh validate --snapshot
```

Salva estado com timestamp em `docs/99-referencias/snapshots/`.

### 4. Ver problemas

```bash
./scripts/faa.sh issues              # todos
./scripts/faa.sh issues --critical   # apenas críticos
```

### 5. Ver roadmap de ações

```bash
./scripts/faa.sh plan
```

Mostra tarefas ordenadas por prioridade com ações concretas.

### 6. JSON para automação

```bash
./scripts/faa.sh state --json | jq .
```

Saída estruturada consumível por scripts/agentes.

---

## 🔧 Como estender FAA v2

### Adicionar nova regra

```python
# plugins/custom_rules.py
from core.rules import Rule, Severity

def check_my_condition(node):
    """Retorna True se válido"""
    return node.path.name.startswith("valid-")

MY_RULE = Rule(
    "my_rule",
    Severity.WARNING,
    check_my_condition,
    "Renomear com prefixo valid-"
)
```

Ativar em `core/rules.py`:

```python
from plugins.custom_rules import MY_RULE
RULES.append(MY_RULE)
```

### Adicionar novo engine

```python
# engines/my_engine.py
def analyze_something(nodes):
    results = []
    for node in nodes:
        # Análise customizada
        pass
    return {"results": results}
```

Integrar em `core/orchestrator.py`:

```python
from engines.my_engine import analyze_something

class FAA:
    def run(self):
        # ... código existente ...
        custom = analyze_something(self.nodes)
        self.state["custom"] = custom
```

---

## 📊 Formato do estado JSON

```json
{
  "version": "2.0",
  "timestamp": "2026-06-26T21:27:14+00:00",
  "metrics": {
    "score": 88.36,
    "integrity": 90.0,
    "decision": "DEGRADED",
    "health": "WARNING"
  },
  "structure": {
    "total_files": 177,
    "missing_critical_files": []
  },
  "issues": {
    "critical": [],
    "warnings": [...],
    "counts": {"critical": 0, "warnings": 22}
  },
  "plan": {
    "total_tasks": 22,
    "critical_tasks": 0,
    "tasks": [...],
    "status": "READY"
  }
}
```

---

## 🎓 Regras de versionamento

### Regra fundamental

**Arquivos com `-vN` não podem ser modificados.**

Exemplos:
- `glossario-v1.md` → FROZEN (imutável)
- `glossario-v2.md` → nova versão (se necessário)

FAA detecta arquivos sem versionamento e gera aviso.

### Consolidação v0.5 → v1

Processo executado:

```bash
# 1. Renomear arquivo
mv arquivo-v0_5.md arquivo-v1.md

# 2. Atualizar frontmatter
sed -i 's/versao: 0.5/versao: 1/' arquivo-v1.md

# 3. Validar
./scripts/faa.sh validate
```

Automatizado nos scripts `consolidate-v1-lote*.sh`.

---

## 🔍 Debugging

### Ver log detalhado

```bash
# Modo verboso não implementado ainda
# Por enquanto, inspecionar estado JSON:
cat docs/99-referencias/faa-state.json | jq .
```

### Verificar regras ativas

```bash
python3 -c "import sys; sys.path.insert(0, 'scripts/faa'); from core.rules import RULES; print([(r.name, r.severity.value) for r in RULES])"
```

### Testar scanner

```bash
python3 scripts/faa/tests/test_basic.py
```

---

## 📈 Métricas explicadas

### Score (0-100)

```python
score = 100 - (total_issues / total_files * 100)
```

Penalizado por:
- Problemas críticos (-peso maior)
- Avisos (-peso menor)

### Integridade (0-100)

```python
integrity = 100
integrity -= missing_critical_files * 20
integrity -= missing_dirs * 10
```

### Decisão

- **APPROVED:** score ≥ 80, 0 críticos, < 5 avisos
- **DEGRADED:** score ≥ 50, 0 críticos, ≥ 5 avisos
- **BLOCKED:** problemas críticos presentes

---

## 🚨 Troubleshooting

### Score caiu após mudanças

```bash
# Ver o que mudou
./scripts/faa.sh issues

# Comparar com snapshot anterior (v2.1)
ls docs/99-referencias/snapshots/
```

### Arquivo crítico ausente

```bash
# FAA indica qual arquivo
./scripts/faa.sh status

# Criar o arquivo
# Validar novamente
./scripts/faa.sh validate
```

### JSON malformado

```bash
# Regenerar estado
rm docs/99-referencias/faa-state.json
./scripts/faa.sh validate
```

---

## 🔄 Workflow de desenvolvimento

### Antes de fazer mudanças

```bash
# 1. Ver estado atual
./scripts/faa.sh status

# 2. Criar snapshot pré-mudança
./scripts/faa.sh snapshot
```

### Após mudanças

```bash
# 1. Validar
./scripts/faa.sh validate

# 2. Verificar impacto
./scripts/faa.sh status

# 3. Se score < 85 ou decision = BLOCKED
./scripts/faa.sh issues --critical
# Corrigir antes de commit
```

### Commit

```bash
# Incluir score no commit
git add .
git commit -m "feat: [descrição] - FAA score: 88.4"
```

---

## 📋 Checklist de qualidade

Antes de cada release:

- [ ] `./scripts/faa.sh validate` executado
- [ ] Score ≥ 85
- [ ] 0 problemas críticos
- [ ] Decisão != BLOCKED
- [ ] Snapshot criado
- [ ] Estado JSON válido

---

## 🧪 Testes

```bash
# Executar testes básicos
python3 scripts/faa/tests/test_basic.py

# Saída esperada:
# ✅ Scanner: OK
# ✅ Rules: OK
# ✅ Planner: OK
# ✅ Pipeline: OK
# 🎉 Todos os testes passaram!
```

---

## 📚 Referências

- `scripts/faa/README.md` — Documentação completa
- `scripts/faa/EXTENDING.md` — Como estender
- `scripts/faa/MIGRATION.md` — Migração v1→v2
- `ENTREGA-COMPLETA.md` — Resumo executivo

---

## 🎯 Métricas de sucesso do projeto

| Métrica | Valor |
|---------|-------|
| Linhas de código FAA | 630 |
| Arquivos consolidados | 30 |
| Score ganho | +7.3 |
| Integridade ganho | +20% |
| Issues resolvidos | 13 |
| Snapshots gerados | 5 |
| Tempo total | ~2h |

---

**Mantenha score ≥ 85 sempre. O FAA é seu aliado.**
