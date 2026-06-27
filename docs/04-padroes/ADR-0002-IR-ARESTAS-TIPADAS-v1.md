# ADR-0002 — Representação Intermediária com Arestas Tipadas

**Status:** Aceito  
**Data:** 2026-06-27  
**Contexto:** Fase 0B — Congelamento da interface arquitetural do runtime

---

## Contexto

Durante a Fase 0A, o motor de dependências v2 (B-06) revelou um ciclo no grafo de dados:

```
REC-000001 → OBS-000001 → EXE-000001 → REC-000001
```

A origem do ciclo é uma referência informativa no corpo de `REC-000001`:

```markdown
O bicarbonato previne a coagulação das proteínas (ver OBS-000001).
```

O motor não distinguia referências estruturais de referências informativas. Ambas
produziam arestas equivalentes no grafo, tornando impossível separar dependências
reais de navegação de conhecimento.

Esse problema não é um bug de implementação. É uma ambiguidade do modelo.

---

## Decisão

> **No SOE-CCG, uma referência nunca é apenas uma referência. Ela possui um significado semântico explícito.**

A Representação Intermediária (IR) do SOE-CCG adota **arestas tipadas**. Toda relação
entre entidades carrega, além dos identificadores de origem e destino, um tipo semântico
(`kind`) e uma origem estrutural (`origin`).

---

## Modelo da IR

### Entidade

```python
Entity
 ├── id         str
 ├── tipo       str
 ├── metadata   dict
 ├── body       str
 ├── outgoing   list[Edge]
 └── incoming   list[Edge]   # preenchido pelo Resolvedor
```

### Aresta

```python
Edge
 ├── source     str          # ID da entidade de origem
 ├── target     str          # ID da entidade de destino
 ├── kind       EdgeKind     # tipo semântico
 ├── origin     EdgeOrigin   # de onde a referência foi extraída
 └── location   str | None   # linha ou campo de origem, para depuração
```

### Tipos semânticos (EdgeKind)

| Valor | Significado | Ciclo permitido? |
|-------|-------------|-----------------|
| `STRUCTURAL` | Dependência obrigatória para interpretar a entidade | ❌ Proibido |
| `COMPOSITIONAL` | Entidade composta por outra (todo/parte) | ❌ Proibido |
| `HIERARCHICAL` | Relação pai/filho em taxonomias | ❌ Proibido |
| `INFORMATIONAL` | Referência de navegação ou citação | ✅ Permitido |
| `DERIVATION` | Entidade derivada de outra (experimento ← receita) | ❌ Proibido |
| `OPTIONAL` | Relação sugerida, não obrigatória | ✅ Permitido |

### Origem estrutural (EdgeOrigin)

| Valor | Significado |
|-------|-------------|
| `FRONTMATTER` | Campo do bloco YAML do arquivo |
| `BODY` | Texto ou tabela no corpo Markdown |
| `GENERATED` | Produzida pelo resolvedor ou inferência |

---

## Mapeamento padrão

O parser aplica as seguintes regras por padrão:

| Origem | Kind padrão | Justificativa |
|--------|-------------|---------------|
| `FRONTMATTER` | `STRUCTURAL` | Campos de metadados expressam dependência formal |
| `BODY` (tabela de ingredientes/técnicas/equipamentos) | `COMPOSITIONAL` | Composição explícita da entidade |
| `BODY` (texto corrido: "ver X", "consulte X") | `INFORMATIONAL` | Navegação do conhecimento |
| `BODY` (campo `receita-base-id`) | `DERIVATION` | Experimento derivado de receita |

O Resolvedor de Referências pode promover o kind de uma aresta com base em
contexto semântico (ex: link em tabela de ingredientes → `COMPOSITIONAL`).

---

## Consequências para cada componente

**Parser** — produz `Edge` com `kind` e `origin` em vez de lista plana de IDs.

**Resolvedor** — opera sobre arestas, resolve IDs, preenche `incoming`, pode
reclassificar `kind` com base em contexto.

**Validador** — verifica regras de negócio apenas sobre arestas `STRUCTURAL`,
`COMPOSITIONAL` e `DERIVATION`.

**Motor de dependências (FAA)** — detecta ciclos apenas em arestas não-`INFORMATIONAL`
e não-`OPTIONAL`. Ciclos informativos geram `INFO`, não `FAIL`.

**Importador SQLite** — persiste arestas na tabela `relacionamentos` com coluna `kind`.

**Motor de consultas** — filtra por `kind` para navegação vs. dependência.

---

## Classificação do DEP-002 após este ADR

O ciclo `REC-000001 → OBS-000001 → EXE-000001 → REC-000001` é composto por:

- `REC-000001 → OBS-000001`: `INFORMATIONAL` (corpo, texto "ver OBS-000001")
- `OBS-000001 → EXE-000001`: `STRUCTURAL` (frontmatter, campo `execucao-id`)
- `EXE-000001 → REC-000001`: `STRUCTURAL` (frontmatter, campo `receita-id`)

Nenhuma aresta `STRUCTURAL` forma um ciclo fechado. O ciclo existe apenas quando
a aresta informativa é incluída. Resultado correto: `INFO`, não `FAIL`.

---

## Regra canônica

> Ciclos em arestas `STRUCTURAL`, `COMPOSITIONAL`, `HIERARCHICAL` ou `DERIVATION`
> são falhas arquiteturais (`FAIL`).  
> Ciclos que envolvam arestas `INFORMATIONAL` ou `OPTIONAL` são avisos de navegação
> (`INFO`).

---

## Alternativas consideradas

**Lista plana de IDs** — simples de implementar, mas incapaz de distinguir
dependência de navegação. Descartada após DEP-002.

**Tipo inferido pelo campo** — detectar `kind` pelo nome do campo YAML. Frágil
para campos novos e para referências no corpo. Descartado.

**Dois campos separados (structural_refs / informational_refs)** — redundante;
a aresta tipada já carrega essa informação de forma mais expressiva.

---

## Decisão relacionada

ADR-0001 — Motor de Conhecimento (estabelece que SQLite é mecanismo de consulta,
não fonte da verdade).

Este ADR complementa o ADR-0001: define que a IR, e não o Markdown nem o SQLite,
é a representação canônica em memória do conhecimento.
