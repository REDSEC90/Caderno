# Referência: Comandos

> Todos os comandos operacionais do SOE-CCG. Execute a partir da raiz do repositório.

---

## Auditoria (FAA)

```bash
# Auditoria completa
python3 scripts/auditoria/auditor-v1.py

# Motor específico
python3 scripts/auditoria/auditor-v1.py --motor [baseline|dados|dependencias|estrutura|filosofia|dominio|cobertura|maturidade|semantica|integridade|padroes|escalabilidade]

# Estado persistido
python3 scripts/auditoria/auditor-v1.py state
python3 scripts/auditoria/auditor-v1.py state --json

# Inspecionar entidade
python3 scripts/auditoria/auditor-v1.py entity [ID]

# Listar problemas
python3 scripts/auditoria/auditor-v1.py issues
python3 scripts/auditoria/auditor-v1.py issues --critical
```

---

## Pipeline de Importação

```bash
# Importar um arquivo
scripts/importacao/importar.sh dados/[tipo]/[arquivo].md

# Reimportar todos os dados
scripts/importacao/importar-todos.sh

# Reconstruir banco do zero
rm banco_de_dados/sqlite/soe-ccg.db
sqlite3 banco_de_dados/sqlite/soe-ccg.db < banco_de_dados/esquemas/schema-sqlite-v1.sql
scripts/importacao/importar-todos.sh
```

---

## Parser e Validação

```bash
# Parsear arquivo (detecta erros de frontmatter)
python3 codigo/parser-v1.py dados/[tipo]/[arquivo].md

# Validar grafo completo
python3 codigo/validador-v1.py
```

---

## SQLite

```bash
# Shell interativo
sqlite3 banco_de_dados/sqlite/soe-ccg.db

# Query direta
sqlite3 banco_de_dados/sqlite/soe-ccg.db "SELECT id, titulo FROM receitas;"

# Com headers e colunas formatadas
sqlite3 -header -column banco_de_dados/sqlite/soe-ccg.db "SELECT * FROM receitas;"

# Exportar CSV
sqlite3 -csv -header banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas;" > exports/receitas.csv
```

---

## Git

```bash
# Estado atual
git status
git diff --stat

# Histórico de um arquivo
git log --oneline dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Ver arquivo em commit específico
git show [hash]:dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Commit padrão
git add dados/[tipo]/[arquivo].md docs/04-padroes/identificadores-v1.md
git commit -m "[tipo]([escopo]): [descrição]"
```

---

## Dependências Python

```bash
# Instalar dependência principal
pip install python-frontmatter --break-system-packages

# Verificar instalação
python3 -c "import frontmatter; print('OK')"
```
