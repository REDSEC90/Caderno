# ESTADO ATUAL DO SISTEMA — SOE-CCG

**Versão da arquitetura:** 1.0  
**Data de emissão:** 2026-06-26  
**Tipo:** Certificado Arquitetural  
**Validade:** até alteração formal via ADR

---

## IDENTIDADE

| Campo | Valor |
|-------|-------|
| **Nome** | SOE-CCG |
| **Definição** | Sistema de Registro, Organização, Evolução e Consulta de Conhecimento Gastronômico |
| **Natureza** | Motor de conhecimento gastronômico — não é gerenciador de receitas |
| **Versão da arquitetura** | 1.0 |
| **Data de congelamento** | 2026-06-26 |
| **Status geral** | ✅ Especificação completa — Implementação autorizada |

---

## FILOSOFIA

**Status:** ✅ Completa e aprovada  
**Documento:** `docs/00-projeto/filosofia.md`

| Axioma | Enunciado resumido | Status |
|--------|-------------------|--------|
| Axioma 1 | Conhecimento existe independente do sistema | ✅ Formalizado |
| Axioma 2 | Toda informação tem uma única localização oficial | ✅ Formalizado |
| Axioma 3 | Markdown é o formato canônico e permanente | ✅ Formalizado |
| Axioma 4 | SQLite é mecanismo de consulta, nunca fonte | ✅ Formalizado |
| Axioma 5 | Implementação é temporária; conhecimento é permanente | ✅ Formalizado |

**Contradições internas:** Nenhuma  
**Decisões não explicadas pela filosofia:** Nenhuma  
**Riscos filosóficos:** Nenhum identificado  

---

## DOMÍNIO

**Status:** ✅ Completo e aprovado

### Entidades

| Entidade | Especificação | Contrato | Template | Esquema | Estados |
|----------|--------------|---------|----------|---------|---------|
| Receita | ✅ | ✅ | ✅ | ✅ | 5 estados |
| Ingrediente | ✅ | ✅ | ✅ | ✅ | 3 estados |
| Técnica | ✅ | ✅ | ✅ | ✅ | 3 estados |
| Equipamento | ✅ | ✅ | ✅ | ✅ | 3 estados |
| Execução | ✅ | ✅ | ✅ | ✅ | 3 estados |
| Observação | ✅ | ✅ | ✅ | ✅ | 3 estados |
| Experimento | ✅ | ✅ | ✅ | ✅ | 4 estados |
| Registro (base) | ✅ | — | — | — | 6 estados universais |

**Cobertura de entidades:** 7/7 (100%)  
**Cobertura de contratos:** 7/7 (100%)  
**Entidades sem ciclo de vida:** 0  
**Relacionamentos documentados:** 13  
**Referências circulares:** 0  

### Contratos — Cobertura

Cada contrato formal define:
- ✅ Campos obrigatórios com mensagem de erro
- ✅ Campos opcionais com comportamento padrão
- ✅ Valores aceitos (enums)
- ✅ Pré-condições por operação (checklist)
- ✅ Pós-condições por operação (checklist)
- ✅ Invariantes permanentes
- ✅ Rejeições explícitas com mensagem de erro
- ✅ Compatibilidade de esquema
- ✅ Critério de aceitação de implementação

---

## PADRONIZAÇÃO

**Status:** ✅ Completa e aprovada

### Templates

| Template | Arquivo | Frontmatter completo | Alinhado ao contrato |
|---------|---------|---------------------|---------------------|
| Receita v1 | `templates/receita-v1.md` | ✅ | ✅ |
| Ingrediente v1 | `templates/ingrediente-v1.md` | ✅ | ✅ |
| Técnica v1 | `templates/tecnica-v1.md` | ✅ | ✅ |
| Equipamento v1 | `templates/equipamento-v1.md` | ✅ | ✅ |
| Execução v1 | `templates/execucao-v1.md` | ✅ | ✅ (corrigido 2026-06-26) |
| Observação v1 | `templates/observacao-v1.md` | ✅ | ✅ (corrigido 2026-06-26) |
| Experimento v1 | `templates/experimento-v1.md` | ✅ | ✅ (corrigido 2026-06-26) |

### Metadados Obrigatórios (todo registro)

`id` · `tipo` · `schema-version` · `versao` · `status` · `criado-em` · `atualizado-em` · `autor`

### Identificadores

