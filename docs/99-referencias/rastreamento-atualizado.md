# Rastreamento do Roadmap — Estado Atualizado

> Última atualização: 2026-06-25 (revisão completa pela análise estrutural)

---

## Resumo Executivo

| Fase | Nome | Status Anterior | Status Atual |
|------|------|----------------|-------------|
| 0 | Identidade | ✅ 100% | ✅ 100% |
| 1 | Constituição | 🟡 60% | ✅ 100% |
| 2 | Governança | 🟡 37% | ✅ 100% |
| 3 | Linguagem | ❌ 0% | ✅ 100% |
| 4 | Domínio | 🟡 30% | ✅ 100% |
| 5 | Contratos | ❌ 0% | 🟡 40% |
| 6 | Catálogos | 🟡 40% | ✅ 90% |
| 7–13 | Fases avançadas | ❌ 0% | ❌ 0% |

**Progresso geral da fundação:** ~78% (era 23%)

---

## FASE 0 — Identidade ✅ CONCLUÍDA

- [x] Nome: SOE-CCG
- [x] Missão documentada em `docs/00-projeto/visão.md`
- [x] Visão documentada em `docs/00-projeto/visão.md`
- [x] Objetivos em `docs/00-projeto/objetivos.md`
- [x] Escopo em `docs/00-projeto/escopo.md`
- [x] Filosofia em `docs/00-projeto/principios.md` e `README.md`
- [x] Estrutura inicial criada
- [x] Organização documental definida

---

## FASE 1 — Constituição ✅ CONCLUÍDA

### Unidade 1 — Filosofia ✅

Arquivo: `docs/00-projeto/filosofia.md`

- [x] Axioma 1: Papel do Conhecimento — formalizado com consequências e implicação arquitetural
- [x] Axioma 2: Fonte da Verdade — formalizado com consequências e implicação arquitetural
- [x] Axioma 3: Papel do Markdown — formalizado com consequências e implicação arquitetural
- [x] Axioma 4: Papel do SQLite — formalizado com consequências e implicação arquitetural
- [x] Axioma 5: Papel da Implementação — formalizado com consequências e implicação arquitetural
- [x] Consequências Filosóficas — 5 derivações documentadas
- [x] Teste Filosófico — 4 perguntas para validação de decisões
- [x] Relação com a Constituição — cadeia de derivação documentada

**Avaliação:** a filosofia está completa, rigorosa e com rigor axiomático. Qualquer desenvolvedor que leia entende por que as decisões arquiteturais foram tomadas.

### Unidade 2 — Leis Fundamentais ✅

Arquivo: `docs/00-projeto/constituicao.md`

- [x] 10 leis fundamentais definidas e numeradas
- [x] Invariantes explícitos (o que nunca muda)
- [x] Restrições permanentes documentadas
- [x] O que pode evoluir documentado

### Unidade 3 — Conceitos Fundamentais ✅

Arquivos: `docs/00-projeto/glossario.md` e `docs/03-modelagem/conceitos-fundamentais.md`

- [x] Registro — definido
- [x] Entidade — definido
- [x] Relacionamento — definido
- [x] Versão — definido
- [x] Histórico — definido
- [x] Identificador — definido
- [x] Metadados — definido
- [x] Template — definido
- [x] Esquema — definido
- [x] Estado — definido (em `docs/04-padroes/politica-arquivamento.md` e `docs/01-dominio/linguagem-soe-ccg.md`)
- [x] Catálogo — definido
- [x] Tag — definido
- [x] Referência — definido

---

## FASE 2 — Governança ✅ CONCLUÍDA

Arquivos em `docs/04-padroes/`:

- [x] Política de Identificadores — `identificadores.md` ✅
- [x] Política de Versionamento — `versionamento.md` ✅
- [x] Política de Metadados — `metadados.md` ✅
- [x] Política de Templates — `politica-templates.md` ✅
- [x] Política de Esquemas — `politica-esquemas.md` ✅
- [x] Política de Arquivamento — `politica-arquivamento.md` ✅
- [x] Política de Revisão — `politica-revisao.md` ✅
- [x] Política de Conflito — `politica-conflito.md` ✅

**Todas as 8 políticas de governança estão completas e documentadas.**

---

## FASE 3 — Linguagem do SOE-CCG ✅ CONCLUÍDA

Arquivo: `docs/01-dominio/linguagem-soe-ccg.md`

- [x] Vocabulário oficial — termos do domínio gastronômico e do sistema
- [x] Termos proibidos — lista de termos que criam ambiguidade
- [x] Estrutura léxica — 6 regras de redação para documentação
- [x] Estrutura de relacionamento — como vínculos são expressos em Markdown
- [x] Semântica dos estados — o que cada estado significa formalmente
- [x] Semântica de versionamento — distinção entre versão de conteúdo e de esquema
- [x] Glossário Oficial — todos os termos em ordem alfabética

**Nenhum termo tem dois significados. Dois conceitos não compartilham o mesmo nome.**

---

## FASE 4 — Domínio ✅ CONCLUÍDA

### Separação de Domínios ✅

Arquivo: `docs/01-dominio/separacao-dominios.md`

- [x] Domínio gastronômico definido
- [x] Domínio do sistema definido
- [x] Mapeamento entre os domínios
- [x] Exemplos de ambiguidade resolvida
- [x] Resumo comparativo

### Especificações de Entidades ✅

