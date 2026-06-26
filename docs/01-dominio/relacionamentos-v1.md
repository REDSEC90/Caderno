# Relacionamentos do SOE-CCG

Relacionamentos entre entidades são sempre expressos por identificadores permanentes, nunca por nomes.

---

## Mapa de Relacionamentos

```
Receita ──────────────── possui ──────────────── Execução (1:N)
Receita ──────────────── referencia ──────────── Ingrediente (N:N)
Receita ──────────────── referencia ──────────── Técnica (N:N)
Receita ──────────────── referencia ──────────── Equipamento (N:N)
Receita ──────────────── pertence a ─────────── Categoria (N:N)

Execução ─────────────── pertence a ─────────── Receita (N:1)
Execução ─────────────── contém ─────────────── Observação (1:N)

Experimento ──────────── pode originar ──────── Receita (N:N)
Experimento ──────────── contém ─────────────── Observação (1:N)

Observação ───────────── vinculada a ────────── qualquer entidade (N:1)

Ingrediente ──────────── pertence a ─────────── Categoria (N:N)
Técnica ──────────────── pertence a ─────────── Categoria (N:N)
Equipamento ──────────── pertence a ─────────── Categoria (N:N)
```

---

## Regras

- Todo relacionamento referencia o ID da entidade, nunca seu nome.
- O nome pode mudar. O ID nunca muda.
- Relacionamentos são unidirecionais na definição, mas consultáveis nos dois sentidos.
- A exclusão de uma entidade nunca destrói os registros que a referenciam.
