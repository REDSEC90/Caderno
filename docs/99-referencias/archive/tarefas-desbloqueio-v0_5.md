# Tarefas — Desbloqueio da Fundação

> Tarefas mínimas precisas para desbloquear as fases do roadmap de maturidade.

---

## 🔴 PRIORIDADE 1 — Desbloquear FASE 1

### Tarefa 1.1 — Formalizar Filosofia

**Arquivo:** `docs/00-projeto/filosofia.md`

**O que fazer:**
Criar documento formal definindo axiomas do sistema com rigor de especificação.

**Estrutura esperada:**

```
# Filosofia do SOE-CCG

## Axioma 1: Papel do Conhecimento
[definição precisa, inequívoca]

## Axioma 2: Fonte da Verdade
[definição precisa, inequívoca]

## Axioma 3: Papel do Markdown
[definição precisa, inequívoca]

## Axioma 4: Papel do SQLite
[definição precisa, inequívoca]

## Axioma 5: Papel da Implementação
[definição precisa, inequívoca]

## Consequências Filosóficas
[derivações lógicas dos axiomas]
```

**Critério de conclusão:** qualquer desenvolvedor que leia entende por que as decisões arquiteturais foram tomadas.

---

### Tarefa 1.2 — Refinar Conceitos Fundamentais

**Arquivo:** `docs/00-projeto/glossario.md` (atualizar)

**O que fazer:**
Adicionar definições formais que faltam e refinar existentes.

**Conceitos a adicionar/refinar:**

- **Estado** — definir formalmente (não apenas exemplos)
- **Catálogo** — definir formalmente sua natureza e papel
- **Tag** — definir conceitualmente (não apenas uso)
- **Referência** — definir formalmente

**Critério de conclusão:** cada conceito tem definição que não admite segunda interpretação.

---

## 🔴 PRIORIDADE 2 — Completar FASE 2 (Governança)

### Tarefa 2.1 — Política de Templates

**Arquivo:** `docs/04-padroes/politica-templates.md`

**O que fazer:**
Definir formalmente como templates nascem, evoluem, versionam e garantem compatibilidade.

**Estrutura esperada:**

```
# Política de Templates

## Definição
O que é um template no SOE-CCG.

## Criação
Quando e como um template nasce.

## Estrutura
Anatomia de um template.

## Versionamento
Como templates evoluem.

## Compatibilidade
Quebra de compatibilidade: quando permitida, quando proibida.

## Depreciação
Como templates antigos são descontinuados.

## Exemplos
Casos concretos aplicando esta política.
```

---

### Tarefa 2.2 — Política de Esquemas

**Arquivo:** `docs/04-padroes/politica-esquemas.md`

**O que fazer:**
Definir formalmente como esquemas de entidades nascem, evoluem e garantem compatibilidade.

**Estrutura esperada:**

```
# Política de Esquemas

## Definição
O que é um esquema. Diferença entre esquema e template.

## Criação
Quando um esquema nasce.

## Estrutura
Anatomia de um esquema.

## Campos
Como campos são adicionados, modificados, removidos.

## Versionamento
Quando um esquema muda de versão.

## Compatibilidade
Mudanças compatíveis vs incompatíveis.

## Migração
Como dados existentes se adaptam a novos esquemas.

## Exemplos
Casos concretos.
```

---

### Tarefa 2.3 — Política de Arquivamento

**Arquivo:** `docs/04-padroes/politica-arquivamento.md`

**O que fazer:**
Definir formalmente como registros são arquivados (nunca excluídos).

**Estrutura esperada:**

```
# Política de Arquivamento

## Princípio
Nada é excluído. Tudo é arquivado.

## Estados
Estados possíveis de um registro (ativo, arquivado, obsoleto, etc).

## Transições
Quando e como registros mudam de estado.

## Histórico
Como o histórico de estados é preservado.

## Consultas
Como registros arquivados aparecem (ou não) em consultas.

## Restauração
Quando e como um registro arquivado retorna ao estado ativo.

## Exemplos
Casos concretos.
```

---

### Tarefa 2.4 — Política de Revisão

**Arquivo:** `docs/04-padroes/politica-revisao.md`

**O que fazer:**
Definir formalmente como registros são aprovados, alterados e auditados.

**Estrutura esperada:**

```
# Política de Revisão

## Ciclo de Aprovação
Quando um registro precisa de aprovação.

## Responsáveis
Quem pode aprovar, alterar, revisar.

## Rastreabilidade
Como mudanças são rastreadas.

## Auditoria
Como o histórico de revisões é consultado.

## Reversão
Quando e como uma mudança é revertida.

## Exemplos
Casos concretos.
```

---

### Tarefa 2.5 — Política de Conflito

**Arquivo:** `docs/04-padroes/politica-conflito.md`

**O que fazer:**
Definir formalmente como conflitos entre regras ou camadas são resolvidos.

**Estrutura esperada:**

