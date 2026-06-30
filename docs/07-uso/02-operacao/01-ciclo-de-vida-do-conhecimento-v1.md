# Ciclo de Vida do Conhecimento

> O fluxo completo desde uma ideia até o conhecimento consolidado no sistema.

---

## Fluxograma Geral

```
┌─────────────────────────────────────────────────────────────┐
│                        IDEIA                                │
│              "Quero registrar uma receita"                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      PESQUISAR                              │
│   Isso já existe? As dependências existem?                  │
└──────────┬────────────────────────────────┬─────────────────┘
           │ NÃO                            │ SIM
           ▼                                ▼
┌──────────────────────┐       ┌────────────────────────────┐
│   CRIAR entidades    │       │   REUTILIZAR IDs existentes│
│   faltantes          │       │   (ING, TEC, EQP)          │
└──────────┬───────────┘       └────────────┬───────────────┘
           └──────────────┬─────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   ESCREVER o arquivo .md                    │
│   Frontmatter + conteúdo + relacionamentos por ID           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     PARSEAR                                 │
│   Parser lê o .md e constrói o KnowledgeGraph               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     RESOLVER                                │
│   Resolver verifica se todos os IDs referenciados existem   │
│                   ┌─────────────┐                           │
│   Referência ok? ─┤  SIM  │ NÃO├─ Corrigir e voltar        │
└──────────────────────┴─────────────────────────────────────┘
                           │ SIM
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     VALIDAR                                 │
│   Validador verifica consistência semântica (ciclos etc.)   │
└──────────────────────────┬──────────────────────────────────┘
                           │ OK
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     IMPORTAR                                │
│   Importador persiste o KnowledgeGraph no SQLite            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     AUDITAR (FAA)                           │
│   Auditoria verifica integridade sistêmica global           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     COMMITAR                                │
│   git commit — snapshot permanente do conhecimento          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     CONSULTAR                               │
│   SQLite, grafo, arquivos Markdown                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Ciclos de Vida por Entidade

Cada entidade tem seus próprios estados válidos:

### Receita (REC)
```
rascunho → testada → refinada
         ↘                   ↘
                              arquivada
```

### Execução (EXE)
```
em-andamento → concluida → consolidada
```

### Experimento (EXP)
```
aberto → concluido → incorporado
                  → descartado
```

### Ingrediente / Técnica / Equipamento / Observação
```
ativo → arquivado
```

---

## Quando Criar vs. Quando Reutilizar

| Situação | Ação |
|----------|------|
| Ingrediente já existe com mesmo conceito | Reutilizar o ID existente |
| Ingrediente com nome parecido mas conceito diferente | Criar novo ING |
| Técnica que já está documentada | Reutilizar o ID |
| Variação de técnica com diferenças críticas | Criar nova TEC com referência à original |
| Segundo preparo da mesma receita | Criar nova EXE (não nova REC) |
| Receita reformulada significativamente | Criar nova versão formal (`-v2`) |
| Correção de erro em receita existente | Editar arquivo existente e re-importar |

---

## O que nunca pode acontecer

- ✗ Criar dois ING com o mesmo conceito (duplicata)
- ✗ Editar o SQLite diretamente
- ✗ Mudar o `id` de uma entidade após criação
- ✗ Referenciar entidades por nome em vez de ID
- ✗ Deletar um arquivo de `dados/` (arquivar, nunca deletar)
- ✗ Commitar o banco SQLite

---

## Por que o ciclo tem esta forma

O loop `Markdown → pipeline → SQLite → consulta → novo conhecimento → Markdown` não é arbitrário. Cada parte tem uma razão:

- **Markdown como fonte**: independente de tecnologia, versionável, legível por humanos sem nenhum software
- **Pipeline obrigatório**: garante que o banco reflete exatamente a fonte — não há divergência possível
- **SQLite como índice derivado**: consultas rápidas sem comprometer a durabilidade da fonte
- **Git como memória**: o histórico de como o conhecimento evoluiu vale tanto quanto o estado atual

---

## Próxima leitura

- Criar a primeira entidade → [`02-criando-entidades-v1.md`](02-criando-entidades-v1.md)
- Tutorial completo de uma sessão → [`../05-fluxos/07-fluxo-completo-v1.md`](../05-fluxos/07-fluxo-completo-v1.md)
