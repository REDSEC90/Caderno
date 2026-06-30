# Troubleshooting — Parser

> Diagnóstico de falhas no componente Parser (`codigo/parser-v1.py`).

**O Parser lê arquivos Markdown e constrói o KnowledgeGraph.**  
Ele falha quando o arquivo tem problema de formato, frontmatter ausente/inválido, ou ID malformado.

---

## Como executar o Parser isoladamente

```bash
# Um arquivo específico
python3 codigo/parser-v1.py dados/ingredientes/ING-000005-meu-ingrediente-v1.md

# Um diretório
python3 codigo/parser-v1.py dados/ingredientes/

# Todos os dados
python3 codigo/parser-v1.py dados/
```

```
# Resultado esperado (sem erros):
[PARSER] ING-000005 processado — 0 arestas
```

---

## Problema 1: `frontmatter ausente` ou `No frontmatter found`

**Sintoma:**
```
ParserError: frontmatter ausente em dados/ingredientes/ING-000005-meu-ingrediente-v1.md
```

**Causa:** O arquivo não tem os delimitadores `---` no início.

**Diagnóstico:**
```bash
head -3 dados/ingredientes/ING-000005-meu-ingrediente-v1.md
```
Se a primeira linha não for `---`, o frontmatter está ausente.

**Solução:** Adicionar o frontmatter no início do arquivo:
```markdown
---
id: ING-000005
tipo: ingrediente
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: seu-nome
tags: []
---

# Nome do Ingrediente
```

**Como evitar:** Sempre copiar de um template em vez de criar do zero.
```bash
cp docs/01-dominio/templates/ingrediente-v1.md dados/ingredientes/ING-000005-slug-v1.md
```

---

## Problema 2: `KeyError: 'id'` ou `id ausente no frontmatter`

**Sintoma:**
```
KeyError: 'id'
```

**Causa:** O campo `id` não existe no frontmatter YAML.

**Diagnóstico:**
```bash
grep "^id:" dados/ingredientes/ING-000005-meu-ingrediente-v1.md
```
Se não retornar nada, o campo está ausente.

**Solução:** Adicionar o campo `id` ao frontmatter:
```yaml
---
id: ING-000005   # ← adicionar esta linha
tipo: ingrediente
...
---
```

**Como evitar:** Usar sempre o template — ele já inclui todos os campos obrigatórios.

---

## Problema 3: `ID inválido: ing-000005` (minúsculas)

**Sintoma:**
```
ValidationError: ID inválido: ing-000005 — prefixo deve ser maiúsculo
```

**Causa:** O prefixo do ID está em minúsculas.

**Diagnóstico:**
```bash
grep "^id:" dados/ingredientes/ING-000005-meu-ingrediente-v1.md
```

**Solução:**
```yaml
# Errado
id: ing-000005

# Correto
id: ING-000005
```

O padrão aceito é `[A-Z]{2,3}-\d{6}`. Exemplos: `REC-000001`, `ING-000042`, `TEC-000003`.

---

## Problema 4: `ID inválido: REC-1` (sem zeros à esquerda)

**Sintoma:**
```
ValidationError: ID inválido: REC-1
```

**Causa:** O número não tem 6 dígitos com zeros à esquerda.

**Solução:**
```yaml
# Errado
id: REC-1

# Correto
id: REC-000001
```

---

## Problema 5: Aresta não detectada (ID não está sendo reconhecido)

**Sintoma:** Você colocou `ING-000001` no frontmatter mas o Parser não gera a aresta.

**Diagnóstico:**
```bash
# Ver as arestas que o Parser gerou
python3 codigo/parser-v1.py dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md --verbose
```

**Causas comuns:**

1. **ID em campo de texto livre** — o Parser reconhece IDs em campos de lista ou nos campos específicos. Um ID solto em `descricao:` pode não ser extraído como aresta.

2. **Campo de frontmatter não reconhecido** — campos como `ingredientes-principais:` (nome customizado) não são reconhecidos. Use os nomes canônicos: `ingredientes`, `tecnicas`, `equipamentos`.

3. **ID com erro tipográfico** — `ING-00001` (5 zeros) não é reconhecido. Deve ter 6 dígitos.

**Campos de frontmatter reconhecidos para arestas:**

| Campo | Tipo de aresta gerado |
|-------|----------------------|
| `ingredientes`, `tecnicas`, `equipamentos` | COMPOSITIONAL |
| `ingredientes-usados`, `tecnicas-aplicadas`, `equipamentos-usados` | COMPOSITIONAL |
| `receita-id` | STRUCTURAL |
| `receita-base-id` | DERIVATION |
| Qualquer outro campo com ID | STRUCTURAL |

---

## Problema 6: `No module named 'frontmatter'`

**Sintoma:**
```
ModuleNotFoundError: No module named 'frontmatter'
```

**Solução:**
```bash
pip install python-frontmatter
# ou, se der conflito de sistema:
pip install python-frontmatter --break-system-packages
```

---

## Próxima leitura

- Se o Parser passou mas ainda há erros → [`02-resolver-v1.md`](02-resolver-v1.md)
- Catálogo completo de erros → [`../03-validacao/07-resolucao-de-erros-v1.md`](../03-validacao/07-resolucao-de-erros-v1.md)
