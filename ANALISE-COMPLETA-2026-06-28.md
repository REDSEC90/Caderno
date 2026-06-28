# Análise Completa do SOE-CCG

**Data:** 2026-06-28  
**Autor:** Kiro (análise automatizada)  
**Versão:** 1.0

---

## 1. Identidade do Projeto

O **SOE-CCG** (Sistema de Registro, Organização, Evolução e Consulta de Conhecimento Gastronômico) é um motor de conhecimento gastronômico — não um gerenciador de receitas.

Sua missão é preservar, organizar, relacionar e evoluir conhecimento culinário de forma permanente, independente de tecnologia. O princípio fundante é que o **conhecimento é permanente** e a **implementação é temporária**.

A cadeia de autoridade é:

```
Filosofia → Constituição → Governança → Especificações → Modelagem → Implementação → Interface
```

Dois documentos de planejamento de próximas versões existem na raiz: `PLAN-SOE-CCG-V2.md` (plataforma semântica) e `PLAN-docs-07-uso-V2.md` (especificação operacional canônica).

---

## 2. Estrutura de Diretórios

```
SOE-CCG/
│
├── README.md                     # Visão geral e status do projeto
├── RESUMO.md                     # Resumo executivo
├── ENTREGA-COMPLETA.md           # Relatório de entrega FAA v2 + consolidação v1
├── CONSOLIDACAO-V1-SUMMARY.md    # Resumo executivo da consolidação
├── PLAN-SOE-CCG-V2.md            # Plano arquitetural V2
├── PLAN-docs-07-uso-V2.md        # Plano da documentação operacional V2
├── LICENSE                       # (vazio)
│
├── dados/                        # ⭐ FONTE OFICIAL DO CONHECIMENTO
│   ├── receitas/                 # 1 receita seed
│   ├── ingredientes/             # 4 ingredientes seed
│   ├── tecnicas/                 # 3 técnicas seed
│   ├── equipamentos/             # 2 equipamentos seed
│   ├── execucoes/                # 1 execução seed
│   ├── observacoes/              # 1 observação seed
│   ├── experimentos/             # (vazio)
│   ├── anexos/                   # (vazio)
│   └── importacao/               # (vazio)
│
├── banco_de_dados/
│   ├── esquemas/
│   │   └── schema-sqlite-v1.sql  # Schema completo SQLite (8 tabelas principais + 9 junção + views)
│   ├── seeds/
│   │   └── seed-categorias.sql   # 10 categorias iniciais
│   ├── sqlite/                   # (vazio — BD ainda não gerado)
│   └── migracoes/                # (vazio)
│
├── codigo/                       # Pipeline computacional (Python)
│   ├── ir-v1.py                  # IR: Entity, Edge, KnowledgeGraph
│   ├── parser-v1.py              # Parser Markdown → KnowledgeGraph
│   ├── resolvedor-v1.py          # Resolver de referências + incoming edges
│   ├── validador-v1.py           # Validador de ciclos e entidades isoladas
│   └── importador-v1.py          # KnowledgeGraph → SQLite
│
├── docs/
│   ├── 00-projeto/               # Visão, constituição, filosofia, princípios, roadmap, glossário, escopo
│   ├── 01-dominio/               # Entidades, relacionamentos, esquemas, templates, contratos, catálogos
│   ├── 02-arquitetura/           # Diagrama mestre, fluxo de dados, versionamento, importação, exportação
│   ├── 03-modelagem/             # Entidades ER, SQLite, IDs, normalização, objetivos, conceitos fundamentais
│   ├── 04-padroes/               # Nomenclatura, IDs, metadados, tags, validação, ADRs, políticas
│   ├── 05-desenvolvimento/       # Casos de uso, padrões de desenvolvimento
│   ├── 06-operacao/              # Guia de operação
│   ├── 07-uso/                   # (vazio — V2 planejada)
│   ├── 98-rascunhos/             # (vazio)
│   └── 99-referencias/           # Relatórios, snapshots FAA, guias, arquivo histórico
│       ├── archive/              # Documentos v0.5 arquivados
│       └── snapshots/            # 5 snapshots históricos do FAA
│
├── scripts/
│   ├── faa.sh                    # Helper CLI para FAA
│   ├── faa/                      # FAA v2 — Ferramenta de governança arquitetural
│   │   ├── faa                   # Executável principal
│   │   ├── config.py
│   │   ├── core/                 # scanner, rules, orchestrator
│   │   ├── engines/              # structure_engine
│   │   ├── issues/               # detector
│   │   ├── metrics/              # coverage
│   │   ├── observability/        # report_console
│   │   ├── planner/              # roadmap_engine, prioritizer
│   │   ├── state/                # state_store
│   │   ├── plugins/              # custom_rules
│   │   └── tests/                # test_basic.py
│   ├── auditoria/                # Sistema de auditoria v1 (predecessora do FAA)
│   │   ├── auditor.py / auditor-v1.py
│   │   ├── config.py / config_v1.py
│   │   └── motores/              # 10+ motores de análise
│   ├── importacao/               # importar.sh
│   ├── manutencao/               # (vazio)
│   ├── instalacao/               # (vazio)
│   ├── copia_seguranca/          # (vazio)
│   ├── consolidate-v1-lote1.sh   # Automação consolidação
│   ├── consolidate-v1-lote2.sh
│   └── consolidate-v1-lote3.sh
│
├── recursos/
│   ├── documentos/               # (vazio)
│   ├── imagens/                  # (vazio)
│   ├── videos/                   # (vazio)
│   └── audios/                   # (vazio)
│
└── testes/                       # (vazio)
```

