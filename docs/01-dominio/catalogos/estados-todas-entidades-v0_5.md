# Estados — Todas as Entidades

> Consolidação dos estados de ciclo de vida de todas as entidades do SOE-CCG em um único arquivo de referência.

---

## Receita

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `rascunho` | Em elaboração, não finalizada | Autor | → `testada`, → `arquivada` |
| `testada` | Executada ao menos uma vez | Sistema (via Execução) | → `validada`, → `arquivada` |
| `validada` | Resultado satisfatório e reproduzível | Autor / Mantenedor | → `publicada`, → `arquivada` |
| `publicada` | Conhecimento consolidado e referenciável | Mantenedor | → `arquivada` |
| `arquivada` | Fora do uso ativo, preservada | Mantenedor / Admin | → `ativa` (restauração) |

---

## Execução

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `registrada` | Preparo documentado, dados em preenchimento | Autor | → `revisada` |
| `revisada` | Dados conferidos e complementados | Autor | → `consolidada` |
| `consolidada` | Registro encerrado, sem alterações futuras | Autor | — (estado final de uso) |

---

## Ingrediente

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `ativo` | Disponível para referência | Sistema (padrão) | → `descontinuado`, → `arquivado` |
| `descontinuado` | Não mais recomendado, histórico preservado | Mantenedor | → `arquivado` |
| `arquivado` | Fora de uso, preservado | Mantenedor / Admin | → `ativo` (restauração) |

---

## Técnica

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `ativo` | Disponível para referência | Sistema (padrão) | → `descontinuado`, → `arquivado` |
| `descontinuado` | Não mais recomendado, histórico preservado | Mantenedor | → `arquivado` |
| `arquivado` | Fora de uso, preservado | Mantenedor / Admin | → `ativo` (restauração) |

---

## Equipamento

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `ativo` | Disponível para referência | Sistema (padrão) | → `descontinuado`, → `arquivado` |
| `descontinuado` | Não mais recomendado, histórico preservado | Mantenedor | → `arquivado` |
| `arquivado` | Fora de uso, preservado | Mantenedor / Admin | → `ativo` (restauração) |

---

## Observação

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `ativo` | Válida e consultável | Sistema (padrão ao criar) | → `arquivado`, → `obsoleto` |
| `arquivado` | Superada ou inválida, preservada | Autor / Mantenedor | → `ativo` (restauração) |
| `obsoleto` | Substituída por versão mais precisa | Autor / Mantenedor | — (estado final) |

---

## Experimento

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `aberto` | Em andamento, sem resultado definitivo | Autor | → `concluido` |
| `concluido` | Finalizado com resultado documentado | Autor | → `incorporado`, → `descartado` |
| `incorporado` | Resultado absorvido por uma Receita ou entidade | Autor | — (estado final) |
| `descartado` | Concluído sem aproveitamento, mantido no histórico | Autor | — (estado final) |

---

## Categoria

| Estado | Significado | Quem atribui | Transições possíveis |
|--------|-------------|-------------|---------------------|
| `ativo` | Disponível para classificação de receitas | Sistema (padrão) / Admin | → `descontinuado`, → `arquivado` |
| `descontinuado` | Não mais recomendada, substituída por outra | Admin | → `arquivado` |
| `arquivado` | Fora de uso, histórico preservado | Admin | → `ativo` (restauração) |

---

## Estados do Ciclo de Vida Universal (Política de Arquivamento)

Estes estados se aplicam a todos os Registros, complementando os estados específicos de cada entidade:

| Estado | Significado | Visibilidade padrão |
|--------|-------------|-------------------|
| `rascunho` | Em construção | Apenas autor |
| `revisao` | Sob validação antes de ativação | Revisores |
| `ativo` | Finalizado e em uso | Todos |
| `deprecado` | Não recomendado, mas ainda válido | Todos (com aviso) |
| `arquivado` | Não mais em uso, preservado | Apenas consultas explícitas |
| `obsoleto` | Substituído por versão mais recente | Apenas histórico |

---

## Diagrama de Estados Universal

```
[rascunho] → [revisao] → [ativo] → [deprecado] → [arquivado]
                │           │                          ↑
                └───────────┴──────────────────────────┘
                                   (arquivamento direto)

[ativo] → [obsoleto]  (quando nova versão substitui)
```

---

## Regra de Ouro dos Estados

**Nenhum estado destrói um Registro.**

Todo Registro, independentemente do estado, pode ser encontrado via consulta explícita. O estado controla visibilidade e disponibilidade para referência — nunca a existência.
