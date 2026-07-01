# SOE-CCG — Architecture Review Oficial (Parte 3 de 3)

> Continuação direta de `02-KERNEL-SPECIFICATION.md`. Cobre os entregáveis 5 a 10.

---

# 5. Plano de Migração

A ordem abaixo é desenhada para que cada passo seja testável isoladamente e para que o passo de maior risco (fusão da stack FAA dupla) só aconteça depois que tudo abaixo dele já estiver estável.

## Passo 1 — `kernel/shared/paths.py`

**O que:** criar o arquivo único de resolução de caminho, substituindo os 4 cálculos divergentes de `ROOT`.
**Impacto:** todos os 4 arquivos que hoje calculam `ROOT` (`codigo/__main__.py`, `codigo/importador.py`, `scripts/faa/config.py`, `scripts/auditoria/config.py`) passam a importar de `kernel.shared.paths` em vez de recalcular.
**Risco:** baixo. É uma extração pura, sem mudança de comportamento — desde que o novo cálculo produza exatamente os mesmos caminhos que os 4 antigos produziam para a árvore atual.
**Rollback:** trivial — reverter para o cálculo local em cada arquivo, já que nenhum dado é movido neste passo.
**Critério de sucesso:** os 13 testes existentes em `testes/` (28+29+43+64+78+109+128 linhas distribuídas) continuam passando sem alteração.

## Passo 2 — `kernel/specification/identity/` + `kernel/specification/contracts/entities/`

**O que:** formalizar como Markdown o que já existe implicitamente em `docs/01-dominio/contratos/*` e na convenção de ID usada em `codigo/ir.py`.
**Impacto:** nenhuma mudança de código — é documentação nova, não reescrita de lógica.
**Risco:** muito baixo.
**Rollback:** não aplicável (é adição pura).

## Passo 3 — `kernel/runtime/schema_registry.py`

**O que:** consome `banco_de_dados/esquemas/schema-sqlite-v1.sql` como input — não o substitui ainda.
**Impacto:** nenhum consumidor existente muda de comportamento; o registry é construído ao lado, validado contra o schema atual.
**Risco:** baixo, mas exige teste de paridade (o registry deve concordar com o schema SQL existente em 100% dos casos antes de qualquer consumidor migrar para ele).
**Rollback:** descartar o registry, manter o consumo direto do `.sql`.

## Passo 4 — `runtime/` inteiro (renomeação 1:1 de `codigo/*.py`)

**O que:** `codigo/parser.py → runtime/parser/markdown_parser.py`, e os demais 4 módulos seguindo o mesmo padrão (ver mapa completo na Seção 6).
**Impacto:** atualização de imports relativos (`from .ir import...`) para os novos caminhos.
**Risco:** médio — é a primeira mudança que toca os 680 linhas de runtime real em produção. Mitigado pelo fato de que os 5 módulos são internamente coesos (todos convergem em `ir.py`), então a renomeação é mecânica.
**Rollback:** manter `codigo/` em paralelo até os testes de `runtime/` passarem, então remover `codigo/` apenas depois de confirmação.
**Dado relevante de risco:** `dados/` tem apenas 13 registros reais hoje (5 ingredientes, 3 técnicas, 2 equipamentos, 1 receita, 1 execução, 1 observação, 0 experimentos, 0 anexos). O sistema está em fase de seed, não de produção — o custo de um erro neste passo é baixo em termos de dado real exposto.

## Passo 5 — `kernel/specification/edges/` + `kernel/runtime/edge_engine/`

**O que:** implementar o modelo de 3 categorias de aresta com `cycle_guard.py`.
**Impacto:** nenhum consumidor existente é afetado ainda — este passo prepara o terreno para o Passo 6.
**Risco:** baixo, é construção isolada.

## Passo 6 — Fusão `scripts/faa/` + `scripts/auditoria/` → `runtime/analysis/`

**Este é o passo de maior risco de todo o plano e só deve acontecer depois que 1–5 estiverem estáveis.**

