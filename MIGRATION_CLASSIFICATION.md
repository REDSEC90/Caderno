# MIGRATION_CLASSIFICATION

> Fase 2 do Roadmap de Migração Arquitetural.
>
> Cada arquivo da cópia recebe categoria, prioridade e estado arquitetural inicial.
>
> Gerado em: 2026-06-26
> Baseado em: MIGRATION_INVENTORY.md

---

## Tabela de Categorias

| Código | Nome |
|--------|------|
| CAT-PRJ | Projeto — visão, filosofia, objetivos, escopo |
| CAT-GOV | Governança — políticas, constituição, leis |
| CAT-LNG | Linguagem — glossário, vocabulário, terminologia |
| CAT-DOM | Domínio — entidades, especificações, ciclo de vida |
| CAT-CTL | Catálogos — taxonomias, tipos, estados, unidades |
| CAT-ARQ | Arquitetura — fluxos, diagramas, importação, exportação |
| CAT-MOD | Modelagem — ER, normalização, IDs, SQLite |
| CAT-PAD | Padrões — nomenclatura, metadados, tags, validação, ADRs |
| CAT-DEV | Desenvolvimento — casos de uso, convenções, guias |
| CAT-OPR | Operação — backup, manutenção, reconstrução |
| CAT-SCR | Scripts — automação, importação |
| CAT-BAN | Banco — esquemas SQL, seeds, migrações |
| CAT-DAD | Dados — registros canônicos em dados/ |
| CAT-REF | Referências — rastreamento, roadmap, validação |

---

## Tabela de Prioridades

| Código | Nome | Critério |
|--------|------|----------|
| P1 | Crítica | Bloqueia ou invalida outros documentos se ausente ou errado |
| P2 | Alta | Necessária para implementação ou coerência do sistema |
| P3 | Média | Completa o sistema, mas não bloqueia |
| P4 | Baixa | Auxiliar, exemplificativa ou operacional |

---

## Estado Arquitetural Inicial

Todos os arquivos entram como `NOT_ANALYZED`.
A progressão completa é:

```
NOT_ANALYZED → ANALYZING → PROPOSAL → REVIEW → APPROVED → MIGRATED → VERIFIED → STABLE
```

---

## Classificação Completa

### docs/00-projeto/ — 8 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 1 | `filosofia.md` | CAT-PRJ | P1 | NOT_ANALYZED | Base axiomática do sistema |
| 2 | `constituicao.md` | CAT-GOV | P1 | NOT_ANALYZED | Leis fundamentais imutáveis |
| 3 | `principios.md` | CAT-PRJ | P1 | NOT_ANALYZED | Derivações operacionais da filosofia |
| 4 | `glossario.md` | CAT-LNG | P1 | NOT_ANALYZED | Vocabulário oficial; qualquer drift cria ambiguidade |
| 5 | `objetivos.md` | CAT-PRJ | P2 | NOT_ANALYZED | — |
| 6 | `escopo.md` | CAT-PRJ | P2 | NOT_ANALYZED | — |
| 7 | `visão.md` | CAT-PRJ | P2 | NOT_ANALYZED | Anomalia A-002 na cópia (nome com escape); usar do principal |
| 8 | `roadmap-master.md` | CAT-REF | P3 | NOT_ANALYZED | Referência de planejamento |

---

### docs/01-dominio/ — 27 arquivos

#### Raiz do domínio