**Total de arquivos relevantes:** ~380 entradas. ~65 arquivos Python, ~2 SQL, ~12 arquivos Markdown de dados, ~100+ arquivos Markdown de documentação.

---

## 3. Estado das Fases do Projeto

| Fase | Nome | Status |
|------|------|--------|
| 0 | Identidade | ✅ Completo |
| 1 | Constituição | ✅ Completo |
| 2 | Governança | ✅ Completo |
| 3 | Linguagem | ✅ Completo |
| 4 | Domínio | ✅ Completo |
| 5 | Contratos | ✅ Completo |
| 6 | Catálogos | ✅ Completo |
| 7 | Relacionamentos | ✅ Completo |
| 8 | Padrões | ✅ Completo |
| 9 | Modelagem | ✅ Completo |
| 10 | Dados Canônicos (seeds) | 🟡 Parcial (expansão contínua) |
| 11 | Casos de Uso | ✅ Completo |
| 12 | Validação | ✅ Completo |
| 13 | Implementação | 🔵 Próxima fase |

**Score FAA (última medição — 2026-06-26):** 88.36/100  
**Integridade estrutural:** 90%  
**Saúde:** WARNING (0 críticos, 22 avisos)  
**Decisão:** DEGRADED (meta: APPROVED)

---

## 4. Domínio — Entidades Definidas

O sistema define **8 entidades** com contratos completos:

| Entidade | Prefixo ID | Contrato | Esquema | Template | Seeds |
|----------|-----------|---------|---------|---------|-------|
| Receita | REC | ✅ | ✅ | ✅ | 1 |
| Execução | EXE | ✅ | ✅ | ✅ | 1 |
| Ingrediente | ING | ✅ | ✅ | ✅ | 4 |
| Técnica | TEC | ✅ | ✅ | ✅ | 3 |
| Equipamento | EQP | ✅ | ✅ | ✅ | 2 |
| Observação | OBS | ✅ | ✅ | ✅ | 1 |
| Experimento | EXP | ✅ | ✅ | ✅ | 0 |
| Categoria | CAT | N/A | N/A | N/A | 10 |

**Total de entidades seed atualmente:** 12 (em `dados/`)

### Sequência de IDs atual