**O que:** convergir as duas stacks em uma implementação só, seguindo a matriz de consumo exata documentada na Seção 1.2 (qual motor vem de qual arquivo).
**Impacto:** dois entrypoints (`scripts/faa/core/orchestrator.py` e `scripts/auditoria/auditor.py`) tornam-se um (`runtime/analysis/orchestrator.py`).
**Risco:** alto, pelos seguintes motivos verificados na auditoria:
- `auditor-v1.py` usa um carregador dinâmico próprio (`_importar_v1` via `importlib.util`) que mistura arquivos de gerações diferentes (`baseline_v1.py` + `dados-v2.py` + `integridade-v2.py` + `padroes.py` sem sufixo) — a lógica de qual arquivo carregar para qual motor não é uniforme e precisa ser replicada com cuidado na fusão.
- O motor `baseline` (com a classe `DecisaoArquitetural`) só existe no lado legado — é a única migração desta etapa que adiciona funcionalidade nova ao `auditor.py`, em vez de apenas consolidar o que já existe lá.
- `semantica-v2.py` deve ser descartado (não portado) — é o único arquivo confirmado como código morto real (Seção 8).
**Rollback:** manter ambos os entrypoints antigos funcionais em paralelo até `runtime/analysis/orchestrator.py` produzir output idêntico ao `auditor.py` atual em todos os 13 motores compartilhados, mais o motor `baseline` portado.
**Critério de sucesso:** rodar `runtime/analysis/orchestrator.py` e `scripts/auditoria/auditor.py` lado a lado sobre o mesmo estado de `dados/` e confirmar resultado idêntico nos 13 motores comuns, antes de remover qualquer arquivo antigo.

## Passo 7 — `docs/` reorganizada

**O que:** mover os 198 arquivos `.md` para a nova estrutura de `docs/` (Seção 3).
**Impacto:** é a mudança mais visível, mas a menos arriscada tecnicamente — nenhum código depende da localização física dos `.md`.
**Risco:** baixo tecnicamente, mas trabalhoso pelo volume (24.347 linhas).
**Por que é o último passo:** só faz sentido reorganizar a documentação depois que a árvore de código já reflete a nova arquitetura — documentar uma estrutura que ainda não existe gera mais um desalinhamento, não menos.

---

# 6. Mapa de Movimentação de Arquivos

Cobertura completa dos 680 linhas de `codigo/`, mais os pontos de maior risco da stack FAA dupla.

