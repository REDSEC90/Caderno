# Identificadores

Política oficial de identificadores do SOE-CCG.

A definição estrutural está em `docs/03-modelagem/ids.md`.

Este documento define as políticas de uso e atribuição.

---

## Política de Atribuição

- O ID é atribuído pelo autor no momento da criação do arquivo.
- A sequência é controlada manualmente até existir um gerador automatizado.
- O próximo ID disponível por prefixo deve ser consultado nos arquivos existentes em `dados/`.

## Política de Imutabilidade

- Nenhum ID pode ser alterado após a criação do registro.
- Nenhum ID pode ser reutilizado, mesmo após arquivamento ou exclusão lógica do registro.

## Política de Referência

- Todo relacionamento entre registros usa exclusivamente IDs.
- Nomes não podem ser usados como referência entre registros.
- Se o nome de uma entidade mudar, nenhuma referência existente precisa ser atualizada.

## Política de Formato

- O formato `[PREFIXO]-[NNNNNN]` é obrigatório e não admite variações.
- Zeros à esquerda são obrigatórios para completar 6 dígitos.
- Prefixos são sempre maiúsculos.

## Controle de Sequência

Até a existência de automação, manter registro do último ID utilizado por prefixo em:

```
docs/04-padroes/identificadores.md  ← este arquivo
```

| Prefixo | Último ID utilizado |
|---------|---------------------|
| `REC`   | REC-000001          |
| `EXE`   | —                   |
| `ING`   | —                   |
| `TEC`   | —                   |
| `EQP`   | —                   |
| `OBS`   | —                   |
| `EXP`   | —                   |
| `CAT`   | —                   |