| Prefixo | Último ID |
|---------|-----------|
| REC | REC-000001 |
| EXE | EXE-000001 |
| ING | ING-000004 |
| TEC | TEC-000003 |
| EQP | EQP-000002 |
| OBS | OBS-000001 |
| EXP | — (nenhum) |
| CAT | CAT-000010 |

---

## 5. Grafo de Relacionamentos Definidos

13 relacionamentos formalmente documentados em `docs/01-dominio/mapa-relacionamentos-v1.md`:

| ID | Nome | Origem → Destino | Cardinalidade | Obrigatório |
|----|------|-----------------|---------------|-------------|
| REL-001 | utiliza | Receita → Ingrediente | N:N | Sim |
| REL-002 | aplica | Receita → Técnica | N:N | Não |
| REL-003 | requer | Receita → Equipamento | N:N | Não |
| REL-004 | pertence-a | Execução → Receita | N:1 | Sim |
| REL-005 | usa | Execução → Ingrediente | N:N | Não |
| REL-006 | aplica | Execução → Técnica | N:N | Não |
| REL-007 | utiliza | Execução → Equipamento | N:N | Não |
| REL-008 | gera | Execução → Observação | 1:N | Não |
| REL-009 | sobre | Observação → qualquer | N:1 | Não |
| REL-010 | parte-de | Experimento → Receita (base) | N:1 | Não |
| REL-011 | origina | Experimento → Receita (nova) | 1:N | Não |
| REL-012 | gera | Experimento → Observação | 1:N | Não |
| REL-013 | pertence-a | Receita → Categoria | N:N | Não |

---

## 6. Pipeline Computacional (codigo/)

O pipeline de processamento é composto por 5 módulos Python em `codigo/`:

### 6.1 ir-v1.py — Representação Intermediária

Define as estruturas de dados em memória:

- `EdgeKind` (Enum): STRUCTURAL, COMPOSITIONAL, HIERARCHICAL, INFORMATIONAL, DERIVATION, OPTIONAL
- `EdgeOrigin` (Enum): FRONTMATTER, BODY, GENERATED
- `Edge` (dataclass): source, target, kind, origin, location
- `Entity` (dataclass): id, tipo, metadata, body, outgoing, incoming
- `KnowledgeGraph` (dataclass): entities dict, add_entity(), get_entity(), get_edges_by_kind()

**ADR-0002** (aceita) formaliza esse modelo: toda aresta carrega tipo semântico explícito para distinção entre dependências estruturais e referências informativas.

### 6.2 parser-v1.py — Parser Markdown → KnowledgeGraph

- Carrega frontmatter YAML + corpo Markdown de cada arquivo
- Extrai arestas do frontmatter: campos com IDs → EdgeKind.STRUCTURAL (ou COMPOSITIONAL para listas de ingredientes/técnicas/equipamentos, ou DERIVATION para `receita-base-id`)
- Extrai arestas do corpo: IDs em tabelas → COMPOSITIONAL; IDs em texto corrido → INFORMATIONAL
- Função principal: `parse_directory(path)` → `KnowledgeGraph`

### 6.3 resolvedor-v1.py — Resolver de Referências

- Itera sobre todas as arestas outgoing do grafo
- Para cada aresta: se o target existe, adiciona a aresta como `incoming` no target
- Se o target não existe: registra como referência quebrada
- Retorna lista de erros `{source, target, kind, erro}`

### 6.4 validador-v1.py — Validador Semântico

- Detecta ciclos via DFS em arestas STRUCTURAL/COMPOSITIONAL/HIERARCHICAL/DERIVATION → severidade CRITICO
- Detecta ciclos em arestas INFORMATIONAL/OPTIONAL → severidade INFO
- Detecta entidades REC/EXE/EXP sem arestas → severidade AVISO

### 6.5 importador-v1.py — KnowledgeGraph → SQLite

- Recebe KnowledgeGraph já resolvido (nunca lê Markdown diretamente)
- Inicializa o banco com `schema-sqlite-v1.sql`
- Cria tabela extra `relacionamentos` para persistir todas as arestas com `kind`
- Mapeia entidades por tipo para as tabelas correspondentes
- Insere registros com INSERT OR REPLACE

