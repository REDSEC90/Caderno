# FAA v1 → v2 — Guia de migração

## Mudança de paradigma

### FAA v1
**Kernel de decisão arquitetural** — responde "o sistema está correto?"

### FAA v2
**Sistema de governança arquitetural contínua** — responde:
- O sistema está correto?
- O que está faltando?
- O que deve ser feito agora?
- Em que ordem?

---

## Comandos equivalentes

| FAA v1 | FAA v2 | Função |
|--------|--------|--------|
| `python3 auditor-v1.py` | `./faa validate` | Auditoria completa |
| `python3 auditor-v1.py state` | `./faa status` | Ver estado |
| `python3 auditor-v1.py state --json` | `./faa state --json` | JSON para agentes |
| `python3 auditor-v1.py issues` | `./faa issues` | Listar problemas |
| ❌ Não existe | `./faa plan` | **NOVO:** Roadmap de ações |
| ❌ Não existe | `./faa snapshot` | **NOVO:** Snapshot histórico |

---

## Diferenciais do FAA v2

### 1. Issue Engine
Transforma problemas em ações concretas.

### 2. Planner
Gera roadmap ordenado por prioridade.

### 3. Snapshots históricos
Permite comparação temporal (base para v2.1).

### 4. Status unificado
Substitui `tree` e `ls` como visão padrão.

---

## Roadmap

### v2.0 (atual)
- ✅ Scanner com classificação automática
- ✅ Motor de regras extensível
- ✅ Issue engine + Planner
- ✅ Snapshots

### v2.1 (próximo)
- [ ] Diff entre snapshots
- [ ] Grafo de dependências
- [ ] Motor semântico
- [ ] Baseline detalhado do v1
