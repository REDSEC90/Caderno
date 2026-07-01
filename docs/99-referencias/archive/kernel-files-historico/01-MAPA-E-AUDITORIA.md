# SOE-CCG — Architecture Review Oficial

> Auditoria arquitetural completa, produzida a partir da leitura real do repositório (304 arquivos, 5.339 linhas de Python, 24.347 linhas de Markdown em `docs/`), não apenas das propostas anteriores. Cada afirmação abaixo foi verificada por grep/leitura direta de código — onde uma proposta anterior generalizava ("existem duplicações"), este documento nomeia o arquivo exato, a linha exata, e quem o consome.

**Como ler este documento:** ele tem 10 seções correspondentes aos 10 entregáveis pedidos. Pode ser lido inteiro como especificação de referência, ou consultado por seção conforme a necessidade do momento.

---

# 1. Mapa Completo do Sistema

## 1.1 Árvore real por volume

| Camada | Localização atual | Arquivos | Linhas | Observação |
|---|---|---|---|---|
| Runtime (núcleo) | `codigo/` | 6 `.py` | 680 | Coeso, todos convergem em `ir.py` |
| FAA — stack A | `scripts/faa/` | 19 `.py` | ~700 | Orientada a orchestrator/engines |
| FAA — stack B | `scripts/auditoria/` | 35 `.py` | ~3.500 | Orientada a motores, 3 gerações coexistindo |
| Documentação | `docs/` | 198 `.md` | 24.347 | 58 só em `07-uso/`, 1 só em `06-operacao/` |
| Dados reais | `dados/` | 13 `.md` | — | Sistema em fase de seed, não produção |
| Banco | `banco_de_dados/` | 5 arquivos | — | `migracoes/` vazia, schema único em SQL puro |
| Raiz solta | `*.md` na raiz | 11 arquivos | ~80 KB | Sem hierarquia entre si |

## 1.2 Módulos e responsabilidades reais (não nominais)

### `codigo/` — Runtime real
```
codigo/ir.py            63 linhas  — Entity, Edge, EdgeKind, EdgeOrigin, KnowledgeGraph
codigo/parser.py       122 linhas  — depende de .ir (Edge, EdgeKind, EdgeOrigin, Entity, KnowledgeGraph)
codigo/resolvedor.py    40 linhas  — depende de .ir (KnowledgeGraph)
codigo/validador.py     92 linhas  — depende de .ir (EdgeKind, KnowledgeGraph)
codigo/importador.py   227 linhas  — depende de .ir (KnowledgeGraph)
codigo/__main__.py     134 linhas  — entrypoint CLI
```
**Acoplamento real:** todos os 5 módulos de execução importam de `.ir` usando import relativo (`from .ir import ...`). `ir.py` é o único nó sem dependências internas — é o verdadeiro kernel de tipos do runtime atual, mesmo morando fisicamente em `codigo/`.

### `scripts/faa/` — Stack A (orchestrator-centric)
```
core/orchestrator.py  → importa de: core.scanner, core.rules, engines.structure_engine,
                          issues.detector, planner.prioritizer, planner.roadmap_engine,
                          metrics.coverage, state.state_store, config
```
**Achado crítico de empacotamento:** todos os imports em `scripts/faa/` são absolutos sem prefixo de pacote (`from core.scanner import...`, não `from scripts.faa.core.scanner import...`). Isso significa que o módulo **só funciona se executado com `scripts/faa/` como diretório de trabalho atual**, ou com manipulação manual de `sys.path`. Não é importável de fora como pacote Python padrão. Isso é uma falha de portabilidade real, não estética.

`orchestrator.py` é o nó central — 8 dependências internas convergindo nele, igual ao papel de `ir.py` em `codigo/`, mas sem a mesma disciplina de import relativo.

### `scripts/auditoria/` — Stack B (motor-centric, 3 gerações)

Esta é a área de maior risco do projeto. A matriz completa de consumo real (verificada por leitura de cada `import`, não suposição):

