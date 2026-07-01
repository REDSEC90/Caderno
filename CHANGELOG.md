# CHANGELOG — SOE-CCG

Todas as mudanças notáveis deste projeto são registradas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [v0.6.0] — 2026-07-01 — Consolidação Global

### Objetivo desta release

Primeira consolidação arquitetural formal do SOE-CCG.
Foco em limpeza, autoridade documental única e rastreabilidade.
Nenhuma funcionalidade nova adicionada — apenas estabilização.

---

### Adicionado

- `docs/INDICE-MESTRE.md` — Índice único de autoridade documental. Define o documento oficial para cada conceito do sistema.
- `docs/MATRIZ-RASTREABILIDADE.md` — Rastreabilidade completa: Lei → Contrato → Implementação → Teste.
- `docs/99-referencias/archive/raiz-historico/` — Arquivo histórico de documentos operacionais da raiz.
- `docs/99-referencias/archive/kernel-files-historico/` — Arquivo histórico do diretório `kernel-files/`.
- `kernel-docs/archive/` — Arquivo de resumos históricos de fases (FASE-0 a FASE-12 RESUMO).
- `scripts/archive/` — Arquivo de scripts de consolidação históricos.
- `scripts/auditoria/archive/` — Arquivo de motores de auditoria em versões obsoletas.

---

### Removido / Arquivado

**Raiz do projeto** (movidos para `docs/99-referencias/archive/raiz-historico/`):
- `ANALISE-COMPLETA-2026-06-28.md`
- `CONCLUSAO-tecnica`
- `CONSOLIDACAO-V1-SUMMARY.md`
- `CORRECOES-APLICADAS.md`
- `ENTREGA-COMPLETA.md`
- `FASE-0-ENTREGA-COMPLETA.md`
- `FASE-0-RESUMO-EXECUTIVO.md`
- `LEIA-ISTO-PRIMEIRO.md`
- `OBSERVACAO.md`
- `OBSERVACAO2.md`
- `PLAN-SOE-CCG-V2.md`
- `PLAN-docs-07-uso-V2.md`
- `RESUMO.md`

**kernel-files/** (movido para `docs/99-referencias/archive/kernel-files-historico/`):
- Diretório inteiro — conteúdo coberto por `kernel-docs/`

**kernel-docs/** (movidos para `kernel-docs/archive/`):
- `FASE-0-RESUMO.md`, `FASE-0-INDICE.md`, `FASE-0-LISTA-COMPONENTES.md`
- `FASE-1-RESUMO.md` a `FASE-12-RESUMO.md`
- `FASE-3-DIAGRAMA-LIFECYCLE.md`

**scripts/** (movidos para `scripts/archive/`):
- `consolidate-v1-lote1.sh`, `consolidate-v1-lote2.sh`, `consolidate-v1-lote3.sh`

**scripts/auditoria/** (movidos para `scripts/auditoria/archive/`):
- `auditor-v1.py`, `config_v1.py`, `models_v1.py`, `utils_v1.py`
- Motores: `baseline_v1.py`, `cobertura_v1.py`, `dados-v2.py`, `dependencias-v2.py`,
  `dominio_v1.py`, `estrutura_v1.py`, `filosofia_v1.py`, `integridade-v2.py`,
  `maturidade_v1.py`, `semantica_v1.py`, `semantica-v2.py`

**docs/00-projeto/glossario-v1.md** (movido para archive):
- Versão menor (61 linhas) substituída pelo canônico `docs/01-dominio/glossario-v1.md` (285 linhas)

**Cache / temporários**:
- Todos os diretórios `__pycache__/` removidos
- `.pytest_cache/` removido

---

### Corrigido

- `kernel/contracts/validator.py` — `ALLOWED_SYS_PATH_ADAPTERS` atualizado: removidas entradas de arquivos agora arquivados (`auditor-v1.py`, `config_v1.py`)
- `kernel/contracts/validator.py` — `_python_files()` agora exclui diretórios `archive/` do scan arquitetural, evitando falsos positivos em material histórico

---

### Testes

- **226/226 passando** (100%)
- Validação arquitetural (`test_kernel_validator_aprova_arquitetura_atual`) — PASS
- Isolamento kernel/codigo verificado: zero imports proibidos

---

### Estado pós-release

| Área                    | Estado              |
|-------------------------|---------------------|
| Arquitetura             | ✅ Congelada        |
| Kernel                  | ✅ Estável          |
| Kernel-docs             | ✅ Consolidados     |
| Contratos               | ✅ Definidos        |
| Documentação            | ✅ Sem conflitos    |
| Autoridade documental   | ✅ Índice mestre    |
| Rastreabilidade         | ✅ Matriz criada    |
| Testes                  | ✅ 226/226          |
| Repositório             | ✅ Limpo            |
| Duplicações             | ✅ Eliminadas       |

---

## Releases anteriores

### [v0.5.x] — Kernel funcional

Implementação das Fases 0–6 do Kernel:
- Bootstrap, Contracts, Registry, Lifecycle, EventBus, ServiceRegistry
- Testes de contrato, integração, unit e golden files
- kernel-docs com constituição, leis, invariantes e políticas

---

[v0.6.0]: https://github.com/soe-ccg/soe-ccg/releases/tag/v0.6.0
