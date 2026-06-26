# Entidades — Modelo ER

Modelo entidade-relacionamento do SOE-CCG, preparatório para o SQLite.

---

## Diagrama

```
┌─────────────┐       ┌─────────────────┐
│   Receita   │──1:N──│    Execução     │
└──────┬──────┘       └────────┬────────┘
       │                       │
       │ N:N                   │ 1:N
       ▼                       ▼
┌─────────────┐       ┌─────────────────┐
│ Ingrediente │       │   Observação    │
└─────────────┘       └─────────────────┘
       
┌─────────────┐
│   Técnica   │◄──N:N──┤  Receita
└─────────────┘
       
┌─────────────┐
│ Equipamento │◄──N:N──┤  Receita
└─────────────┘
       
┌─────────────┐       ┌─────────────────┐
│ Experimento │──N:N──│    Receita      │
└──────┬──────┘       └─────────────────┘
       │ 1:N
       ▼
┌─────────────────┐
│   Observação    │
└─────────────────┘

┌─────────────┐
│  Categoria  │◄──N:N──┤  Receita, Ingrediente, Técnica, Equipamento
└─────────────┘
```

---

## Tabelas Principais

| Tabela          | Chave primária |
|-----------------|----------------|
| `receitas`      | `id` (REC-NNNNNN) |
| `execucoes`     | `id` (EXE-NNNNNN) |
| `ingredientes`  | `id` (ING-NNNNNN) |
| `tecnicas`      | `id` (TEC-NNNNNN) |
| `equipamentos`  | `id` (EQP-NNNNNN) |
| `observacoes`   | `id` (OBS-NNNNNN) |
| `experimentos`  | `id` (EXP-NNNNNN) |
| `categorias`    | `id` (CAT-NNNNNN) |

## Tabelas de Relacionamento

| Tabela                       | Relacionamento               |
|------------------------------|------------------------------|
| `receita_ingrediente`        | Receita N:N Ingrediente      |
| `receita_tecnica`            | Receita N:N Técnica          |
| `receita_equipamento`        | Receita N:N Equipamento      |
| `receita_categoria`          | Receita N:N Categoria        |
| `experimento_receita`        | Experimento N:N Receita      |