### Estado operacional do pipeline

Ao executar o pipeline com os dados seed atuais:

```
Entidades: 12
Refs quebradas: 0
Issues: 12 (todos auto-ciclos CRITICO)
```

**Problema detectado:** o validador reporta ciclos do tipo `X → X` (self-loops) em todas as entidades. Isso indica que o parser está gerando arestas onde source == target — provavelmente o campo `id` no frontmatter sendo interpretado como referência para si mesmo. É um bug no parser que precisa ser corrigido antes da fase de implementação.

**Problema de naming:** os arquivos usam hífen (`ir-v1.py`, `parser-v1.py`) mas os imports internos usam underscore (`from ir_v1 import ...`). Isso impede execução direta dos scripts (`python3 parser-v1.py`). Os módulos só funcionam se carregados manualmente com `importlib`.

---

## 7. Schema SQLite

O arquivo `banco_de_dados/esquemas/schema-sqlite-v1.sql` define:

### Tabelas Principais (8)

| Tabela | Campos chave | Status check |
|--------|-------------|-------------|
| receitas | id (REC), titulo, status, modo_de_preparo, autor | rascunho/testada/validada/publicada/arquivada |
| ingredientes | id (ING), nome, tipo_ingrediente, unidade_padrao | ativo/descontinuado/arquivado |
| tecnicas | id (TEC), nome, tipo_tecnica, dificuldade | ativo/descontinuado/arquivado |
| equipamentos | id (EQP), nome, tipo_equipamento, material | ativo/descontinuado/arquivado |
| execucoes | id (EXE), receita_id (FK), data_execucao, avaliações | registrada/revisada/consolidada |
| observacoes | id (OBS), conteudo, entidade_id, entidade_tipo | ativo/arquivado/obsoleto |
| experimentos | id (EXP), titulo, hipotese, receita_base_id (FK) | aberto/concluido/incorporado/descartado |
| categorias | id (CAT), nome | ativo |

### Tabelas de Relacionamento N:N (8)

receita_ingrediente, receita_tecnica, receita_equipamento, receita_categoria, execucao_ingrediente, execucao_tecnica, execucao_equipamento, experimento_receita

### Tabela de Histórico

`historico_estados`: rastreia todas as transições de estado de qualquer entidade

### Índices

11 índices para performance em status, autor, receita_id, data, entidade_id

### Views

- `vw_receitas_ativas`: receitas não arquivadas com total de execuções e data da última
- `vw_ingredientes_uso`: ingredientes ativos com contagem de uso em receitas e execuções

**Estado:** schema 100% definido. O banco SQLite físico (`banco_de_dados/sqlite/soe-ccg.db`) não existe ainda — diretório vazio.

---

## 8. Catálogos e Vocabulários Controlados

### Categorias (CAT — seed-categorias.sql)
10 categorias definidas: Doces e Sobremesas, Pães e Panificação, Molhos e Caldas, Conservas, Pratos Principais, Entradas, Bebidas, Massas, Confeitaria, Culinária Mineira.

### Catálogos documentados (docs/01-dominio/catalogos/)

| Catálogo | Arquivo |
|----------|---------|
| Tipos de Ingredientes | tipos-ingredientes-v1.md |
| Categorias | categorias-v1.md |
| Estados de Receita | estados-receita-v1.md |
| Tipos de Equipamentos | tipos-equipamentos-v1.md |
| Unidades de Medida | unidades-medida-v1.md |
| Tipos de Técnicas | tipos-tecnicas-v1.md |
| Estados de todas as entidades | estados-todas-entidades-v1.md |
| Catálogos expandidos | catalogos-expandidos-v1.md |

---

## 9. Documentação (docs/)

