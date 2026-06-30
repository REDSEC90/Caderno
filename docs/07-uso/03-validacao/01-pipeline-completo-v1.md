# Pipeline de Validação — Visão Geral

> Como um arquivo Markdown se transforma em dados persistidos no SQLite.

---

## O Pipeline em Cinco Etapas

```
┌──────────────┐
│  Arquivo .md │  (fonte canônica)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│    PARSER    │  Lê o .md, extrai entidade e arestas, constrói KnowledgeGraph
│  parser-v1   │
└──────┬───────┘
       │ KnowledgeGraph (em memória)
       ▼
┌──────────────┐
│   RESOLVER   │  Percorre as arestas, verifica se cada destino existe
│ resolvedor-v1│  → referências quebradas são erros
└──────┬───────┘
       │ KnowledgeGraph resolvido
       ▼
┌──────────────┐
│  VALIDADOR   │  Verifica consistência semântica: ciclos, status, regras de negócio
│ validador-v1 │
└──────┬───────┘
       │ KnowledgeGraph validado
       ▼
┌──────────────┐
│  IMPORTADOR  │  Persiste entidades e arestas no SQLite
│importador-v1 │  Nunca lê Markdown diretamente
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  SQLite DB   │  Índice derivado — pronto para consulta
└──────────────┘
```

Cada etapa pode rejeitar o input. Um arquivo que falha no Parser nunca chega ao Importador.

---

## Componentes e Responsabilidades

| Componente | Arquivo | Responsabilidade |
|------------|---------|-----------------|
| Parser | `codigo/parser-v1.py` | Ler Markdown → construir KnowledgeGraph |
| IR (Intermediate Representation) | `codigo/ir-v1.py` | Definir as estruturas: Entity, Edge, KnowledgeGraph |
| Resolver | `codigo/resolvedor-v1.py` | Verificar que referências apontam para entidades existentes |
| Validador | `codigo/validador-v1.py` | Verificar consistência semântica (ciclos, estados) |
| Importador | `codigo/importador-v1.py` | Persistir no SQLite |
| FAA | `scripts/auditoria/auditor-v1.py` | Auditoria sistêmica do repositório inteiro |

---

## Separação de Responsabilidades

**O Parser** não verifica se as referências existem — apenas extrai o que está no arquivo.

**O Resolver** não verifica consistência semântica — apenas confirma que cada ID referenciado tem uma entidade correspondente.

**O Validador** não persiste nada — apenas verifica regras.

**O Importador** nunca lê Markdown — recebe apenas o grafo já resolvido.

Essa separação permite tratar cada tipo de erro na camada correta, sem misturar responsabilidades.

---

## Documentos Detalhados por Componente

- [02-parser.md](02-parser.md) — como o Parser funciona, o que ele extrai
- [03-resolver.md](03-resolver.md) — como o Resolver verifica referências
- [04-validador.md](04-validador.md) — regras de validação semântica
- [05-faa.md](05-faa.md) — Framework de Auditoria Arquitetural completo
- [06-importador.md](06-importador.md) — como o Importador persiste no SQLite
- [07-resolucao-de-erros.md](07-resolucao-de-erros.md) — catálogo de erros e soluções

---

## Por que o pipeline tem cinco etapas separadas

Cada etapa tem uma responsabilidade única e pode falhar de forma independente. Isso significa:
- Um erro no Parser não contamina a lógica do Resolver
- Erros de referência (Resolver) são distintos de erros de consistência (Validador)
- O banco (Importador) recebe apenas grafos que passaram por todas as verificações

Qualquer implementação alternativa que misturasse responsabilidades tornaria impossível distinguir onde um erro ocorreu — e dificultaria enormemente o diagnóstico.

---

## Executando o pipeline completo

```bash
python3 -m codigo
```

```
# Resultado esperado:
[PARSER]    13 arquivos processados
[RESOLVER]  0 referências quebradas
[VALIDADOR] 0 issues
[IMPORTADOR] 13 entidades importadas
```

Se qualquer etapa falhar, a pipeline para naquele ponto e reporta o erro. Corrigir o problema e executar novamente.

---

## Próxima leitura

- Cada componente em detalhe → [`02-parser-v1.md`](02-parser-v1.md) → [`03-resolver-v1.md`](03-resolver-v1.md) → [`04-validador-v1.md`](04-validador-v1.md) → [`05-faa-v1.md`](05-faa-v1.md)
- Quando algo deu errado → [`../09-troubleshooting/README-v1.md`](../09-troubleshooting/README-v1.md)
