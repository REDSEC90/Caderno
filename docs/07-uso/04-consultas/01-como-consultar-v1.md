# Como Consultar o Conhecimento

> Três formas de acessar o conhecimento no SOE — quando usar cada uma.

---

## As Três Formas de Consulta

### 1. Leitura direta dos arquivos Markdown

**Quando usar:** Leitura humana, inspeção rápida, busca por texto livre.

```bash
# Abrir uma receita diretamente
cat dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Buscar por texto em todos os arquivos
grep -r "bicarbonato" dados/ --include="*.md" -l

# Listar todos os ingredientes por nome
grep -r "^# " dados/ingredientes/ | sed 's/.*# //'
```

**Limitação:** Sem filtros estruturados, sem joins, sem agregações.

---

### 2. Consultas SQL via SQLite

**Quando usar:** Filtros, ordenação, agregações, joins entre entidades, exportação.

```bash
# Shell interativo
sqlite3 banco_de_dados/sqlite/soe-ccg.db

# Query direta
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo FROM receitas WHERE status = 'testada';"
```

**Limitação:** Reflete o estado no momento da última importação. Se um arquivo foi editado e não reimportado, o banco está desatualizado.

---

### 3. Grafo de conhecimento (via FAA/IR)

**Quando usar:** Navegação de relacionamentos, análise de dependências, inspeção de arestas.

```bash
# Ver entidade e todas as suas arestas
python3 scripts/auditoria/auditor-v1.py entity REC-000001

# Ver estado global do sistema
python3 scripts/auditoria/auditor-v1.py state --json
```

**Limitação:** Mais complexo. Mais poderoso para análise estrutural.

---

## Garantindo que o Banco Está Atualizado

Antes de qualquer consulta SQL importante:

```bash
# Verificar última atualização do banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT MAX(atualizado_em) FROM receitas;"

# Se necessário, reimportar
scripts/importacao/importar-todos.sh
```
