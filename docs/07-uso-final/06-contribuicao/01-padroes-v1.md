# Padrões de Contribuição

> Regras que todo contribuidor — humano ou agente — deve seguir.

---

## Padrões de Nomenclatura

### Arquivos de dados
```
[PREFIXO]-[NNNNNN]-[slug]-v[schema-version].md

Exemplos válidos:
  REC-000002-pao-de-queijo-mineiro-v1.md
  ING-000005-polvilho-azedo-v1.md
  TEC-000004-emulsificacao-v1.md

Inválidos:
  receita-pao-de-queijo.md         ← sem ID
  REC-2-pao-queijo-v1.md           ← ID sem zeros
  REC-000002-Pão-de-Queijo-v1.md  ← maiúsculas e acento no slug
```

### Slugs
- Apenas minúsculas
- Sem acentos (use: `e` em vez de `é`, `a` em vez de `ã`)
- Hífens como separadores
- Sem underscores, pontos ou outros caracteres

### Identificadores
- Prefixo em maiúsculas: `REC`, `ING`, `TEC`, `EQP`, `EXE`, `OBS`, `EXP`
- 6 dígitos com zeros à esquerda: `000001` a `999999`
- Sequência nunca retroativa — IDs arquivados nunca são reutilizados

---

## Padrões de Frontmatter

Todo frontmatter deve:
- Começar na **primeira linha** do arquivo (sem BOM, sem linhas em branco antes)
- Usar `---` como delimitadores
- Ter `id`, `tipo`, `schema-version`, `status`, `criado-em`, `atualizado-em`, `autor`
- Usar datas em `YYYY-MM-DD` (ISO 8601)
- Não deixar campos obrigatórios com valores placeholder (`YYYY-MM-DD`, `TBD`, `null`)

---

## Padrões de Commit

```
[tipo]([escopo]): [descrição imperativa no presente]

tipos:   feat | fix | refactor | docs | chore | audit
escopos: rec | ing | tec | eqp | exe | obs | exp | schema | docs | faa

Bons exemplos:
  feat(rec): cria REC-000002 pao-de-queijo-mineiro
  fix(ing): corrige tipo-ingrediente de ING-000003 para mineral
  docs(07-uso): adiciona fluxo de criação de experimento
  audit(faa): resolve falha DEP-002 ciclo informacional
  chore(ing): arquiva ING-000005 duplicata de ING-000001

Maus exemplos:
  update files           ← sem contexto
  fix bug                ← qual bug?
  WIP                    ← nunca commitar WIP
```

---

## Padrões de Tags

Tags são strings em minúsculas, sem acentos, com hífens. Devem descrever categorias reais — não termos genéricos.

```yaml
# Bom
tags: [doce, brasileiro, laticinio, caramelizacao]

# Mau — termos genéricos sem valor semântico
tags: [comida, receita, ingrediente, coisa]
```

Consulte `docs/04-padroes/tags-v1.md` para o catálogo de tags aprovadas.

---

## Codificação e Formatação

- Todos os arquivos: `UTF-8` sem BOM
- Quebras de linha: LF (Unix) — não CRLF
- Sem trailing whitespace
- Uma linha em branco ao final do arquivo
