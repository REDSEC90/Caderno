# Cookbook — Criar uma Receita (REC)

> Exemplo completo e copiável. A receita só pode ser criada depois que todos os ingredientes, técnicas e equipamentos que ela usa já existirem no sistema.

**Tempo:** ~15 minutos (+ tempo para criar dependências, se necessário)  
**Resultado:** Uma receita completa com relacionamentos, validada e importada.

---

## Pré-condições

**Regra fundamental:** Uma Receita não pode referenciar IDs que não existem.  
Crie as dependências nesta ordem: `EQP → TEC → ING → REC`

```bash
# Verificar que os ingredientes existem
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE status = 'ativo' ORDER BY nome;"

# Verificar que as técnicas existem
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM tecnicas WHERE status = 'ativo' ORDER BY nome;"

# Verificar que os equipamentos existem
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM equipamentos WHERE status = 'ativo' ORDER BY nome;"
```

Se alguma dependência não existir, crie primeiro:
- Ingredientes → [`01-criar-ingrediente-v1.md`](01-criar-ingrediente-v1.md)
- Técnicas → [`03-criar-tecnica-v1.md`](03-criar-tecnica-v1.md)
- Equipamentos → [`04-criar-equipamento-v1.md`](04-criar-equipamento-v1.md)

---

## Passo 1 — Planejar os IDs que serão usados

Antes de criar o arquivo, anotar os IDs de todas as dependências:

```bash
# Exemplo para Pão de Queijo Mineiro:
sqlite3 banco_de_dados/sqlite/soe-ccg.db "
  SELECT id, nome FROM ingredientes WHERE nome IN (
    'Polvilho Azedo', 'Queijo Minas Meia-Cura', 'Ovo', 'Óleo', 'Leite Integral', 'Sal Refinado'
  );
"
```

Anotar os resultados — você vai precisar deles no frontmatter.

---

## Passo 2 — Obter o próximo ID de REC

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM receitas ORDER BY id DESC LIMIT 1;"
```

```
# Resultado esperado:
REC-000001
```

O próximo é `REC-000002`.

---

## Passo 3 — Criar o arquivo

```bash
cp docs/01-dominio/templates/receita-v1.md \
   dados/receitas/REC-000002-[slug-do-titulo]-v1.md
```

---

## Passo 4 — Editar o arquivo

```markdown
---
id: REC-000002
tipo: receita
schema-version: 1
versao: 1
status: rascunho
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: [seu-nome]
origem: [tradicional | adaptada | criação própria]
tags: [[tag1], [tag2]]
ingredientes: [ING-000005, ING-000006, ING-000007]
tecnicas: [TEC-000001, TEC-000004]
equipamentos: [EQP-000001, EQP-000003]
---

# [Título da Receita]

## Descrição
[Uma ou duas frases sobre o que é a receita.]

## Informações
- **Rendimento:** [quantidade + unidade]
- **Tempo de preparo:** [estimativa]
- **Dificuldade:** [fácil | média | difícil]
- **Categorias:** [doce | salgado | pão | massa | ...]

## Ingredientes

| ID         | Nome                | Quantidade | Unidade |
|------------|---------------------|------------|---------|
| ING-000005 | [Nome Ingrediente 1]| [qtd]      | [un]    |
| ING-000006 | [Nome Ingrediente 2]| [qtd]      | [un]    |

## Técnicas

| ID         | Técnica              |
|------------|---------------------|
| TEC-000001 | [Nome Técnica 1]    |

## Equipamentos

| ID         | Equipamento          |
|------------|---------------------|
| EQP-000001 | [Nome Equipamento 1] |

## Modo de Preparo

1. [Primeiro passo]
2. [Segundo passo]
3. [...]

## Notas

[Observações relevantes sobre pontos críticos, variações possíveis, etc.]
```

**Exemplo real preenchido (Pão de Queijo Mineiro):**

```markdown
---
id: REC-000002
tipo: receita
schema-version: 1
versao: 1
status: rascunho
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: joao
origem: tradicional mineira
tags: [pao, queijo, brasileiro, sem-gluten]
ingredientes: [ING-000005, ING-000006, ING-000007, ING-000008, ING-000001, ING-000003]
tecnicas: [TEC-000005, TEC-000006]
equipamentos: [EQP-000004, EQP-000001]
---

