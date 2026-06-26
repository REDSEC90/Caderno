# Roadmap Mestre — Fundação do SOE-CCG

> Roadmap de maturidade arquitetural, não de tarefas.
>
> O objetivo é eliminar toda ambiguidade do sistema antes da primeira linha de código.

## Critério de Conclusão da Fundação

Um desenvolvedor experiente, sem acesso ao código original e apenas com a documentação do SOE-CCG, consegue implementar um sistema compatível, chegando às mesmas decisões arquiteturais e ao mesmo comportamento esperado.

Quando esse critério for atendido, a documentação deixa de ser apenas documentação e passa a ser a **especificação oficial do sistema**.

---

## FASE 0 — Identidade (Concluída)

**Objetivo:** responder "o que é o SOE-CCG?"

- [x] Nome
- [x] Missão
- [x] Visão
- [x] Objetivos
- [x] Escopo
- [x] Filosofia
- [x] Estrutura inicial
- [x] Organização documental

---

## FASE 1 — Constituição

**Objetivo:** definir as leis permanentes do sistema. Nada abaixo poderá contrariar esta camada.

**Pré-requisito:** Fase 0 concluída.

### Unidade 1 — Filosofia

- [ ] Papel do conhecimento
- [ ] Fonte da verdade
- [ ] Papel do Markdown
- [ ] Papel do SQLite
- [ ] Papel da implementação

### Unidade 2 — Leis Fundamentais

- [ ] O que nunca muda
- [ ] Invariantes
- [ ] Restrições permanentes

```
Todo registro possui ID permanente.
Todo relacionamento ocorre por ID.
Conhecimento nunca depende da implementação.
Markdown é o formato canônico.
```

### Unidade 3 — Conceitos Fundamentais

Definir formalmente: Registro, Entidade, Relacionamento, Versão, Estado, Histórico, Catálogo, Template, Esquema, Metadado, Tag, Referência.

- [ ] Cada conceito definido com precisão suficiente para não admitir segunda interpretação

---

## FASE 2 — Governança

**Objetivo:** definir a administração do sistema.

**Pré-requisito:** Fase 1 concluída.

- [ ] Política de Identificadores — estrutura, prefixos, imutabilidade, geração, reserva, compatibilidade
- [ ] Política de Versionamento — versionamento lógico, estrutural, compatibilidade, depreciação
- [ ] Política de Metadados — obrigatórios, opcionais, tipagem, evolução
- [ ] Política de Templates — nascimento, evolução, compatibilidade, versionamento
- [ ] Política de Esquemas — estrutura, evolução, compatibilidade
- [ ] Política de Arquivamento — estados, histórico, nunca excluir
- [ ] Política de Revisão — aprovação, alteração, auditoria
- [ ] Política de Conflito — resolução quando regras se contradizem, o que ocorre quando uma entidade evolui quebrando um contrato anterior

---

## FASE 3 — Linguagem do SOE-CCG

**Objetivo:** criar o vocabulário oficial e eliminar ambiguidade terminológica. Nenhuma palavra terá dois significados.

**Pré-requisito:** Fase 2 concluída.

- [ ] Vocabulário — todos os termos oficiais do domínio
- [ ] Estrutura léxica — como os documentos são escritos
- [ ] Estrutura de relacionamento — como as entidades se conectam
- [ ] Semântica — o que cada elemento significa no domínio
- [ ] Glossário Oficial

> Nota: os termos "gramática" e "sintaxe" foram evitados deliberadamente para não conflitar com seus significados técnicos em linguística e teoria de linguagens formais — o que violaria o próprio princípio desta fase.

---

## FASE 4 — Domínio

**Objetivo:** especificar cada entidade do sistema.

**Pré-requisito:** Fase 3 concluída.

> Esta fase opera em dois planos distintos que devem ser mantidos separados:
> - **Domínio gastronômico** — ingredientes, técnicas, execuções (conceitos do problema)
> - **Domínio do sistema** — registros, entidades, estados, catálogos (conceitos do SOE-CCG)

Para cada entidade, responder:

- [ ] Identidade — o que é?
- [ ] Responsabilidade — para que existe?
- [ ] Limites — o que nunca faz?
- [ ] Atributos — quais campos possui?
- [ ] Estados — como evolui?
- [ ] Eventos — o que pode acontecer?
- [ ] Relacionamentos — com quem conversa?
- [ ] Dependências — do que depende?
- [ ] Restrições — o que é proibido?
- [ ] Ciclo de vida — nascimento, evolução, arquivamento

---

## FASE 5 — Contratos

**Objetivo:** cada entidade recebe um contrato formal.

**Pré-requisito:** Fase 4 concluída.

> Antes de escrever os contratos das entidades, esta fase deve produzir um único entregável intermediário: o **template canônico de contrato**. Sem ele, cada contrato terá forma diferente.