| # | Arquivo | Categoria | Prioridade | Estado | Excl. Cópia | Observação |
|---|---------|-----------|------------|--------|-------------|------------|
| 9 | `linguagem-soe-ccg.md` | CAT-LNG | P1 | NOT_ANALYZED | ✅ | Vocabulário oficial + termos proibidos; bloqueador da Fase 3 |
| 10 | `separacao-dominios.md` | CAT-DOM | P1 | NOT_ANALYZED | — | Principal tem versão recente (25/06); comparar |
| 11 | `template-especificacao-entidade.md` | CAT-DOM | P1 | NOT_ANALYZED | ✅ | Template canônico; precede todas as especificações |
| 12 | `template-contrato.md` | CAT-DOM | P1 | NOT_ANALYZED | ✅ | Bloqueador da Fase 5 (Contratos) |
| 13 | `mapa-relacionamentos.md` | CAT-DOM | P1 | NOT_ANALYZED | ✅ | Bloqueador da Fase 7 (Relacionamentos) |
| 14 | `especificacao-registro.md` | CAT-DOM | P1 | NOT_ANALYZED | ✅ | Entidade base de todo o sistema |
| 15 | `especificacao-receita.md` | CAT-DOM | P1 | NOT_ANALYZED | ✅ | Entidade central; maior arquivo (9,2KB) |
| 16 | `especificacao-execucao.md` | CAT-DOM | P1 | NOT_ANALYZED | ✅ | Vincula receita ao conhecimento empírico |
| 17 | `especificacao-ingrediente.md` | CAT-DOM | P2 | NOT_ANALYZED | ✅ | — |
| 18 | `especificacao-tecnica.md` | CAT-DOM | P2 | NOT_ANALYZED | ✅ | — |
| 19 | `especificacao-equipamento.md` | CAT-DOM | P2 | NOT_ANALYZED | ✅ | — |
| 20 | `especificacao-observacao.md` | CAT-DOM | P2 | NOT_ANALYZED | ✅ | — |
| 21 | `especificacao-experimento.md` | CAT-DOM | P2 | NOT_ANALYZED | ✅ | — |
| 22 | `entidades.md` | CAT-DOM | P2 | NOT_ANALYZED | — | Verificar se obsolescido pelas especificações |
| 23 | `ciclo-de-vida.md` | CAT-DOM | P2 | NOT_ANALYZED | — | Verificar se absorvido pelas especificações |
| 24 | `relacionamentos.md` | CAT-DOM | P2 | NOT_ANALYZED | — | Verificar se obsolescido por mapa-relacionamentos |
| 25 | `catalogacao.md` | CAT-DOM | P3 | NOT_ANALYZED | — | — |
| 26 | `overview.md` | CAT-DOM | P3 | NOT_ANALYZED | — | — |

#### catalogos/

| # | Arquivo | Categoria | Prioridade | Estado | Excl. Cópia | Observação |
|---|---------|-----------|------------|--------|-------------|------------|
| 27 | `estados-todas-entidades.md` | CAT-CTL | P1 | NOT_ANALYZED | ✅ | Catálogo central de estados |
| 28 | `catalogos-expandidos.md` | CAT-CTL | P2 | NOT_ANALYZED | ✅ | Escalas, materiais, métodos, vocabulário |
| 29 | `estados-receita.md` | CAT-CTL | P2 | NOT_ANALYZED | — | Verificar redundância com estados-todas-entidades |
| 30 | `categorias.md` | CAT-CTL | P2 | NOT_ANALYZED | — | — |
| 31 | `tipos-ingredientes.md` | CAT-CTL | P2 | NOT_ANALYZED | — | — |
| 32 | `tipos-tecnicas.md` | CAT-CTL | P2 | NOT_ANALYZED | — | — |
| 33 | `tipos-equipamentos.md` | CAT-CTL | P2 | NOT_ANALYZED | — | — |
| 34 | `unidades-medida.md` | CAT-CTL | P2 | NOT_ANALYZED | — | — |

#### esquemas/

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 35 | `esquema-receita-v1.md` | CAT-DOM | P1 | NOT_ANALYZED | Contrato de campos; precede schema SQL |
| 36 | `esquema-execucao-v1.md` | CAT-DOM | P1 | NOT_ANALYZED | — |
| 37 | `esquema-ingrediente-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 38 | `esquema-tecnica-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 39 | `esquema-equipamento-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 40 | `esquema-observacao-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |

#### templates/

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 41 | `receita-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | Instância do template para o autor |
| 42 | `execucao-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 43 | `ingrediente-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 44 | `tecnica-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 45 | `equipamento-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 46 | `observacao-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |
| 47 | `experimento-v1.md` | CAT-DOM | P2 | NOT_ANALYZED | — |

---

