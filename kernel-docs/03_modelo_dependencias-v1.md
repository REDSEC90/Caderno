---
id: KDOC-003
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Modelo de Dependencias

## Camadas

```text
docs/00-projeto/constituicao-v1.md
        ↓
kernel-docs/
        ↓
kernel/
        ↓
codigo/ e scripts/
        ↓
entrypoints
```

## Registro

Cada modulo registrado declara:

- `name`
- `version`
- `provides`
- `requires`
- `entrypoint`
- `description`

## Resolucao

O registry resolve dependencias por capacidade, nao por import direto.

Se dois modulos fornecem a mesma capacidade, o sistema falha antes da execucao.

Se uma capacidade exigida nao tem provedor, o sistema falha antes da execucao.

Se ha ciclo de dependencias, o sistema falha antes da execucao.