- [x] Template de Especificação — `docs/01-dominio/template-especificacao-entidade.md`
- [x] Especificação de Registro — `docs/01-dominio/especificacao-registro.md`
- [x] Especificação de Receita — `docs/01-dominio/especificacao-receita.md`
- [x] Especificação de Ingrediente — `docs/01-dominio/especificacao-ingrediente.md`
- [x] Especificação de Técnica — `docs/01-dominio/especificacao-tecnica.md`
- [x] Especificação de Equipamento — `docs/01-dominio/especificacao-equipamento.md`
- [x] Especificação de Execução — `docs/01-dominio/especificacao-execucao.md`
- [x] Especificação de Observação — `docs/01-dominio/especificacao-observacao.md`
- [x] Especificação de Experimento — `docs/01-dominio/especificacao-experimento.md`

**Para cada entidade, respondido formalmente:**
- [x] Identidade — o que é?
- [x] Responsabilidade — para que existe?
- [x] Limites — o que nunca faz?
- [x] Atributos — quais campos possui?
- [x] Estados — como evolui?
- [x] Eventos — o que pode acontecer?
- [x] Relacionamentos — com quem conversa?
- [x] Dependências — do que depende?
- [x] Restrições — o que é proibido?
- [x] Ciclo de vida — nascimento, evolução, arquivamento

---

## FASE 5 — Contratos 🟡 INICIADA PARCIALMENTE

**O que existe:**
- [x] Estrutura do contrato definida conceitualmente na especificação de cada entidade
- [x] Campos obrigatórios e opcionais definidos nos esquemas existentes
- [x] Restrições e invariantes documentados por entidade

**O que falta:**
- [ ] Template canônico de contrato (documento independente)
- [ ] Contratos formais individuais por entidade (documentos separados dos esquemas)
- [ ] Definição formal de pré-condições e pós-condições por operação
- [ ] Definição formal de invariantes como contrato (não apenas como restrições)

**Bloqueador:** FASE 4 agora está completa — esta fase pode ser iniciada.

---

## FASE 6 — Catálogos ✅ 90% CONCLUÍDA

**Arquivos existentes em `docs/01-dominio/catalogos/`:**
- [x] Categorias — `categorias.md`
- [x] Estados — `estados-receita.md` (apenas Receita; demais estados em especificações)
- [x] Tipos — `tipos-ingredientes.md`, `tipos-tecnicas.md`, `tipos-equipamentos.md`
- [x] Unidades — `unidades-medida.md`

**Arquivos novos adicionados:**
- [x] Classificações — `catalogos-expandidos.md` (classificações de receitas)
- [x] Escalas — `catalogos-expandidos.md` (escala numérica 1–10, dificuldade, relevância)
- [x] Materiais — `catalogos-expandidos.md` (materiais de equipamentos)
- [x] Métodos — `catalogos-expandidos.md` (métodos culinários)
- [x] Vocabulário controlado — `catalogos-expandidos.md` (tags padronizadas)
- [x] Estados por entidade — em `especificacao-[entidade].md` respectivos

**Falta:**
- [ ] Consolidação dos estados de todas as entidades em arquivo único `estados-todas-entidades.md`

---

## FASE 7 — Relacionamentos ❌ NÃO INICIADA

**Bloqueador:** FASE 6 praticamente completa — pode ser iniciada.

**Próximo passo:**
Criar `docs/01-dominio/mapa-relacionamentos.md` com mapeamento completo de todos os relacionamentos entre entidades, com nome, direção, cardinalidade, restrições e significado de cada vínculo.

---

## FASES 8–13 ❌ NÃO INICIADAS

Seguem a ordem: 8 (Padrões) → 9 (Modelagem) → 10 (Dados Canônicos) → 11 (Casos de Uso) → 12 (Validação Arquitetural) → 13 (Implementação).

---

## Próximas Ações Prioritárias

### Prioridade 1 — Finalizar FASE 6

1. Criar `docs/01-dominio/catalogos/estados-todas-entidades.md` consolidando os estados de todas as entidades.

### Prioridade 2 — Completar FASE 5 (Contratos)

2. Criar `docs/01-dominio/template-contrato.md` com estrutura formal de contrato.
3. Criar contrato formal para cada entidade usando o template.

### Prioridade 3 — Iniciar FASE 7 (Relacionamentos)

4. Criar `docs/01-dominio/mapa-relacionamentos.md`.

### Prioridade 4 — Iniciar FASE 8 (Padrões)

5. Consolidar padrões de nomenclatura de arquivos.
6. Definir estrutura Markdown padrão para cada entidade.
7. Definir convenções de organização de `dados/`.

---

## Critério de Implementabilidade — Avaliação Atual

**Pergunta:** um desenvolvedor experiente, sem acesso ao código, consegue implementar um sistema compatível apenas com a documentação atual?

**Resposta:** Parcialmente. A fundação filosófica, a governança e o domínio estão suficientemente definidos para iniciar. As lacunas restantes são nas fases de contratos formais, relacionamentos detalhados e modelagem física (SQLite).

**Principais lacunas restantes:**
- Contratos formais com pré/pós-condições por operação
- Mapa completo de relacionamentos
- Modelo ER formal
- Esquema SQLite

**Progresso em relação ao critério:** ~65% (era ~10% antes desta análise).

---

## Métricas de Maturidade Atualizadas

| Fase | Progresso | Status |
|------|-----------|--------|
| 0 — Identidade | 100% | ✅ |
| 1 — Constituição | 100% | ✅ |
| 2 — Governança | 100% | ✅ |
| 3 — Linguagem | 100% | ✅ |
| 4 — Domínio | 100% | ✅ |
| 5 — Contratos | 40% | 🟡 |
| 6 — Catálogos | 90% | 🟡 |
| 7 — Relacionamentos | 0% | ❌ |
| 8 — Padrões | 30% | 🟡 |
| 9 — Modelagem | 20% | 🟡 |
| 10–13 | 0% | ❌ |

**Progresso geral da fundação:** ~78%
