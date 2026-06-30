# Referência: Relacionamentos (Arestas)

---

## Tipos de Aresta (EdgeKind)

| Tipo | Semântica | Origem Típica | Ciclo = Erro? |
|------|-----------|---------------|---------------|
| `STRUCTURAL` | Dependência estrutural — destino necessário para origem existir | Frontmatter (campo simples) | **Sim** |
| `COMPOSITIONAL` | Composição — origem é composta de destinos | Frontmatter (`ingredientes`, `tecnicas`, `equipamentos`) e tabelas no corpo | **Sim** |
| `HIERARCHICAL` | Hierarquia pai/filho | Frontmatter (campos de hierarquia) | **Sim** |
| `DERIVATION` | Derivação — origem foi criada a partir do destino | Frontmatter (`receita-base-id`) | Não |
| `INFORMATIONAL` | Menção contextual — referência no corpo do texto | Corpo do documento (fora de tabelas) | **Não** |
| `OPTIONAL` | Referência opcional — ausência não é erro | Frontmatter (campos opcionais) | Não |

---

## Origem das Arestas (EdgeOrigin)

| Origem | Onde | Exemplo |
|--------|------|---------|
| `FRONTMATTER` | Campo YAML entre `---` | `ingredientes: [ING-000001]` |
| `BODY` | Corpo do documento Markdown | `"Ver ING-000004 para detalhes"` |
| `GENERATED` | Gerada automaticamente pelo sistema | — |

---

## Tabelas de Relacionamento no SQLite

| Tabela | Conecta |
|--------|---------|
| `receita_ingrediente` | REC → ING |
| `receita_tecnica` | REC → TEC |
| `receita_equipamento` | REC → EQP |
| `execucao_ingrediente` | EXE → ING |
| `execucao_tecnica` | EXE → TEC |
| `execucao_equipamento` | EXE → EQP |
| `experimento_receita` | EXP → REC |
| `relacionamentos` | Grafo geral (todas as arestas tipadas) |

---

## Regras de Ciclo

- Ciclos em `STRUCTURAL | COMPOSITIONAL | HIERARCHICAL | DERIVATION` → **CRÍTICO** — corrigir obrigatoriamente
- Ciclos em `INFORMATIONAL | OPTIONAL` → **INFO** — semanticamente válido, não requer ação
