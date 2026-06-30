# Cheat Sheet — SOE-CCG

> Consulta operacional em 10 segundos. Mantenha aberto durante o trabalho.

---

## Ordem de Criação (sempre seguir)

```
EQP → TEC → ING → REC → EXE → OBS / EXP
```

---

## Prefixos e Localizações

| Prefixo | Entidade | Diretório |
|---------|---------|-----------|
| `REC` | Receita | `dados/receitas/` |
| `ING` | Ingrediente | `dados/ingredientes/` |
| `TEC` | Técnica | `dados/tecnicas/` |
| `EQP` | Equipamento | `dados/equipamentos/` |
| `EXE` | Execução | `dados/execucoes/` |
| `OBS` | Observação | `dados/observacoes/` |
| `EXP` | Experimento | `dados/experimentos/` |

---

## Nome do Arquivo

```
[PREFIXO]-[NNNNNN]-[slug-sem-acento]-v1.md
Ex: ING-000005-polvilho-azedo-v1.md
```

---

## Frontmatter Mínimo

```yaml
---
id: [PREFIXO]-[NNNNNN]
tipo: [tipo-canônico]
schema-version: 1
versao: 1
status: [status-valido]
criado-em: YYYY-MM-DD
atualizado-em: YYYY-MM-DD
autor: nome
tags: []
---
```

---

## Sessão de Trabalho (ordem)

```bash
git pull                                    # 1. Sincronizar
python3 scripts/auditoria/auditor-v1.py    # 2. Estado inicial
# ... criar/editar arquivos ...
scripts/importacao/importar.sh [arquivo]   # 3. Importar cada arquivo
python3 scripts/auditoria/auditor-v1.py    # 4. Verificar FAA
git add [arquivos] docs/04-padroes/identificadores-v1.md
git commit -m "[tipo]([escopo]): [descrição]"
git push                                    # 5. Publicar
```

---

## Verificações Rápidas

```bash
# Existe um ING com nome similar?
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%[termo]%';"

# Quem referencia este ID?
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, kind FROM relacionamentos WHERE target = '[ID]';"

# Arestas de uma entidade
python3 scripts/auditoria/auditor-v1.py entity [ID]

# FAA rápido (só falhas)
python3 scripts/auditoria/auditor-v1.py issues --critical
```

---

## Tipos de Status por Entidade

| Entidade | Status válidos |
|----------|---------------|
| REC | `rascunho` `testada` `refinada` `arquivada` |
| ING / TEC / EQP / OBS | `ativo` `arquivado` |
| EXE | `registrada` `revisada` `consolidada` |
| EXP | `aberto` `concluido` `incorporado` `descartado` |

---

## Nunca

```
✗ Editar SQLite diretamente
✗ Deletar arquivos de dados/
✗ Reutilizar IDs arquivados
✗ Referenciar entidade por nome (usar ID)
✗ Commitar soe-ccg.db
✗ Criar sem verificar duplicata
✗ Criar REC antes dos ING/TEC/EQP que ela usa
```

---

## Padrão de Commit

```
feat(rec): cria REC-000002 pao-de-queijo-mineiro
fix(ing): corrige tipo de ING-000003
feat(exe): registra EXE-000002 execucao 2026-06-27
chore(ing): arquiva ING-000005 duplicata de ING-000001
audit(faa): resolve ciclo DEP-002
docs(07-uso): adiciona fluxo de experimento
```

---

## Reconstruir Banco do Zero

```bash
rm banco_de_dados/sqlite/soe-ccg.db
sqlite3 banco_de_dados/sqlite/soe-ccg.db < banco_de_dados/esquemas/schema-sqlite-v1.sql
scripts/importacao/importar-todos.sh
```

*Nenhuma informação é perdida — tudo vem dos arquivos Markdown.*
