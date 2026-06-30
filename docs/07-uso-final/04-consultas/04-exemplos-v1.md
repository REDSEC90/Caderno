# Exemplos de Consultas

> Casos de uso reais com queries completas e interpretação dos resultados.

---

## Caso 1: "O que eu já sei sobre leite?"

```bash
# Via arquivo
grep -r "leite" dados/ --include="*.md" -l

# Via banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db << 'SQL'
  -- O ingrediente
  SELECT id, nome, descricao FROM ingredientes WHERE nome LIKE '%leite%';

  -- Receitas que usam leite
  SELECT r.id, r.titulo FROM receitas r
  JOIN receita_ingrediente ri ON ri.receita_id = r.id
  JOIN ingredientes i ON i.id = ri.ingrediente_id
  WHERE i.nome LIKE '%leite%';

  -- Observações sobre leite
  SELECT obs.id, obs.relevancia FROM observacoes obs
  JOIN ingredientes i ON i.id = obs.entidade_id
  WHERE i.nome LIKE '%leite%';
SQL
```

---

## Caso 2: "Que receitas posso fazer com o que já tenho?"

Suponha que você tem: Leite Integral, Açúcar, Sal, Bicarbonato.

```sql
-- Receitas cujos ingredientes são um subconjunto dos que você tem
SELECT r.id, r.titulo,
       COUNT(ri.ingrediente_id) AS total_ing,
       SUM(CASE WHEN ri.ingrediente_id IN ('ING-000001','ING-000002','ING-000003','ING-000004')
                THEN 1 ELSE 0 END) AS ing_disponiveis
FROM receitas r
JOIN receita_ingrediente ri ON ri.receita_id = r.id
WHERE r.status != 'arquivada'
GROUP BY r.id
HAVING total_ing = ing_disponiveis;
```

---

## Caso 3: "Qual receita evoluiu mais?"

```sql
SELECT r.id, r.titulo,
       COUNT(e.id) AS total_execucoes,
       MAX(e.data_execucao) AS ultima_execucao
FROM receitas r
JOIN execucoes e ON e.receita_id = r.id
GROUP BY r.id
ORDER BY total_execucoes DESC;
```

---

## Caso 4: "O que aprendi nos últimos 30 dias?"

```sql
SELECT obs.id, obs.relevancia, obs.entidade_id, obs.criado_em
FROM observacoes obs
WHERE obs.criado_em >= date('now', '-30 days')
  AND obs.status = 'ativo'
ORDER BY obs.relevancia DESC, obs.criado_em DESC;
```

---

## Caso 5: "Qual a saúde atual do sistema?"

```bash
# Score e decisão
python3 scripts/auditoria/auditor-v1.py state

# Problemas críticos
python3 scripts/auditoria/auditor-v1.py issues --critical

# Entidades sem execução
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo FROM vw_receitas_ativas WHERE total_execucoes = 0;"
```