```text
codigo/ir.py
    ↓
runtime/ir/intermediate_representation.py

codigo/parser.py
    ↓
runtime/parser/markdown_parser.py

codigo/resolvedor.py
    ↓
runtime/resolver/reference_resolver.py

codigo/validador.py
    ↓
runtime/validator/entity_validator.py

codigo/importador.py
    ↓
runtime/importer/sqlite_importer.py

codigo/__main__.py
    ↓
interfaces/terminal/cli/__main__.py

scripts/faa/core/orchestrator.py
    ↓
runtime/analysis/orchestrator.py   (FUNDIDO com scripts/auditoria/auditor.py)

scripts/faa/core/scanner.py
    ↓
runtime/analysis/orchestrator.py   (lógica de scan absorvida, scanner deixa de ser arquivo próprio)

scripts/faa/core/rules.py
    ↓
runtime/analysis/orchestrator.py   (lógica de rules absorvida)

scripts/faa/engines/structure_engine.py
    ↓
runtime/analysis/engines/structure_engine.py

scripts/faa/planner/prioritizer.py
    ↓
runtime/analysis/planner/prioritizer.py

scripts/faa/planner/roadmap_engine.py
    ↓
runtime/analysis/planner/roadmap_engine.py

scripts/faa/state/state_store.py
    ↓
runtime/analysis/state/state_store.py

scripts/faa/plugins/custom_rules.py
    ↓
runtime/analysis/plugins/custom_rules.py

scripts/faa/issues/detector.py
    ↓
runtime/analysis/orchestrator.py   (lógica absorvida — detecção de issues vira parte do orchestrator)

scripts/faa/metrics/coverage.py
    ↓
runtime/analysis/metrics/coverage.py

scripts/faa/observability/report_console.py
    ↓
runtime/analysis/reports/console_report.py

scripts/auditoria/auditor.py
    ↓
runtime/analysis/orchestrator.py   (FUNDIDO com scripts/faa/core/orchestrator.py — ver Passo 6)

scripts/auditoria/motores/estrutura.py
    ↓
runtime/analysis/auditors/structure_auditor.py

scripts/auditoria/motores/filosofia.py
    ↓
runtime/analysis/auditors/philosophy_auditor.py

scripts/auditoria/motores/dominio.py
    ↓
runtime/analysis/auditors/domain_auditor.py

scripts/auditoria/motores/templates.py
    ↓
runtime/analysis/auditors/templates_auditor.py

scripts/auditoria/motores/contratos.py
    ↓
runtime/analysis/auditors/contracts_auditor.py

scripts/auditoria/motores/dados.py
    ↓
runtime/analysis/auditors/data_auditor.py

scripts/auditoria/motores/integridade.py
    ↓
runtime/analysis/auditors/integrity_auditor.py

scripts/auditoria/motores/semantica.py
    ↓
runtime/analysis/auditors/semantics_auditor.py

scripts/auditoria/motores/padroes.py
    ↓
runtime/analysis/auditors/patterns_auditor.py

scripts/auditoria/motores/escalabilidade.py
    ↓
runtime/analysis/auditors/scalability_auditor.py

scripts/auditoria/motores/dependencias.py
    ↓
runtime/analysis/auditors/dependency_auditor.py

scripts/auditoria/motores/cobertura.py
    ↓
runtime/analysis/auditors/coverage_auditor.py

scripts/auditoria/motores/maturidade.py
    ↓
runtime/analysis/auditors/maturity_auditor.py

scripts/auditoria/motores/baseline_v1.py
    ↓
runtime/analysis/auditors/baseline_auditor.py   (PORTADO — único motor exclusivo do legado, ver Seção 2.4)

scripts/auditoria/models.py + scripts/auditoria/models_v1.py (classe DecisaoArquitetural)
    ↓
runtime/analysis/decision/architectural_decision.py   (FUSÃO — DecisaoArquitetural portada de models_v1.py)

scripts/auditoria/relatorios/console.py
    ↓
runtime/analysis/reports/markdown_report.py

scripts/importacao/importar.sh
    ↓
infrastructure/import/importar.sh

scripts/copia_seguranca/*
    ↓
infrastructure/backup/

scripts/instalacao/*
    ↓
infrastructure/install/

scripts/manutencao/*
    ↓
infrastructure/maintenance/

banco_de_dados/sqlite/soe-ccg.db (+ .db-shm, .db-wal)
    ↓
infrastructure/database/sqlite/soe-ccg.db

banco_de_dados/esquemas/schema-sqlite-v1.sql
    ↓
infrastructure/database/schemas/schema-sqlite-v1.sql

banco_de_dados/seeds/seed-categorias-v1.sql
    ↓
infrastructure/database/seeds/seed-categorias-v1.sql

dados/receitas/* (1 registro hoje)
    ↓
domain/recipes/

dados/ingredientes/* (5 registros hoje)
    ↓
domain/ingredients/

dados/tecnicas/* (3 registros hoje)
    ↓
domain/techniques/

dados/equipamentos/* (2 registros hoje)
    ↓
domain/equipment/

dados/execucoes/* (1 registro hoje)
    ↓
domain/executions/

dados/observacoes/* (1 registro hoje)
    ↓
domain/observations/

docs/01-dominio/contratos/*.md  (7 arquivos)
    ↓
kernel/specification/contracts/entities/

docs/01-dominio/esquemas/*.md  (7 arquivos)
    ↓
kernel/specification/schemas/

docs/01-dominio/templates/*.md  (9 arquivos)
    ↓
domain/templates/

docs/01-dominio/catalogos/*.md  (8 arquivos)
    ↓
domain/catalogs/

docs/01-dominio/catalogacao-v1.md, entidades-v1.md, glossario-v1.md,
linguagem-soe-ccg-v1.md, mapa-relacionamentos-v1.md, relacionamentos-v1.md,
separacao-dominios-v1.md, overview-v1.md, ciclo-de-vida-v1.md  (9 arquivos soltos restantes)
    ↓
docs/03-domain/

docs/07-uso/08-agentes/*  (4 arquivos)
    ↓
interfaces/agents/

docs/07-uso/* (resto, 54 arquivos)
    ↓
docs/08-user/

docs/00-projeto/*  (8 arquivos)
    ↓
docs/00-governance/

docs/05-desenvolvimento/* (2 arquivos)
    ↓
docs/06-development/

docs/06-operacao/* (1 arquivo)
    ↓
docs/07-operation/
```

---

# 7. Arquivos Novos Recomendados