| Motor | `auditor.py` (entrypoint atual) | `auditor-v1.py` (entrypoint legado) | Status |
|---|---|---|---|
| baseline | — | `baseline_v1.py` | exclusivo do legado |
| estrutura | `estrutura.py` | `estrutura_v1.py` | duplicado vivo |
| filosofia | `filosofia.py` | `filosofia_v1.py` | duplicado vivo |
| dominio | `dominio.py` | `dominio_v1.py` | duplicado vivo |
| templates | `templates.py` | — | exclusivo do atual |
| contratos | `contratos.py` | — | exclusivo do atual |
| dados | `dados.py` | `dados-v2.py` | duplicado vivo (note a inversão: "-v2" é consumido pelo entrypoint "v1") |
| integridade | `integridade.py` | `integridade-v2.py` | duplicado vivo |
| semantica | `semantica.py` | `semantica_v1.py` | duplicado vivo — **e ainda existe `semantica-v2.py`, que nenhum dos dois entrypoints importa** |
| padroes | `padroes.py` | `padroes.py` (mesmo arquivo) | compartilhado, não duplicado |
| escalabilidade | `escalabilidade.py` | `escalabilidade.py` (mesmo arquivo) | compartilhado, não duplicado |
| dependencias | `dependencias.py` | `dependencias-v2.py` | duplicado vivo |
| cobertura | `cobertura.py` | `cobertura_v1.py` | duplicado vivo |
| maturidade | `maturidade.py` | `maturidade_v1.py` | duplicado vivo |

**Conclusão do mapa:** não são "duas versões", são efetivamente **três populações de arquivo** — os sem sufixo (consumidos por `auditor.py`), os com sufixo consumidos por `auditor-v1.py` (que mistura `_v1`, `-v1` e `-v2` sem padrão consistente de nomenclatura), e `semantica-v2.py`, que é órfão de ambos.

### Imports de suporte (`models`/`config`/`utils`) — duas famílias paralelas e completas

```
Família atual:  models.py     → config.py     → utils.py    (consumida por auditor.py + 13 motores)
Família legada: models_v1.py  → config_v1.py                (consumida por auditor-v1.py + 8 motores _v1)
```

`models_v1.py` não é um subconjunto de `models.py` — tem uma classe própria e genuína, `DecisaoArquitetural` (com campos `aprovado`, `pontuacao_geral`, `grupos`, `grupos_reprovados`, `artefatos_ausentes`, `artefatos_presentes`, `artefatos_total`), que **não existe em `models.py`**. Isso é tratado na Seção 8 como item a portar, não a descartar.

## 1.3 Dependências de documentação

`docs/05-desenvolvimento/` tem apenas 2 arquivos; `docs/06-operacao/` tem apenas 1. Comparado aos 58 de `docs/07-uso/`, isso é uma assimetria real de maturidade entre módulos de documentação — não apenas uma questão de organização de pastas.

---

# 2. Auditoria Arquitetural

## 2.1 Duplicações (confirmadas, não estimadas)

| Tipo | Localização | Severidade |
|---|---|---|
| Stack de execução duplicada | `scripts/faa/` vs `scripts/auditoria/` cumprindo o mesmo papel (auditoria arquitetural) com designs incompatíveis | **Crítica** |
| Motores duplicados vivos | 10 dos 13 motores em `scripts/auditoria/motores/` têm 2 implementações ativas (ver matriz 1.2) | **Crítica** |
| `ROOT` hardcoded divergente | `codigo/__main__.py`, `codigo/importador.py` (`.parent.parent`), `scripts/faa/config.py` (`.parent.parent.parent`), `scripts/auditoria/config.py` (`.parent.parent.parent.resolve()`) — 4 cálculos independentes do mesmo valor lógico | **Crítica** |
| `models`/`config`/`utils` duplicados | Família completa `_v1` paralela à atual, sem ponte de migração | **Alta** |

## 2.2 Violações de responsabilidade

- **Import circular estrutural em `motores/__init__.py`:** o arquivo faz `from motores import (estrutura, filosofia, ...)` — o próprio pacote `motores` importando de si mesmo dentro do seu `__init__.py`. Funciona apenas por acidente de como o Python resolve esse caso específico; é frágil a qualquer refatoração de empacotamento.
- **Documentação invertida:** `scripts/auditoria/README.md` descreve exclusivamente o `auditor-v1.py` ("FAA v1") como se fosse o sistema vigente, mas é `auditor.py` (sem sufixo) que tem o conjunto mais completo e atual de motores (13, incluindo `templates` e `contratos`, que o v1 não possui). Quem lê o README primeiro é guiado para o caminho errado.
- **Empacotamento não portável em `scripts/faa/`:** já descrito em 1.2 — imports absolutos sem prefixo de pacote tornam o módulo dependente do diretório de execução.