### 9.1 docs/00-projeto/
- `visão-v1.md` — Visão do sistema
- `constituicao-v1.md` — 10 Leis Fundamentais (autoridade máxima)
- `filosofia-v1.md` — 5 Axiomas filosóficos
- `principios-v1.md` — Princípios operacionais
- `objetivos-v1.md` — Objetivos do sistema
- `escopo-v1.md` — Escopo definido
- `roadmap-master-v1.md` — Visão de 5 anos
- `glossario-v1.md` — Glossário do projeto

### 9.2 docs/01-dominio/
- Especificações de todas as 8 entidades (`especificacao-*.md`)
- Contratos de todas as 7 entidades principais (`contratos/contrato-*.md`)
- Esquemas YAML de 7 entidades (`esquemas/esquema-*.md`)
- Templates de 7 entidades (`templates/`)
- `entidades-v1.md`, `relacionamentos-v1.md`, `mapa-relacionamentos-v1.md`
- `linguagem-soe-ccg-v1.md` — Vocabulário oficial único
- `ciclo-de-vida-v1.md`, `catalogacao-v1.md`, `separacao-dominios-v1.md`
- `glossario-v1.md` — 60+ termos
- `overview-v1.md`

### 9.3 docs/02-arquitetura/
- `diagrama-mestre-v1.md` — Diagrama ASCII completo do sistema
- `fluxo-dados-v1.md`, `versionamento-v1.md`, `importacao-v1.md`, `exportacao-v1.md`
- `estrutura-diretorios-v1.md`

### 9.4 docs/03-modelagem/
- `entidades-er-v1.md` — Modelo ER com diagrama
- `relacionamentos-v1.md`, `normalizacao-v1.md`, `ids-v1.md`, `sqlite-v1.md`
- `objetivo-v1.md`, `conceitos-fundamentais-v1.md`

### 9.5 docs/04-padroes/
- `nomenclatura-v1.md`, `identificadores-v1.md`, `metadados-v1.md`
- `tags-v1.md`, `validacao-v1.md`, `versionamento-v1.md`
- `politica-conflito-v1.md`, `politica-revisao-v1.md`, `politica-arquivamento-v1.md`
- `politica-esquemas-v1.md`, `politica-templates-v1.md`
- `ADR-0001-MOTOR-DE-CONHECIMENTO-v1.md` — ADR aceita
- `ADR-0002-IR-ARESTAS-TIPADAS-v1.md` — ADR aceita (2026-06-27)

### 9.6 docs/05-desenvolvimento/
- `casos-de-uso-v1.md` — Todos os fluxos UC-001 a UC-N
- `padroes-desenvolvimento-v1.md`

### 9.7 docs/06-operacao/
- `guia-operacao-v1.md`

### 9.8 docs/07-uso/
**Vazio.** Documentação operacional V2 planejada em `PLAN-docs-07-uso-V2.md`. Existe um pacote ZIP com uma estrutura proposta em `docs/docs-07-uso-manual-operacional.zip` já extraída em `docs/docs-07-uso-manual-operacional/docs/07-uso/` (estrutura completa já criada, mas fora do lugar canônico).

### 9.9 docs/99-referencias/
- `guia-tecnico-faa-v2.md`
- `roadmap-consolidacao-v1.md`
- `relatorio-consolidacao-v1-2026-06-26.md`
- `progresso-consolidacao-v1.txt`
- `faa-state.json` (16KB) — estado completo FAA
- `faa-state-summary.json` — sumário JSON
- `FAA-v1-RELATORIO-FINAL.md`, `FAA-v1-CONCLUSAO.md`
- `auditoria-v1-2026-06-26.md`
- `snapshots/` — 5 snapshots históricos (faa-snapshot-*.json)
- `archive/` — documentos v0.5 arquivados (5 arquivos)

---

## 10. FAA v2 — Ferramenta de Governança Arquitetural

O **FAA** (Ferramenta de Auditoria Arquitetural) v2 é um sistema Python de 630 linhas / 23 arquivos localizado em `scripts/faa/`.

### Capacidades
- Scanner com classificação automática de arquivos
- Motor de regras extensível (2 regras ativas)
- Detector de issues com severidade (critical/warning/info)
- Planner que converte problemas em ações ordenadas
- Cálculo de métricas (score, integridade, cobertura)
- Persistência de estado JSON
- Snapshots históricos com timestamp
- CLI com 6 comandos

