# Metadados

Define o conjunto padronizado de metadados presente em todo registro do SOE-CCG.

---

## Campos Obrigatórios

| Campo            | Tipo   | Descrição                                              |
|------------------|--------|--------------------------------------------------------|
| `id`             | string | Identificador permanente. Ex: `REC-000001`             |
| `tipo`           | string | Tipo da entidade. Ex: `receita`, `ingrediente`         |
| `schema-version` | string | Versão do esquema utilizado na criação                 |
| `versao`         | string | Versão do registro. Começa em `1`                      |
| `status`         | string | Estado no ciclo de vida. Ver esquema da entidade       |
| `criado-em`      | date   | Data de criação. Formato: `YYYY-MM-DD`                 |
| `atualizado-em`  | date   | Data da última atualização. Formato: `YYYY-MM-DD`      |
| `autor`          | string | Identificador do autor do registro                     |

## Campos Opcionais

| Campo    | Tipo   | Descrição                                              |
|----------|--------|--------------------------------------------------------|
| `origem` | string | Fonte, inspiração ou referência do conhecimento        |
| `tags`   | list   | Lista de tags livres para classificação transversal    |

---

## Formato no Arquivo

Os metadados são declarados como frontmatter YAML no início de cada arquivo Markdown.

```yaml
---
id: REC-000001
tipo: receita
schema-version: 1
versao: 1
status: rascunho
criado-em: 2026-06-25
atualizado-em: 2026-06-25
autor: autor
origem: 
tags: []
---
```

---

## Regras

- O frontmatter deve ser o primeiro bloco do arquivo, sem linhas anteriores.
- `id` nunca muda após a criação.
- `atualizado-em` deve ser atualizado a cada alteração relevante.
- `tags` usa lista YAML: `[tag-a, tag-b]` ou bloco multiline.
- Campos opcionais ausentes devem ser declarados vazios, não omitidos.
