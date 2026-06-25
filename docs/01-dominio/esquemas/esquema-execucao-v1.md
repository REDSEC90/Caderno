# Esquema: Execução v1

Define os campos da entidade Execução, sua obrigatoriedade e tipos válidos.

---

## Metadados

| Campo            | Obrigatório | Tipo   | Descrição                                        |
|------------------|-------------|--------|--------------------------------------------------|
| `id`             | sim         | string | Identificador permanente. Formato: `EXE-NNNNNN`  |
| `tipo`           | sim         | string | Valor fixo: `execucao`                           |
| `schema-version` | sim         | string | Versão deste esquema. Valor: `1`                 |
| `versao`         | sim         | string | Versão do registro                               |
| `status`         | sim         | string | `registrada`, `revisada`, `consolidada`          |
| `criado-em`      | sim         | date   | Data de criação. Formato: `YYYY-MM-DD`           |
| `atualizado-em`  | sim         | date   | Data da última atualização                       |
| `autor`          | sim         | string | Identificador do autor                           |
| `tags`           | não         | list   | Lista de tags livres                             |

---

## Conteúdo

| Campo             | Obrigatório | Tipo   | Descrição                                              |
|-------------------|-------------|--------|--------------------------------------------------------|
| `receita-id`      | sim         | string | ID da Receita executada. Ex: `REC-000001`              |
| `receita-versao`  | sim         | string | Versão da receita utilizada nesta execução             |
| `data-execucao`   | sim         | date   | Data em que o preparo ocorreu                          |
| `resultado`       | não         | string | `otimo`, `bom`, `regular`, `ruim`                      |
| `avaliacao`       | não         | text   | Descrição qualitativa do resultado                     |
| `variações`       | não         | text   | Alterações feitas em relação à receita original        |
| `metricas`        | não         | list   | Medições realizadas durante o preparo                  |
| `observacoes`     | não         | list   | IDs de Observações vinculadas a esta execução          |
| `notas`           | não         | text   | Notas livres                                           |

---

## Regras

- Toda execução deve referenciar uma receita existente via `receita-id`.
- `receita-versao` registra qual versão da receita foi usada, preservando rastreabilidade.
- Execução nunca altera a receita vinculada.
- `id` é atribuído na criação e nunca muda.
