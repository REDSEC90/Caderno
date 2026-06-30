# Troubleshooting — SOE-CCG

> Diagnóstico por componente. Encontre o problema, vá direto ao arquivo certo.

---

## Qual componente está falhando?

```
Erro ao ler o arquivo .md
      → 01-parser-v1.md

ID não encontrado / referência quebrada
      → 02-resolver-v1.md

Ciclo detectado / status inválido
      → 03-validador-v1.md

Script de importação falhou
      → 04-importador-v1.md

Banco vazio / dessincronizado
      → 05-sqlite-v1.md

FAA reprovado / score baixo
      → 06-faa-v1.md
```

---

## Índice

| Arquivo | Componente | Problemas cobertos |
|---------|------------|-------------------|
| [`01-parser-v1.md`](01-parser-v1.md) | Parser | Frontmatter ausente, ID inválido, aresta não detectada |
| [`02-resolver-v1.md`](02-resolver-v1.md) | Resolver | Referência quebrada, entidade arquivada referenciada, ciclos |
| [`03-validador-v1.md`](03-validador-v1.md) | Validador | Status inválido, entidade isolada, regras de negócio |
| [`04-importador-v1.md`](04-importador-v1.md) | Importador | Script de importação, arquivos não encontrados |
| [`05-sqlite-v1.md`](05-sqlite-v1.md) | SQLite | Banco vazio, entidade não aparece, dessincronização |
| [`06-faa-v1.md`](06-faa-v1.md) | FAA | Score baixo, sistema reprovado, artefato ausente, ciclos |

---

## Diagnóstico geral rápido

Se não souber qual componente está falhando:

```bash
# 1. Rodar o pipeline completo e ver onde falha
python3 -m codigo 2>&1 | head -30

# 2. Rodar o FAA e ver as issues
python3 scripts/auditoria/auditor-v1.py issues --critical

# 3. Inspecionar uma entidade suspeita
python3 scripts/auditoria/auditor-v1.py entity [ID-SUSPEITO]
```

---

## Erros mais comuns (atalho)

| Mensagem de erro | Ir para |
|-----------------|---------|
| `No module named 'frontmatter'` | [Parser #6](01-parser-v1.md#problema-6-no-module-named-frontmatter) |
| `frontmatter ausente` | [Parser #1](01-parser-v1.md#problema-1-frontmatter-ausente-ou-no-frontmatter-found) |
| `KeyError: 'id'` | [Parser #2](01-parser-v1.md#problema-2-keyerror-id-ou-id-ausente-no-frontmatter) |
| `referencia_quebrada: ING-000099` | [Resolver #1](02-resolver-v1.md#problema-1-referencia_quebrada-ing-000099) |
| `[BAS-002] artefato ausente` | [FAA #1](06-faa-v1.md#problema-1-bas-002-sistema-reprovado--artefato-ausente) |
| `[DEP-002] ciclo detectado` | [FAA #2](06-faa-v1.md#problema-2-dep-002-ciclo-detectado) |
| `YYYY-MM-DD` literal no frontmatter | [FAA #3](06-faa-v1.md#problema-3-dad-001-frontmatter-inválido-em-dados) |
| Banco vazio após importar | [SQLite #2](05-sqlite-v1.md#problema-2-entidade-importada-mas-não-aparece-no-banco) |

---

## Último recurso

Se o problema não está coberto aqui:

```bash
# Ver o catálogo completo de erros
cat docs/07-uso/03-validacao/07-resolucao-de-erros-v1.md

# Ver os exemplos reais de como o sistema funciona
cat docs/07-uso/08-exemplos-reais-v1.md
```
