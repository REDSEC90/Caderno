# Erros Comuns

> Os erros que aparecem com mais frequência — e como evitá-los da próxima vez.

---

## Erro 1: Criar Duplicata

**Sintoma:** Dois ING com o mesmo conceito. O banco retorna dois resultados para a mesma busca.

**Causa:** Não verificar existência antes de criar.

**Prevenção:**
```bash
# SEMPRE antes de criar qualquer ING, TEC ou EQP:
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%[termo]%';"
```

**Correção:** Arquivar o duplicado. Atualizar todos os registros que referenciavam o ID duplicado para usar o ID canônico. Re-importar.

---

## Erro 2: ID no frontmatter ≠ ID no nome do arquivo

**Sintoma:** Parser usa o ID do frontmatter. O arquivo `ING-000005-farinha-v1.md` com `id: ING-000006` no frontmatter cria uma entidade `ING-000006` — que não corresponde ao nome do arquivo.

**Prevenção:** Copiar o template e imediatamente verificar que o ID no frontmatter é idêntico ao prefixo-número do nome do arquivo.

---

## Erro 3: Referenciar por nome em vez de ID

**Sintoma:** Validação falha com `referencia_quebrada` ou dados inconsistentes.

```yaml
# Errado
ingredientes: [Leite Integral, Açúcar]

# Correto
ingredientes: [ING-000001, ING-000002]
```

**Causa:** Confundir o campo de relacionamento com texto descritivo.

---

## Erro 4: Criar REC antes de ING/TEC/EQP

**Sintoma:** `referencia_quebrada: ING-000005` durante a importação.

**Causa:** Criar a Receita antes de criar os ingredientes que ela referencia.

**Prevenção:** Seguir a ordem: `EQP → TEC → ING → REC → EXE → OBS/EXP`

---

## Erro 5: Não atualizar `atualizado-em`

**Sintoma:** O banco mostra data de criação antiga mesmo após edições recentes. Histórico de mudanças fica opaco.

**Prevenção:** Sempre que editar qualquer campo, atualizar `atualizado-em` para a data atual.

---

## Erro 6: Esquecer de re-importar após edição

**Sintoma:** O arquivo Markdown foi editado mas o banco SQLite ainda mostra o valor antigo.

**Prevenção:** Após qualquer edição, sempre executar:
```bash
scripts/importacao/importar.sh dados/[entidade]/[arquivo].md
```

---

## Erro 7: Commitar o banco SQLite

**Sintoma:** `git diff` mostra mudanças em `banco_de_dados/sqlite/soe-ccg.db`.

**Prevenção:** Verificar que `soe-ccg.db` está no `.gitignore`. Se não estiver:
```bash
echo "banco_de_dados/sqlite/*.db" >> .gitignore
git rm --cached banco_de_dados/sqlite/soe-ccg.db
git commit -m "chore: remove banco sqlite do versionamento"
```

---

## Erro 8: Status inválido

**Sintoma:** FAA reporta erro de validação no motor `dados`.

**Causa:** Usar um valor de status que não está no catálogo.

**Prevenção:** Consultar `docs/01-dominio/catalogos/estados-todas-entidades-v1.md` antes de preencher o campo `status`. Os valores são case-sensitive (`rascunho`, não `Rascunho`).

---

## Erro 9: Campo date com placeholder

**Sintoma:** FAA ou importador falha. Banco recebe string `YYYY-MM-DD` literal.

**Causa:** Copiar o template e esquecer de substituir os valores de exemplo.

**Prevenção:** Depois de copiar qualquer template, revisar todos os campos antes de salvar. Nunca importar um arquivo com `criado-em: YYYY-MM-DD` literal.
