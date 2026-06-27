# FAA v2 — Framework de Auditoria Arquitetural

> Sistema de governança arquitetural contínua para o SOE-CCG

## Filosofia

FAA v2 não é apenas auditoria — é um **kernel de governança** que:

- 🔍 **Observa** o estado completo do sistema
- 🧠 **Entende** problemas e suas causas
- 📋 **Propõe** ações ordenadas e priorizadas

## Uso

### Status unificado (substitui tree/ls)

```bash
./faa status
```

Exibe:
- Score global
- Decisão arquitetural (APPROVED/DEGRADED/BLOCKED)
- Integridade estrutural
- Cobertura por categoria
- Issues críticos
- Próximas ações

### Auditoria completa

```bash
./faa validate
```

Executa análise completa e atualiza estado em `docs/99-referencias/faa-state.json`.

### Listar problemas

```bash
./faa issues              # todos
./faa issues --critical   # apenas críticos
```

### Ver plano de ação

```bash
./faa plan
```

Converte issues em roadmap ordenado por prioridade.

### Criar snapshot histórico

```bash
./faa snapshot
```

Salva estado com timestamp em `docs/99-referencias/snapshots/`.

### Estado para agentes (JSON)

```bash
./faa state --json
```

Saída estruturada consumível por LLMs e automação.

## Arquitetura FAA v2

```
FAA v2
│
├── 1. COLLECT    → scanner.py (escaneia árvore)
├── 2. CLASSIFY   → scanner.py (categoriza arquivos)
├── 3. VALIDATE   → rules.py (valida contra regras)
├── 4. DETECT     → detector.py (identifica issues)
├── 5. PLAN       → prioritizer.py (gera roadmap)
├── 6. MEASURE    → coverage.py (calcula métricas)
├── 7. PERSIST    → state_store.py (salva estado)
└── 8. REPORT     → report_console.py (visualiza)
```

## Estrutura de pastas

```
faa/
├── core/
│   ├── orchestrator.py    # orquestrador central
│   ├── scanner.py         # coleta e classificação
│   └── rules.py           # motor de regras
│
├── engines/
│   └── structure_engine.py
│
├── issues/
│   └── detector.py        # detecção de problemas
│
├── planner/
│   └── prioritizer.py     # geração de roadmap
│
├── metrics/
│   └── coverage.py        # métricas do sistema
│
├── state/
│   └── state_store.py     # persistência
│
├── observability/
│   └── report_console.py  # saída visual
│
├── config.py              # configuração central
└── faa                    # CLI principal
```

## Estado do sistema (faa-state.json)

```json
{
  "version": "2.0",
  "timestamp": "2026-06-26T21:00:00Z",
  "metrics": {
    "score": 85.5,
    "integrity": 100.0,
    "decision": "APPROVED",
    "health": "OK"
  },
  "structure": {
    "total_files": 142,
    "missing_dirs": [],
    "missing_critical_files": []
  },
  "issues": {
    "critical": [],
    "warnings": [],
    "counts": { "critical": 0, "warnings": 0 }
  },
  "plan": {
    "total_tasks": 0,
    "critical_tasks": 0,
    "tasks": [],
    "status": "READY"
  }
}
```

## Regras implementadas (v2.0)

| Regra | Severidade | Ação |
|-------|------------|------|
| `versioned_naming` | WARNING | Adicionar sufixo -v1.md |
| `frontmatter_required` | CRITICAL | Adicionar frontmatter YAML |

## Diferencial FAA v2

### FAA v1:
- ✅ Valida estrutura
- ✅ Detecta problemas
- ✅ Calcula score

### FAA v2:
- ✅ Tudo do v1
- ✅ **Issues → Ações** (issue engine)
- ✅ **Ações → Roadmap** (planner)
- ✅ **Snapshots históricos** (versionamento)
- ✅ **Status unificado** (observabilidade)

## Exit codes

- `0` — sistema aprovado (APPROVED/DEGRADED)
- `1` — sistema bloqueado (BLOCKED) com problemas críticos

## Consumo por agentes

Um agente LLM pode:

1. Executar `./faa validate`
2. Ler `docs/99-referencias/faa-state.json`
3. Obter:
   - Decisão global
   - Lista de problemas
   - Roadmap de ações priorizadas
   - Métricas de integridade

**Sem ler arquivos individuais.**

## Evolução planejada (v2.1+)

- [ ] Motor semântico (análise de conteúdo com LLM)
- [ ] Diff entre snapshots (evolução temporal)
- [ ] Grafo de dependências entre docs
- [ ] Score por subsistema
- [ ] Bloqueio automático de mudanças ruins
- [ ] Integração com CI/CD

## Princípios fundamentais

1. **Tudo vira grafo** — nada é isolado
2. **Tudo gera estado** — nenhuma execução é descartada
3. **Toda inconsistência vira issue** — nada é silencioso
4. **Toda issue vira plano** — problema sem ação não existe
5. **Toda mudança gera diff** — histórico sempre obrigatório

---

**FAA v2 não é mais auditoria — é consciência arquitetural contínua.**
