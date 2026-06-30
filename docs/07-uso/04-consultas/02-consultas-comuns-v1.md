# Consultas Comuns

> Queries prontas para copiar e usar.

---

## Listagens

```sql
-- Todas as receitas não arquivadas
SELECT id, titulo, status FROM receitas
WHERE status != 'arquivada' ORDER BY titulo;

-- Todos os ingredientes ativos
SELECT id, nome, tipo_ingrediente FROM ingredientes
WHERE status = 'ativo' ORDER BY nome;

-- Todas as técnicas
SELECT id, nome FROM tecnicas ORDER BY nome;

-- Receitas por status
SELECT status, COUNT(*) AS total FROM receitas GROUP BY status;
```

---

## Buscas por Nome

```sql
-- Ingrediente por nome aproximado
SELECT id, nome FROM ingredientes WHERE nome LIKE '%leite%';

-- Receita por título
SELECT id, titulo, status FROM receitas WHERE titulo LIKE '%doce%';

-- Técnica por nome
SELECT id, nome FROM tecnicas WHERE nome LIKE '%redu%';
```

---

## Joins e Relacionamentos

```sql
-- Ingredientes de uma receita específica
SELECT i.id, i.nome
FROM ingredientes i
JOIN receita_ingrediente ri ON ri.ingrediente_id = i.id
WHERE ri.receita_id = 'REC-000001';

-- Técnicas de uma receita
SELECT t.id, t.nome
FROM tecnicas t
JOIN receita_tecnica rt ON rt.tecnica_id = t.id
WHERE rt.receita_id = 'REC-000001';

-- Receitas que usam um ingrediente
SELECT r.id, r.titulo
FROM receitas r
JOIN receita_ingrediente ri ON ri.receita_id = r.id
WHERE ri.ingrediente_id = 'ING-000001';
```

---

## Análise

```sql
-- Ingredientes mais usados
SELECT i.nome, COUNT(ri.receita_id) AS total
FROM ingredientes i
LEFT JOIN receita_ingrediente ri ON ri.ingrediente_id = i.id
GROUP BY i.id ORDER BY total DESC;

-- Receitas sem execução registrada
SELECT r.id, r.titulo FROM receitas r
LEFT JOIN execucoes e ON e.receita_id = r.id
WHERE e.id IS NULL;

-- Ingredientes nunca usados em receitas
SELECT i.id, i.nome FROM ingredientes i
LEFT JOIN receita_ingrediente ri ON ri.ingrediente_id = i.id
WHERE ri.receita_id IS NULL;
```

---

## Execuções

```sql
-- Todas as execuções de uma receita
SELECT id, data_execucao, status FROM execucoes
WHERE receita_id = 'REC-000001' ORDER BY data_execucao;

-- Execuções recentes (30 dias)
SELECT e.id, r.titulo, e.data_execucao
FROM execucoes e JOIN receitas r ON r.id = e.receita_id
WHERE e.data_execucao >= date('now', '-30 days')
ORDER BY e.data_execucao DESC;
```

---

## Exportação

```bash
# Exportar receitas para CSV
sqlite3 -csv -header banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas;" \
  > exports/receitas-$(date +%Y%m%d).csv
```

---

## Próxima leitura

- Consultas de relacionamentos complexos (2+ graus) → [`03-navegacao-no-grafo-v1.md`](03-navegacao-no-grafo-v1.md)
- Exemplos completos com output → [`04-exemplos-v1.md`](04-exemplos-v1.md)
