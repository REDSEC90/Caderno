# Rastreamento do Roadmap — Estado Atual

> Última atualização: 2026-06-25 19:08 BRT

## FASE 0 — Identidade ✅ CONCLUÍDA

- [x] Nome: SOE-CCG
- [x] Missão: documentada em `docs/00-projeto/visão.md`
- [x] Visão: documentada em `docs/00-projeto/visão.md`
- [x] Objetivos: documentados em `docs/00-projeto/objetivos.md`
- [x] Escopo: documentado em `docs/00-projeto/escopo.md`
- [x] Filosofia: documentada em `docs/00-projeto/principios.md` e `README.md`
- [x] Estrutura inicial: criada
- [x] Organização documental: definida

---

## FASE 1 — Constituição ✅ CONCLUÍDA

### Unidade 1 — Filosofia ✅ CONCLUÍDA

Arquivo: `docs/00-projeto/filosofia.md`

- [x] Papel do conhecimento — formalizado como Axioma 1
- [x] Fonte da verdade — formalizado como Axioma 2
- [x] Papel do Markdown — formalizado como Axioma 3
- [x] Papel do SQLite — formalizado como Axioma 4
- [x] Papel da implementação — formalizado como Axioma 5

**Status:** filosofia completa com rigor axiomático.

### Unidade 2 — Leis Fundamentais ✅ CONCLUÍDA

Arquivo: `docs/00-projeto/constituicao.md`

- [x] 10 leis fundamentais definidas
- [x] Invariantes explícitos
- [x] Restrições permanentes documentadas

### Unidade 3 — Conceitos Fundamentais ✅ CONCLUÍDA

Arquivos: `docs/00-projeto/glossario.md` e `docs/03-modelagem/conceitos-fundamentais.md`

- [x] Registro
- [x] Entidade
- [x] Relacionamento
- [x] Versão
- [x] Histórico
- [x] Identificador
- [x] Metadados
- [x] Template
- [x] Esquema
- [x] Estado
- [x] Catálogo
- [x] Tag
- [x] Referência

**Status:** todos os conceitos fundamentais definidos com precisão.

---

## FASE 2 — Governança 🟡 PARCIALMENTE CONCLUÍDA

Arquivos existentes em `docs/04-padroes/`:

- [x] Política de Identificadores — `identificadores.md` ✅
- [x] Política de Versionamento — `versionamento.md` ✅
- [x] Política de Metadados — `metadados.md` ✅
- [ ] Política de Templates — **FALTANTE**
- [ ] Política de Esquemas — **FALTANTE**
- [ ] Política de Arquivamento — **FALTANTE**
- [ ] Política de Revisão — **FALTANTE**
- [ ] Política de Conflito — **FALTANTE**

**Status:** 3 de 8 políticas definidas. As 5 restantes são críticas para avançar.

---

## FASE 3 — Linguagem do SOE-CCG ❌ NÃO INICIADA

- [ ] Vocabulário — todos os termos oficiais do domínio
- [ ] Estrutura léxica — como os documentos são escritos
- [ ] Estrutura de relacionamento — como as entidades se conectam
- [ ] Semântica — o que cada elemento significa no domínio
- [ ] Glossário Oficial — existe `glossario.md`, mas não está formalizado como "oficial"

**Bloqueador:** FASE 2 incompleta.

---

## FASE 4 — Domínio 🟡 PARCIALMENTE CONCLUÍDA

Arquivos existentes:
- `docs/01-dominio/entidades.md` — define 7 entidades
- `docs/01-dominio/ciclo-de-vida.md` — define ciclo de vida
- `docs/01-dominio/relacionamentos.md` — define relacionamentos básicos

**Para cada entidade (Receita, Ingrediente, Técnica, Equipamento, Execução, Observação, Experimento):**

Estrutura parcial existe, mas falta responder formalmente:

