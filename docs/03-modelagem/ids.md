# Identificadores

Define o sistema de identificação permanente de todos os registros do SOE-CCG.

---

## Formato

```
[PREFIXO]-[NÚMERO]
```

O número possui 6 dígitos com zeros à esquerda.

---

## Prefixos

| Prefixo | Entidade     |
|---------|--------------|
| `REC`   | Receita      |
| `EXE`   | Execução     |
| `ING`   | Ingrediente  |
| `TEC`   | Técnica      |
| `EQP`   | Equipamento  |
| `OBS`   | Observação   |
| `EXP`   | Experimento  |
| `CAT`   | Categoria    |

---

## Exemplos

```
REC-000001
ING-000042
TEC-000007
EQP-000003
EXE-000001
OBS-000015
EXP-000002
CAT-000001
```

---

## Regras

- O ID é atribuído na criação do registro e nunca muda.
- O ID nunca é reutilizado, mesmo que o registro seja arquivado.
- O nome pode mudar. A descrição pode mudar. O ID permanece.
- Relacionamentos entre registros sempre usam IDs, nunca nomes.
- A sequência numérica é global por prefixo e sempre crescente.
- O número inicial é `000001`.