### docs/02-arquitetura/ — 7 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 48 | `diagrama-mestre.md` | CAT-ARQ | P2 | NOT_ANALYZED | — |
| 49 | `diagrama-mestre.txt` | CAT-ARQ | P3 | NOT_ANALYZED | Verificar redundância com .md |
| 50 | `fluxo-dados.md` | CAT-ARQ | P2 | NOT_ANALYZED | — |
| 51 | `importacao.md` | CAT-ARQ | P2 | NOT_ANALYZED | — |
| 52 | `exportacao.md` | CAT-ARQ | P3 | NOT_ANALYZED | — |
| 53 | `versionamento.md` | CAT-ARQ | P2 | NOT_ANALYZED | — |
| 54 | `estrutura-diretorios.md` | CAT-ARQ | P2 | NOT_ANALYZED | — |

---

### docs/03-modelagem/ — 7 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 55 | `conceitos-fundamentais.md` | CAT-MOD | P1 | NOT_ANALYZED | Definições formais; base de todo o sistema |
| 56 | `entidades-er.md` | CAT-MOD | P2 | NOT_ANALYZED | — |
| 57 | `objetivo.md` | CAT-MOD | P2 | NOT_ANALYZED | — |
| 58 | `normalizacao.md` | CAT-MOD | P2 | NOT_ANALYZED | — |
| 59 | `relacionamentos.md` | CAT-MOD | P2 | NOT_ANALYZED | Verificar sobreposição com mapa-relacionamentos |
| 60 | `ids.md` | CAT-MOD | P2 | NOT_ANALYZED | — |
| 61 | `sqlite.md` | CAT-MOD | P2 | NOT_ANALYZED | — |

---

### docs/04-padroes/ — 12 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 62 | `identificadores.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 63 | `versionamento.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 64 | `metadados.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 65 | `politica-templates.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 66 | `politica-esquemas.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 67 | `politica-arquivamento.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 68 | `politica-revisao.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 69 | `politica-conflito.md` | CAT-GOV | P1 | NOT_ANALYZED | — |
| 70 | `ADR-0001-MOTOR-DE-CONHECIMENTO.md` | CAT-PAD | P2 | NOT_ANALYZED | Decisão arquitetural registrada |
| 71 | `validacao.md` | CAT-PAD | P2 | NOT_ANALYZED | — |
| 72 | `nomenclatura.md` | CAT-PAD | P2 | NOT_ANALYZED | — |
| 73 | `tags.md` | CAT-PAD | P2 | NOT_ANALYZED | — |

---

### docs/05-desenvolvimento/ — 2 arquivos (exclusivos da cópia)

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 74 | `padroes-desenvolvimento.md` | CAT-DEV | P2 | NOT_ANALYZED | ✅ Convenções para implementadores |
| 75 | `casos-de-uso.md` | CAT-DEV | P2 | NOT_ANALYZED | ✅ UC-001 a UC-010 formalizados |

---

### docs/06-operacao/ — 1 arquivo (exclusivo da cópia)

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 76 | `guia-operacao.md` | CAT-OPR | P3 | NOT_ANALYZED | ✅ Backup, reconstrução, manutenção |

---

### docs/99-referencias/ — 5 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 77 | `validacao-arquitetural-fase12.md` | CAT-REF | P2 | NOT_ANALYZED | ✅ Checklist de completude |
| 78 | `rastreamento-atualizado.md` | CAT-REF | P2 | NOT_ANALYZED | ✅ Estado 78%; versão mais recente |
| 79 | `rastreamento-roadmap.md` | CAT-REF | P3 | NOT_ANALYZED | Versão 23%; desatualizado — não migrar como está |
| 80 | `roadmap-maturidade-arquitetural.md` | CAT-REF | P2 | NOT_ANALYZED | — |
| 81 | `tarefas-desbloqueio.md` | CAT-REF | P3 | NOT_ANALYZED | Tarefas já executadas na cópia; verificar utilidade residual |

---

### banco_de_dados/ — 3 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 82 | `esquemas/schema-sqlite-v1.sql` | CAT-BAN | P1 | NOT_ANALYZED | ✅ Schema completo: 8 tabelas, 9 N:N, histórico, índices, 2 views |
| 83 | `seeds/seed-categorias.sql` | CAT-BAN | P3 | NOT_ANALYZED | ✅ 10 categorias iniciais |
| 84 | `seeds/.gitkeep` | CAT-BAN | P4 | NOT_ANALYZED | Arquivo estrutural |

---

### scripts/ — 1 arquivo

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 85 | `importacao/importar.sh` | CAT-SCR | P3 | NOT_ANALYZED | ✅ Placeholder documentado; inicializa banco |

