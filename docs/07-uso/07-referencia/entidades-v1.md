# Referência: Entidades

| Entidade | Prefixo | Tabela SQLite | Diretório | Status válidos |
|----------|---------|---------------|-----------|----------------|
| Receita | `REC` | `receitas` | `dados/receitas/` | `rascunho` `testada` `refinada` `arquivada` |
| Ingrediente | `ING` | `ingredientes` | `dados/ingredientes/` | `ativo` `arquivado` |
| Técnica | `TEC` | `tecnicas` | `dados/tecnicas/` | `ativo` `arquivado` |
| Equipamento | `EQP` | `equipamentos` | `dados/equipamentos/` | `ativo` `arquivado` |
| Execução | `EXE` | `execucoes` | `dados/execucoes/` | `registrada` `revisada` `consolidada` |
| Observação | `OBS` | `observacoes` | `dados/observacoes/` | `ativo` `arquivado` |
| Experimento | `EXP` | `experimentos` | `dados/experimentos/` | `aberto` `concluido` `incorporado` `descartado` |

---

## Campos Obrigatórios Comuns (todos os tipos)

| Campo | Formato | Exemplo |
|-------|---------|---------|
| `id` | `[PREFIXO]-[NNNNNN]` | `REC-000001` |
| `tipo` | string canônica | `receita` |
| `schema-version` | inteiro | `1` |
| `versao` | inteiro | `1` |
| `status` | string do catálogo | `rascunho` |
| `criado-em` | `YYYY-MM-DD` | `2026-06-27` |
| `atualizado-em` | `YYYY-MM-DD` | `2026-06-27` |
| `autor` | string | `nome-do-autor` |
| `tags` | lista de strings | `[brasileiro, doce]` |

---

## Campos de Relacionamento por Entidade

| Entidade | Campo | Tipo de Aresta gerada |
|----------|-------|----------------------|
| Receita | `ingredientes: [ING-…]` | COMPOSITIONAL |
| Receita | `tecnicas: [TEC-…]` | COMPOSITIONAL |
| Receita | `equipamentos: [EQP-…]` | COMPOSITIONAL |
| Execução | `receita-id: REC-…` | STRUCTURAL |
| Observação | `entidade-referenciada: [ID]` | STRUCTURAL |
| Experimento | `receita-base-id: REC-…` | DERIVATION |

---

## Ciclos de Vida

```
Receita:    rascunho → testada → refinada
                                        ↘ arquivada

Execução:   registrada → revisada → consolidada

Experimento: aberto → concluido → incorporado
                              ↘ descartado
```
