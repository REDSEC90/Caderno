# ADRs — Architectural Decision Records

> Quando escrever uma ADR, como estruturá-la e onde registrá-la.

---

## O que é uma ADR

Uma ADR registra formalmente uma decisão arquitetural: o contexto que levou à decisão, as alternativas consideradas, a decisão tomada e suas consequências. É o equivalente de "minuta de reunião de arquitetura" — preserva o raciocínio, não apenas o resultado.

ADRs existentes do SOE:
- `ADR-0001` — Motor de Conhecimento como paradigma central
- `ADR-0002` — IR com arestas tipadas (EdgeKind + EdgeOrigin)

---

## Quando Escrever uma ADR

Escreva uma ADR quando:

- Uma decisão afeta o comportamento do Parser, Resolver, Validador ou Importador
- Uma mudança altera o esquema SQLite de forma que dados existentes precisam ser migrados
- Uma nova política de sistema é estabelecida (ex: como tratar ciclos informacionais)
- Uma decisão foi difícil — havia duas ou mais alternativas genuinamente plausíveis
- Uma decisão vai contra o que alguém "esperaria" sem contexto

**Não** escreva uma ADR para:
- Adicionar uma nova entidade (REC, ING, etc.) — isso é operação normal
- Corrigir um bug óbvio
- Adicionar documentação

---

## Formato Obrigatório

```markdown
# ADR-[NNNN] — [Título Descritivo]

**Status:** Proposta | Em Revisão | Aceita | Supersedida por ADR-[NNNN]
**Data:** YYYY-MM-DD

---

## Contexto

[O problema ou situação que levou a esta decisão. Neutro — sem recomendar ainda.]

## Alternativas Consideradas

### Alternativa A — [Nome]
[Descrição. Prós. Contras.]

### Alternativa B — [Nome]
[Descrição. Prós. Contras.]

## Decisão

[A escolha feita e por quê. Explícito sobre o que foi descartado e por quê.]

## Consequências

[O que muda. O que fica mais difícil. O que fica mais fácil. Dívida técnica criada.]

## Implementação

[Como implementar. Arquivos afetados. Migração necessária, se houver.]
```

---

## Numeração e Localização

- Próxima ADR: consultar `docs/04-padroes/` e incrementar o maior número existente
- Nome do arquivo: `ADR-[NNNN]-[SLUG-DESCRITIVO]-v1.md`
- Localização: `docs/04-padroes/`
- Commit: `docs(adr): cria ADR-0003 politica-de-versionamento-de-schema`

---

## ADRs Supersedidas

Quando uma ADR é substituída por outra, atualizar o `Status` da antiga:
```markdown
**Status:** Supersedida por ADR-0005
```

A ADR antiga permanece no repositório — o histórico de raciocínio tem valor.
