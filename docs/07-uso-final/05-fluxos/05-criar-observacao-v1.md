# Fluxo: Criar uma Observação

> Observações capturam o que foi aprendido — são o vetor de evolução do conhecimento.

---

## Quando criar uma Observação

- Você descobriu algo sobre um ingrediente, técnica ou equipamento durante um preparo
- Há uma relação química, física ou prática que vale documentar
- Algo surpreendente aconteceu e você quer registrar para não esquecer
- Uma hipótese informal surgiu e pode virar um Experimento depois

Observações não precisam ser conclusivas. Uma OBS `"bicarbonato em excesso = sabor amargo"` tem valor mesmo que ainda não haja experimento para quantificar.

---

## Passo a Passo

```bash
# 1. Obter próximo ID de OBS
cp docs/01-dominio/templates/observacao-v1.md \
   dados/observacoes/OBS-000002-queijo-temperatura-fusao-v1.md

nano dados/observacoes/OBS-000002-queijo-temperatura-fusao-v1.md
```

Frontmatter:
```yaml
---
id: OBS-000002
tipo: observacao
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
entidade-referenciada: ING-000006
tipo-entidade: ingrediente
relevancia: alta
tags: [queijo, temperatura, fusao, pao-de-queijo]
---
```

Conteúdo:
```markdown
# Temperatura de fusão do queijo Minas meia-cura

O queijo Minas meia-cura começa a fundir a partir de ~55°C.
No pão de queijo, a temperatura do polvilho escaldado (±80°C) é suficiente
para fundir o queijo e criar a estrutura característica.

Queijo em temperatura ambiente (não gelado) funde mais uniformemente.
Queijo gelado pode criar grumos.

**Consequência prática:** retirar o queijo da geladeira 30min antes do preparo.

Ver também: EXE-000002 — observado na execução do pão de queijo de 2026-06-26.
```

```bash
scripts/importacao/importar.sh dados/observacoes/OBS-000002-queijo-temperatura-fusao-v1.md
git commit -am "feat(obs): cria OBS-000002 temperatura fusao queijo"
```

---

## Verificação final

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, status FROM observacoes WHERE id = 'OBS-000002';"
```

```
# Resultado esperado:
OBS-000002|ativo
```

```bash
# Ver arestas criadas pela OBS
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT target, kind FROM relacionamentos WHERE source = 'OBS-000002';"
```

---

## Problemas comuns

| Problema | Causa | Solução |
|----------|-------|---------|
| OBS sem arestas no banco | `entidade-referenciada` ausente no frontmatter | Adicionar o campo e reimportar |
| OBS isolada no FAA | Mesma causa — sem vínculo com nenhuma entidade | Vincular a pelo menos um ING, TEC ou EXE |

---

## Próxima leitura

- Transformar a observação em hipótese formal → [`04-criar-experimento-v1.md`](04-criar-experimento-v1.md)
