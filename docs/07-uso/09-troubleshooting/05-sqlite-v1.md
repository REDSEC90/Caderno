# Troubleshooting — SQLite

> Diagnóstico de problemas com o banco de dados SQLite.

**O SQLite é um índice derivado — nunca a fonte de verdade.**  
Se algo está errado no banco, a correção sempre acontece nos arquivos Markdown, nunca no banco diretamente.

---

## Verificações rápidas

```bash
# O banco existe?
ls banco_de_dados/sqlite/

# O banco tem as tabelas esperadas?
sqlite3 banco_de_dados/sqlite/soe-ccg.db ".tables"

# Quantas entidades há em cada tabela?
sqlite3 banco_de_dados/sqlite/soe-ccg.db "
  SELECT 'receitas' as tabela, COUNT(*) FROM receitas UNION ALL
  SELECT 'ingredientes', COUNT(*) FROM ingredientes UNION ALL
  SELECT 'tecnicas', COUNT(*) FROM tecnicas UNION ALL
  SELECT 'equipamentos', COUNT(*) FROM equipamentos UNION ALL
  SELECT 'execucoes', COUNT(*) FROM execucoes;
"
```

---

## Problema 1: Banco não existe ou está vazio

**Sintoma:**
```
sqlite3: banco_de_dados/sqlite/soe-ccg.db: unable to open database
```
ou banco existe mas `.tables` retorna nada.

**Solução — Criar o banco do zero:**
```bash
mkdir -p banco_de_dados/sqlite

sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

echo "Tabelas criadas:"
sqlite3 banco_de_dados/sqlite/soe-ccg.db ".tables"
```

**Solução — Popular com os dados existentes:**
```bash
python3 -m codigo
# ou
scripts/importacao/importar-todos.sh
```

```
# Resultado esperado:
[IMPORTADOR] 13 entidades importadas
```

---

## Problema 2: Entidade importada mas não aparece no banco

**Sintoma:** O importador rodou sem erros, mas `SELECT * FROM ingredientes WHERE id = 'ING-000005'` retorna vazio.

**Diagnóstico:**
```bash
# Verificar se o arquivo existe
ls dados/ingredientes/ING-000005-*.md

# Verificar se o Parser consegue ler o arquivo
python3 codigo/parser-v1.py dados/ingredientes/ING-000005-slug-v1.md

# Importar novamente e observar a saída
scripts/importacao/importar.sh dados/ingredientes/ING-000005-slug-v1.md
```

**Causas comuns:**

1. O arquivo tem erro de frontmatter que silenciou o import → ver [`01-parser-v1.md`](01-parser-v1.md)
2. O ID no frontmatter não bate com o nome do arquivo → o importador pode ter usado o ID errado
3. O banco foi recriado após o import → re-importar

---

## Problema 3: Banco dessincronizado dos arquivos Markdown

**Sintoma:** Você editou um arquivo Markdown mas o banco ainda mostra os valores antigos.

**Causa:** Edições nos arquivos Markdown não se propagam automaticamente para o banco. É preciso re-importar.

**Solução:**
```bash
# Re-importar o arquivo editado
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Verificar
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, atualizado_em FROM receitas WHERE id = 'REC-000001';"
```

---

## Problema 4: Banco corrompido ou inconsistente

**Sintoma:** Queries retornam erros, tabelas com dados incorretos, ou o banco não abre.

**Solução — Reconstruir do zero (nenhuma informação é perdida):**
```bash
# Remover o banco atual
rm banco_de_dados/sqlite/soe-ccg.db

# Recriar o schema
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

# Reimportar todos os dados
scripts/importacao/importar-todos.sh
```

O banco é totalmente reconstituível a partir dos arquivos Markdown em `dados/`. Destruir o banco não destrói nenhum dado.

---

## Problema 5: Tentando editar o banco diretamente

**Situação:** Você tem vontade de fazer `UPDATE ingredientes SET nome = 'Leite UHT' WHERE id = 'ING-000001'` diretamente no SQLite.

**NÃO FAÇA ISSO.**

O banco é derivado. Na próxima importação, todos os dados são sobrescritos a partir dos arquivos Markdown. Qualquer edição direta no banco será perdida.

**Solução correta:**
```bash
# Editar o arquivo Markdown
nano dados/ingredientes/ING-000001-leite-integral-v1.md
# Alterar o conteúdo desejado
# Atualizar atualizado-em: 2026-06-28

# Re-importar
scripts/importacao/importar.sh dados/ingredientes/ING-000001-leite-integral-v1.md

# Verificar
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE id = 'ING-000001';"
```

---

## Próxima leitura

- Para verificar integridade do grafo → execute `python3 scripts/auditoria/auditor-v1.py --motor dependencias`
- Consultas úteis no banco → [`../04-consultas/02-consultas-comuns-v1.md`](../04-consultas/02-consultas-comuns-v1.md)