| Arquivo | Diretório | Finalidade | Dependências | Prioridade |
|---|---|---|---|---|
| `paths.py` | `kernel/shared/` | Fonte única de caminhos, elimina os 4 cálculos de ROOT | nenhuma | **P0 — bloqueia tudo o resto** |
| `naming.md` | `kernel/specification/policies/` | Convenção formal de sufixo de versão, causa raiz da duplicação encontrada | `versioning/version_scheme.md` | **P0** |
| `cycle_guard.py` | `kernel/runtime/edge_engine/` | Impede DerivedEdge usar DerivedEdge como input — gap identificado na análise V2 | `specification/edges/cycles.md` | **P1** |
| `schema_registry.py` | `kernel/runtime/` | Fecha a lacuna de SchemaRegistry ausente identificada na análise V2 | `specification/schemas/*` | **P1** |
| `architectural_decision.py` | `runtime/analysis/decision/` | Porta `DecisaoArquitetural`, hoje exclusiva de `models_v1.py` | `runtime/analysis/auditors/baseline_auditor.py` | **P1** |
| `baseline_auditor.py` | `runtime/analysis/auditors/` | Porta o único motor exclusivo do entrypoint legado | `kernel/runtime/policy_engine.py` | **P1** |
| `pipeline_definition.py` | `runtime/pipeline/` | Formaliza a ordem Parser→Resolver→Validator→Executor→FAA→Importer, hoje implícita em `codigo/__main__.py` | `kernel/PUBLIC_API.md` | **P2** |
| `PUBLIC_API.md` | `kernel/` | Lista os 5 pontos de entrada permitidos do kernel | todos os módulos de `kernel/runtime/` | **P2** |
| `DEPENDENCY_RULES.md` | `kernel/` | Formaliza a regra "specification nunca importa de runtime" | nenhuma | **P2** |
| `0001-v4-architecture.md` | `governance/decisions/` (ADR) | Registra esta própria auditoria como decisão formal | esta auditoria | **P2** |

---

# 8. Arquivos a Remover

Tabela final de decisão, par a par, derivada diretamente da matriz da Seção 1.2.

| Par/grupo | Qual permanece | Qual remover | Justificativa |
|---|---|---|---|
| `estrutura.py` / `estrutura_v1.py` | `estrutura.py` (vira `structure_auditor.py`) | `estrutura_v1.py` | `estrutura.py` é mais recente e é o consumido pelo entrypoint com mais motores ativos (13 vs 12) |
| `filosofia.py` / `filosofia_v1.py` | `filosofia.py` | `filosofia_v1.py` | mesmo critério |
| `dominio.py` / `dominio_v1.py` | `dominio.py` | `dominio_v1.py` | mesmo critério |
| `dados.py` / `dados-v2.py` | `dados.py` | `dados-v2.py` | **atenção:** apesar do nome "-v2" sugerir mais recente, é `dados.py` (sem sufixo) que está ativo no entrypoint principal; confirmar manualmente se há lógica em `dados-v2.py` que `dados.py` não tem antes de remover |
| `integridade.py` / `integridade-v2.py` | `integridade.py` | `integridade-v2.py` | mesmo alerta de nomenclatura do item acima |
| `semantica.py` / `semantica_v1.py` / `semantica-v2.py` | `semantica.py` | `semantica_v1.py` **e** `semantica-v2.py` | único caso com 3 arquivos; `semantica-v2.py` é código morto confirmado (nenhum entrypoint o importa) |
| `dependencias.py` / `dependencias-v2.py` | `dependencias.py` | `dependencias-v2.py` | mesmo alerta de nomenclatura |
| `cobertura.py` / `cobertura_v1.py` | `cobertura.py` | `cobertura_v1.py` | mesmo critério |
| `maturidade.py` / `maturidade_v1.py` | `maturidade.py` | `maturidade_v1.py` | mesmo critério |
| `baseline_v1.py` | **portar para `baseline_auditor.py`** | — | não é duplicado, é exclusivo — não remover, migrar (ver Seção 7) |
| `models.py` / `models_v1.py` | `models.py`, **enriquecido com `DecisaoArquitetural`** | `models_v1.py` (após a fusão) | fundir antes de remover, não remover diretamente |
| `config.py` / `config_v1.py` | `config.py` | `config_v1.py` | depois que `kernel/shared/paths.py` absorver a resolução de ROOT de ambos |
| `utils.py` / `utils_v1.py` | `utils.py` | `utils_v1.py` | sem diferença funcional identificada na auditoria — confirmar com diff antes de remover |
| `auditor.py` / `auditor-v1.py` | nenhum dos dois — ambos viram `runtime/analysis/orchestrator.py` | ambos, após a fusão completa (Passo 6) | não é caso de "escolher um", é caso de fusão genuína |
| `relatorios/console.py` / `relatorios/console_v1.py` | `console.py` | `console_v1.py` | mesmo critério dos motores |

**Nota de processo:** nenhuma remoção deste passo deve acontecer antes do Passo 6 do plano de migração (Seção 5) ter sido validado com paridade de output confirmada. Remover antes disso é o cenário de maior risco de perda de funcionalidade silenciosa identificado nesta auditoria.

---

# 9. Mapa de Dependências

```text
Interfaces
     ↓
Runtime
     ↓
Kernel
     ↓
Domain
     ↓
Infrastructure
```

**Mapa expandido, com os módulos reais desta auditoria posicionados:**

