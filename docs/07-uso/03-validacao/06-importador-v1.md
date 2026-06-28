# Importador

> Como o Importador persiste o KnowledgeGraph no banco SQLite.

---

## O que o Importador faz

O Importador (`codigo/importador-v1.py`) recebe um `KnowledgeGraph` já parseado e resolvido, e persiste os dados no banco SQLite.

**Ele nunca lê Markdown diretamente.** Sempre opera sobre o grafo em memória.

---

## O que é persistido

Para cada entidade no grafo:
- Dados tabulares na tabela correspondente (`receitas`, `ingredientes`, etc.)
- Arestas na tabela `relacionamentos`

Para cada aresta:
- `source` — ID da entidade de origem
- `target` — ID da entidade de destino
- `kind` — tipo de aresta (STRUCTURAL, COMPOSITIONAL, etc.)
- `origin` — de onde veio (FRONTMATTER, BODY, GENERATED)
- `location` — campo ou contexto de origem

---

## Executando

```bash
# Via script shell (recomendado para uso diário)
scripts/importacao/importar.sh dados/ingredientes/ING-000005-farinha-de-trigo-v1.md

# Reimportar todos (reconstrução completa do banco)
scripts/importacao/importar-todos.sh
```

---

## Reconstruindo o Banco do Zero

Se o banco for corrompido ou perdido:

```bash
# 1. Remover banco corrompido
rm banco_de_dados/sqlite/soe-ccg.db

# 2. Criar esquema
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

# 3. Carregar seeds (categorias etc.)
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/seeds/seed-categorias.sql

# 4. Reimportar todos os dados
scripts/importacao/importar-todos.sh
```

Nenhuma informação é perdida — tudo vem dos arquivos Markdown.

---

## Resolução de Conflitos

Se o Importador encontrar um ID que já existe no banco:
- A linha é sobrescrita (UPDATE)
- O histórico no banco não é preservado — o git preserva

Por isso o comportamento correto para corrigir um dado é: editar o `.md` → reimportar. O banco sempre reflete o estado atual dos arquivos Markdown.
