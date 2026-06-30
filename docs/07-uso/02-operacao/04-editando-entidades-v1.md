# Editando Entidades

> Como alterar um registro existente sem quebrar referências.

---

## Regra Geral

O único campo que nunca pode ser alterado é o `id`.

Todo o resto — nome, campos de conteúdo, status, tags, até os relacionamentos — pode ser modificado com os cuidados adequados.

---

## Edição Simples (correção ou adição de conteúdo)

Para corrigir uma informação, adicionar uma nota ou atualizar um campo:

```bash
# 1. Editar o arquivo
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# 2. Atualizar atualizado-em no frontmatter
#    atualizado-em: 2026-06-27

# 3. Re-importar
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# 4. Verificar
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, atualizado_em FROM receitas WHERE id = 'REC-000001';"

# 5. Commitar
git commit -am "fix(rec): corrige tempo de preparo de REC-000001"
```

---

## Alterando Relacionamentos

Quando adicionar ou remover um ID de uma lista de relacionamentos, o Resolver precisa verificar novamente:

```bash
# Após editar os campos ingredientes/tecnicas/equipamentos no frontmatter:
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Verificar que a auditoria de dependências está ok
python3 scripts/auditoria/auditor-v1.py --motor dependencias
```

⚠️ Se remover um ID de `ingredientes`, certifique-se de que nenhuma Execução registra esse ingrediente como usado — pode criar inconsistência.

---

## Renomeando um Ingrediente ou Técnica

"Renomear" no SOE significa alterar o campo `nome` (ou o título H1) do arquivo. O ID não muda.

```bash
# Editar o arquivo
nano dados/ingredientes/ING-000001-leite-integral-v1.md
# Alterar: # Leite Integral  →  # Leite Integral Pasteurizado

# Atualizar atualizado-em
# Re-importar
scripts/importacao/importar.sh dados/ingredientes/ING-000001-leite-integral-v1.md
```

Nenhuma referência existente precisa ser atualizada — todas apontam para `ING-000001`, não para o nome.

---

## Alterando Status

Mudança de status segue as transições válidas (ver `docs/01-dominio/catalogos/estados-todas-entidades-v1.md`):

```bash
# Promover uma receita de 'rascunho' para 'testada' após primeira execução
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
# Alterar: status: rascunho  →  status: testada
# Atualizar atualizado-em

scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
git commit -am "feat(rec): promove REC-000001 para status testada"
```

---

## Verificando Quem Referencia uma Entidade (antes de editar)

Antes de alterar algo que outros registros podem depender:

```bash
# Quem referencia ING-000001?
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, kind FROM relacionamentos WHERE target = 'ING-000001';"

# Via grep nos arquivos
grep -r "ING-000001" dados/ --include="*.md"
```

Isso evita alterações que quebram silenciosamente dependentes.

---

## Por que o `id` nunca muda

O identificador é a identidade permanente no grafo. Cada arquivo que referencia `ING-000001` confia que esse ID aponta para Leite Integral agora e sempre. Mudar o ID quebraria silenciosamente todas essas referências — sem erro no Parser, sem aviso do Resolver, apenas dados incorretos no banco.

---

## Próxima leitura

- Como arquivar em vez de deletar → [`05-removendo-entidades-v1.md`](05-removendo-entidades-v1.md)
- Como criar uma nova versão formal → [`06-versionamento-v1.md`](06-versionamento-v1.md)
