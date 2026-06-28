# Primeiros Passos

> Do zero ao primeiro registro funcionando. Execute cada passo em ordem.

---

## Pré-requisitos

```bash
python3 --version    # 3.10 ou superior
git --version        # qualquer versão recente
sqlite3 --version    # normalmente já instalado
```

---

## 1. Clonar o repositório

```bash
git clone <url-do-repositorio> SOE-CCG
cd SOE-CCG
```

---

## 2. Instalar dependências Python

```bash
pip install python-frontmatter
```

✅ Verificar:
```bash
python3 -c "import frontmatter; print('OK')"
```

---

## 3. Verificar estrutura

```bash
ls dados/          # receitas/ ingredientes/ tecnicas/ equipamentos/ execucoes/ observacoes/ experimentos/
ls docs/07-uso/    # este manual
ls scripts/        # auditoria/ importacao/ faa/
ls codigo/         # parser-v1.py resolvedor-v1.py validador-v1.py importador-v1.py
```

---

## 4. Inicializar o banco SQLite (se ainda não existir)

```bash
mkdir -p banco_de_dados/sqlite

sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

echo "Banco criado:"
sqlite3 banco_de_dados/sqlite/soe-ccg.db ".tables"
```

---

## 5. Rodar a auditoria inicial

```bash
python3 scripts/auditoria/auditor-v1.py
```

Resultado esperado num repositório saudável:
```
  Pontuação geral: 90%+
  Decisão arquitetural: APROVADO
```

Se houver falhas, consulte `docs/07-uso/03-validacao/04-faa.md`.

---

## 6. Explorar os dados existentes

```bash
# Ver receitas no sistema
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas;"

# Ver ingredientes
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes ORDER BY nome;"

# Ou direto nos arquivos
ls dados/receitas/
cat dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

---

## 7. Seu primeiro registro

Crie um ingrediente simples para validar o pipeline completo:

```bash
# Passo 1 — Consultar próximo ID disponível
# Abrir docs/04-padroes/identificadores-v1.md e ver tabela de controle
# Se ING-000004 é o último, o próximo é ING-000005

# Passo 2 — Copiar template
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000005-acucar-mascavo-v1.md

# Passo 3 — Editar (use o editor de sua preferência)
# Preencher id, nome, status, criado-em, atualizado-em, autor

# Passo 4 — Importar
scripts/importacao/importar.sh dados/ingredientes/ING-000005-acucar-mascavo-v1.md

# Passo 5 — Verificar
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE id = 'ING-000005';"

# Passo 6 — Atualizar controle de IDs e commitar
git add dados/ingredientes/ING-000005-acucar-mascavo-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(ing): adiciona ING-000005 acucar mascavo"
```

✅ Se o `SELECT` retornou o ingrediente, o pipeline está funcionando.

---

## Próximo passo

Leia `01-introducao/03-como-pensar-no-soe.md` antes de criar qualquer coisa mais complexa.
