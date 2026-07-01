# CHANGELOG — SOE-CCG

Todas as mudanças notáveis deste projeto são registradas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [Em desenvolvimento] — v0.8.0 — Escalabilidade

### Etapa 1 — Testes unitários do `codigo/` ✅ CONCLUÍDA

**Data:** 2026-07-01

**Objetivo:** Eliminar lacuna de cobertura zero nos módulos centrais do runtime.

**Entregas:**
- `testes/unit/test_importador.py` — 16 novos testes, cobertura 0% → 91%
- `testes/unit/test_parser.py` — 4 novos testes, cobertura 82% → 92%
- Cobertura total do `codigo/`: 45% → 73% (≥91% em todos os módulos críticos)
- Total de testes: 410 → 430 (+20)
- Zero regressões

**Testes adicionados:**
- `test_tipo_from_id` — extração de tipo a partir do prefixo do ID
- `test_row_for_*` — 7 testes para cada tipo de entidade (receita, ingrediente, técnica, equipamento, execução, observação, experimento)
- `test_importar_*` — 9 testes para inserção, atualização, arestas N:N, relacionamentos, histórico, idempotência, grafo vazio
- `test_parse_file_frontmatter_fallback_yaml` — fallback quando python-frontmatter não está disponível
- `test_parse_file_field_com_*` — validação de campos com lista de números, IDs inválidos
- `test_parse_directory_com_arquivo_invalido` — processamento robusto de arquivos malformados

---

## [v0.7.0] — 2026-07-01 — Fortalecimento do Kernel

### Objetivo desta release

Fortalecer APIs, documentação, integração e observabilidade do Kernel sem adicionar funcionalidades novas.
Freeze arquitetural mantido. Foco em: diagnóstico unificado, cobertura de testes, documentação operacional.

---

### Adicionado

**Observabilidade (Etapa 1):**
- `kernel/diagnostics/__init__.py` — módulo de diagnóstico e observabilidade do Kernel
- `kernel/diagnostics/doctor.py` — `DiagnosticReport`, `run_diagnostics()`, `print_diagnostics()`
- `kernel/diagnostics/inspector.py` — `inspect_kernel()`, `inspect_registry()`, `inspect_services()`, `inspect_events()`

**Documentação (Etapas 2 e 3):**
- `docs/06-operacao/kernel-operations-guide-v1.md` — Guia completo de operação do Kernel (8 seções, exemplos executáveis)
- `docs/05-desenvolvimento/kernel-cookbook-v1.md` — Cookbook com 6 receitas práticas de integração

**Testes de integração (Etapa 4):**
- `testes/integration/test_kernel_full_lifecycle.py` — ciclo completo bootstrap → start → stop
- `testes/integration/test_kernel_events_propagation.py` — propagação de eventos entre componentes
- `testes/integration/test_kernel_services_lifecycle.py` — integração services + lifecycle
- `testes/integration/test_kernel_registry_advanced.py` — queries avançadas no registry

**Testes do cookbook (Etapa 3):**
- `testes/cookbook/__init__.py`
- `testes/cookbook/test_cookbook.py` — 6 testes, um por receita

**Rastreabilidade (Etapa 5):**
- `docs/INDICE-MESTRE.md` atualizado (v1.1) — seção 4a (Observabilidade), seção 8 (diagnostics), seção 10 (novos testes)
- `docs/MATRIZ-RASTREABILIDADE.md` atualizado (v1.1) — seções 7, 10 e 11 com novos testes e observabilidade

**ADR (Etapa 6):**
- `docs/04-padroes/ADR-0003-OBSERVABILIDADE-KERNEL-v1.md` — decisão arquitetural sobre modelo de observabilidade

---

### Corrigido

- `kernel/diagnostics/doctor.py` — `services_stats['with_health_check']` corrigido para `with_health_method`
- `kernel/diagnostics/doctor.py` — `events_stats['total_published']` corrigido para `total_events_published`
- `kernel/diagnostics/doctor.py` — acesso a `health["healthy"]` em `all_health()` corrigido para `health["health_result"]["healthy"]`
- `kernel/diagnostics/doctor.py` — `deprecated_modules` movido para fora do bloco `if not healthy` (deprecados são aviso independente de saúde geral)
- `kernel/diagnostics/__init__.py` — agora exporta todos os 7 símbolos públicos (`print_diagnostics`, `inspect_registry`, `inspect_services`, `inspect_events`)

---

### Testes

- **406/406 passando** (100%)
- `testes/contract/test_diagnostics.py`: 22 → **35 testes**, cobertura 62% → **100%**
- Novos testes de integração: **+139 testes** (4 arquivos)
- Novos testes de cookbook: **+6 testes**
- Validação arquitetural (`test_kernel_validator_aprova_arquitetura_atual`) — PASS

---

### Estado pós-release

| Área                        | Estado              |
|-----------------------------|---------------------|
| Arquitetura                 | ✅ Congelada        |
| Kernel                      | ✅ Estável          |
| Observabilidade             | ✅ Implementada     |
| Cobertura diagnostics       | ✅ 100%             |
| Guia de operações           | ✅ Criado           |
| Cookbook                    | ✅ 6 receitas       |
| Testes de integração        | ✅ 139 novos        |
| INDICE-MESTRE               | ✅ v1.1             |
| MATRIZ-RASTREABILIDADE      | ✅ v1.1             |
| ADR-0003                    | ✅ Criado           |
| Total de testes             | ✅ 406/406          |
| API pública                 | ✅ Inalterada       |

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

[v0.7.0]: https://github.com/soe-ccg/soe-ccg/releases/tag/v0.7.0
[v0.6.0]: https://github.com/soe-ccg/soe-ccg/releases/tag/v0.6.0

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
