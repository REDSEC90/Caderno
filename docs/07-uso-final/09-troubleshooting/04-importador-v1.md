# Troubleshooting — Importador

> Diagnóstico de falhas no script de importação (`scripts/importacao/importar.sh`).

**O Importador persiste o grafo resolvido no SQLite.**  
Ele falha quando o banco não existe, quando há conflito de schema, ou quando o pipeline anterior (Parser/Resolver) falhou silenciosamente.

---

## Como executar a importação

```bash
# Arquivo individual
scripts/importacao/importar.sh dados/ingredientes/ING-000005-slug-v1.md

# Todos os dados (reconstrução completa)
scripts/importacao/importar-todos.sh
```

```
# Resultado esperado:
[OK] ING-000005 importado com sucesso
```

---

## Problema 1: `No such file or directory: soe-ccg.db`

**Sintoma:**
```
sqlite3.OperationalError: unable to open database file
```

**Causa:** O banco SQLite não existe ainda.

**Solução:**
```bash
mkdir -p banco_de_dados/sqlite

sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

echo "Tabelas criadas:"
sqlite3 banco_de_dados/sqlite/soe-ccg.db ".tables"
```

```
# Resultado esperado:
equipamentos     execucoes        experimentos     ingredientes
observacoes      receita_equipamento  receita_ingrediente  receita_tecnica
receitas         relacionamentos  tecnicas
```

---

## Problema 2: `no such table: ingredientes`

**Sintoma:**
```
sqlite3.OperationalError: no such table: ingredientes
```

**Causa:** O banco existe mas o schema não foi aplicado (banco vazio ou schema desatualizado).

**Solução:**
```bash
# Verificar se as tabelas existem
sqlite3 banco_de_dados/sqlite/soe-ccg.db ".tables"

# Se vazio, aplicar schema
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql
```

Se as tabelas existirem mas com schema antigo, reconstruir do zero:
```bash
rm banco_de_dados/sqlite/soe-ccg.db
sqlite3 banco_de_dados/sqlite/soe-ccg.db < banco_de_dados/esquemas/schema-sqlite-v1.sql
scripts/importacao/importar-todos.sh
```

---

## Problema 3: Arquivo importado sem erro mas não aparece no banco

**Sintoma:** O script termina sem erro mas `SELECT ... WHERE id = 'ING-000005'` retorna vazio.

**Diagnóstico:**
```bash
# 1. O arquivo existe?
ls dados/ingredientes/ING-000005-*.md

# 2. O Parser consegue ler?
python3 codigo/parser-v1.py dados/ingredientes/ING-000005-slug-v1.md

# 3. Há erro silencioso no importador?
python3 codigo/importador-v1.py dados/ingredientes/ING-000005-slug-v1.md 2>&1

# 4. Verificar o banco diretamente
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes ORDER BY id DESC LIMIT 5;"
```

**Causas comuns:**
- O arquivo tem frontmatter inválido que o Parser ignorou silenciosamente → ver [`01-parser-v1.md`](01-parser-v1.md)
- O campo `id` no frontmatter não bate com o prefixo esperado → o importador pode ter descartado
- Permissão de escrita no banco → verificar `ls -la banco_de_dados/sqlite/`

---

## Problema 4: `UNIQUE constraint failed`

**Sintoma:**
```
sqlite3.IntegrityError: UNIQUE constraint failed: ingredientes.id
```

**Causa:** Tentativa de inserir um ID que já existe. Normalmente o importador faz UPDATE (não INSERT), então esse erro indica algo inesperado no script.

**Diagnóstico:**
```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT * FROM ingredientes WHERE id = 'ING-000005';"
```

**Solução:** Se o ID já existe e você quer atualizar, editar o arquivo `.md` e reimportar — o importador deve fazer UPDATE automaticamente. Se o problema persistir, verificar a versão do script de importação.

---

## Problema 5: `importar-todos.sh` — ordem errada de importação

**Sintoma:** Erros de `referencia_quebrada` ao importar todos os dados de uma vez.

**Causa:** O script `importar-todos.sh` pode estar importando Receitas antes dos Ingredientes que elas referenciam.

**Solução:** A ordem correta de importação é:
```bash
# Importar na ordem das dependências
scripts/importacao/importar.sh dados/equipamentos/
scripts/importacao/importar.sh dados/tecnicas/
scripts/importacao/importar.sh dados/ingredientes/
scripts/importacao/importar.sh dados/receitas/
scripts/importacao/importar.sh dados/execucoes/
scripts/importacao/importar.sh dados/observacoes/
scripts/importacao/importar.sh dados/experimentos/
```

Verificar se o `importar-todos.sh` respeita esta ordem. Se não respeitar, executar manualmente na sequência acima.

---

## Reconstrução completa do banco (sem perda de dados)

Quando tudo mais falhar:

```bash
# Passo 1 — destruir o banco atual
rm banco_de_dados/sqlite/soe-ccg.db

# Passo 2 — recriar schema
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

# Passo 3 — reimportar tudo na ordem correta
for dir in equipamentos tecnicas ingredientes receitas execucoes observacoes experimentos; do
  echo "=== Importando $dir ==="
  scripts/importacao/importar.sh dados/$dir/
done

# Passo 4 — verificar resultado
sqlite3 banco_de_dados/sqlite/soe-ccg.db "
  SELECT 'receitas' as t, COUNT(*) FROM receitas UNION ALL
  SELECT 'ingredientes', COUNT(*) FROM ingredientes UNION ALL
  SELECT 'tecnicas', COUNT(*) FROM tecnicas UNION ALL
  SELECT 'equipamentos', COUNT(*) FROM equipamentos;
"

# Passo 5 — rodar FAA
python3 scripts/auditoria/auditor-v1.py
```

Nenhuma informação é perdida — o banco é sempre reconstruível a partir dos arquivos Markdown.

---

## Próxima leitura

- Banco dessincronizado → [`05-sqlite-v1.md`](05-sqlite-v1.md)
- Guia completo do Importador → [`../03-validacao/06-importador-v1.md`](../03-validacao/06-importador-v1.md)
