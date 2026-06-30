# SOE-CCG — Architecture Review Oficial (Parte 2 de 3)

> Continuação direta de `01-MAPA-E-AUDITORIA.md`. Esta parte cobre o entregável 4: Kernel Specification completa.

---

# 4. Kernel Specification

## 4.1 Princípio fundador

O kernel divide-se em duas metades com regras de dependência diferentes:

```
kernel/specification/   →   só descreve leis (idealmente Markdown puro, sem Python executável)
kernel/runtime/          →   implementa essas leis em Python
kernel/shared/            →   tipos/utilidades usados por ambos os lados
```

`kernel/runtime/` pode importar de `kernel/specification/` (lendo regras como dados). `kernel/specification/` nunca importa de `kernel/runtime/` — a lei não depende do mecanismo que a executa. Esta é a regra mais importante de toda a especificação e está repetida em `kernel/DEPENDENCY_RULES.md` para ser impossível de não ver.

## 4.2 `kernel/specification/identity/`

**Responsabilidade:** definir, sem ambiguidade, a forma de todo identificador no sistema — não apenas IDs de entidade.

| Conceito | Exemplo real do domínio | Arquivo |
|---|---|---|
| ID | `REC-000001` | `ids.md` |
| Nome | `receita-doce-leite` | `names.md` |
| Tag | `#receita` | `tags.md` |
| Referência | `REC-000001#ingrediente` | `references.md` |
| URI | (a definir — hoje inexistente no sistema) | `uris.md` |
| Alias | (a definir) | `aliases.md` |

**Por que isto é maior do que a V3 tratou:** a V3 tinha `kernel/identity/id_scheme.py` como um único módulo. Na prática, o domínio já usa pelo menos 4 formas distintas de identificador (ID, nome, tag, referência composta) que hoje não têm grammar formal nenhuma — são convenção observada em `codigo/ir.py` e usada sem documentação central. Separar por tipo evita que o módulo de identidade vire um arquivo único de 500 linhas tentando cobrir 4 conceitos diferentes.

**Dependências permitidas:** nenhuma. Este é o nível mais fundamental do kernel.

## 4.3 `kernel/specification/contracts/`

**Responsabilidade:** o que cada peça do sistema promete entregar ou aceitar.

```
contracts/
├── entities/        # As 7 entidades de domínio — já existem como docs/01-dominio/contratos/*
├── runtime/          # NOVO — o que o runtime deve garantir ao processar uma entidade
├── plugins/          # NOVO — formaliza scripts/faa/plugins/custom_rules.py, hoje sem contrato escrito
├── storage/          # NOVO — o que o SQLite deve refletir do Markdown (a derivação)
├── api/               # NOVO
└── interfaces/        # NOVO — contrato de CLI/agentes (parcialmente coberto por docs/07-uso/08-agentes hoje)
```

**Objetos centrais por subpasta:**

- `entities/`: 7 contratos, um por entidade (Receita, Ingrediente, Técnica, Equipamento, Execução, Observação, Experimento). Cada um especifica campos obrigatórios, campos opcionais, e o esquema de frontmatter que o `runtime/parser/` deve aceitar.
- `runtime/`: contrato do pipeline (o que `parser → resolver → validator → executor → importer` deve garantir entre etapas). Hoje essa ordem existe apenas implicitamente no código de `codigo/__main__.py`; vira contrato formal aqui.
- `plugins/`: contrato de extensão. Hoje `scripts/faa/plugins/custom_rules.py` (60 linhas) existe sem nenhuma documentação do que um plugin pode/deve fazer — este contrato fecha essa lacuna.
- `storage/`: a contraparte formal da política "Markdown é fonte, SQLite é índice" — aqui fica especificado exatamente quais campos do Markdown viram quais colunas do SQLite, servindo de fonte para `schema/definitions/`.

**Dependências permitidas:** `contracts/` pode referenciar `identity/` (um contrato de entidade usa a grammar de ID definida lá). Nunca o contrário.

## 4.4 `kernel/specification/schemas/`

Sucessor direto de `docs/01-dominio/esquemas/*` (7 arquivos hoje). Cada esquema é a forma estrutural de uma entidade — distinto do contrato (que é a *promessa* de comportamento) e do template (que é o *ponto de partida* para um autor humano, hoje em `docs/01-dominio/templates/`).

A distinção esquema/contrato/template, hoje borrada em `docs/01-dominio/` (todos misturados no mesmo nível de pasta), passa a ser explícita: esquema é estrutura, contrato é comportamento, template é ergonomia de autoria.

## 4.5 `kernel/specification/states/`

Sucessor de `docs/01-dominio/catalogos/estados-receita-v1.md` e `estados-todas-entidades-v1.md`.

**Objetos centrais:**
- Uma máquina de estados por entidade (`receita_states.md` e os demais).
- Um arquivo agregador (`entity_states.md`) com a visão consolidada, igual ao que já existe hoje, mas promovido de "catálogo de domínio" para "lei de kernel" — porque estado de entidade não é conhecimento de domínio, é regra estrutural do sistema.

## 4.6 `kernel/specification/policies/`

| Política | O que resolve | Status hoje |
|---|---|---|
| `source_of_truth.md` | "Markdown é fonte, SQLite é índice" | Existe como prosa em `docs/00-projeto/filosofia-v1.md`; aqui vira regra verificável |
| `derivation.md` | Quando e como derivar SQLite a partir de Markdown | Inexistente formalmente — hoje implícito em `codigo/importador.py` |
| `naming.md` | Convenção de sufixo de versão de arquivo | **Inexistente** — e é exatamente a ausência desta política que permitiu a auditoria encontrar `_v1`, `-v1` e `-v2` coexistindo sem padrão em `scripts/auditoria/motores/` |

