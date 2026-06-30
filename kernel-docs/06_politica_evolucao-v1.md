---
id: KDOC-006
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Politica de Evolucao

## Freeze

Durante estabilizacao do kernel:

- nao criar features fora do kernel;
- nao mover `codigo/` sem adapter;
- nao remover FAA legado sem paridade de output;
- nao alterar documentos `v1` sem criar nova versao.

## Mudanca Estrutural

Toda mudanca estrutural deve:

1. atualizar `kernel-docs/` quando mudar regra;
2. atualizar contrato quando mudar mecanismo;
3. passar nos testes;
4. preservar compatibilidade dos entrypoints existentes.

## Criterio de Aceite

Uma mudanca estrutural so esta aceita quando `kernel.contracts.validator.validate_architecture()` retorna sem erros.
