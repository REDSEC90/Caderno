# Cookbook — Registrar uma Execução (EXE) e Observação (OBS)

> Como registrar o que aconteceu durante um preparo e capturar insights.

---

## Criar uma Execução (EXE)

**O que é uma Execução:** o registro de um preparo real. Cada vez que você prepara uma receita, é uma nova EXE. Execuções mal-sucedidas têm tanto valor quanto as bem-sucedidas.

**Uma EXE por preparo, sempre — mesma receita preparada 10 vezes = 10 EXEs e 1 REC.**

### Pré-condição

A Receita referenciada deve existir no sistema:

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas WHERE id = 'REC-000001';"
```

```
# Resultado esperado:
REC-000001|Doce de Leite Artesanal|testada
```

### Passo 1 — Obter o próximo ID de EXE

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM execucoes ORDER BY id DESC LIMIT 1;"
```

### Passo 2 — Criar o arquivo

```bash
cp docs/01-dominio/templates/execucao-v1.md \
   dados/execucoes/EXE-000002-doce-de-leite-execucao2-v1.md
```

### Passo 3 — Editar

```markdown
---
id: EXE-000002
tipo: execucao
schema-version: 1
versao: 1
status: concluida
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: [seu-nome]
receita-id: REC-000001
tags: [doce-de-leite, teste-acucar]
---

# Execução — Doce de Leite Artesanal — 2026-06-28

## Referência
- **Receita:** REC-000001 — Doce de Leite Artesanal
- **Data de execução:** 2026-06-28

## Ingredientes Utilizados

| ID         | Nome                 | Quantidade | Unidade |
|------------|----------------------|------------|---------|
| ING-000001 | Leite Integral       | 1000       | ml      |
| ING-000002 | Açúcar Refinado      | 300        | g       |
| ING-000003 | Sal Refinado         | 1          | pitada  |
| ING-000004 | Bicarbonato de Sódio | 1          | g       |

## Métricas

| Métrica            | Valor   |
|--------------------|---------|
| Tempo total        | 2h 20min|
| Peso final         | 290g    |
| Temperatura máxima | 107°C   |

## Avaliações

- Sabor: 9/10
- Textura: 8/10
- Aparência: 8/10
- Geral: 9/10

## Desvios em Relação à Receita

- Açúcar aumentado de 250g para 300g (teste de sabor mais intenso)

## Observações

Sabor notavelmente mais intenso e cor mais escura com 300g de açúcar.
Ponto firme atingido em 2h20. Resultado próximo do pingo de leite desejado.
```

### Passo 4 — Importar, verificar e commitar

```bash
scripts/importacao/importar.sh dados/execucoes/EXE-000002-doce-de-leite-execucao2-v1.md

sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, receita_id, status FROM execucoes WHERE id = 'EXE-000002';"
```

```
# Resultado esperado:
EXE-000002|REC-000001|concluida
```

```bash
git add dados/execucoes/EXE-000002-doce-de-leite-execucao2-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(exe): registra EXE-000002 segundo preparo doce-de-leite 2026-06-28"
```

---

## Criar uma Observação (OBS)

**O que é uma Observação:** um insight, descoberta ou nota vinculada a qualquer entidade do sistema. Capture observações no momento em que surgem — insights não registrados são perdidos.

**Bons exemplos de OBS:**
- "O bicarbonato previne coagulação das proteínas do leite"
- "Açúcar com 300g produz sabor mais intenso que com 250g"
- "Polvilho azedo vencido perde elasticidade"

### Passo 1 — Criar o arquivo

```bash
# Próximo ID de OBS
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM observacoes ORDER BY id DESC LIMIT 1;"

cp docs/01-dominio/templates/observacao-v1.md \
   dados/observacoes/OBS-000002-acucar-300g-sabor-v1.md
```

### Passo 2 — Editar

```markdown
---
id: OBS-000002
tipo: observacao
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: [seu-nome]
entidade-id: ING-000002
tags: [acucar, sabor, proporcao]
relevancia: alta
---

# Proporção de Açúcar Afeta Intensidade de Sabor

## Observação
Aumentar a proporção de açúcar de 250g para 300g por litro de leite no doce de
leite artesanal (REC-000001) produziu sabor notavelmente mais intenso e cor mais
escura, sem comprometer a textura. A experiência foi registrada em EXE-000002.

## Contexto
- Executado em: EXE-000002 (2026-06-28)
- Receita base: REC-000001
- Ingrediente: ING-000002 (Açúcar Refinado)

## Implicações
- Hipótese confirmada: proporção de açúcar é variável relevante para intensidade de sabor
- Próximo teste: comparar com proporção intermediária (275g) para calibrar
- Pode-se considerar documentar como variação oficial na receita (v2)
```

### Passo 3 — Importar e commitar

```bash
scripts/importacao/importar.sh dados/observacoes/OBS-000002-acucar-300g-sabor-v1.md

git add dados/observacoes/OBS-000002-acucar-300g-sabor-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(obs): registra OBS-000002 proporcao acucar sabor doce-leite"
```

---

## Quando criar OBS vs. colocar no corpo da EXE

| Situação | Ação |
|----------|------|
| Insight pontual sobre aquele preparo específico | Campo `Observações` na EXE |
| Aprendizado aplicável a futuros preparos | Criar OBS vinculada ao ING ou TEC |
| Descoberta sobre um ingrediente | OBS com `entidade-id` apontando para o ING |
| Comparação entre duas execuções | OBS vinculada à REC |
| Insight sobre uma técnica | OBS com `entidade-id` apontando para o TEC |

**Regra de ouro:** se o insight teria valor para alguém que nunca viu esta EXE específica, crie uma OBS. Se é específico daquele momento, fica na EXE.
