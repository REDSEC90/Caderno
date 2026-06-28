# Validador

> Verificação de consistência semântica do grafo de conhecimento.

---

## O que o Validador faz

O Validador (`codigo/validador-v1.py`) recebe um `KnowledgeGraph` já resolvido e verifica **consistência semântica** — regras que o Resolver não pode checar (ele só verifica existência de referências).

O Validador detecta:
1. **Ciclos em arestas críticas** (`STRUCTURAL`, `COMPOSITIONAL`, `HIERARCHICAL`, `DERIVATION`) — severidade `CRÍTICO`
2. **Ciclos em arestas informacionais** (`INFORMATIONAL`, `OPTIONAL`) — severidade `INFO` (semanticamente válido)
3. **Entidades isoladas** de tipos que sempre devem ter relações (`REC`, `EXE`, `EXP`) — severidade `AVISO`

---

## Arestas Críticas vs. Informacionais

| Categoria | EdgeKinds | Ciclo = ? |
|-----------|-----------|-----------|
| Crítica | STRUCTURAL, COMPOSITIONAL, HIERARCHICAL, DERIVATION | **Erro** — dependência impossível de resolver |
| Informacional | INFORMATIONAL, OPTIONAL | **Válido** — referências cruzadas entre documentos |

Esta distinção é a base da ADR-0002. Um ciclo onde `REC-000001` menciona `OBS-000001` no corpo do texto (INFORMATIONAL), que por sua vez menciona `EXE-000001` (INFORMATIONAL), que pertence estruturalmente a `REC-000001` (STRUCTURAL) — somente a aresta STRUCTURAL importa para detecção de ciclo crítico.

---

## Saída do Validador

Lista de issues, cada uma com:
```python
{
  'entity_id':   'REC-000001',         # entidade de origem do ciclo
  'tipo_issue':  'ciclo',              # ou 'entidade_isolada'
  'severidade':  'CRITICO',            # CRITICO | AVISO | INFO
  'mensagem':    'Ciclo detectado: REC-000001 -> OBS-000001 -> REC-000001'
}
```

---

## Entidades Isoladas

Receitas, Execuções e Experimentos **sem nenhuma aresta** (nem outgoing, nem incoming) são reportados como `AVISO`. Isso indica um registro provavelmente mal-formado:

- Uma REC sem nenhum ingrediente referenciado
- Uma EXE sem vínculo com nenhuma REC
- Um EXP completamente desconectado

Ingredientes, Técnicas e Equipamentos **podem** existir sem relações — são entidades reutilizáveis que aguardam uso.

---

## Executando

O Validador é invocado automaticamente pelo pipeline de importação. Para execução manual:

```bash
python3 codigo/validador-v1.py
```

Saída esperada num sistema saudável:
```
Sem issues.
```

Saída com ciclo crítico:
```
[CRITICO] REC-000001 (ciclo): Ciclo detectado: REC-000001 -> TEC-000001 -> REC-000001
```

---

## Diagnóstico de Ciclos Críticos

Se um ciclo crítico for detectado:

```bash
# Inspecionar as arestas das entidades envolvidas
python3 scripts/auditoria/auditor-v1.py entity REC-000001
python3 scripts/auditoria/auditor-v1.py entity TEC-000001
```

Identificar qual aresta específica cria o ciclo. Geralmente é uma referência que foi colocada no frontmatter (STRUCTURAL/COMPOSITIONAL) quando deveria ser apenas uma menção no corpo (INFORMATIONAL).

**Correção:** Mover a referência problemática do frontmatter para o corpo do texto. Uma menção contextual vira aresta INFORMATIONAL — ciclo deixa de ser crítico.
