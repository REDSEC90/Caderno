# Esquema: Observação v1

Define os campos da entidade Observação, sua obrigatoriedade e tipos válidos.

---

## Metadados

| Campo            | Obrigatório | Tipo   | Descrição                                        |
|------------------|-------------|--------|--------------------------------------------------|
| `id`             | sim         | string | Identificador permanente. Formato: `OBS-NNNNNN`  |
| `tipo`           | sim         | string | Valor fixo: `observacao`                         |
| `schema-version` | sim         | string | Versão deste esquema. Valor: `1`                 |
| `versao`         | sim         | string | Versão do registro                               |
| `criado-em`      | sim         | date   | Data de criação. Formato: `YYYY-MM-DD`           |
| `atualizado-em`  | sim         | date   | Data da última atualização                       |
| `autor`          | sim         | string | Identificador do autor                           |
| `tags`           | não         | list   | Lista de tags livres                             |

---

## Conteúdo

| Campo          | Obrigatório | Tipo   | Descrição                                                  |
|----------------|-------------|--------|------------------------------------------------------------|
| `entidade-id`  | sim         | string | ID da entidade à qual esta observação está vinculada       |
| `entidade-tipo`| sim         | string | Tipo da entidade: `receita`, `execucao`, `experimento` etc.|
| `conteudo`     | sim         | text   | Texto da observação                                        |
| `notas`        | não         | text   | Notas livres                                               |

---

## Regras

- `id` é atribuído na criação e nunca muda.
- Uma observação pertence a exatamente uma entidade, identificada por `entidade-id` e `entidade-tipo`.
- Observações não são editadas; novas versões geram novo registro com referência ao anterior.
