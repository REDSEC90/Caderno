# Removendo Entidades

> No SOE, "remover" significa arquivar. Nunca deletar.

---

## A Regra Fundamental

**Nunca delete um arquivo de `dados/`.**

Deletar destrói conhecimento. O arquivo `.md` é o registro histórico. Uma vez criado, ele existe para sempre — no máximo muda de `status: ativo` para `status: arquivado`.

O git preserva o histórico mesmo de arquivos deletados, mas a intenção do sistema é que os arquivos permaneçam presentes em disco.

---

## Como Arquivar

```bash
# 1. Abrir o arquivo
nano dados/ingredientes/ING-000005-ingrediente-duplicado-v1.md

# 2. Alterar o status
#    status: ativo  →  status: arquivado

# 3. Adicionar metadados de arquivamento (opcional mas recomendado)
#    data-arquivamento: 2026-06-27
#    motivo-arquivamento: "Duplicata de ING-000001 — usar ING-000001"

# 4. Atualizar atualizado-em

# 5. Re-importar
scripts/importacao/importar.sh dados/ingredientes/ING-000005-ingrediente-duplicado-v1.md

# 6. Commitar
git commit -am "chore(ing): arquiva ING-000005 duplicata de ING-000001"
```

---

## Detectando Dependentes Antes de Arquivar

Arquivar uma entidade que outras dependem cria inconsistência. Sempre verificar:

```bash
# Quem referencia esta entidade?
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, kind, origin FROM relacionamentos WHERE target = 'ING-000005';"

# Via grep nos arquivos
grep -r "ING-000005" dados/ --include="*.md"
```

Se houver dependentes, você tem duas opções:
1. Arquivar com cuidado e documentar no `motivo-arquivamento` que os dependentes devem migrar para outro ID.
2. Migrar todos os dependentes para a entidade correta antes de arquivar.

---

## Acessando Entidades Arquivadas

Entidades arquivadas não aparecem nas consultas padrão, mas continuam acessíveis:

```sql
-- Ver todos os ingredientes arquivados
SELECT id, nome FROM ingredientes WHERE status = 'arquivado';

-- Acessar uma entidade arquivada específica
SELECT * FROM ingredientes WHERE id = 'ING-000005';
```

O arquivo `.md` também continua em `dados/ingredientes/` — ainda pode ser lido diretamente.
