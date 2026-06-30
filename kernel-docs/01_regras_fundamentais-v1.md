---
id: KDOC-001
tipo: kernel-doc
versao: 1
status: ativo
autor: SOE-CCG
---

# Regras Fundamentais

## Dependencia Unidirecional

O fluxo permitido e:

```text
aplicacoes -> modulos -> kernel
```

O kernel nunca importa `codigo`, `scripts`, `dados` ou qualquer implementacao de negocio.

## Paths

`kernel/shared/paths.py` e a unica fonte de verdade para paths estruturais.

Arquivos fora dele nao podem definir:

```python
ROOT = Path(__file__)
```

## Imports

Imports circulares sao proibidos.

Adapters de `sys.path` sao tolerados apenas em entrypoints legados enquanto `scripts/` nao for pacote Python instalavel.

## Determinismo

O bootstrap deve ser repetivel.

Inicializar o kernel duas vezes deve registrar os mesmos modulos, na mesma ordem logica e com os mesmos contratos.