## 2.3 Código morto confirmado

| Arquivo | Por que é morto |
|---|---|
| `scripts/auditoria/motores/semantica-v2.py` | Não é importado por `auditor.py` (que usa `semantica.py`) nem por `auditor-v1.py` (que usa `semantica_v1.py`). Nenhum caminho de execução o alcança. |

Diferente dos demais arquivos com sufixo, que são "duplicados vivos" (alcançáveis via `auditor-v1.py`), este é o único caso de código genuinamente inalcançável encontrado na auditoria.

## 2.4 Módulos que podem ser fundidos

- `scripts/faa/` + `scripts/auditoria/` → um único framework de análise (detalhado nas Seções 3 e 4). Cumprem o mesmo papel conceitual (auditoria arquitetural do próprio repositório) com dois designs que não se comunicam.
- `models.py` + `models_v1.py` → fusão simples: copiar `DecisaoArquitetural` de `models_v1.py` para `models.py`, eliminando a necessidade do arquivo legado.
- `padroes.py` e `escalabilidade.py` já são compartilhados entre os dois entrypoints — não precisam de ação, servem de prova de que a convergência é tecnicamente viável para os demais pares.

## 2.5 Módulos que devem ser separados

- `kernel/` (ver V3 anterior) já estava sobrecarregado misturando especificação e implementação — confirmado e aprofundado na Seção 4 deste documento.
- `docs/01-dominio/` mistura 4 responsabilidades (`contratos/`, `esquemas/`, `templates/`, `catalogos/`) mais 17 arquivos soltos no nível raiz da própria pasta — confirmado por contagem direta (48 arquivos totais em `docs/01-dominio/`).

---

# 3. Arquitetura V4 — Árvore Completa

A V4 herda a separação Kernel/Runtime/Domain/Infrastructure/Interfaces da V3, mas incorpora três correções que a auditoria acima tornou obrigatórias: (a) o kernel divide-se em `specification/` (sem código executável, idealmente só Markdown/dados estruturados) e `runtime/` (implementação Python das leis do kernel) — separando lei de mecanismo; (b) a stack FAA dupla converge fisicamente em `runtime/analysis/`, um único framework; (c) `schema/` ganha estrutura de camadas derivadas (`definitions/ → generated/`), preparando o sistema para múltiplos alvos de serialização sem reescrever o registry a cada novo formato.

