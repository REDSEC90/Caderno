# Fluxo: Registrar uma Execução

> Tutorial para registrar um preparo real de uma receita existente.

**Objetivo:** Registrar o segundo preparo do Doce de Leite Artesanal (REC-000001).

---

## Quando criar uma Execução

Sempre que você preparar uma receita — independentemente do resultado. Execuções mal-sucedidas têm tanto valor quanto as bem-sucedidas: documentam o que não funciona.

Uma Execução nunca substitui uma Receita. Se você preparou a mesma receita dez vezes, há dez Execuções e uma Receita.

---

## Passo 1 — Confirmar que a Receita existe

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas WHERE id = 'REC-000001';"
```

A Receita deve existir com `status` de pelo menos `rascunho`.

---

## Passo 2 — Obter o próximo ID de EXE

Consultar `docs/04-padroes/identificadores-v1.md`.
Se `EXE-000001` é o último → próximo é `EXE-000002`.

---

## Passo 3 — Criar o arquivo

```bash
cp docs/01-dominio/templates/execucao-v1.md \
   dados/execucoes/EXE-000002-doce-de-leite-execucao2-v1.md

nano dados/execucoes/EXE-000002-doce-de-leite-execucao2-v1.md
```

Frontmatter:
```yaml
---
id: EXE-000002
tipo: execucao
schema-version: 1
versao: 1
status: concluida
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
tags: [doce-de-leite, segundo-preparo]
---
```

Conteúdo:
```markdown
# Execução — Doce de Leite Artesanal — 2026-06-27

## Referência
- **Receita:** REC-000001
- **Data de execução:** 2026-06-27

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
| Tempo total        | 2h 15min|
| Peso final         | 285g    |
| Temperatura máxima | 107°C   |

## Avaliações

- Sabor: 9/10
- Textura: 8/10
- Aparência: 8/10
- Geral: 9/10

## Desvios em Relação à Receita

- Açúcar aumentado de 250g para 300g (teste da hipótese de sabor mais intenso)

## Observações

Sabor mais intenso e levemente mais escuro. Ponto firme atingido em 2h15.
Açúcar 300g produziu resultado mais próximo do pingo de leite desejado.
```

---

## Passo 4 — Importar

```bash
scripts/importacao/importar.sh dados/execucoes/EXE-000002-doce-de-leite-execucao2-v1.md
```

---

## Passo 5 — Atualizar status da Receita (se necessário)

Se esta é a primeira execução de uma receita em `status: rascunho`:
```bash
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
# Alterar: status: rascunho → status: testada
# Atualizar: atualizado-em: 2026-06-27

scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

---

## Passo 6 — Registrar descobertas como Observações

Se o preparo revelou algo relevante, crie uma OBS:
```bash
cp docs/01-dominio/templates/observacao-v1.md \
   dados/observacoes/OBS-000002-acucar-300g-sabor-v1.md
# Frontmatter: entidade-referenciada: EXE-000002, relevancia: media
```

---

## Passo 7 — Commitar

```bash
git add dados/execucoes/EXE-000002-doce-de-leite-execucao2-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(exe): registra EXE-000002 segundo preparo doce-de-leite 2026-06-27"
```
