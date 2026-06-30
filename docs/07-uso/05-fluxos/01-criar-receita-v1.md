# Fluxo: Criar uma Receita

> Tutorial completo, passo a passo. Baseado em um exemplo real.

**Objetivo:** Registrar uma nova receita de Pão de Queijo Mineiro.

---

## Passo 1 — Identificar os ingredientes necessários

Antes de criar a Receita, os ingredientes devem existir no sistema.

Ingredientes que usaremos: polvilho azedo, queijo Minas meia-cura, ovos, óleo, leite, sal.

```bash
# Verificar quais já existem
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%polvilho%'
   UNION SELECT id, nome FROM ingredientes WHERE nome LIKE '%queijo%'
   UNION SELECT id, nome FROM ingredientes WHERE nome LIKE '%ovo%';"
```

Suponha que apenas `ING-000001 Leite Integral` já existe. Os demais precisam ser criados.

---

## Passo 2 — Criar os ingredientes faltantes

Para cada ingrediente faltante, repita este processo:

```bash
# Verificar próximo ID de ING (tabela em docs/04-padroes/identificadores-v1.md)
# Suponha: ING-000004 é o último → próximo é ING-000005

# Copiar template
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000005-polvilho-azedo-v1.md

# Editar
nano dados/ingredientes/ING-000005-polvilho-azedo-v1.md
```

Frontmatter mínimo para o polvilho:
```yaml
---
id: ING-000005
tipo: ingrediente
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
tags: [amido, fermentado, brasileiro]
---

# Polvilho Azedo

## Informações
- **Tipo:** Amido fermentado
- **Unidade padrão:** g

## Descrição
Amido de mandioca fermentado e seco. Confere elasticidade característica ao pão de queijo.
```

Importar imediatamente:
```bash
scripts/importacao/importar.sh dados/ingredientes/ING-000005-polvilho-azedo-v1.md
```

Repetir para: `ING-000006-queijo-minas-meia-cura-v1.md`, `ING-000007-ovo-v1.md`, `ING-000008-oleo-v1.md`, `ING-000009-sal-v1.md`.

---

## Passo 3 — Verificar/criar técnicas necessárias

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM tecnicas WHERE nome LIKE '%mistura%'
   UNION SELECT id, nome FROM tecnicas WHERE nome LIKE '%form%';"
```

Se não existir técnica de "modelagem manual", criar:
```bash
cp docs/01-dominio/templates/tecnica-v1.md \
   dados/tecnicas/TEC-000004-modelagem-manual-v1.md
# Editar e importar
```

---

## Passo 4 — Verificar/criar equipamentos necessários

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM equipamentos;"
```

Criar o que faltar (`forma-para-forno`, `tigela` etc.).

---

## Passo 5 — Criar a Receita

```bash
# Próximo ID de REC
# Suponha: REC-000001 é o último → próximo é REC-000002

cp docs/01-dominio/templates/receita-v1.md \
   dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md

nano dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
```

Frontmatter da Receita:
```yaml
---
id: REC-000002
tipo: receita
schema-version: 1
versao: 1
status: rascunho
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
origem: receita familiar
tags: [brasileiro, lanche, queijo, gluten-free]
ingredientes: [ING-000005, ING-000006, ING-000007, ING-000008, ING-000001, ING-000009]
tecnicas: [TEC-000004]
equipamentos: [EQP-000003]
---
```

---

## Passo 6 — Importar e validar

```bash
# Importar
scripts/importacao/importar.sh dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md

# Verificar no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas WHERE id = 'REC-000002';"

# Verificar relacionamentos
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, target, kind FROM relacionamentos WHERE source = 'REC-000002';"
```

---

## Passo 7 — Rodar FAA

```bash
python3 scripts/auditoria/auditor-v1.py
```

Resultado esperado: sem novas falhas.

---

## Passo 8 — Atualizar controle de IDs e commitar

```bash
# Atualizar docs/04-padroes/identificadores-v1.md
# ING: ING-000009 (ou o último criado)
# REC: REC-000002
# TEC: TEC-000004 (se criado)
# EQP: EQP-000003 (se criado)

git add dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
git add dados/ingredientes/
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(rec): cria REC-000002 pao-de-queijo-mineiro com 5 novos ING"
```

---

## Passo 9 — Registrar a primeira execução (opcional mas recomendado)

Se você preparou o pão de queijo ao criar esta receita, registre a execução agora:
→ Ver [02-criar-execucao.md](02-criar-execucao.md)

✅ Receita criada, importada, auditada e commitada.

---

## Verificação final

```bash
# Receita no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas WHERE id = 'REC-000002';"
```

```
# Resultado esperado:
REC-000002|Pão de Queijo Mineiro|rascunho
```

```bash
# Relacionamentos criados
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT target, kind FROM relacionamentos WHERE source = 'REC-000002' ORDER BY kind;"
```

```
# Resultado esperado:
EQP-000003|COMPOSITIONAL
ING-000005|COMPOSITIONAL
ING-000006|COMPOSITIONAL
ING-000007|COMPOSITIONAL
ING-000008|COMPOSITIONAL
ING-000009|COMPOSITIONAL
TEC-000004|COMPOSITIONAL
```

---

## Problemas comuns neste fluxo

| Problema | Causa | Solução |
|----------|-------|---------|
| `referencia_quebrada: ING-000007` ao importar a REC | Ingrediente ainda não foi importado | Importar o ING primeiro, depois importar a REC |
| Relacionamentos não aparecem no banco | IDs no frontmatter com formato errado (minúsculas, sem zeros) | Corrigir o formato: `ING-000007`, não `ing-7` |
| FAA reprovado após criar a receita | A receita referencia um ID que o Resolver não encontrou | `python3 scripts/auditoria/auditor-v1.py entity REC-000002` para ver as arestas |

---

## Próxima leitura

- Registrar o primeiro preparo → [`02-criar-execucao-v1.md`](02-criar-execucao-v1.md)
- Versão rápida (só os comandos) → [`../10-cookbook/02-criar-receita-v1.md`](../10-cookbook/02-criar-receita-v1.md)
