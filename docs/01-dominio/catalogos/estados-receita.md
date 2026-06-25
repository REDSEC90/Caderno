# Estados de Receita

Catálogo controlado de estados válidos no ciclo de vida de uma Receita.

---

## Estados

| Código       | Descrição                                                              | Transições permitidas               |
|--------------|------------------------------------------------------------------------|--------------------------------------|
| `rascunho`   | Definição inicial, ainda não executada.                                | → `testada`                          |
| `testada`    | Executada ao menos uma vez.                                            | → `validada`, → `rascunho`           |
| `validada`   | Resultado considerado satisfatório e reproduzível.                     | → `publicada`, → `testada`           |
| `publicada`  | Conhecimento consolidado, referenciável por outras entidades.          | → `arquivada`                        |
| `arquivada`  | Mantida no histórico, fora de uso ativo. Não aceita novas execuções.   | —                                    |

---

## Regras

- Toda receita inicia no estado `rascunho`.
- O estado `arquivada` é terminal.
- Receitas arquivadas permanecem consultáveis e referenciáveis no histórico.
- A transição de estado é registrada nos metadados com data e motivo.
