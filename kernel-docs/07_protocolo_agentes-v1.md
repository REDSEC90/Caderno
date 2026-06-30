---
id: KDOC-007
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Protocolo de Agentes

## Autoridades

- Codex executa alteracoes no repositorio.
- Claude pode propor arquitetura e revisar decisao conceitual.
- Kernel e a autoridade final para enforcement tecnico automatizado.

## Ordem de Decisao

1. Constituicao do projeto.
2. Kernel-docs.
3. Contratos do kernel.
4. Testes automatizados.
5. Implementacao atual.

## Regra para Agentes

Um agente nao deve implementar nova estrutura se ela violar `kernel-docs/`.

Quando houver conflito entre conveniencia local e regra do kernel, a regra do kernel vence.
