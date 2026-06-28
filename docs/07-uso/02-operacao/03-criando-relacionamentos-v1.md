# Criando Relacionamentos

> Provavelmente o documento mais importante da seção de operação. Leia com atenção.

---

## O que é um Relacionamento

Um relacionamento é uma aresta direcional no grafo de conhecimento. Ele conecta uma entidade de origem a uma entidade de destino e carrega um significado semântico específico — não é apenas um link.

```
REC-000001  ──[COMPOSITIONAL]──→  ING-000001
    │
    └──[COMPOSITIONAL]──→  TEC-000001
    │
    └──[DERIVATION]──→  EXP-000001 (se existir)
```

---

## Os Seis Tipos de Aresta (EdgeKind)

### STRUCTURAL
**Significado:** Referência estrutural — a entidade de destino é necessária para que a de origem faça sentido.

**Origem:** Qualquer campo de frontmatter que contenha um ID isolado (não em listas composicionais).

**Exemplo:**
```yaml
# EXE frontmatter
receita-id: REC-000001   ← aresta STRUCTURAL: EXE → REC
```

**Pode gerar ciclo?** Sim — ciclos STRUCTURAL são sempre problemáticos.

---

### COMPOSITIONAL
**Significado:** Composição — a entidade de origem é composta em parte pelas entidades de destino.

**Origem:** Campos de frontmatter que são listas de IDs (`ingredientes`, `tecnicas`, `equipamentos`, `ingredientes-usados`, `tecnicas-aplicadas`) **e** IDs que aparecem em linhas de tabela Markdown (linhas que começam com `|`).

**Exemplo:**
```yaml
# REC frontmatter
ingredientes: [ING-000001, ING-000002, ING-000003, ING-000004]
```
```markdown
# REC body — tabela de ingredientes
| ING-000001 | Leite Integral | 1000 | ml |   ← aresta COMPOSITIONAL
```

**Pode gerar ciclo?** Raramente. Uma Receita não pode ser composta de si mesma.

---

### DERIVATION
**Significado:** Derivação — a entidade de origem foi criada a partir da entidade de destino.

**Origem:** Campo `receita-base-id` no frontmatter de Experimentos.

**Exemplo:**
```yaml
# EXP frontmatter
receita-base-id: REC-000001   ← aresta DERIVATION: EXP → REC
```

**Pode gerar ciclo?** Não em uso normal.

---

### INFORMATIONAL
**Significado:** Menção contextual — a entidade de destino é mencionada no corpo do documento como contexto, mas não como dependência estrutural.

**Origem:** IDs encontrados no corpo do documento em linhas que **não** são linhas de tabela.

**Exemplo:**
```markdown
# OBS body
O bicarbonato (ING-000004) cumpre duas funções: ...    ← aresta INFORMATIONAL
Ver também a execução EXE-000001 onde isso foi observado.   ← aresta INFORMATIONAL
```

**Pode gerar ciclo?** Sim — e esses ciclos são **semanticamente válidos**. Uma OBS menciona EXE que pertence a REC que é mencionada pela OBS é um ciclo informacional legítimo.

---

### HIERARCHICAL
**Significado:** Hierarquia — relação pai/filho entre entidades do mesmo tipo.

**Origem:** Campos de frontmatter que expressam hierarquia (como categoria pai/filho).

**Pode gerar ciclo?** Não — hierarquias nunca devem ter ciclos.

---

### OPTIONAL
**Significado:** Referência opcional — o destino pode ou não existir, e a ausência não é um erro.

**Pode gerar ciclo?** Raramente relevante.

---

## Como os Relacionamentos São Criados

### Via Frontmatter (arestas STRUCTURAL, COMPOSITIONAL, DERIVATION)

Você cria arestas estruturais simplesmente preenchendo os campos de frontmatter com IDs:

```yaml
---
# Em uma Receita
ingredientes: [ING-000001, ING-000002]    ← 2 arestas COMPOSITIONAL
tecnicas: [TEC-000001]                    ← 1 aresta COMPOSITIONAL
equipamentos: [EQP-000001]               ← 1 aresta COMPOSITIONAL
---
```

```yaml
---
# Em uma Execução
receita-id: REC-000001                   ← 1 aresta STRUCTURAL
---
```

```yaml
---
# Em um Experimento
receita-base-id: REC-000001              ← 1 aresta DERIVATION
---
```

### Via Corpo do Documento (arestas INFORMATIONAL)

Qualquer menção de um ID válido no corpo do texto cria uma aresta INFORMATIONAL automaticamente:

```markdown
## Observações

O efeito foi observado na execução EXE-000001. O ingrediente ING-000004
(bicarbonato de sódio) tem papel químico direto neste processo.
```

Isso cria automaticamente duas arestas INFORMATIONAL: `OBS-000001 → EXE-000001` e `OBS-000001 → ING-000004`.

---

## Regras Críticas

**1. Referencie por ID, nunca por nome.**
```yaml
# ✅ Correto
ingredientes: [ING-000001, ING-000002]

# ✗ Errado — nome pode mudar, ID não
ingredientes: [Leite Integral, Açúcar Refinado]
```

**2. O destino deve existir antes de ser referenciado.**
O Resolver verificará. Se `ING-000099` não existe, a importação falhará com `referencia_quebrada`.

**3. Ciclos STRUCTURAL são sempre erros.**
Se a auditoria reportar `[DEP-002] Ciclo detectado` em arestas STRUCTURAL, revise os relacionamentos. Ciclos INFORMATIONAL podem ser aceitos.

**4. Não crie relacionamentos "por hábito".**
Uma OBS sobre o comportamento do bicarbonato deve referenciar `ING-000004` porque é relevante para o conhecimento, não porque "todo documento deve ter relações".

---

## Verificando Relacionamentos

```bash
# Ver todas as arestas de uma entidade
python3 scripts/auditoria/auditor-v1.py entity REC-000001

# Verificar ciclos no grafo
python3 scripts/auditoria/auditor-v1.py --motor dependencias

# Ver todas as arestas no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, target, kind, origin FROM relacionamentos ORDER BY source;"
```
