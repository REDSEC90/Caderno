# Esquema: Experimento v1

Define os campos da entidade Experimento, sua obrigatoriedade e tipos válidos.

---

## Metadados

| Campo            | Obrigatório | Tipo   | Descrição                                         |
|------------------|-------------|--------|---------------------------------------------------|
| `id`             | sim         | string | Identificador permanente. Formato: `EXP-NNNNNN`   |
| `tipo`           | sim         | string | Valor fixo: `experimento`                         |
| `schema-version` | sim         | string | Versão deste esquema. Valor: `1`                  |
| `versao`         | sim         | string | Versão do registro                                |
| `status`         | sim         | string | `aberto`, `concluido`, `incorporado`, `descartado`|
| `criado-em`      | sim         | date   | Data de criação. Formato: `YYYY-MM-DD`            |
| `atualizado-em`  | sim         | date   | Data da última atualização                        |
| `autor`          | sim         | string | Identificador do autor                            |
| `tags`           | não         | list   | Lista de tags livres                              |

---

## Conteúdo

| Campo           | Obrigatório | Tipo   | Descrição                                                    |
|-----------------|-------------|--------|--------------------------------------------------------------|
| `hipotese`      | sim         | text   | Pergunta ou hipótese que motiva o experimento                |
| `objetivo`      | sim         | text   | O que se quer aprender ou validar                            |
| `receita-base`  | não         | string | ID da Receita usada como ponto de partida. Ex: `REC-000001`  |
| `variaveis`     | não         | list   | Variáveis sendo testadas (ingrediente, técnica, temperatura) |
| `execucoes`     | não         | list   | IDs das Execuções vinculadas a este experimento              |
| `conclusao`     | não         | text   | Resultado do experimento após análise                        |
| `notas`         | não         | text   | Notas livres                                                 |

---

## Regras

- `hipotese` e `objetivo` são obrigatórios — definem o propósito do experimento.
- Um experimento pode referenciar múltiplas execuções para comparação.
- `status: incorporado` indica que a conclusão foi absorvida em uma receita ou técnica.
- `status: descartado` indica hipótese refutada — o registro é preservado para rastreabilidade.
- `id` é atribuído na criação e nunca muda.
