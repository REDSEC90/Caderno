# Template de Especificação de Entidade

> Modelo canônico para documentar cada entidade do SOE-CCG com precisão suficiente para implementação independente.

---

## Uso

Este template deve ser aplicado a cada entidade oficial do SOE-CCG.

Toda especificação produzida com este template deve ser capaz de responder, sem ambiguidade, à pergunta de um desenvolvedor experiente que nunca viu o sistema.

---

## Estrutura Obrigatória

---

### 1. Identidade

> O que é esta entidade? Definição em uma frase, sem exemplos.

**Definição formal:**
[Uma frase única que identifica inequivocamente o que esta entidade representa no domínio gastronômico e no sistema.]

**Categoria gastronômica:**
[O que esta entidade representa no mundo real da culinária, independentemente do sistema.]

**Categoria no sistema:**
[Como o SOE-CCG modela esta entidade — tipo de registro, natureza, papel.]

---

### 2. Responsabilidade

> Para que esta entidade existe? O que ela resolve?

**Propósito principal:**
[Uma frase. O que acontece de errado se esta entidade não existir?]

**Responsabilidades explícitas:**
- [Responsabilidade 1]
- [Responsabilidade 2]
- [...]

---

### 3. Limites

> O que esta entidade NUNCA faz? Onde ela termina e outra começa?

**Esta entidade NÃO:**
- [Limitação 1 — o que pertence a outra entidade]
- [Limitação 2]
- [...]

**Fronteira com [Entidade X]:**
[Quando surge dúvida sobre se algo pertence a esta entidade ou a X, a regra é: ...]

---

### 4. Atributos

> Quais campos esta entidade possui?

Referência ao esquema: `docs/01-dominio/esquemas/esquema-[entidade]-v1.md`

**Campos obrigatórios resumidos:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | string | Identificador permanente |
| ... | ... | ... |

**Campos opcionais resumidos:**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| ... | ... | ... |

---

### 5. Estados

> Quais estados pode assumir? Quando e como transita?

**Estados possíveis:**

| Estado | Significado | Quem pode atribuir |
|--------|-------------|-------------------|
| ... | ... | ... |

**Diagrama de transição:**

```
[estado_inicial] → [estado_2] → [estado_final]
                       ↓
                   [estado_alternativo]
```

**Regras de transição:**
- De [A] para [B]: [condição]
- De [B] para [C]: [condição]

---

### 6. Eventos

> O que pode acontecer com esta entidade? Eventos são mudanças observáveis.

| Evento | Descrição | Gatilho |
|--------|-----------|---------|
| criação | Registro criado pela primeira vez | Usuário registra nova entidade |
| atualização | Campo modificado | Usuário altera informação |
| arquivamento | Registro sai do uso ativo | Estado transita para `arquivado` |
| ... | ... | ... |

---

### 7. Relacionamentos

> Com quem se relaciona? Qual a natureza de cada vínculo?

| Relacionamento | Com | Cardinalidade | Natureza |
|----------------|-----|---------------|----------|
| [verbo] | [Entidade] | 1:N / N:1 / N:N | [descrição] |

**Como o relacionamento é expresso:**
Por identificador permanente (`[PREFIXO]-NNNNNN`), nunca por nome.

---

### 8. Dependências

> De quais outras entidades ou conceitos esta entidade depende para existir ou funcionar?

**Dependências obrigatórias:**
- [Entidade ou conceito]: [por que depende]

**Dependências opcionais:**
- [Entidade ou conceito]: [quando se aplica]

---

### 9. Restrições

> Regras que esta entidade deve sempre obedecer. Invariantes.

1. [Restrição 1 — nunca pode ser violada]
2. [Restrição 2]
3. [...]

**Restrições herdadas da Constituição:**
- ID é imutável após criação
- Histórico nunca é destruído
- Relacionamentos usam IDs, nunca nomes

---

### 10. Ciclo de Vida

> Como esta entidade nasce, evolui e encerra?

**Nascimento:**
[Como um registro desta entidade é criado. Quem pode criar. Campos mínimos necessários.]

**Evolução:**
[Como o registro muda ao longo do tempo. O que pode ser alterado. O que não pode.]

**Arquivamento:**
[Quando e como o registro sai do uso ativo. O que ocorre com seus relacionamentos.]

---

## Exemplo de Aplicação

Ver `docs/01-dominio/especificacao-receita.md` como referência de especificação completa.

---

## Critério de Completude

Uma especificação produzida com este template está completa quando:

1. Um desenvolvedor que nunca viu o sistema consegue implementar a entidade corretamente.
2. Não há nenhuma pergunta óbvia sobre a entidade que o documento não responda.
3. Os limites estão suficientemente definidos para que não haja confusão com outras entidades.
4. Todos os campos do esquema são justificados pelos atributos documentados.