`naming.md` é o item de maior prioridade desta subpasta — não é teórico, é a causa raiz documentada de boa parte da Seção 2 desta auditoria.

## 4.7 `kernel/specification/invariants/`

Os 8 invariantes já formalizados no protocolo de agentes (`docs/07-uso/08-agentes/`) sobem de nível: deixam de ser "regra de uso para agentes" e passam a ser "lei do kernel que qualquer consumidor — agente, humano, ou módulo interno — deve respeitar". A diferença não é cosmética: hoje, se um módulo Python violar um desses invariantes, não há checagem automática; com `kernel/runtime/policy_engine.py` consultando este arquivo, a violação pode ser detectada em tempo de execução.

## 4.8 `kernel/specification/edges/`

A área mais sensível tecnicamente, porque é onde a auditoria encontrou um problema real de design (o import circular em `motores/__init__.py`) que serve de lição direta: regras de grafo precisam de guarda explícita contra autorreferência.

```
edges/
├── types.md         # DocumentEdge (estrutural/frontmatter) / ResolvedEdge (estado de processo,
│                     #   não aresta permanente) / DerivedEdge (inferida)
├── rules.md
├── inference.md
└── cycles.md         # Regra: DerivedEdge nunca pode usar outro DerivedEdge como input de inferência
```

`cycles.md` formaliza como lei o que `kernel/runtime/edge_engine/cycle_guard.py` implementa como código — exatamente o padrão specification/runtime que organiza todo o kernel.

## 4.9 `kernel/specification/versioning/`

Formaliza o uso real de sufixo de versão — `version_scheme.md` define o vocabulário (major/minor/draft) que deveria ter existido antes de `scripts/auditoria/motores/` acumular 3 convenções de sufixo diferentes (`_v1`, `-v1`, `-v2`) no mesmo diretório.

---

## 4.10 `kernel/runtime/` — a metade executável

Cada arquivo aqui implementa uma área de `specification/` correspondente. Tabela de rastreabilidade direta:

| Arquivo em `kernel/runtime/` | Implementa | Substitui no sistema atual |
|---|---|---|
| `id_generator.py` | `specification/identity/ids.md` | Geração de ID hoje informal em `codigo/ir.py` |
| `schema_registry.py` | `specification/schemas/*` | Lacuna identificada na análise V2 anterior — SchemaRegistry estava ausente |
| `transition_engine.py` | `specification/states/*` | Validação de estado hoje espalhada em `codigo/validador.py` |
| `edge_engine.py` + `cycle_guard.py` | `specification/edges/*` | Modelo de 3 categorias de aresta acordado no ciclo V2 |
| `policy_engine.py` | `specification/policies/*` | Inexistente hoje — política era só prosa, sem verificação |

## 4.11 `kernel/shared/paths.py`

Um único arquivo, mas a correção de maior impacto prático imediato de toda a especificação. Substitui os 4 cálculos de `ROOT` confirmados pela auditoria:

```
codigo/__main__.py          → ROOT = Path(__file__).parent.parent
codigo/importador.py        → ROOT = Path(__file__).parent.parent  (recalculado independentemente)
scripts/faa/config.py       → ROOT = Path(__file__).parent.parent.parent
scripts/auditoria/config.py → ROOT = Path(__file__).parent.parent.parent.resolve()
```

Quatro arquivos, quatro cálculos do mesmo valor lógico, três profundidades de `.parent` diferentes. Qualquer movimentação de arquivo nesta migração (Seção 5/6) quebra pelo menos um desses cálculos silenciosamente se `kernel/shared/paths.py` não for o primeiro passo executado.

## 4.12 APIs internas do kernel

O kernel expõe exatamente 5 pontos de entrada para o resto do sistema, documentados em `kernel/PUBLIC_API.md`:

```python
kernel.runtime.id_generator.generate(entity_type: str) -> str
kernel.runtime.schema_registry.get(entity_type: str) -> Schema
kernel.runtime.transition_engine.validate(entity_type: str, from_state: str, to_state: str) -> bool
kernel.runtime.edge_engine.resolve(edge: DocumentEdge) -> ResolvedEdge
kernel.runtime.policy_engine.check(action: str, context: dict) -> PolicyResult
```

Nada além disso é importável de fora do kernel. Esta restrição é o que `kernel/PUBLIC_API.md` existe para registrar e o que `kernel/DEPENDENCY_RULES.md` existe para impor.

## 4.13 Dependências permitidas — tabela final do kernel

| De | Pode importar | Não pode importar |
|---|---|---|
| `kernel/specification/` | nada (exceto outras partes de `specification/`) | `kernel/runtime/`, qualquer coisa fora do kernel |
| `kernel/runtime/` | `kernel/specification/`, `kernel/shared/` | `runtime/`, `domain/`, `infrastructure/`, `interfaces/` |
| `kernel/shared/` | nada | tudo o resto |
| Resto do sistema | os 5 pontos de `kernel/PUBLIC_API.md` | implementação interna do kernel diretamente |

---
*(Continua na Parte 3: Plano de Migração, Mapa de Movimentação de Arquivos, Arquivos Novos, Arquivos a Remover, Mapa de Dependências, Roadmap V3→V4→V5.)*
