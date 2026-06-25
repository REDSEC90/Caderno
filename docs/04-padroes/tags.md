# Tags

Define a política de uso de tags no SOE-CCG.

---

## Propósito

Tags são rótulos livres para classificação transversal.

Complementam as categorias controladas sem substituí-las.

Permitem agrupamentos ad hoc que não justificam uma categoria formal.

---

## Formato

Minúsculas, sem acentos, com hífens. Sem espaços.

```
sem-gluten
alta-precisao
confeitaria-francesa
longa-duracao
fermentacao-natural
```

---

## Uso no Frontmatter

```yaml
tags: [sem-gluten, alta-precisao, fermentacao-natural]
```

ou

```yaml
tags:
  - sem-gluten
  - alta-precisao
  - fermentacao-natural
```

---

## Diferença entre Tag e Categoria

| Aspecto        | Categoria                        | Tag                          |
|----------------|----------------------------------|------------------------------|
| Controle       | Catálogo controlado              | Livre                        |
| Localização    | `catalogos/categorias.md`        | Frontmatter do registro      |
| Uso            | Agrupamento semântico formal     | Classificação transversal    |
| Tabela SQLite  | Sim                              | Tabela auxiliar ou texto     |

---

## Regras

- Tags não substituem categorias.
- Não há catálogo obrigatório de tags, mas consistência é recomendada.
- Uma tag que se torna recorrente e relevante pode ser promovida a categoria.
- Tags obsoletas são simplesmente descontinuadas nos novos registros.