# Pão de Queijo Mineiro

## Descrição
Pão de queijo tradicional feito com polvilho azedo e queijo minas meia-cura.
Casca crocante, interior elástico e sabor acentuado.

## Informações
- **Rendimento:** ~30 unidades médias
- **Tempo de preparo:** 45 minutos (+ 30 min de descanso opcional)
- **Dificuldade:** fácil
- **Categorias:** pão, café, lanche

## Ingredientes

| ID         | Nome                    | Quantidade | Unidade |
|------------|-------------------------|------------|---------|
| ING-000005 | Polvilho Azedo          | 500        | g       |
| ING-000006 | Queijo Minas Meia-Cura  | 200        | g       |
| ING-000007 | Ovo                     | 2          | unidade |
| ING-000008 | Óleo                    | 100        | ml      |
| ING-000001 | Leite Integral          | 200        | ml      |
| ING-000003 | Sal Refinado            | 1          | colher  |

## Técnicas

| ID         | Técnica              |
|------------|---------------------|
| TEC-000005 | Escaldamento        |
| TEC-000006 | Modelagem manual    |

## Equipamentos

| ID         | Equipamento          |
|------------|---------------------|
| EQP-000004 | Tigela grande        |
| EQP-000001 | Panela de fundo grosso|

## Modo de Preparo

1. Ferver o leite com o óleo e o sal.
2. Jogar sobre o polvilho ainda fervendo e misturar vigorosamente (escaldamento).
3. Deixar amornar (~10 min) antes de adicionar os ovos.
4. Adicionar os ovos um a um, incorporando bem a cada adição.
5. Adicionar o queijo ralado e misturar.
6. Modelar bolinhas do tamanho de uma noz.
7. Assar a 180°C por 25-30 minutos até dourar.

## Notas

- O escaldamento do polvilho é o passo mais crítico — o líquido deve estar fervendo.
- Polvilho doce pode ser usado em até 50% da proporção para textura mais suave.
- Congelar as bolinhas cruas funciona bem — assar diretamente do congelador.
```

---

## Passo 5 — Verificar antes de importar

```bash
# Rodar o Parser para checar erros antes de importar
python3 codigo/parser-v1.py dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
```

```
# Resultado esperado:
[PARSER] REC-000002 processado — 6 arestas COMPOSITIONAL
```

---

## Passo 6 — Importar

```bash
scripts/importacao/importar.sh dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
```

```
# Resultado esperado:
[OK] REC-000002 importado com sucesso
```

---

## Passo 7 — Verificar

```bash
# A receita está no banco?
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas WHERE id = 'REC-000002';"

# Os relacionamentos foram criados?
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT i.id, i.nome
   FROM ingredientes i
   JOIN receita_ingrediente ri ON ri.ingrediente_id = i.id
   WHERE ri.receita_id = 'REC-000002';"
```

```
# Resultado esperado:
REC-000002|Pão de Queijo Mineiro|rascunho

ING-000005|Polvilho Azedo
ING-000006|Queijo Minas Meia-Cura
ING-000007|Ovo
ING-000008|Óleo
ING-000001|Leite Integral
ING-000003|Sal Refinado
```

---

## Passo 8 — Commitar

```bash
git add dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(rec): cria REC-000002 pao-de-queijo-mineiro"
```

---

## Status da receita ao longo do tempo

```
rascunho      → ainda não foi preparada
   ↓
testada       → após a primeira execução bem-sucedida
   ↓
refinada      → após ajustes e múltiplas execuções
   ↓
arquivada     → substituída por versão reformulada
```

Para promover de `rascunho` para `testada` após o primeiro preparo:
```bash
# Editar o arquivo
nano dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
# Alterar status: rascunho → testada
# Atualizar atualizado-em

# Re-importar
scripts/importacao/importar.sh dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
git commit -am "feat(rec): promove REC-000002 para testada após primeira execução"
```

---

## Próximo passo

Com a receita criada, você pode:
- Registrar o primeiro preparo → [`05-criar-execucao-v1.md`](05-criar-execucao-v1.md)
- Ver o fluxo completo de uma sessão → [`../05-fluxos/07-fluxo-completo-v1.md`](../05-fluxos/07-fluxo-completo-v1.md)