- [ ] Identidade — mencionada, não formalizada
- [ ] Responsabilidade — mencionada, não formalizada
- [ ] Limites — **não documentado**
- [ ] Atributos — definidos em esquemas
- [ ] Estados — parcial em `catalogos/estados-receita.md`
- [ ] Eventos — **não documentado**
- [ ] Relacionamentos — básico em `relacionamentos.md`
- [ ] Dependências — **não explícito**
- [ ] Restrições — **não explícito**
- [ ] Ciclo de vida — genérico em `ciclo-de-vida.md`, não por entidade

**Nota crítica:** falta separação explícita entre **domínio gastronômico** e **domínio do sistema**.

**Bloqueador:** FASE 3 incompleta.

---

## FASE 5 — Contratos ❌ NÃO INICIADA

- [ ] Template canônico de contrato — **não existe**
- [ ] Contratos por entidade — **não existem**

**Bloqueador:** FASE 4 incompleta.

---

## FASE 6 — Catálogos 🟡 PARCIALMENTE CONCLUÍDA

Arquivos existentes em `docs/01-dominio/catalogos/`:

- [x] Categorias — `categorias.md`
- [x] Estados — `estados-receita.md` (apenas receita)
- [x] Tipos — `tipos-ingredientes.md`, `tipos-tecnicas.md`, `tipos-equipamentos.md`
- [x] Unidades — `unidades-medida.md`
- [ ] Classificações — **faltante**
- [ ] Escalas — **faltante**
- [ ] Materiais — **faltante**
- [ ] Métodos — **faltante**
- [ ] Vocabulário controlado — **faltante**

**Status:** base existe, mas incompleta. Faltam estados de outras entidades.

**Bloqueador:** FASE 5 incompleta.

---

## FASES 7-13 ❌ NÃO INICIADAS

Bloqueadas pelas fases anteriores.

---

## Análise de Bloqueios

### Bloqueio Crítico 1: FASE 1 Unidade 1
A filosofia existe informalmente, mas não está formalizada com rigor de axiomas. Isso impede que as fases seguintes tenham base sólida.

### Bloqueio Crítico 2: FASE 2 — 5 políticas faltantes
Sem políticas de Templates, Esquemas, Arquivamento, Revisão e Conflito, não há governança suficiente para prosseguir.

### Bloqueio Crítico 3: FASE 4 — especificação de entidades incompleta
Entidades mencionadas, mas não especificadas com rigor suficiente. Falta estrutura formal de resposta para cada uma.

---

## Próximas Ações Prioritárias

### Prioridade 1 — Desbloquear FASE 1
1. Formalizar Unidade 1 — Filosofia com rigor axiomático
2. Refinar conceitos fundamentais restantes

### Prioridade 2 — Completar FASE 2
3. Escrever Política de Templates
4. Escrever Política de Esquemas
5. Escrever Política de Arquivamento
6. Escrever Política de Revisão
7. Escrever Política de Conflito

### Prioridade 3 — Formalizar FASE 4
8. Criar template de especificação de entidade
9. Especificar cada entidade usando o template

---

## Métricas de Maturidade

| Fase | Progresso | Bloqueada por |
|------|-----------|---------------|
| 0 — Identidade | 100% ✅ | — |
| 1 — Constituição | 60% 🟡 | Filosofia não formalizada |
| 2 — Governança | 37% 🟡 | FASE 1 |
| 3 — Linguagem | 0% ❌ | FASE 2 |
| 4 — Domínio | 30% 🟡 | FASE 3 |
| 5 — Contratos | 0% ❌ | FASE 4 |
| 6 — Catálogos | 40% 🟡 | FASE 5 |
| 7-13 | 0% ❌ | Fases anteriores |

**Progresso geral da fundação:** ~23%

---

## Critério de Implementabilidade

**Pergunta:** um desenvolvedor experiente, sem acesso ao código, consegue implementar um sistema compatível apenas com a documentação atual?

**Resposta:** Não. Faltam definições críticas em múltiplas camadas.

**Principais lacunas:**
- Filosofia não axiomatizada
- 5 políticas de governança faltantes
- Especificação formal de entidades incompleta
- Contratos inexistentes
- Catálogos parciais
