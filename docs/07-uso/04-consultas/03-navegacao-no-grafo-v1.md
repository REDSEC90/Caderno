# Navegação no Grafo de Conhecimento

> Como navegar pelas relações entre entidades — além de queries SQL simples.

---

## O que é navegar no grafo

Navegar no grafo significa seguir arestas entre entidades para descobrir conhecimento indiretamente conectado. Não é apenas "buscar um ingrediente" — é responder perguntas como:

- "Que outras receitas usam os mesmos ingredientes que REC-000001?"
- "Quais observações existem sobre ingredientes usados em receitas que já executei?"
- "Se eu arquivar ING-000001, quantas receitas ficam com referência quebrada?"

---

## Via SQLite: Relações Diretas

```sql
-- Todos os dependentes de um ingrediente
SELECT r.id, r.titulo
FROM receitas r
JOIN receita_ingrediente ri ON ri.receita_id = r.id
WHERE ri.ingrediente_id = 'ING-000001';

-- Todas as observações sobre entidades usadas em uma receita
SELECT obs.id, obs.entidade_id, obs.relevancia
FROM observacoes obs
WHERE obs.entidade_id IN (
  SELECT ingrediente_id FROM receita_ingrediente WHERE receita_id = 'REC-000001'
  UNION
  SELECT tecnica_id    FROM receita_tecnica    WHERE receita_id = 'REC-000001'
);
```

---

## Via SQLite: Relações Indiretas (2 Graus)

```sql
-- Receitas que compartilham ingredientes com REC-000001 (receitas "irmãs")
SELECT DISTINCT r2.id, r2.titulo
FROM receita_ingrediente ri1
JOIN receita_ingrediente ri2 ON ri2.ingrediente_id = ri1.ingrediente_id
JOIN receitas r2 ON r2.id = ri2.receita_id
WHERE ri1.receita_id = 'REC-000001'
  AND ri2.receita_id != 'REC-000001';

-- Execuções de todas as receitas que usam uma técnica específica
SELECT e.id, e.data_execucao, r.titulo
FROM execucoes e
JOIN receitas r ON r.id = e.receita_id
JOIN receita_tecnica rt ON rt.receita_id = r.id
WHERE rt.tecnica_id = 'TEC-000001'
ORDER BY e.data_execucao DESC;
```

---

## Via Auditor: Inspeção do Grafo em Memória

O auditor carrega o grafo completo e permite inspecionar arestas reais (incluindo INFORMATIONAL que podem não estar na tabela SQL):

```bash
# Ver todas as arestas de uma entidade (outgoing e incoming)
python3 scripts/auditoria/auditor-v1.py entity REC-000001

# Ver o grafo completo em JSON
python3 scripts/auditoria/auditor-v1.py state --json | python3 -m json.tool

# Ver todas as issues no grafo
python3 scripts/auditoria/auditor-v1.py issues
```

---

## Análise de Impacto (antes de arquivar/remover)

```sql
-- Impacto de arquivar ING-000001: quantas receitas são afetadas?
SELECT COUNT(DISTINCT receita_id) AS receitas_afetadas
FROM receita_ingrediente
WHERE ingrediente_id = 'ING-000001';

-- Quais receitas especificamente?
SELECT r.id, r.titulo, r.status
FROM receitas r
JOIN receita_ingrediente ri ON ri.receita_id = r.id
WHERE ri.ingrediente_id = 'ING-000001'
ORDER BY r.status;

-- Impacto de arquivar TEC-000001
SELECT COUNT(DISTINCT receita_id) AS receitas_afetadas
FROM receita_tecnica WHERE tecnica_id = 'TEC-000001';
```

---

## Views Pré-construídas (Schema SQLite)

O schema define views úteis que podem ser usadas diretamente:

```sql
-- Receitas ativas com contagem de execuções
SELECT * FROM vw_receitas_ativas ORDER BY total_execucoes DESC;

-- Ingredientes mais usados em receitas e execuções
SELECT * FROM vw_ingredientes_uso ORDER BY total_receitas DESC;
```

---

## Histórico de Estados

```sql
-- Ver histórico de mudanças de status de uma entidade
SELECT estado_anterior, estado_novo, autor, registrado_em, nota
FROM historico_estados
WHERE entidade_id = 'REC-000001'
ORDER BY registrado_em;
```
