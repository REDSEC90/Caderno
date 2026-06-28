# Resolver (Resolvedor)

> Como o Resolver verifica que todas as referências apontam para entidades reais.

---

## O que o Resolver faz

O Resolver (`codigo/resolvedor-v1.py`) recebe um `KnowledgeGraph` e percorre todas as arestas. Para cada aresta, verifica se a entidade de destino existe no grafo.

Se existir: preenche o campo `incoming` da entidade de destino (grafo bidirecional).
Se não existir: reporta um erro `referencia_quebrada`.

---

## Erros do Resolver

| Erro | O que significa | Como corrigir |
|------|----------------|---------------|
| `referencia_quebrada` | O ID referenciado não existe no grafo | Criar a entidade faltante, ou corrigir o ID no arquivo |

### Exemplo de erro

```
{
  'source': 'REC-000002',
  'target': 'ING-000099',
  'kind': 'COMPOSITIONAL',
  'erro': 'referencia_quebrada'
}
```

Significa que `REC-000002` declara usar `ING-000099`, mas esse ingrediente não existe no sistema.

**Solução:** criar `dados/ingredientes/ING-000099-[slug]-v1.md` ou corrigir o ID na receita.

---

## Por que o Resolver é uma Etapa Separada

O Parser produz um grafo "otimista" — extrai todas as referências declaradas. O Resolver verifica a realidade — confirma que as referências declaradas são válidas.

Essa separação permite:
- Importar um conjunto de arquivos em batch e ter relatório completo de todos os quebrados
- Distinguir "erro de parse" (arquivo malformado) de "erro de referência" (arquivo válido mas com link quebrado)
