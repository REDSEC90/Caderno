# Versionamento

Define as camadas independentes de versionamento do SOE-CCG.

---

## Camadas de Versão

### Versão do Registro

Campo `versao` nos metadados de cada arquivo.

Incrementa quando o conteúdo do registro sofre alteração relevante.

```
versao: 1  →  versao: 2  →  versao: 3
```

### Versão do Esquema

Campo `schema-version` nos metadados de cada arquivo.

Incrementa quando a estrutura de campos de uma entidade muda.

```
esquema-receita-v1.md  →  esquema-receita-v2.md
```

Registros antigos preservam a versão de esquema com a qual foram criados.

### Versão do Template

Expressa no nome do arquivo.

```
receita-v1.md  →  receita-v2.md
```

Templates antigos são preservados para referência.

### Versão da Arquitetura

Documentada em `docs/02-arquitetura/` e controlada pelo histórico do repositório.

---

## Regras

- Versões nunca são destruídas.
- `versao` do registro é um inteiro incremental começando em `1`.
- `schema-version` do registro indica qual esquema foi usado na criação.
- Migração entre versões de esquema é documentada em `banco_de_dados/migracoes/`.
- As quatro camadas de versão são independentes entre si.