### Comandos disponíveis
```bash
./scripts/faa.sh status      # Status unificado + score
./scripts/faa.sh validate    # Auditoria completa
./scripts/faa.sh issues      # Lista problemas
./scripts/faa.sh plan        # Roadmap de ações priorizadas
./scripts/faa.sh snapshot    # Criar snapshot histórico
./scripts/faa.sh state --json # JSON para consumo por agentes
```

### Módulos
```
scripts/faa/
  config.py               — configuração central
  core/
    scanner.py            — varredura de arquivos
    rules.py              — motor de regras
    orchestrator.py       — orquestração do pipeline
  engines/
    structure_engine.py   — análise estrutural
  issues/
    detector.py           — detecção de problemas
  metrics/
    coverage.py           — cálculo de cobertura
  planner/
    roadmap_engine.py     — geração de roadmap
    prioritizer.py        — priorização de ações
  state/
    state_store.py        — persistência de estado
  observability/
    report_console.py     — relatório visual
  plugins/
    custom_rules.py       — regras customizáveis
  tests/
    test_basic.py         — testes automatizados
```

### Histórico de evolução do score

| Snapshot | Score | Integridade | Saúde | Críticos |
|---------|-------|-------------|-------|---------|
| 20260626-212435 | ~81.1 | 70% | CRITICAL | 1 |
| 20260626-212613 | ~83.x | ~75% | CRITICAL | 1 |
| 20260626-212633 | ~85.x | ~80% | WARNING | 0 |
| 20260626-212647 | ~87.x | ~88% | WARNING | 0 |
| 20260626-212702 | ~88.x | ~90% | WARNING | 0 |
| 20260626-212714 | 88.36 | 90.0% | WARNING | 0 |

---

## 11. Sistema de Auditoria (scripts/auditoria/)

Sistema predecessor ao FAA, com maior granularidade de motores temáticos. Duas versões coexistem: `v1` e a versão original (sem sufixo).

### Motores disponíveis

| Motor | Arquivo | Propósito |
|-------|---------|-----------|
| baseline | baseline_v1.py | Linha de base de cobertura |
| cobertura | cobertura.py / cobertura_v1.py | Cobertura documental |
| contratos | contratos.py | Validação de contratos |
| dados | dados.py / dados-v2.py | Análise dos dados |
| dependencias | dependencias.py / dependencias-v2.py | Grafo de dependências |
| dominio | dominio.py / dominio_v1.py | Análise do domínio |
| escalabilidade | escalabilidade.py | Avaliação de escalabilidade |
| estrutura | estrutura.py / estrutura_v1.py | Estrutura de diretórios |
| filosofia | filosofia.py / filosofia_v1.py | Aderência filosófica |
| integridade | integridade.py / integridade-v2.py | Integridade dos arquivos |
| maturidade | maturidade.py / maturidade_v1.py | Nível de maturidade |
| padroes | padroes.py | Conformidade de padrões |
| semantica | semantica.py / semantica_v1.py / semantica-v2.py | Análise semântica |
| templates | templates.py | Validação de templates |

---

## 12. Dados Seed — Estado Atual

### Receita

**REC-000001** — Doce de Leite Artesanal  
Status: `testada` | Dificuldade: média | Rendimento: ~300g  
Referencia: ING-000001, ING-000002, ING-000003, ING-000004  
Técnicas: TEC-000001, TEC-000003  
Equipamentos: EQP-000001, EQP-000002  

### Ingredientes

| ID | Nome | Tipo | Status |
|----|------|------|--------|
| ING-000001 | Leite Integral | Laticínio | ativo |
| ING-000002 | Açúcar Refinado | — | ativo |
| ING-000003 | Sal Refinado | — | ativo |
| ING-000004 | Bicarbonato de Sódio | — | ativo |

### Técnicas