| Prefixo | Entidade | Último ID |
|---------|----------|-----------|
| `REC` | Receita | REC-000001 |
| `ING` | Ingrediente | ING-000004 |
| `TEC` | Técnica | TEC-000003 |
| `EQP` | Equipamento | EQP-000002 |
| `EXE` | Execução | EXE-000001 |
| `OBS` | Observação | OBS-000001 |
| `EXP` | Experimento | — |
| `CAT` | Categoria | CAT-000010 |

> ⚠️ Tabela em `docs/04-padroes/identificadores.md` não reflete estes valores. Atualização necessária antes de criar novos registros (VAF-0032).

### Políticas de Governança

| Política | Arquivo | Status |
|---------|---------|--------|
| Identificadores | `politica-identificadores.md` (via `identificadores.md`) | ✅ |
| Versionamento | `versionamento.md` | ✅ |
| Metadados | `metadados.md` | ✅ |
| Templates | `politica-templates.md` | ✅ |
| Esquemas | `politica-esquemas.md` | ✅ |
| Arquivamento | `politica-arquivamento.md` | ✅ |
| Revisão | `politica-revisao.md` | ✅ |
| Conflito | `politica-conflito.md` | ✅ |

**Cobertura de governança:** 8/8 políticas (100%)

---

## INTEGRIDADE

**Status:** ✅ Aprovada (1 pendência menor)

### Referências nos dados reais

| Registro | Referências | Válidas |
|---------|-------------|---------|
| REC-000001 | ING-000001, ING-000002, ING-000003, ING-000004 | ✅ |
| EXE-000001 | REC-000001, ING-000001–4, TEC-000001, TEC-000003, EQP-000001–2 | ✅ |
| OBS-000001 | EXE-000001 | ✅ |

**Referências quebradas:** 0  
**Duplicidades de ID:** 0  
**Inconsistências de schema:** 0 (após correção dos 3 templates)  

### Banco de Dados

| Componente | Status |
|-----------|--------|
| Schema SQL v1 | ✅ Completo — 7 tabelas principais + 8 N:N + histórico + índices + views |
| Seeds de categorias | ✅ 10 categorias iniciais |
| Seeds de ingredientes | ⏳ Pendente (dados em Markdown; SQL a gerar na Fase 13) |
| Seeds de técnicas | ⏳ Pendente |
| Seeds de equipamentos | ⏳ Pendente |
| Banco .db instanciado | ⏳ Pendente (criado pelo importador na Fase 13) |

---

## COBERTURA DOCUMENTAL

**Quanto da arquitetura está documentada:**

| Camada | Cobertura |
|--------|-----------|
| Filosofia | 100% |
| Constituição | 100% |
| Governança | 100% |
| Linguagem | 100% |
| Domínio — entidades | 100% |
| Domínio — contratos | 100% |
| Domínio — relacionamentos | 100% |
| Domínio — catálogos | 95% |
| Padrões | 100% |
| Modelagem | 100% |
| Casos de uso | 100% |
| Implementação (Fase 13) | 0% — não iniciada |

**Cobertura geral da especificação: ~98%**  
**Cobertura da implementação: 0%** — intencional; especificação foi concluída antes do código

---

## COBERTURA DO DOMÍNIO

| Item | Total | Documentados |
|------|-------|-------------|
| Entidades | 7 | 7 (100%) |
| Contratos | 7 | 7 (100%) |
| Templates | 7 | 7 (100%) |
| Relacionamentos | 13 | 13 (100%) |
| Catálogos | 11 | 11 (100%) |
| Políticas de governança | 8 | 8 (100%) |
| Casos de uso | 10 | 10 (100%) |
| Dados canônicos (registros) | — | 11 registros seed |

---

## RISCOS ARQUITETURAIS

| Risco | Nível | Descrição | Mitigação |
|-------|-------|-----------|-----------|
| Tabela de IDs desatualizada | 🟡 Médio | `identificadores.md` não reflete IDs usados nos dados reais | Corrigir antes de criar novos registros |
| Seeds SQL ausentes | 🟡 Médio | Ingredientes, técnicas e equipamentos existem só em Markdown | Importador da Fase 13 resolve automaticamente |
| Script de importação é placeholder | 🟡 Médio | `scripts/importacao/importar.sh` sem implementação real | Fase 13 substitui pelo parser Python |
| Banco SQLite não instanciado | 🟢 Baixo | Não bloqueia nada; Markdown é a fonte | Criado automaticamente na primeira execução do importador |
| Ausência de validação automática | 🟢 Baixo | Validação de contratos é manual até Fase 13 | Validador será primeiro entregável da Fase 13 |