```
# Política de Conflito

## Definição
O que é um conflito no SOE-CCG.

## Hierarquia
Ordem de precedência entre camadas (Constituição > Governança > Domínio > Implementação).

## Detecção
Como conflitos são identificados.

## Resolução
Processo para resolver conflito.

## Quando Constituição é contraditória
Como conflitos internos da constituição são resolvidos (quem decide).

## Quando Entidade conflita com Contrato
O que acontece quando uma evolução de entidade quebra contrato anterior.

## Casos Especiais
Situações onde regras normais não se aplicam.

## Exemplos
Casos concretos de conflito e sua resolução.
```

---

## 🟡 PRIORIDADE 3 — Formalizar FASE 4 (Domínio)

### Tarefa 3.1 — Separar Domínios

**Arquivos:**
- `docs/01-dominio/dominio-gastronomico.md` (novo)
- `docs/01-dominio/dominio-sistema.md` (novo)

**O que fazer:**

**dominio-gastronomico.md:**
Definir conceitos do problema: ingrediente, técnica, equipamento, receita no sentido gastronômico.

**dominio-sistema.md:**
Definir conceitos do SOE-CCG: registro, entidade, estado, catálogo no sentido do sistema.

**Critério de conclusão:** fica claro que "Ingrediente" é um conceito gastronômico implementado como "Entidade" no sistema.

---

### Tarefa 3.2 — Template de Especificação de Entidade

**Arquivo:** `docs/01-dominio/template-especificacao-entidade.md`

**O que fazer:**
Criar template formal para especificar cada entidade.

**Estrutura esperada:**

```
# Template de Especificação de Entidade

## Uso
Este template deve ser usado para especificar cada entidade do SOE-CCG.

## Estrutura

### 1. Identidade
O que é esta entidade? Definição em uma frase.

### 2. Responsabilidade
Para que esta entidade existe? O que ela resolve?

### 3. Limites
O que esta entidade NUNCA faz? Responsabilidades que NÃO são dela.

### 4. Atributos
Quais campos possui? (referência ao esquema)

### 5. Estados
Quais estados pode assumir? Diagrama de transição.

### 6. Eventos
O que pode acontecer com esta entidade? (criação, alteração, arquivamento, etc)

### 7. Relacionamentos
Com quem se relaciona? Natureza de cada relacionamento.

### 8. Dependências
De quais outras entidades ou conceitos depende?

### 9. Restrições
Regras que esta entidade deve sempre obedecer (invariantes).

### 10. Ciclo de Vida
Nascimento: como é criada
Evolução: como muda ao longo do tempo
Arquivamento: quando e como sai de circulação

## Exemplo
[exemplo completo usando uma entidade]
```

---

### Tarefa 3.3 — Especificar Entidade: Registro

**Arquivo:** `docs/01-dominio/especificacao-registro.md`

**O que fazer:**
Aplicar template de especificação à entidade fundamental "Registro".

**Usar:** template criado em Tarefa 3.2.

**Critério de conclusão:** especificação completa, sem ambiguidades.

---

### Tarefa 3.4 — Especificar Entidade: Receita

**Arquivo:** `docs/01-dominio/especificacao-receita.md`

**O que fazer:**
Aplicar template de especificação à entidade "Receita".

---

### Tarefa 3.5 — Especificar Entidade: Ingrediente

**Arquivo:** `docs/01-dominio/especificacao-ingrediente.md`

---

### Tarefa 3.6 — Especificar Entidade: Técnica

**Arquivo:** `docs/01-dominio/especificacao-tecnica.md`

---

### Tarefa 3.7 — Especificar Entidade: Equipamento

**Arquivo:** `docs/01-dominio/especificacao-equipamento.md`

---

### Tarefa 3.8 — Especificar Entidade: Execução

**Arquivo:** `docs/01-dominio/especificacao-execucao.md`

---

### Tarefa 3.9 — Especificar Entidade: Observação

**Arquivo:** `docs/01-dominio/especificacao-observacao.md`

---

### Tarefa 3.10 — Especificar Entidade: Experimento

**Arquivo:** `docs/01-dominio/especificacao-experimento.md`

---

## Ordem de Execução Recomendada

1. **Tarefa 1.1** — Filosofia (desbloqueia entendimento geral)
2. **Tarefa 1.2** — Conceitos Fundamentais (base conceitual)
3. **Tarefas 2.1 a 2.5** — Políticas (pode ser paralelo)
4. **Tarefa 3.1** — Separação de Domínios (esclarece planos)
5. **Tarefa 3.2** — Template de Especificação
6. **Tarefas 3.3 a 3.10** — Especificações de Entidades (pode ser paralelo)

---

## Estimativa de Esforço

| Tarefa | Complexidade | Esforço |
|--------|--------------|---------|
| 1.1 | Alta | 3-4h |
| 1.2 | Média | 1-2h |
| 2.1-2.5 | Média cada | 1-2h cada |
| 3.1 | Média | 2h |
| 3.2 | Alta | 3h |
| 3.3-3.10 | Média cada | 1-2h cada |

**Total estimado:** 25-35 horas de trabalho focado.

---

## Após Conclusão

Com estas tarefas concluídas:
- FASE 1 estará completa
- FASE 2 estará completa
- FASE 4 estará estruturada formalmente

Isso permitirá avançar para:
- FASE 3 — Linguagem (vocabulário formalizado)
- FASE 5 — Contratos (template já existirá)
- Demais fases sequencialmente