```text
SOE-CCG/

├── kernel/                                    # Estável por design. Dependência só de fora pra dentro.
│   │
│   ├── specification/                         # SOMENTE leis. Idealmente sem Python executável.
│   │   ├── identity/
│   │   │   ├── ids.md                         # Grammar formal: REC-######, ING-######...
│   │   │   ├── names.md                       # receita-doce-leite (slug canônico)
│   │   │   ├── tags.md                        # #receita
│   │   │   ├── references.md                  # REC-000001#ingrediente
│   │   │   ├── uris.md
│   │   │   └── aliases.md
│   │   ├── contracts/
│   │   │   ├── entities/                      # Sucessor de docs/01-dominio/contratos/* (7 arquivos)
│   │   │   │   ├── receita.md
│   │   │   │   ├── ingrediente.md
│   │   │   │   ├── tecnica.md
│   │   │   │   ├── equipamento.md
│   │   │   │   ├── execucao.md
│   │   │   │   ├── observacao.md
│   │   │   │   └── experimento.md
│   │   │   ├── runtime/                       # NOVO — contrato do que o runtime deve garantir
│   │   │   ├── plugins/                       # NOVO — contrato de extensão (scripts/faa/plugins hoje informal)
│   │   │   ├── storage/                       # NOVO — contrato do que o SQLite deve refletir
│   │   │   ├── api/                           # NOVO
│   │   │   └── interfaces/                    # NOVO — contrato de CLI/agentes
│   │   ├── schemas/                           # Sucessor de docs/01-dominio/esquemas/* (7 arquivos)
│   │   ├── states/
│   │   │   ├── receita_states.md              # Sucessor de docs/01-dominio/catalogos/estados-receita-v1.md
│   │   │   └── entity_states.md               # Sucessor de estados-todas-entidades-v1.md
│   │   ├── policies/
│   │   │   ├── source_of_truth.md             # "Markdown é fonte, SQLite é índice" formalizado
│   │   │   ├── derivation.md
│   │   │   └── naming.md                      # Resolve a inconsistência -v1/_v1/-v2 encontrada na auditoria
│   │   ├── invariants/
│   │   │   └── invariant_definitions.md       # Os 8 invariantes do protocolo de agentes
│   │   ├── versioning/
│   │   │   └── version_scheme.md
│   │   └── edges/
│   │       ├── types.md                       # DocumentEdge / ResolvedEdge / DerivedEdge
│   │       ├── rules.md
│   │       ├── inference.md
│   │       └── cycles.md                      # Guarda anti-ciclo, formalizada como regra (não só código)
│   │
│   ├── runtime/                                # Implementação Python das leis acima. Único lugar com .py no kernel.
│   │   ├── id_generator.py
│   │   ├── schema_registry.py
│   │   ├── transition_engine.py
│   │   ├── edge_engine.py
│   │   │   └── cycle_guard.py                 # Implementação executável de specification/edges/cycles.md
│   │   ├── policy_engine.py
│   │   └── tests/
│   │       ├── test_id_generator.py
│   │       ├── test_schema_registry.py
│   │       ├── test_transition_engine.py
│   │       ├── test_edge_engine.py
│   │       └── test_policy_engine.py
│   │
│   ├── shared/                                 # Tipos e utilidades usadas por specification/ e runtime/ simultaneamente
│   │   └── paths.py                            # Substitui os 4 cálculos de ROOT divergentes encontrados na auditoria
│   │
│   ├── README.md
│   ├── KERNEL_SPECIFICATION.md
│   ├── DEPENDENCY_RULES.md                     # kernel nunca importa de runtime/domain/infrastructure/interfaces
│   ├── PUBLIC_API.md
│   └── VERSION_POLICY.md
│
├── runtime/                                    # Implementa o que o kernel especifica
│   │
│   ├── pipeline/                               # NOVO — define a ordem formal (estava implícita)
│   │   └── pipeline_definition.py              # Parser → Resolver → Validator → Executor → FAA → Importer
│   │
│   ├── parser/                                 # Sucessor de codigo/parser.py
│   │   ├── markdown_parser.py
│   │   └── tests/
│   │
│   ├── resolver/                               # Sucessor de codigo/resolvedor.py
│   │   ├── reference_resolver.py
│   │   └── tests/
│   │
│   ├── validator/                              # Sucessor de codigo/validador.py
│   │   ├── entity_validator.py                 # Consulta kernel/runtime/schema_registry.py
│   │   └── tests/
│   │
│   ├── executor/
│   │
│   ├── importer/                               # Sucessor de codigo/importador.py
│   │   ├── sqlite_importer.py
│   │   └── tests/
│   │
│   ├── ir/                                     # Sucessor de codigo/ir.py — o nó central confirmado na auditoria
│   │   ├── intermediate_representation.py      # Entity, Edge, EdgeKind, EdgeOrigin, KnowledgeGraph
│   │   └── tests/
│   │
│   ├── eventbus/
│   │
│   ├── cache/
│   │
│   ├── analysis/                               # FUSÃO de scripts/faa/ + scripts/auditoria/ — fim da stack dupla
│   │   ├── orchestrator.py                     # Sucessor único de core/orchestrator.py (FAA-A) + auditor.py (FAA-B)
│   │   ├── auditors/                           # Sucessor unificado de scripts/auditoria/motores/*
│   │   │   ├── structure_auditor.py            # estrutura.py — única versão, sem sufixo
│   │   │   ├── philosophy_auditor.py           # filosofia.py
│   │   │   ├── domain_auditor.py                # dominio.py
│   │   │   ├── templates_auditor.py            # templates.py
│   │   │   ├── contracts_auditor.py             # contratos.py
│   │   │   ├── data_auditor.py                  # dados.py
│   │   │   ├── integrity_auditor.py             # integridade.py
│   │   │   ├── semantics_auditor.py             # semantica.py
│   │   │   ├── patterns_auditor.py              # padroes.py
│   │   │   ├── scalability_auditor.py           # escalabilidade.py
│   │   │   ├── dependency_auditor.py            # dependencias.py
│   │   │   ├── coverage_auditor.py              # cobertura.py
│   │   │   ├── maturity_auditor.py              # maturidade.py
│   │   │   └── baseline_auditor.py              # PORTADO de baseline_v1.py — único motor exclusivo do legado
│   │   ├── engines/                             # Sucessor de scripts/faa/engines/
│   │   │   └── structure_engine.py
│   │   ├── planner/                             # Sucessor de scripts/faa/planner/
│   │   │   ├── prioritizer.py
│   │   │   └── roadmap_engine.py
│   │   ├── metrics/                             # Sucessor de scripts/faa/metrics/ + auditoria coverage
│   │   │   └── coverage.py
│   │   ├── reports/                             # Sucessor de scripts/faa/observability/ + auditoria/relatorios/
│   │   │   ├── console_report.py
│   │   │   └── markdown_report.py
│   │   ├── state/                               # Sucessor de scripts/faa/state/
│   │   │   └── state_store.py
│   │   ├── plugins/                             # Sucessor de scripts/faa/plugins/
│   │   │   └── custom_rules.py
│   │   ├── decision/                            # NOVO — porta DecisaoArquitetural de models_v1.py
│   │   │   └── architectural_decision.py
│   │   └── tests/
│   │       └── test_analysis.py
│   │
│   ├── diagnostics/
│   │
│   ├── compatibility/
│   │
│   └── README.md
│
├── domain/                                     # Conhecimento culinário-gastronômico — Markdown como fonte
│   │
│   ├── recipes/                                # Sucessor de dados/receitas/ (1 registro real hoje)
│   ├── ingredients/                             # Sucessor de dados/ingredientes/ (5 registros reais hoje)
│   ├── techniques/                              # Sucessor de dados/tecnicas/ (3 registros reais hoje)
│   ├── equipment/                               # Sucessor de dados/equipamentos/ (2 registros reais hoje)
│   ├── executions/                              # Sucessor de dados/execucoes/ (1 registro real hoje)
│   ├── experiments/                             # Sucessor de dados/experimentos/ (0 registros hoje)
│   ├── observations/                            # Sucessor de dados/observacoes/ (1 registro real hoje)
│   ├── attachments/                             # Sucessor de dados/anexos/ (0 registros hoje)
│   │
│   ├── knowledge/                               # NOVO — conhecimento transversal, não preso a uma entidade só
│   │
│   ├── catalogs/                                # Absorve docs/01-dominio/catalogos/* (8 arquivos)
│   ├── templates/                               # Absorve docs/01-dominio/templates/* (9 arquivos)
│   │
│   └── README.md                                # ENTITY_INDEX, RELATION_INDEX, CATALOG_INDEX
│
├── infrastructure/
│   │
│   ├── database/
│   │   ├── sqlite/
│   │   │   └── soe-ccg.db                       # Sucessor de banco_de_dados/sqlite/* (204 KB hoje)
│   │   ├── schemas/
│   │   │   └── schema-sqlite-v1.sql             # Sucessor de banco_de_dados/esquemas/*
│   │   ├── migrations/                          # Hoje vazia — primeira migração real entra aqui
│   │   │   └── 0001_initial.sql
│   │   └── seeds/
│   │       └── seed-categorias-v1.sql
│   │
│   ├── storage/
│   │   ├── archive/
│   │   └── cache/
│   │
│   ├── import/
│   │   └── importar.sh                          # Sucessor de scripts/importacao/importar.sh
│   ├── export/
│   ├── backup/                                  # Sucessor de scripts/copia_seguranca/
│   ├── install/                                 # Sucessor de scripts/instalacao/
│   ├── maintenance/                             # Sucessor de scripts/manutencao/
│   ├── logging/
│   ├── metrics/
│   ├── security/
│   └── configuration/                           # NOVO — separado de install/, porque configuração cresce sozinha
│
├── interfaces/
│   │
│   ├── terminal/                                # NOVO — CLI e TUI são coisas diferentes, separadas explicitamente
│   │   ├── cli/
│   │   │   └── __main__.py                      # Sucessor de codigo/__main__.py
│   │   └── tui/
│   │
│   ├── agents/                                  # Absorve docs/07-uso/08-agentes/ (4 arquivos)
│   │   ├── agent_contract.md
│   │   ├── operation_sequences.md
│   │   └── invariants_reference.md
│   │
│   ├── api/
│   │   └── rest/
│   │
│   └── sdk/
│
├── tools/                                       # Auditoria de REPOSITÓRIO (meta), distinto de runtime/analysis (produto)
│   ├── generator/
│   ├── migration/
│   ├── benchmark/
│   └── release/
│
├── standards/                                    # NOVO — fonte normativa única (hoje espalhada em 3 lugares)
│   ├── naming/                                   # Resolve -v1 vs _v1 vs -v2, encontrado 10x na auditoria
│   ├── metadata/
│   ├── markdown/
│   ├── frontmatter/
│   ├── ids/
│   ├── relationships/
│   ├── serialization/
│   ├── schemas/
│   ├── templates/
│   └── quality/
│
├── governance/                                   # NOVO — separa decisão de documentação
│   ├── adr/                                      # Decisões arquiteturais como as desta auditoria
│   ├── rfc/
│   ├── decisions/
│   ├── roadmap/
│   └── deprecation/                              # Onde registrar formalmente a remoção dos arquivos da Seção 8
│
├── build/                                        # NOVO — tudo gerado automaticamente, nunca editado à mão
│   ├── artifacts/
│   ├── generated/                                # Ex: schema SQL gerado a partir de schema/definitions/
│   └── packages/
│
├── schema/                                       # NOVO nível raiz — camadas de derivação explícitas
│   ├── definitions/                              # Fonte única em Python/YAML
│   ├── generated/                                # SQL, JSON Schema, OpenAPI — todos derivados, nunca editados
│   ├── migration/
│   └── registry/
│
├── tests/
│   ├── kernel/
│   ├── runtime/
│   ├── domain/
│   ├── infrastructure/
│   ├── interfaces/
│   ├── contract/                                 # Sucessor de testes/contract/
│   ├── golden/                                   # Sucessor de testes/golden/ (invalid/, minimal/)
│   ├── integration/                              # Sucessor de testes/integration/
│   ├── regression/                               # Sucessor de testes/regression/
│   ├── unit/                                     # Sucessor de testes/unit/
│   └── fixtures/
│
├── docs/                                          # Reorganizada por camada — espelha a árvore acima
│   ├── 00-governance/                             # NOVO nome — antes 00-projeto
│   ├── 01-kernel/                                 # Documenta kernel/specification + kernel/runtime
│   ├── 02-runtime/
│   ├── 03-domain/
│   ├── 04-infrastructure/
│   ├── 05-interfaces/
│   ├── 06-development/                            # Hoje só 2 arquivos — assimetria sinalizada na Seção 2
│   ├── 07-operation/                              # Hoje só 1 arquivo — assimetria sinalizada na Seção 2
│   ├── 08-user/                                   # Sucessor de docs/07-uso/ (58 arquivos hoje)
│   ├── 09-reference/
│   ├── 10-release/
│   ├── 98-drafts/
│   └── 99-archive/
│
├── resources/
│   ├── images/
│   ├── videos/
│   ├── audio/
│   └── documents/
│
├── workspace/
│   ├── drafts/
│   ├── imports/                                   # Sucessor de dados/importacao/
│   └── experiments/
│
├── .git/
├── .gitignore
├── README.md
├── LICENSE                                        # GPLv3, confirmado padrão — sem ação necessária
├── CHANGELOG.md                                    # Consolida os 11 arquivos .md soltos hoje na raiz
├── ARCHITECTURE.md                                 # Este documento, versão definitiva pós-decisão
└── governance/decisions/0001-v4-architecture.md    # Esta auditoria, formalizada como ADR
```

---
*(Continua na próxima seção do mesmo arquivo: Kernel Specification, Plano de Migração, Mapa de Movimentação, Arquivos Novos, Arquivos a Remover, Mapa de Dependências e Roadmap V3→V4→V5.)*
