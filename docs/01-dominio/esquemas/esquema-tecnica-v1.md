# Esquema: Técnica v1

Define os campos da entidade Técnica, sua obrigatoriedade e tipos válidos.

---

## Metadados

| Campo            | Obrigatório | Tipo   | Descrição                                        |
|------------------|-------------|--------|--------------------------------------------------|
| `id`             | sim         | string | Identificador permanente. Formato: `TEC-NNNNNN`  |
| `tipo`           | sim         | string | Valor fixo: `tecnica`                            |
| `schema-version` | sim         | string | Versão deste esquema. Valor: `1`                 |
| `versao`         | sim         | string | Versão do registro                               |
| `status`         | sim         | string | `ativo`, `descontinuado`, `arquivado`            |
| `criado-em`      | sim         | date   | Data de criação. Formato: `YYYY-MM-DD`           |
| `atualizado-em`  | sim         | date   | Data da última atualização                       |
| `autor`          | sim         | string | Identificador do autor                           |
| `origem`         | não         | string | Fonte ou referência do conhecimento              |
| `tags`           | não         | list   | Lista de tags livres                             |

---

## Conteúdo

| Campo            | Obrigatório | Tipo   | Descrição                                       |
|------------------|-------------|--------|-------------------------------------------------|
| `nome`           | sim         | string | Nome da técnica                                 |
| `tipo`           | sim         | string | Código de `tipos-tecnicas.md`                   |
| `categorias`     | não         | list   | Lista de códigos de `categorias.md`             |
| `descricao`      | sim         | text   | Descrição do procedimento                       |
| `equipamentos`   | não         | list   | IDs de Equipamentos normalmente utilizados      |
| `notas`          | não         | text   | Notas livres                                    |

---

## Regras

- `id` é atribuído na criação e nunca muda.
- `nome` pode mudar; o `id` permanece.
- Referências em `equipamentos` usam IDs, nunca nomes.
