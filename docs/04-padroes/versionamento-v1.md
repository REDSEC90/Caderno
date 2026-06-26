# Versionamento — Padrões

Política oficial de versionamento do SOE-CCG.

A definição estrutural está em `docs/02-arquitetura/versionamento.md`.

Este documento define as políticas de uso.

---

## Versão do Registro (`versao`)

Incrementa quando o conteúdo do registro sofre alteração relevante.

**O que gera incremento:**
- Alteração no modo de preparo.
- Adição ou remoção de ingrediente, técnica ou equipamento.
- Mudança de título ou descrição.
- Alteração de qualquer campo de conteúdo.

**O que não gera incremento:**
- Correção de erro tipográfico sem alteração de significado.
- Adição de tag.
- Atualização de `atualizado-em`.

## Versão do Esquema (`schema-version`)

Incrementa quando a estrutura de campos da entidade muda.

Um registro preserva a `schema-version` com que foi criado.

Migração para nova versão de esquema é opcional e documentada em `banco_de_dados/migracoes/`.

## Versão do Template

Expressa no nome do arquivo: `receita-v1.md`, `receita-v2.md`.

Templates anteriores são preservados indefinidamente.

Novos registros devem usar sempre o template mais recente.

---

## Regras Gerais

- Versões nunca retrocedem.
- Versões nunca são destruídas.
- `versao: 1` é o valor inicial de todo registro novo.
- `schema-version: 1` é o valor inicial de todo esquema novo.
