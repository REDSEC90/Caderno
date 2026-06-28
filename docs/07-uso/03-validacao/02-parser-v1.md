# Parser

> Como o Parser transforma um arquivo Markdown em uma entidade do grafo.

---

## O que o Parser faz

O Parser (`codigo/parser-v1.py`) lê um arquivo `.md` e produz um objeto `Entity` com todas as suas arestas (`Edge`). Múltiplos arquivos geram um `KnowledgeGraph`.

Ele **não valida** se as referências existem — isso é trabalho do Resolver. Ele apenas extrai.

---

## Extração do Frontmatter

O Parser usa `python-frontmatter` para separar o YAML do conteúdo Markdown. Do YAML, ele extrai:

1. O `id` da entidade
2. O `tipo` da entidade
3. Todos os metadados como dicionário
4. **Arestas do frontmatter** — qualquer campo que contenha IDs válidos

### Regras de extração de arestas do frontmatter

| Campo | EdgeKind gerado |
|-------|----------------|
| `receita-base-id` | DERIVATION |
| `ingredientes`, `tecnicas`, `equipamentos`, `ingredientes-usados`, `tecnicas-aplicadas`, `equipamentos-usados` | COMPOSITIONAL |
| Qualquer outro campo com um ID isolado ou lista de IDs | STRUCTURAL |

---

## Extração do Corpo

Do corpo Markdown, o Parser extrai arestas de cada linha que contém IDs válidos:

| Tipo de linha | EdgeKind gerado |
|---------------|----------------|
| Linha de tabela (começa com `\|`) | COMPOSITIONAL |
| Qualquer outra linha com IDs | INFORMATIONAL |

### Por que a distinção tabela vs. texto?

Tabelas no SOE são usadas para listar ingredientes, técnicas e equipamentos de forma estruturada. Um ID em uma tabela representa uma relação de composição, não uma menção contextual.

Um ID no corpo de texto de uma Observação é uma menção contextual — `INFORMATIONAL`.

---

## Padrão de ID Reconhecido

O Parser reconhece IDs que seguem o padrão exato:
```
[A-Z]{2,3}-\d{6}
```

Exemplos válidos: `REC-000001`, `ING-000042`, `TEC-000003`
Inválidos: `rec-000001` (minúsculas), `REC-1` (sem zeros), `RECEITA-000001` (prefixo longo)

---

## Executando o Parser Manualmente

```bash
# Parsear um único arquivo
python3 codigo/parser-v1.py dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Parsear um diretório completo
python3 codigo/parser-v1.py dados/receitas/

# Parsear todos os dados
python3 codigo/parser-v1.py dados/
```
