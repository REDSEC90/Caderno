# Cookbook — Criar um Ingrediente (ING)

> Exemplo completo e copiável. Substitua os valores marcados com `[...]` pelos seus dados.

**Tempo:** ~5 minutos  
**Resultado:** Um novo ingrediente no sistema, validado e importado.

---

## Pré-condições

```bash
# O banco deve existir
ls banco_de_dados/sqlite/soe-ccg.db

# Verificar que o ingrediente não existe ainda
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%[NOME-APROXIMADO]%';"
```

```
# Resultado esperado (vazio = podemos criar):
(nenhum resultado)
```

Se retornar um resultado, use o ID existente em vez de criar um novo.

---

## Passo 1 — Obter o próximo ID

```bash
# Ver o último ID de ING usado
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM ingredientes ORDER BY id DESC LIMIT 1;"
```

```
# Resultado esperado (exemplo):
ING-000004
```

O próximo é `ING-000005`. Se o banco estiver vazio, o primeiro é `ING-000001`.

---

## Passo 2 — Criar o arquivo

```bash
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000005-[slug-do-nome]-v1.md
```

**Regra do slug:** minúsculas, sem acentos, hífens no lugar de espaços.
- `Açúcar Mascavo` → `acucar-mascavo`
- `Leite de Coco` → `leite-de-coco`
- `Farinha de Trigo Integral` → `farinha-de-trigo-integral`

---

## Passo 3 — Editar o arquivo

Conteúdo mínimo obrigatório:

```markdown
---
id: ING-000005
tipo: ingrediente
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: [seu-nome]
tags: [[tag1], [tag2]]
---

# [Nome do Ingrediente]

## Informações
- **Tipo:** [Laticínio | Grão | Proteína | Gordura | Tempero | ...]
- **Unidade padrão:** [g | ml | unidade | colher]

## Descrição
[Uma ou duas frases descrevendo o ingrediente.]
```

**Exemplo real preenchido:**

```markdown
---
id: ING-000005
tipo: ingrediente
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: joao
tags: [acucar, adocante, nao-refinado]
---

# Açúcar Mascavo

## Informações
- **Tipo:** Adoçante
- **Unidade padrão:** g

## Descrição
Açúcar não refinado com melaço incorporado. Sabor mais intenso e levemente
caramelizado comparado ao açúcar refinado. Ideal para bolos rústicos e doces
de sabor mais complexo.

## Substitutos
- Açúcar demerara (sabor mais suave)
- Açúcar refinado + melaço (equivalente artesanal)
```

---

## Passo 4 — Importar

```bash
scripts/importacao/importar.sh dados/ingredientes/ING-000005-acucar-mascavo-v1.md
```

```
# Resultado esperado:
[OK] ING-000005 importado com sucesso
```

---

## Passo 5 — Verificar

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome, status FROM ingredientes WHERE id = 'ING-000005';"
```

```
# Resultado esperado:
ING-000005|Açúcar Mascavo|ativo
```

---

## Passo 6 — Atualizar controle de IDs e commitar

```bash
# Atualizar docs/04-padroes/identificadores-v1.md com o novo último ID

git add dados/ingredientes/ING-000005-acucar-mascavo-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(ing): adiciona ING-000005 acucar-mascavo"
```

---

## Resultado final

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome, status FROM ingredientes ORDER BY id;"
```

```
# Resultado esperado:
ING-000001|Leite Integral|ativo
ING-000002|Açúcar Refinado|ativo
ING-000003|Sal Refinado|ativo
ING-000004|Bicarbonato de Sódio|ativo
ING-000005|Açúcar Mascavo|ativo   ← novo
```

---

## Problemas comuns

| Problema | Causa | Solução |
|----------|-------|---------|
| `referencia_quebrada` ao importar | Outro arquivo referencia este ING antes de ele existir | Importar este ING primeiro |
| `status inválido` | Valor de status incorreto | Status válidos para ING: `ativo`, `arquivado` |
| ID duplicado | Já existe um ING com esse número | Verificar o próximo ID disponível |

---

## Próximo passo

Com o ingrediente criado, você pode:
- Criar mais ingredientes → repetir este guia
- Criar uma receita que usa este ingrediente → [`02-criar-receita-v1.md`](02-criar-receita-v1.md)
- Criar uma técnica → [`03-criar-tecnica-v1.md`](03-criar-tecnica-v1.md)
