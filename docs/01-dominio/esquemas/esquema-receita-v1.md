# Esquema: Receita v1

Define os campos da entidade Receita, sua obrigatoriedade e tipos válidos.

---

## Metadados

| Campo            | Obrigatório | Tipo     | Descrição                                      |
|------------------|-------------|----------|------------------------------------------------|
| `id`             | sim         | string   | Identificador permanente. Formato: `REC-NNNNNN` |
| `tipo`           | sim         | string   | Valor fixo: `receita`                          |
| `schema-version` | sim         | string   | Versão deste esquema. Valor: `1`               |
| `versao`         | sim         | string   | Versão do registro. Ex: `1`, `2`               |
| `status`         | sim         | string   | Ver `estados-receita.md`                       |
| `criado-em`      | sim         | date     | Data de criação. Formato: `YYYY-MM-DD`         |
| `atualizado-em`  | sim         | date     | Data da última atualização                     |
| `autor`          | sim         | string   | Identificador do autor                         |
| `origem`         | não         | string   | Fonte ou inspiração do conhecimento            |
| `tags`           | não         | list     | Lista de tags livres                           |

---

## Conteúdo

| Campo              | Obrigatório | Tipo     | Descrição                                           |
|--------------------|-------------|----------|-----------------------------------------------------|
| `titulo`           | sim         | string   | Nome da receita                                     |
| `descricao`        | não         | string   | Descrição resumida                                  |
| `categorias`       | não         | list     | Lista de códigos de `categorias.md`                 |
| `rendimento`       | não         | string   | Quantidade produzida. Ex: `500g`, `12 unidades`     |
| `tempo-preparo`    | não         | string   | Tempo estimado de preparo                           |
| `tempo-cozimento`  | não         | string   | Tempo estimado de cozimento                         |
| `dificuldade`      | não         | string   | `baixa`, `media`, `alta`                            |
| `ingredientes`     | sim         | list     | Lista de referências a IDs de Ingredientes          |
| `tecnicas`         | não         | list     | Lista de referências a IDs de Técnicas              |
| `equipamentos`     | não         | list     | Lista de referências a IDs de Equipamentos          |
| `modo-de-preparo`  | sim         | text     | Descrição do processo de preparo                    |
| `notas`            | não         | text     | Observações livres sobre a receita                  |

---

## Regras

- `id` é atribuído na criação e nunca muda.
- `schema-version` identifica este esquema. Mudanças estruturais geram nova versão do esquema.
- `versao` incrementa a cada alteração relevante no conteúdo.
- Referências em `ingredientes`, `tecnicas` e `equipamentos` usam IDs, nunca nomes.
