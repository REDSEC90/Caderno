# Esquema: Ingrediente v1

Define os campos da entidade Ingrediente, sua obrigatoriedade e tipos válidos.

---

## Metadados

| Campo            | Obrigatório | Tipo   | Descrição                                        |
|------------------|-------------|--------|--------------------------------------------------|
| `id`             | sim         | string | Identificador permanente. Formato: `ING-NNNNNN`  |
| `tipo`           | sim         | string | Valor fixo: `ingrediente`                        |
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

| Campo             | Obrigatório | Tipo   | Descrição                                         |
|-------------------|-------------|--------|---------------------------------------------------|
| `nome`            | sim         | string | Nome do ingrediente                               |
| `nome-cientifico` | não         | string | Nome científico quando aplicável                  |
| `tipo`            | sim         | string | Código de `tipos-ingredientes.md`                 |
| `categorias`      | não         | list   | Lista de códigos de `categorias.md`               |
| `unidade-padrao`  | sim         | string | Código de unidade padrão de `unidades-medida.md`  |
| `descricao`       | não         | text   | Descrição e características do ingrediente        |
| `notas`           | não         | text   | Notas livres                                      |

---

## Regras

- `id` é atribuído na criação e nunca muda.
- `nome` pode mudar; o `id` permanece.
- `unidade-padrao` é a unidade de referência nas receitas; outras unidades podem ser usadas com conversão explícita.