**Riscos bloqueadores para implementação:** 0  
**Riscos críticos:** 0  

---

## DECISÕES CONGELADAS

As decisões abaixo não podem ser alteradas sem ADR formal e justificativa forte:

| Decisão | Documento | Desde |
|---------|-----------|-------|
| Markdown como formato canônico | `filosofia.md` — Axioma 3 | Fundação |
| SQLite como índice derivado, nunca fonte | `filosofia.md` — Axioma 4 | Fundação |
| IDs no formato `[PREFIXO]-NNNNNN` | `identificadores.md` | Fase 2 |
| IDs imutáveis após criação | Todos os contratos — Invariante 1 | Fase 5 |
| IDs nunca reutilizados | Todos os contratos — Invariante 2 | Fase 5 |
| Relacionamentos por ID, nunca por nome | `constituicao.md` — Lei 8 | Fase 1 |
| Exclusão substituída por arquivamento | `politica-arquivamento.md` | Fase 2 |
| Histórico append-only | Todos os contratos — invariante de histórico | Fase 5 |
| Fluxo unidirecional Markdown → SQLite | `filosofia.md` — Axioma 2 | Fundação |
| Frontmatter YAML obrigatório em todos os registros | `padroes-desenvolvimento.md` | Fase 8 |
| 8 prefixos de ID: REC, ING, TEC, EQP, EXE, OBS, EXP, CAT | `identificadores.md` | Fase 2 |
| Estrutura de diretórios `dados/[entidade]/` | `estrutura-diretorios.md` | Fase 2 |
| Estados controlados por catálogo | `estados-todas-entidades.md` | Fase 6 |
| Modelo canônico SQLite v1 | `schema-sqlite-v1.sql` | Fase 9 |

---

## PENDÊNCIAS ANTES DA IMPLEMENTAÇÃO

### Pendências críticas (bloqueadoras)

```
Nenhuma pendência crítica.
Arquitetura considerada apta para implementação.
```

### Pendências menores (não-bloqueadoras)

1. **Atualizar tabela de controle de IDs** em `docs/04-padroes/identificadores.md`  
   — Reflexo dos IDs já existentes em `dados/`

2. **Seeds SQL para ingredientes, técnicas e equipamentos**  
   — Podem ser gerados automaticamente pelo importador na Fase 13

3. **Expandir dados canônicos**  
   — Fase 10 é contínua; seeds atuais são suficientes para iniciar a Fase 13

---

## VALIDAÇÃO ARQUITETURAL FINAL

**Matriz completa:** `docs/99-referencias/MATRIZ_DE_VALIDACAO_ARQUITETURAL.md`

| Motor | Resultado |
|-------|-----------|
| Filosófico | ✅ APROVADO |
| Domínio | ✅ APROVADO |
| Padronização | ✅ APROVADO |
| Integridade | ✅ APROVADO |
| Semântico | ✅ APROVADO |
| Conhecimento | ✅ APROVADO |
| Evolução | ✅ APROVADO |
| Implementabilidade | ✅ APROVADO |

**Requisitos validados:** 62  
**Aprovados:** 61  
**Reprovados:** 0  
**Bloqueadores:** 0  

---

## FASE 13 — IMPLEMENTAÇÃO AUTORIZADA

**Status:** ⏳ Autorizada — não iniciada

### Ordem de execução

| Etapa | Descrição | Dependências |
|-------|-----------|-------------|
| 13.1 | Parser Markdown | Nenhuma |
| 13.2 | Validador de Contratos | 13.1 |
| 13.3 | Importador SQLite | 13.1 + 13.2 |
| 13.4 | CLI básica | 13.3 |
| 13.5 | API REST | 13.3 |
| 13.6 | Interface Web | 13.5 |

### Linguagem recomendada

Python — por alinhamento com `PyYAML`, `python-frontmatter`, `sqlite3`, `click`/`typer`, `FastAPI`.

### Primeiro entregável

Parser + Validador que:
- Lê qualquer arquivo `.md` de `dados/`
- Extrai frontmatter YAML e corpo Markdown
- Valida contra contrato da entidade correspondente
- Retorna lista de violações (vazia = válido)

---

## HISTÓRICO DE VERSÕES DESTE DOCUMENTO

| Versão | Data | Evento |
|--------|------|--------|
| 1.0 | 2026-06-26 | Emissão inicial após VAF completa |
