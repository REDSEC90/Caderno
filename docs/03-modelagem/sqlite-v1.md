# SQLite

Define o papel, as convenções e as decisões de uso do SQLite no SOE-CCG.

---

## Papel

O SQLite é o mecanismo de consulta do SOE-CCG.

Não é a fonte do conhecimento.

O banco é sempre derivado de `dados/` e pode ser reconstruído a qualquer momento.

---

## Localização

```
banco_de_dados/sqlite/
```

---

## Convenções

### Nomes de tabelas

Minúsculas, plural, separados por underline.

```
receitas
execucoes
ingredientes
tecnicas
equipamentos
observacoes
experimentos
categorias
receita_ingrediente
receita_tecnica
receita_equipamento
receita_categoria
experimento_receita
```

### Nomes de colunas

Minúsculas, separados por underline.

```
id
schema_version
criado_em
atualizado_em
receita_id
entidade_tipo
```

### Tipos

| Dado               | Tipo SQLite |
|--------------------|-------------|
| ID                 | TEXT        |
| Texto curto        | TEXT        |
| Texto longo        | TEXT        |
| Data               | TEXT (ISO 8601: YYYY-MM-DD) |
| Número inteiro     | INTEGER     |
| Número decimal     | REAL        |
| Booleano           | INTEGER (0 ou 1) |

---

## Regras

- Toda tabela possui `id` como chave primária do tipo TEXT.
- Toda tabela possui `criado_em` e `atualizado_em`.
- Foreign keys são habilitadas por sessão com `PRAGMA foreign_keys = ON`.
- O banco não armazena informação que não exista em `dados/`.
- Migrações de esquema são documentadas em `banco_de_dados/migracoes/`.