O template canônico de contrato inclui:

- [ ] Template canônico de contrato definido

Para cada entidade, o contrato define:

- [ ] Campos obrigatórios
- [ ] Campos opcionais
- [ ] Tipos
- [ ] Restrições
- [ ] Valores aceitos
- [ ] Cardinalidade
- [ ] Validação
- [ ] Compatibilidade
- [ ] Eventos
- [ ] Pré-condições
- [ ] Pós-condições
- [ ] Invariantes

---

## FASE 6 — Catálogos

**Objetivo:** padronizar todos os valores reutilizáveis do sistema.

**Pré-requisito:** Fase 5 concluída.

- [ ] Categorias
- [ ] Estados
- [ ] Tipos
- [ ] Unidades
- [ ] Classificações
- [ ] Escalas
- [ ] Materiais
- [ ] Métodos
- [ ] Vocabulário controlado

---

## FASE 7 — Relacionamentos

**Objetivo:** desenhar o sistema inteiro no plano do domínio, não apenas ER.

**Pré-requisito:** Fase 6 concluída.

Exemplo:

```
Receita → utiliza → Ingrediente → executada por → Execução → gera → Observação
```

Cada relacionamento recebe:

- [ ] Nome
- [ ] Direção
- [ ] Cardinalidade
- [ ] Restrições
- [ ] Significado

---

## FASE 8 — Padrões

**Objetivo:** definir as convenções de implementação.

**Pré-requisito:** Fase 7 concluída.

- [ ] Nomenclatura
- [ ] Estrutura Markdown
- [ ] Estrutura SQLite
- [ ] Convenções
- [ ] Organização
- [ ] Importação
- [ ] Exportação
- [ ] Validação
- [ ] Logs
- [ ] Erros
- [ ] Mensagens

---

## FASE 9 — Modelagem

**Objetivo:** desenhar os modelos de dados. SQLite aparece somente aqui.

**Pré-requisito:** Fase 8 concluída.

```
Modelo Conceitual → Modelo Lógico → Modelo Físico → SQLite
```

- [ ] Modelo conceitual
- [ ] Modelo lógico
- [ ] Modelo físico
- [ ] Esquema SQLite

---

## FASE 10 — Dados Canônicos

**Objetivo:** registrar os primeiros dados reais do sistema.

**Pré-requisito:** Fase 9 concluída. Somente agora existe domínio suficiente.

- [ ] Ingredientes
- [ ] Equipamentos
- [ ] Técnicas
- [ ] Receitas
- [ ] Execuções
- [ ] Observações
- [ ] Experimentos

---

## FASE 11 — Casos de Uso

**Objetivo:** documentar todos os fluxos do usuário.

**Pré-requisito:** Fase 10 concluída.

- [ ] Usuário registra ingrediente
- [ ] Usuário registra execução
- [ ] Usuário consulta técnica
- [ ] Usuário compara versões
- [ ] Usuário importa documentos
- [ ] Usuário exporta catálogo

---

## FASE 12 — Validação Arquitetural

**Objetivo:** verificar que a especificação formal emergiu — que toda ambiguidade foi eliminada.

**Pré-requisito:** Fases 1 a 11 concluídas.

> Esta fase não pergunta "todos os documentos foram escritos?". Pergunta "o sistema é implementável por qualquer desenvolvedor experiente apenas pela documentação?". A diferença é fundamental.
>
> Além do checklist de completude, esta fase exige uma revisão cruzada: leitura da documentação com objetivo explícito de encontrar decisões não cobertas.

### Checklist de Completude

- [ ] Constituição completa?
- [ ] Governança completa?
- [ ] Entidades completas?
- [ ] Templates completos?
- [ ] Contratos completos?
- [ ] Catálogos completos?
- [ ] IDs definidos?
- [ ] Relacionamentos definidos?
- [ ] Casos de uso definidos?

### Critério Final

- [ ] Nenhuma ambiguidade restante?
- [ ] Um desenvolvedor externo consegue implementar um sistema compatível apenas com esta documentação?

Somente quando todas as respostas forem "sim", o projeto passa para a implementação.

---

## FASE 13 — Implementação

**Objetivo:** implementar o sistema que já existe conceitualmente.

**Pré-requisito:** Fase 12 aprovada integralmente.

```
Importador → Validador → SQLite → CLI → API → Interface
```

---

## Nota sobre a Especificação Formal

A especificação formal não é um documento a ser escrito — ela é o produto final emergente de todas as fases anteriores quando constituição, governança, linguagem, domínio, contratos, catálogos, relacionamentos, padrões e modelagem estão coerentes entre si.

A Fase 12 verifica que essa especificação emergiu. Se o checklist passa, a especificação formal existe. O critério de maturidade — implementabilidade independente — é o teste dessa emergência.
