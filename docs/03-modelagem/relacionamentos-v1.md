# Relacionamentos — Modelagem

Define como os relacionamentos entre entidades são implementados no SQLite.

---

## Tabelas de Relacionamento N:N

### receita_ingrediente

| Campo           | Tipo    | Descrição                          |
|-----------------|---------|------------------------------------|
| `receita_id`    | TEXT    | ID da Receita                      |
| `ingrediente_id`| TEXT    | ID do Ingrediente                  |
| `quantidade`    | REAL    | Quantidade utilizada               |
| `unidade`       | TEXT    | Código de unidade de medida        |
| `notas`         | TEXT    | Observação sobre o uso (opcional)  |

### receita_tecnica

| Campo        | Tipo | Descrição          |
|--------------|------|--------------------|
| `receita_id` | TEXT | ID da Receita      |
| `tecnica_id` | TEXT | ID da Técnica      |
| `ordem`      | INT  | Ordem de aplicação |

### receita_equipamento

| Campo           | Tipo | Descrição            |
|-----------------|------|----------------------|
| `receita_id`    | TEXT | ID da Receita        |
| `equipamento_id`| TEXT | ID do Equipamento    |

### receita_categoria

| Campo          | Tipo | Descrição          |
|----------------|------|--------------------|
| `receita_id`   | TEXT | ID da Receita      |
| `categoria_id` | TEXT | ID da Categoria    |

### experimento_receita

| Campo            | Tipo | Descrição            |
|------------------|------|----------------------|
| `experimento_id` | TEXT | ID do Experimento    |
| `receita_id`     | TEXT | ID da Receita gerada |

---

## Relacionamentos 1:N (chave estrangeira na tabela filha)

| Tabela filha   | Campo          | Referência          |
|----------------|----------------|---------------------|
| `execucoes`    | `receita_id`   | `receitas.id`       |
| `observacoes`  | `entidade_id`  | ID de qualquer entidade |

---

## Regras

- Todas as chaves estrangeiras referenciam o campo `id` da tabela correspondente.
- A exclusão de uma entidade pai não remove os registros filhos; apenas marca a referência como inativa.
- `observacoes` usa `entidade_id` + `entidade_tipo` por referenciar múltiplas tabelas.
