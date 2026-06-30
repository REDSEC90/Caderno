# Manual para Agentes — SOE-CCG

> Protocolo formal para operação automatizada do sistema.

Esta seção é normativa para qualquer sistema automatizado — scripts, pipelines de CI/CD, agentes de IA — que opere sobre o repositório.

---

## Índice

| Arquivo | Conteúdo |
|---------|----------|
| [`01-protocolo-operacional-v1.md`](01-protocolo-operacional-v1.md) | Sequência obrigatória para cada operação de escrita |
| [`02-invariantes-v1.md`](02-invariantes-v1.md) | 8 regras que nunca têm exceção |
| [`03-sequencias-validas-v1.md`](03-sequencias-validas-v1.md) | O que fazer, em que ordem, em cada situação |

---

## Leitura obrigatória antes de implementar qualquer agente

```
02-invariantes-v1.md           ← primeiro: o que nunca fazer
01-protocolo-operacional-v1.md ← segundo: como estruturar cada operação
03-sequencias-validas-v1.md    ← terceiro: sequências completas por cenário
```

Depois: [`../07-referencia/comandos-v1.md`](../07-referencia/comandos-v1.md) para a referência de comandos.

---

## Princípio fundamental

O agente é um operador do sistema, não o sistema. Toda decisão de negócio pertence ao humano. O agente executa operações dentro das regras — não as define, não as contorna.
