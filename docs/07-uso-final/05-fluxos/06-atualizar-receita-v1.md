# Fluxo: Atualizar uma Receita Existente

> Três cenários: correção simples, adição de ingrediente, e reformulação completa.

---

## Cenário A — Correção ou Adição de Informação

**Situação:** Descobriu que o tempo de preparo do Doce de Leite é 2h, não "~2h estimado".

```bash
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

# Alterar no conteúdo:
# - **Tempo de preparo:** ~2h (estimado) → 2h (confirmado em EXE-000001)
# Alterar no frontmatter:
# atualizado-em: 2026-06-27

scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
git commit -am "fix(rec): corrige tempo de preparo de REC-000001 para 2h confirmado"
```

---

## Cenário B — Adicionar um Ingrediente

**Situação:** Decidiu adicionar extrato de baunilha como ingrediente opcional.

### B1. Verificar se o ingrediente existe

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%baunilha%';"
```

### B2. Criar se não existir

```bash
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000010-extrato-baunilha-v1.md
# Editar e importar
scripts/importacao/importar.sh dados/ingredientes/ING-000010-extrato-baunilha-v1.md
```

### B3. Adicionar à Receita

```bash
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

No frontmatter:
```yaml
ingredientes: [ING-000001, ING-000002, ING-000003, ING-000004, ING-000010]
```

Na tabela de ingredientes do corpo:
```markdown
| ING-000010 | Extrato de Baunilha | 5 | ml |
```

```bash
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
git commit -am "feat(rec): adiciona ING-000010 extrato-baunilha como ingrediente de REC-000001"
```

---

## Cenário C — Reformulação Completa (nova versão formal)

**Situação:** A receita foi completamente revisada com novas proporções, nova técnica e resultado muito diferente.

```bash
# Criar v2
cp dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md \
   dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md

nano dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md
# versao: 2
# atualizado-em: 2026-06-27
# Fazer as alterações de conteúdo

# Arquivar v1
nano dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
# status: arquivada

# Importar ambas
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md
scripts/importacao/importar.sh dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md

git add dados/receitas/
git commit -m "feat(rec): versao v2 de REC-000001 com proporcoes revisadas"
```

---

## Verificação final (para qualquer cenário)

```bash
# Verificar que o banco reflete a edição
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status, atualizado_em FROM receitas WHERE id = 'REC-000001';"
```

```
# Resultado esperado (campo atualizado_em com a data de hoje):
REC-000001|Doce de Leite Artesanal|testada|2026-06-28
```

---

## Problemas comuns

| Problema | Causa | Solução |
|----------|-------|---------|
| Banco ainda mostra dados antigos após edição | O arquivo foi editado mas não reimportado | `scripts/importacao/importar.sh [arquivo]` |
| Relacionamento removido mas ainda aparece no banco | Mesmo motivo | Reimportar — o importador sobrescreve os relacionamentos |
| `atualizado-em` não mudou no banco | Campo não foi atualizado no frontmatter | Sempre atualizar `atualizado-em` manualmente ao editar |

---

## Próxima leitura

- Registrar execuções com a receita atualizada → [`02-criar-execucao-v1.md`](02-criar-execucao-v1.md)
- Sessão completa de trabalho → [`07-fluxo-completo-v1.md`](07-fluxo-completo-v1.md)