| ID | Nome | Tipo | Dificuldade |
|----|------|------|-------------|
| TEC-000001 | Redução | Calor úmido — concentração | média |
| TEC-000002 | Caramelização | — | — |
| TEC-000003 | Agitação Contínua | — | — |

### Equipamentos

| ID | Nome |
|----|------|
| EQP-000001 | Panela de Fundo Grosso |
| EQP-000002 | Colher de Silicone |

### Execução

**EXE-000001** — Doce de Leite Artesanal v1  
Status: `consolidada` | Data: 2026-06-25  
Avaliação geral: bom | Sabor: 7/10 | Textura: 9/10 | Aparência: 6/10

### Observação

**OBS-000001** — Efeito do Bicarbonato  
Referencia: EXE-000001 (contexto) + informativa para REC-000001

---

## 13. Decisões Arquiteturais (ADRs)

### ADR-0001 — Motor de Conhecimento (aceita)
Define que o sistema é centrado em conhecimento, não em documentos. Toda informação passa pelo Motor de Conhecimento. SQLite armazena rede de entidades + relacionamentos, não documentos.

### ADR-0002 — IR com Arestas Tipadas (aceita, 2026-06-27)
Formaliza o modelo de Representação Intermediária. Toda aresta possui `kind` (STRUCTURAL/COMPOSITIONAL/HIERARCHICAL/INFORMATIONAL/DERIVATION/OPTIONAL) e `origin` (FRONTMATTER/BODY/GENERATED).

Resolve o problema DEP-002: o ciclo `REC-000001 → OBS-000001 → EXE-000001 → REC-000001` é composto por uma aresta INFORMATIONAL (corpo do Markdown) + duas STRUCTURAL (frontmatter). Como não há ciclo exclusivamente em arestas STRUCTURAL, o resultado correto é INFO, não FAIL.

---

## 14. Planejamento V2

### PLAN-SOE-CCG-V2.md — Plataforma Semântica

Objetivo: transformar o SOE-CCG de sistema documental em plataforma semântica viva.

Pipeline V2:
```
Markdown → Parser → IR → KnowledgeGraph → SQLite
```

Roadmap de 6 fases:
1. **Plataforma**: migração para pacote Python `soe/`, RuntimeContext, Schema Registry
2. **Formalização**: KnowledgeGraph residente, Query Engine, interfaces públicas
3. **Validação**: Rule Engine declarativo, DSL, migração regras FAA
4. **Inferência**: DerivedEdges, proveniência, explicabilidade
5. **Reatividade**: Event Bus, snapshots imutáveis, atualização incremental
6. **Extensibilidade**: plugins, ontologia, múltiplos domínios

Estrutura proposta `soe/` (pacote Python):
```
soe/
  core/       — graph, parser, resolver, importer, ir
  platform/   — context, lifecycle, config, logging, schema_registry, metrics
  engines/    — query, validation, inference, indexing
  consumers/  — faa, cli, api, gui
  plugins/    — base, domains
```

### PLAN-docs-07-uso-V2.md — Especificação Operacional

Proposta de `docs/07-uso/` como produto oficial normativo com 13 seções (00-políticas a 12-apêndices). Objetivo: fonte única de verdade para operação do sistema, consumível por humanos e agentes de IA.

---

## 15. Documentação Operacional Existente

Em `docs/docs-07-uso-manual-operacional/docs/07-uso/` existe uma estrutura já criada (mas fora do lugar canônico `docs/07-uso/`):

```
01-introducao/     — 4 arquivos (o-que-e-o-soe, primeiros-passos, como-pensar, glossario)
02-operacao/       — 7 arquivos (ciclo-de-vida, criar-entidades, relacionamentos, editar, remover, versionar, boas-praticas)
03-validacao/      — 6 arquivos (pipeline, parser, resolver, validador, faa, importador, resolucao-erros)
04-consultas/      — 4 arquivos (como-consultar, consultas-comuns, navegacao-no-grafo, exemplos)
05-fluxos/         — 7 arquivos (criar-receita, criar-execucao, criar-tecnica, criar-experimento, criar-observacao, atualizar-receita, fluxo-completo)
06-contribuicao/   — 5 arquivos (padroes, regras, adr, checklist, erros-comuns)
07-referencia/     — 5 arquivos (entidades, relacionamentos, estados, comandos, cheat-sheet)
README.md
08-exemplos-reais.md
```

