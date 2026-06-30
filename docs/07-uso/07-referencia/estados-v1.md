# Referência: Estados das Entidades

---

## Tabela Completa de Estados por Entidade

| Entidade | Estado | Significado |
|----------|--------|-------------|
| **Receita** | `rascunho` | Criada, sem execução registrada |
| | `testada` | Tem pelo menos uma Execução |
| | `refinada` | Múltiplas execuções, proporções estabilizadas |
| | `arquivada` | Fora de uso ativo, preservada no sistema |
| **Ingrediente** | `ativo` | Em uso normal |
| | `arquivado` | Não mais em uso, preservado |
| **Técnica** | `ativo` | Em uso normal |
| | `arquivado` | Não mais em uso, preservada |
| **Equipamento** | `ativo` | Em uso normal |
| | `arquivado` | Não mais em uso, preservado |
| **Execução** | `registrada` | Registrada, pode ser editada |
| | `revisada` | Revisada e confirmada |
| | `consolidada` | Final — não deve ser alterada |
| **Observação** | `ativo` | Válida e relevante |
| | `arquivado` | Superada ou irrelevante |
| **Experimento** | `aberto` | Em andamento |
| | `concluido` | Finalizado, com resultado |
| | `incorporado` | Resultado integrado a uma receita |
| | `descartado` | Hipótese refutada ou abandonada |

---

## Transições Válidas

```
Receita:      rascunho → testada → refinada → arquivada
                                              (também de testada diretamente)

Execução:     registrada → revisada → consolidada

Experimento:  aberto → concluido → incorporado
                               ↘ descartado

ING/TEC/EQP:  ativo → arquivado

OBS:          ativo → arquivado
```

Transições inversas (ex: `consolidada → registrada`) não são permitidas. Usar arquivamento e criar nova entidade se necessário.
