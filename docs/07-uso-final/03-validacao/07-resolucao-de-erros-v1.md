# Resolução de Erros

> Catálogo de todos os erros conhecidos e como corrigi-los.

---

## Erros do Parser

### `frontmatter ausente`
**Causa:** O arquivo não tem os delimitadores `---`.
```markdown
# Errado — sem frontmatter
# Meu Ingrediente
Descrição aqui.
```
**Correção:**
```markdown
---
id: ING-000005
tipo: ingrediente
...
---
# Meu Ingrediente
```

### `KeyError: 'id'` ou `id ausente`
**Causa:** Campo `id` não está no frontmatter.
**Correção:** Adicionar `id: [PREFIXO]-[NNNNNN]` ao frontmatter.

### `ID inválido: ing-000005`
**Causa:** ID em minúsculas ou com formato incorreto.
**Correção:** O prefixo deve ser maiúsculo: `ING-000005`.

---

## Erros do Resolver

### `referencia_quebrada: ING-000099`
**Causa:** Uma entidade referencia `ING-000099` mas esse ID não existe no sistema.
**Diagnóstico:**
```bash
ls dados/ingredientes/ | grep "000099"
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM ingredientes WHERE id = 'ING-000099';"
```
**Correção:** Criar o ingrediente, ou corrigir o ID no arquivo de origem.

---

## Erros do FAA

### [BAS-002] Sistema reprovado — artefato ausente
**Causa:** Um documento obrigatório do baseline não existe.
**Diagnóstico:** A mensagem indica exatamente qual arquivo criar.
```
→ Criar: docs/00-projeto/visão-v1.md
```
**Correção:** Criar o arquivo com conteúdo mínimo válido:
```bash
cat > docs/00-projeto/visão-v1.md << 'EOF'
# Visão do SOE-CCG

> Declaração de visão de longo prazo do sistema.

## Visão

[Conteúdo da visão]
EOF
git add docs/00-projeto/visão-v1.md
git commit -m "docs(projeto): cria visão-v1 para completar baseline"
```

### [DEP-002] Ciclo detectado
**Diagnóstico:**
```bash
python3 scripts/auditoria/auditor-v1.py entity [ID-1]
python3 scripts/auditoria/auditor-v1.py entity [ID-2]
```
Ver o `kind` das arestas. Se todas forem INFORMATIONAL, o ciclo é semanticamente válido.
Se houver arestas STRUCTURAL no ciclo, revisar os relacionamentos — um dos vínculos está semanticamente incorreto.

### [ERR-000] No module named 'frontmatter'
```bash
pip install python-frontmatter --break-system-packages
```

---

## Erros de status inválido

**Causa:** O campo `status` tem um valor não reconhecido pelo catálogo.

**Diagnóstico:** Ver `docs/01-dominio/catalogos/estados-todas-entidades-v1.md` para ver os valores válidos por tipo.

**Valores válidos por entidade:**

| Entidade | Status válidos |
|----------|---------------|
| Receita | `rascunho`, `testada`, `refinada`, `arquivada` |
| Ingrediente | `ativo`, `arquivado` |
| Técnica | `ativo`, `arquivado` |
| Equipamento | `ativo`, `arquivado` |
| Execução | `em-andamento`, `concluida`, `consolidada` |
| Observação | `ativo`, `arquivado` |
| Experimento | `aberto`, `concluido`, `incorporado`, `descartado` |
