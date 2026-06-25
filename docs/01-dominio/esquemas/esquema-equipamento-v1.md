# Esquema: Equipamento v1

Define os campos da entidade Equipamento, sua obrigatoriedade e tipos válidos.

---

## Metadados

| Campo            | Obrigatório | Tipo   | Descrição                                        |
|------------------|-------------|--------|--------------------------------------------------|
| `id`             | sim         | string | Identificador permanente. Formato: `EQP-NNNNNN`  |
| `tipo`           | sim         | string | Valor fixo: `equipamento`                        |
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

| Campo        | Obrigatório | Tipo   | Descrição                                   |
|--------------|-------------|--------|---------------------------------------------|
| `nome`       | sim         | string | Nome do equipamento                         |
| `tipo`       | sim         | string | Código de `tipos-equipamentos.md`           |
| `categorias` | não         | list   | Lista de códigos de `categorias.md`         |
| `descricao`  | não         | text   | Descrição e características do equipamento  |
| `notas`      | não         | text   | Notas livres                                |

---

## Regras

- `id` é atribuído na criação e nunca muda.
- `nome` pode mudar; o `id` permanece.