---

### dados/ — 12 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Excl. Cópia | Observação |
|---|---------|-----------|------------|--------|-------------|------------|
| 86 | `receitas/REC-000001-doce-de-leite-artesanal-v1.md` | CAT-DAD | P2 | NOT_ANALYZED | — | Cópia usa nome correto com prefixo; principal não |
| 87 | `ingredientes/ING-000001-leite-integral.md` | CAT-DAD | P3 | NOT_ANALYZED | — | — |
| 88 | `ingredientes/ING-000002-acucar-refinado.md` | CAT-DAD | P3 | NOT_ANALYZED | — | — |
| 89 | `ingredientes/ING-000003-sal-refinado.md` | CAT-DAD | P3 | NOT_ANALYZED | — | — |
| 90 | `ingredientes/ING-000004-bicarbonato-sodio.md` | CAT-DAD | P3 | NOT_ANALYZED | — | — |
| 91 | `equipamentos/EQP-000001-panela-fundo-grosso.md` | CAT-DAD | P3 | NOT_ANALYZED | — | — |
| 92 | `equipamentos/EQP-000002-colher-silicone.md` | CAT-DAD | P3 | NOT_ANALYZED | — | — |
| 93 | `execucoes/EXE-000001-doce-leite-v1-execucao1.md` | CAT-DAD | P3 | NOT_ANALYZED | — | — |
| 94 | `observacoes/OBS-000001-bicarbonato-efeito.md` | CAT-DAD | P3 | NOT_ANALYZED | ✅ | — |
| 95 | `tecnicas/TEC-000001-reducao.md` | CAT-DAD | P3 | NOT_ANALYZED | ✅ | — |
| 96 | `tecnicas/TEC-000002-caramelizacao.md` | CAT-DAD | P3 | NOT_ANALYZED | ✅ | — |
| 97 | `tecnicas/TEC-000003-agitacao-continua.md` | CAT-DAD | P3 | NOT_ANALYZED | ✅ | — |

---

### Raiz — 3 arquivos

| # | Arquivo | Categoria | Prioridade | Estado | Observação |
|---|---------|-----------|------------|--------|------------|
| 98 | `README.md` | CAT-PRJ | P2 | NOT_ANALYZED | Cópia tem status 78%; comparar |
| 99 | `.gitignore` | CAT-OPR | P3 | NOT_ANALYZED | Comparar com principal |
| 100 | `LICENSE` | CAT-PRJ | P4 | NOT_ANALYZED | Vazio em ambos |

---

## Resumo por Prioridade

| Prioridade | Total |
|------------|-------|
| P1 — Crítica | 22 |
| P2 — Alta | 52 |
| P3 — Média | 20 |
| P4 — Baixa | 6 |
| **Total** | **100** |

## Resumo por Categoria

| Categoria | Total |
|-----------|-------|
| CAT-DOM | 31 |
| CAT-CTL | 8 |
| CAT-GOV | 11 |
| CAT-ARQ | 7 |
| CAT-MOD | 7 |
| CAT-DAD | 12 |
| CAT-PAD | 4 |
| CAT-PRJ | 7 |
| CAT-BAN | 3 |
| CAT-REF | 5 |
| CAT-DEV | 2 |
| CAT-OPR | 2 |
| CAT-SCR | 1 |
| CAT-LNG | 2 |

---

## Ordem de Análise (Fase 3)

Baseada em dependências lógicas entre categorias:

```
1. CAT-PRJ   filosofia, princípios
2. CAT-GOV   leis, políticas
3. CAT-LNG   linguagem, glossário
4. CAT-CTL   catálogos
5. CAT-DOM   especificações, contratos
6. CAT-ARQ   arquitetura
7. CAT-MOD   modelagem
8. CAT-BAN   banco, schema
9. CAT-DEV   desenvolvimento
10. CAT-OPR  operação
11. CAT-SCR  scripts
12. CAT-DAD  dados
13. CAT-REF  rastreamento
```

---

## Próxima Fase

**Fase 3 — Estado Arquitetural:** cada arquivo recebe análise de conteúdo, identificação de gaps e proposta de ação.

Arquivo de saída: `MIGRATION_STATUS.md`