```text
interfaces/terminal/cli/__main__.py
     ↓ (consome)
runtime/pipeline/  →  runtime/parser/  →  runtime/resolver/  →  runtime/validator/  →  runtime/importer/
     ↓ (todos consultam)
kernel/PUBLIC_API.md  (os 5 pontos de entrada — Seção 4.12)
     ↓ (implementado por)
kernel/runtime/{id_generator, schema_registry, transition_engine, edge_engine, policy_engine}.py
     ↓ (lê como dados)
kernel/specification/{identity, contracts, schemas, states, policies, invariants, edges, versioning}/
     ↓ (descreve)
domain/{recipes, ingredients, techniques, equipment, executions, experiments, observations}/
     ↓ (persistido via)
infrastructure/database/{sqlite, schemas, migrations, seeds}/
```

`runtime/analysis/` (a fusão FAA) é um consumidor lateral, não parte da cadeia principal — ele lê `domain/` e `kernel/specification/` para auditar conformidade, mas nunca é dependência de `runtime/parser/` ou dos demais módulos do pipeline principal:

```text
runtime/analysis/orchestrator.py
     ↓ (lê, nunca escreve)
domain/*  +  kernel/specification/*
     ↓ (produz)
runtime/analysis/reports/  +  runtime/analysis/state/state_store.py
```

**Regra de violação a vigiar:** se algum dia `runtime/parser/` ou `runtime/validator/` precisar importar de `runtime/analysis/`, isso é sinal de que lógica de auditoria vazou para dentro do pipeline principal — um anti-padrão que deve ser barrado por revisão, não só por convenção.

---

# 10. Roadmap de Evolução V3 → V4 → V5

## V3 (proposta anterior, já avaliada)
Estabeleceu a separação em 5 camadas (Kernel/Runtime/Domain/Infrastructure/Interfaces). Correta na divisão macro, mas com kernel raso (sem distinguir especificação de implementação) e sem visibilidade sobre a profundidade real da duplicação na stack FAA — porque a V3 foi escrita antes desta auditoria linha-a-linha.

## V4 (esta proposta)
Resolve três lacunas concretas da V3, todas verificadas nesta auditoria:
1. Kernel dividido em `specification/` (lei) e `runtime/` (mecanismo) — evita que o kernel vire um "God Object" disfarçado, risco já levantado em ciclos de análise anteriores.
2. Stack FAA dupla convergida fisicamente em `runtime/analysis/`, com matriz de migração motor-a-motor verificada (não estimada).
3. `kernel/shared/paths.py` como correção de maior impacto prático imediato — resolve um bug latente real (4 cálculos divergentes de ROOT) antes de qualquer outra mudança.

**Critério de saída do V4:** todos os 7 passos do plano de migração (Seção 5) executados, com paridade de output confirmada no Passo 6, e zero arquivos da Seção 8 ainda presentes no repositório.

## V5 (preparação, não execução imediata)

Itens que esta auditoria identifica como prováveis necessidades futuras, mas que não devem ser antecipados antes do V4 estar consolidado — antecipar architecture nesta fase é o mesmo erro que gerou a stack FAA dupla original:

- **`schema/definitions/ → generated/`** como pipeline real de múltiplos alvos de serialização (SQL, JSON Schema, OpenAPI, GraphQL) a partir de uma única fonte. A V4 já reserva o diretório (Seção 3), mas a lógica de geração multi-alvo é trabalho de V5.
- **`interfaces/api/rest/` e `interfaces/api/grpc/`** como exposição real de rede — hoje o sistema é CLI-only (`codigo/__main__.py`), então construir API antes de o pipeline estar 100% migrado para `runtime/` seria repetir o erro de paralelismo prematuro encontrado nesta auditoria.
- **Banco PostgreSQL como alternativa ao SQLite** — mencionado nas propostas anteriores como `infrastructure/database/postgres/`, mas sem dado real hoje (13 registros em `dados/`) que justifique a complexidade antes do volume de domínio crescer.
- **Consolidação dos 11 arquivos `.md` soltos na raiz** (`ANALISE-COMPLETA-2026-06-28.md`, `CONSOLIDACAO-V1-SUMMARY.md`, etc., ~80 KB de prosa histórica) em `CHANGELOG.md` — não bloqueia nenhuma migração de código, pode acontecer em paralelo a qualquer passo do V4, mas fica fora do escopo crítico desta auditoria.

**Regra de governança para V5:** nenhum item desta lista deve iniciar implementação antes que `governance/adr/` registre uma decisão formal — o padrão exato que `governance/decisions/0001-v4-architecture.md` (Seção 7) estabelece para esta própria migração.
