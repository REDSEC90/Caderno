# Sequências Válidas de Operação

> Quais operações podem ser executadas, em que ordem, e quais são proibidas.

Este documento complementa os invariantes. Enquanto [`02-invariantes-v1.md`](02-invariantes-v1.md) diz o que nunca fazer, este documento diz o que fazer e em que ordem.

---

## Sequência 1 — Criar uma entidade nova

```
verificar_existencia(tipo, nome)
       ↓ não existe
obter_proximo_id(tipo)
       ↓
copiar_template(tipo, id, slug)
       ↓
preencher_frontmatter(arquivo)
       ↓
executar_parser(arquivo)        ← parar se houver erro
       ↓
importar(arquivo)               ← parar se houver erro
       ↓
verificar_banco(id)             ← confirmar que foi importado
       ↓
atualizar_controle_ids(tipo, id)
       ↓
git_commit(arquivo, mensagem)
```

**Restrição de ordem:** Entidades devem ser criadas antes das entidades que as referenciam.

```
EQP → TEC → ING → REC → EXE → OBS / EXP
```

Nunca criar uma REC antes de existirem todos os ING, TEC e EQP que ela vai referenciar.

---

## Sequência 2 — Editar uma entidade existente

```
git_pull()                       ← sincronizar antes de editar
       ↓
verificar_dependentes(id)        ← quem referencia esta entidade?
       ↓
editar_arquivo(arquivo)
atualizar_campo(atualizado_em, data_hoje)
       ↓
[SE alterou relacionamentos]:
  executar_resolver()            ← verificar que referências ainda são válidas
       ↓
importar(arquivo)
       ↓
verificar_banco(id)
       ↓
git_commit(arquivo, mensagem)
```

**Campo proibido de alterar:** `id`. Qualquer outro campo pode ser editado.

**Verificar dependentes antes de alterar nome ou status:**
```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, kind FROM relacionamentos WHERE target = '[ID]';"
```

---

## Sequência 3 — Arquivar uma entidade

```
verificar_dependentes(id)
       ↓
[SE há dependentes ativos]:
  decidir: migrar_dependentes(id_novo) OU arquivar_com_aviso()
       ↓
editar_arquivo(arquivo)
  status: ativo → status: arquivado
  data-arquivamento: [data]
  motivo-arquivamento: "[motivo]"
  atualizado-em: [data]
       ↓
importar(arquivo)
       ↓
git_commit(arquivo, "chore([tipo]): arquiva [ID] — [motivo]")
```

**Nunca:** `rm dados/[tipo]/[ID]-*.md`. Arquivar, nunca deletar.

---

## Sequência 4 — Sessão de trabalho completa (múltiplas entidades)

```
git_pull()
auditar()                        ← estado inicial — registrar score de entrada
       ↓
[para cada entidade a criar, na ordem EQP→TEC→ING→REC→EXE→OBS/EXP]:
  sequencia_1_criar_entidade()
       ↓
atualizar_controle_ids()         ← uma vez ao final, não a cada entidade
       ↓
auditar()                        ← estado final — verificar que não introduziu regressões
       ↓
git_add(todos_os_arquivos_novos)
git_add(docs/04-padroes/identificadores-v1.md)
git_commit(mensagem_descritiva_da_sessao)
git_push()
```

---

## Sequência 5 — Reconstrução do banco

```
[SOMENTE quando o banco estiver corrompido ou ausente]

rm banco_de_dados/sqlite/soe-ccg.db
criar_schema()
       ↓
[importar na ordem]:
  importar(dados/equipamentos/)
  importar(dados/tecnicas/)
  importar(dados/ingredientes/)
  importar(dados/receitas/)
  importar(dados/execucoes/)
  importar(dados/observacoes/)
  importar(dados/experimentos/)
       ↓
auditar()
```

Nenhum commit necessário — o banco não é versionado.

---

## Operações proibidas (jamais executar)

| Operação | Por quê é proibida |
|----------|-------------------|
| `UPDATE [tabela] SET ... WHERE id = '[ID]'` no SQLite | Banco é derivado — sobrescrito na próxima importação |
| `INSERT INTO [tabela] VALUES (...)` no SQLite | Mesma razão |
| `rm dados/[tipo]/[ID]-*.md` | Destrói histórico permanentemente |
| Alterar o campo `id` de um arquivo existente | Quebra todas as referências existentes |
| Criar entidade sem verificar existência | Produz duplicatas que corrompem o grafo |
| Reutilizar um ID de entidade arquivada | Cria ambiguidade histórica irresolvível |
| Commitar `banco_de_dados/sqlite/soe-ccg.db` | Banco é derivado, não pertence ao versionamento |

---

## Verificações pós-operação obrigatórias

Após qualquer sequência de escrita, antes do commit:

```bash
# 1. Parser lê todos os arquivos novos sem erro
python3 codigo/parser-v1.py dados/[tipo]/[ID]-*.md

# 2. Banco reflete o que foi criado
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, [campo_principal] FROM [tabela] WHERE id = '[ID]';"

# 3. FAA não introduziu regressões
python3 scripts/auditoria/auditor-v1.py issues --critical

# 4. git status mostra apenas os arquivos esperados
git status
```

Se qualquer verificação falhar, **não commitar**. Corrigir primeiro.
