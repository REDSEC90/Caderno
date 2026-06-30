# Troubleshooting — Resolver

> Diagnóstico de falhas no componente Resolver (`codigo/resolvedor-v1.py`).

**O Resolver verifica se cada ID referenciado em um arquivo realmente existe no sistema.**  
Ele falha quando um arquivo referencia IDs que não existem, ou quando entidades foram arquivadas mas ainda são referenciadas.

---

## Como executar o Resolver isoladamente

```bash
# Resolver opera sobre o grafo inteiro (precisa parsear tudo primeiro)
python3 -m codigo --ate-resolver

# Ou verificar referências de um arquivo específico
python3 codigo/resolvedor-v1.py dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

---

## Problema 1: `referencia_quebrada: ING-000099`

**Sintoma:**
```
ResolverError: referencia_quebrada em REC-000002
  → ING-000099 não existe no sistema
```

**Causa:** O arquivo referencia um ID que não existe em nenhum arquivo de `dados/`.

**Diagnóstico:**
```bash
# Verificar se existe no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE id = 'ING-000099';"

# Verificar se existe como arquivo
ls dados/ingredientes/ | grep "000099"
```

**Soluções possíveis:**

*Opção A — O ID está errado no arquivo de origem:*
```bash
# Abrir o arquivo que tem a referência errada
nano dados/receitas/REC-000002-minha-receita-v1.md
# Corrigir o ID para o valor correto
```

*Opção B — A entidade referenciada ainda não foi criada:*
```bash
# Criar o ingrediente primeiro
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000099-nome-do-ingrediente-v1.md
# Editar, importar, depois importar o arquivo que o referencia
```

**Como evitar:** Sempre criar as dependências antes de referenciar. A ordem correta é `EQP → TEC → ING → REC → EXE → OBS/EXP`.

---

## Problema 2: Referência a entidade arquivada

**Sintoma:**
```
ResolverWarning: REC-000002 referencia ING-000005 (status: arquivado)
```

**Causa:** Um arquivo referencia uma entidade que existe mas está arquivada.

**Diagnóstico:**
```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome, status FROM ingredientes WHERE id = 'ING-000005';"
```

**Soluções possíveis:**

*Opção A — Migrar a referência para o ID correto:*
```bash
# Ver qual é o ID canônico que substituiu o arquivado
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT * FROM ingredientes WHERE id = 'ING-000005';"
# Geralmente o campo motivo-arquivamento indica para qual ID migrar

# Atualizar o arquivo de origem
nano dados/receitas/REC-000002-minha-receita-v1.md
# Trocar ING-000005 pelo ID correto
```

*Opção B — Reativar a entidade (se o arquivamento foi um erro):*
```bash
nano dados/ingredientes/ING-000005-slug-v1.md
# Alterar status: arquivado → status: ativo
scripts/importacao/importar.sh dados/ingredientes/ING-000005-slug-v1.md
```

---

## Problema 3: Ciclo de referências STRUCTURAL

**Sintoma:**
```
ValidatorError: ciclo detectado — REC-000001 → ING-000001 → REC-000001
  arestas STRUCTURAL formam ciclo
```

**Causa:** Duas entidades se referenciam mutuamente em campos estruturais.

**Diagnóstico:**
```bash
python3 scripts/auditoria/auditor-v1.py entity REC-000001
python3 scripts/auditoria/auditor-v1.py entity ING-000001
```

Ver o `kind` das arestas. Arestas STRUCTURAL em ciclo são sempre erro. Arestas INFORMATIONAL em ciclo são semanticamente válidas (menções cruzadas).

**Solução:** Revisar os frontmatters. Um dos dois arquivos tem uma referência incorreta no campo estrutural. Ingredientes não referenciam Receitas em campos estruturais — a relação é unidirecional (REC → ING).

---

## Problema 4: Arquivo importado mas referências não aparecem no banco

**Sintoma:** O arquivo foi importado sem erros, mas `SELECT ... FROM relacionamentos WHERE source = 'REC-000001'` não retorna as arestas esperadas.

**Diagnóstico:**
```bash
# Ver o que o Parser extraiu (antes de importar)
python3 codigo/parser-v1.py dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md --verbose
```

**Causa provável:** Os IDs estão no corpo do documento em um formato não reconhecido, ou em um campo de frontmatter com nome não canônico.

Ver [Problema 5 do Troubleshooting do Parser](01-parser-v1.md#problema-5-aresta-não-detectada) para os campos reconhecidos.

---

## Próxima leitura

- Se o Resolver passou mas há erros de validação → [`03-validador-v1.md`](03-validador-v1.md)
- Se o banco não está populado corretamente → [`05-sqlite-v1.md`](05-sqlite-v1.md)
- Catálogo completo → [`../03-validacao/07-resolucao-de-erros-v1.md`](../03-validacao/07-resolucao-de-erros-v1.md)
