#!/bin/bash
# SOE-CCG — Importador de Markdown para SQLite
# Uso: ./importar.sh dados/receitas/REC-000001-*.md
# Status: PLACEHOLDER — implementação pendente (Fase 13)

DB="banco_de_dados/sqlite/soe-ccg.db"
SCHEMA="banco_de_dados/esquemas/schema-sqlite-v1.sql"

if [ ! -f "$DB" ]; then
  echo "Banco não encontrado. Criando..."
  sqlite3 "$DB" < "$SCHEMA"
  sqlite3 "$DB" < "banco_de_dados/seeds/seed-categorias.sql"
  echo "Banco criado em $DB"
fi

echo "TODO: Implementar parse de frontmatter YAML e inserção no SQLite"
echo "Ver: docs/05-desenvolvimento/padroes-desenvolvimento.md"
echo "Arquivo alvo: $1"
