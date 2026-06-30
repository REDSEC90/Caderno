# Troubleshooting — Validador

> Diagnóstico de falhas no componente Validador (`codigo/validador-v1.py`).

**O Validador verifica consistência semântica — ciclos críticos, entidades isoladas, regras de negócio.**  
Ele opera sobre um grafo já resolvido. Se o Resolver falhou, o Validador nunca é chamado.

---

## Como executar o Validador isoladamente

```bash
python3 codigo/validador-v1.py
```

```
# Resultado esperado (sem problemas):
Sem issues.
```

```
# Resultado com problema crítico:
[CRITICO] REC-000001 (ciclo): Ciclo detectado: REC-000001 → TEC-000001 → REC-000001
[AVISO]   ING-000005 (entidade_isolada): Ingrediente sem referências — pode ser duplicata ou erro
```

---

## Problema 1: Ciclo crítico detectado

**Sintoma:**
```
[CRITICO] REC-000002 (ciclo): Ciclo detectado: REC-000002 → TEC-000004 → REC-000002
  arestas envolvidas: STRUCTURAL
```

**Causa:** Duas entidades se referenciam mutuamente em campos estruturais (frontmatter). Isso cria dependência circular irresolvível.

**Diagnóstico:**
```bash
# Inspecionar as arestas de cada entidade no ciclo
python3 scripts/auditoria/auditor-v1.py entity REC-000002
python3 scripts/auditoria/auditor-v1.py entity TEC-000004
```

Procurar qual aresta tem `kind: STRUCTURAL` ou `kind: COMPOSITIONAL` apontando de TEC para REC.

**Causa mais comum:** Um ID foi colocado no frontmatter de TEC quando deveria estar apenas no corpo do texto.

```yaml
# ERRADO — TEC-000004 com referência estrutural a uma REC no frontmatter
---
id: TEC-000004
receita-de-origem: REC-000002   ← isso gera aresta STRUCTURAL de TEC → REC
---
```

```yaml
# CORRETO — mover a menção para o corpo do documento
---
id: TEC-000004
---

# Emulsificação

Técnica desenvolvida originalmente para REC-000002.  ← aresta INFORMATIONAL — não cria ciclo crítico
```

**Solução:**
1. Identificar qual campo do frontmatter está criando a aresta problemática
2. Remover esse campo do frontmatter
3. Se a informação for relevante, mencioná-la no corpo do texto (vira aresta INFORMATIONAL)
4. Re-importar

---

## Problema 2: Entidade isolada — tipo REC, EXE ou EXP

**Sintoma:**
```
[AVISO] REC-000002 (entidade_isolada): Receita sem nenhuma aresta — sem ingredientes, técnicas ou execuções
```

**Causa:** Uma Receita foi criada mas não tem nenhum relacionamento. Pode ser:
- Frontmatter com os campos `ingredientes`, `tecnicas` e `equipamentos` vazios ou ausentes
- Arquivo criado mas não importado após adicionar os relacionamentos
- Receita genuinamente vazia (esqueleto não preenchido)

**Diagnóstico:**
```bash
# Ver o arquivo diretamente
cat dados/receitas/REC-000002-*.md | head -30

# Ver as arestas no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, target, kind FROM relacionamentos WHERE source = 'REC-000002';"
```

**Solução:**
```bash
# Editar e adicionar os IDs de ingredientes, técnicas, equipamentos
nano dados/receitas/REC-000002-slug-v1.md
# Preencher: ingredientes: [ING-000001, ING-000002, ...]

# Re-importar
scripts/importacao/importar.sh dados/receitas/REC-000002-slug-v1.md
```

---

## Problema 3: `status inválido`

**Sintoma:**
```
[CRITICO] ING-000005 (status_invalido): 'em-andamento' não é status válido para ingrediente
  valores válidos: ativo, arquivado
```

**Causa:** O campo `status` foi preenchido com um valor que não existe no catálogo para aquele tipo de entidade.

**Diagnóstico:**
```bash
grep "^status:" dados/ingredientes/ING-000005-*.md
```

**Valores válidos por entidade:**

| Entidade | Status válidos |
|----------|---------------|
| REC | `rascunho` `testada` `refinada` `arquivada` |
| ING / TEC / EQP / OBS | `ativo` `arquivado` |
| EXE | `em-andamento` `concluida` `consolidada` |
| EXP | `aberto` `concluido` `incorporado` `descartado` |

**Solução:**
```bash
nano dados/ingredientes/ING-000005-*.md
# Corrigir: status: em-andamento → status: ativo

scripts/importacao/importar.sh dados/ingredientes/ING-000005-*.md
```

---

## Próxima leitura

- Diagnóstico de ciclos via FAA → [`06-faa-v1.md`](06-faa-v1.md#problema-2-dep-002-ciclo-detectado)
- Catálogo de estados por entidade → `docs/01-dominio/catalogos/estados-todas-entidades-v1.md`
- Guia completo do Validador → [`../03-validacao/04-validador-v1.md`](../03-validacao/04-validador-v1.md)