Total: ~38 arquivos de documentação operacional já escritos.

---

## 16. Problemas e Pendências Identificados

### Bloqueadores para fase 13 (Implementação)

| # | Problema | Severidade | Impacto |
|---|---------|-----------|---------|
| P1 | Bug no validador: self-loops (X→X) em todas as entidades | Alto | Pipeline gera 12 falsos positivos CRITICO |
| P2 | Naming inconsistente: arquivos com hífen, imports com underscore | Alto | Scripts não executam diretamente |
| P3 | Banco SQLite não criado (sqlite/ vazio) | Médio | Sem camada de consulta funcional |
| P4 | 22 avisos FAA pendentes | Médio | Score 88.36 vs meta ≥ 95 |

### Pendências de expansão

| # | Pendência | Status |
|---|-----------|--------|
| E1 | Dados seed (fase 10) | Em expansão contínua — 12 entidades hoje |
| E2 | docs/07-uso/ vazio (lugar canônico) | Conteúdo existe fora do lugar |
| E3 | Experimentos: nenhum seed criado | Zero registros EXP |
| E4 | Banco SQLite nunca inicializado | `sqlite/` vazio |
| E5 | scripts/testes/ vazio | Sem testes de integração |
| E6 | Script de reconstrução do BD | `importar.sh` existe mas BD não foi gerado |
| E7 | Cobertura de documentação: 107 docs, 15 dados, 0 schema (FAA) | Schema count = 0 no estado FAA |

### Duplicações e resíduos

| Item | Situação |
|------|---------|
| scripts/auditoria/ | Duas versões coexistem (v0 e v1). Código legado não removido. |
| docs/docs-07-uso-manual-operacional/ | Conteúdo fora do lugar canônico + ZIP ainda presente |
| banco_de_dados/seeds/.gitkeep | Placeholder desnecessário com seed-categorias.sql presente |

---

## 17. Avaliação Geral

### Pontos Fortes

- **Fundação filosófica e documental excepcional.** As 10 Leis Fundamentais, os 5 Axiomas e os contratos de entidades formam uma base sólida e consistente.
- **Separação Markdown/SQLite bem implementada.** O princípio "Markdown é fonte, SQLite é índice" está rigorosamente respeitado em todos os documentos e no código.
- **Arestas tipadas (ADR-0002)** resolvem elegantemente a ambiguidade entre dependência estrutural e referência informativa no grafo.
- **FAA v2 funcional** com métricas objetivas, snapshots históricos e CLI completo.
- **Schema SQLite completo** com constraints, FKs, índices e views úteis.
- **Documentação operacional** (07-uso) já escrita e detalhada, aguardando posicionamento canônico.

### Pontos de Atenção

- **Pipeline não executável diretamente** devido ao naming com hífen vs underscore.
- **Bug de self-loops no validador** obscurece issues reais com 12 falsos positivos.
- **BD SQLite nunca foi instanciado** — a camada de consulta ainda não existe fisicamente.
- **Duplicação no sistema de auditoria** — duas versões paralelas sem consolidação clara.
- **Fase 10 muito inicial** — 12 entidades seed para um sistema de horizonte de 5 anos.

### Estado Geral

O projeto está em estado **pré-implementação avançado**: toda a especificação está completa, o pipeline computacional foi escrito, os contratos e esquemas estão definidos, e a governança arquitetural está operacional. A Fase 13 (Implementação) pode ser iniciada após correção dos dois bloqueadores técnicos (P1 e P2).

---

*Análise gerada automaticamente em 2026-06-28. Baseada na leitura direta de todos os arquivos relevantes do projeto e execução do pipeline de parsing.*
