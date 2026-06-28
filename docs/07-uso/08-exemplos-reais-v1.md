# Exemplos Reais — SOE-CCG

> Casos completos do mundo real. Do zero à validação FAA.
> Este é o melhor recurso para entender o sistema funcionando.

---

## Como ler este documento

Cada exemplo mostra:
- A **situação** e a decisão inicial
- O **fluxo completo** passo a passo com comandos reais
- As **entidades e arestas** criadas no grafo
- A **validação FAA** e como verificar o resultado

---

## Exemplo 1: Criar uma Receita do Zero

**Situação:** Você quer registrar Brigadeiro Clássico. Nunca registrou nada neste sistema antes.

### Decisão Inicial

Perguntas que você faz antes de começar:
- "Existe uma receita de brigadeiro?" → `sqlite3 ... "SELECT * FROM receitas WHERE titulo LIKE '%brigadeiro%';"` → Não existe.
- "Existem os ingredientes (leite condensado, manteiga, chocolate em pó, chocolate granulado)?" → Verificar um a um.

Resultado da verificação: Nenhum dos ingredientes existe. Nenhuma técnica pertinente existe.

### Execução

**Passo 1 — Obter IDs disponíveis**
Consultar `docs/04-padroes/identificadores-v1.md`. Suponha: ING-000004 é o último, TEC-000003 o último, EQP-000002 o último, REC-000001 o último.

**Passo 2 — Criar equipamentos**
```bash
cp docs/01-dominio/templates/equipamento-v1.md dados/equipamentos/EQP-000003-panela-antiaderente-v1.md
# Editar: id: EQP-000003, status: ativo, criado-em: 2026-06-27
scripts/importacao/importar.sh dados/equipamentos/EQP-000003-panela-antiaderente-v1.md
```

**Passo 3 — Criar técnicas**
```bash
cp docs/01-dominio/templates/tecnica-v1.md dados/tecnicas/TEC-000004-cozimento-em-ponto-v1.md
# Editar: id: TEC-000004, nome: Cozimento em Ponto
scripts/importacao/importar.sh dados/tecnicas/TEC-000004-cozimento-em-ponto-v1.md
```

**Passo 4 — Criar ingredientes (um por arquivo)**
```bash
for slug in "leite-condensado" "manteiga-sem-sal" "chocolate-em-po" "granulado-chocolate"; do
  # Obter próximo ID, criar arquivo, editar, importar
done
# IDs criados: ING-000005 a ING-000008
```

**Passo 5 — Criar a Receita**
```bash
cp docs/01-dominio/templates/receita-v1.md \
   dados/receitas/REC-000002-brigadeiro-classico-v1.md
```

Frontmatter:
```yaml
---
id: REC-000002
tipo: receita
schema-version: 1
versao: 1
status: rascunho
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
origem: receita familiar tradicional
tags: [doce, brasileiro, chocolate, festa]
ingredientes: [ING-000005, ING-000006, ING-000007, ING-000008]
tecnicas: [TEC-000004]
equipamentos: [EQP-000003]
---
```

```bash
scripts/importacao/importar.sh dados/receitas/REC-000002-brigadeiro-classico-v1.md
```

### Entidades e Arestas Criadas

```
REC-000002 ──[COMPOSITIONAL]──→ ING-000005 (leite condensado)
           ──[COMPOSITIONAL]──→ ING-000006 (manteiga sem sal)
           ──[COMPOSITIONAL]──→ ING-000007 (chocolate em pó)
           ──[COMPOSITIONAL]──→ ING-000008 (granulado chocolate)
           ──[COMPOSITIONAL]──→ TEC-000004 (cozimento em ponto)
           ──[COMPOSITIONAL]──→ EQP-000003 (panela antiaderente)
```

### Validação FAA

```bash
python3 scripts/auditoria/auditor-v1.py
# Esperado: APROVADO, sem novas falhas
```

```bash
# Verificar no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, target, kind FROM relacionamentos WHERE source = 'REC-000002';"
```

```bash
# Atualizar identificadores e commitar
git add dados/ docs/04-padroes/identificadores-v1.md
git commit -m "feat(rec): cria REC-000002 brigadeiro com 4 ING + TEC + EQP"
```

---

## Exemplo 2: Reutilizar um Ingrediente Existente

**Situação:** Você quer criar Arroz Doce. Já existe `ING-000001 Leite Integral` no sistema. Não recrie — reutilize.

### Decisão Inicial

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%leite%';"
# Resultado: ING-000001 | Leite Integral
```

Leite Integral existe como `ING-000001`. Não criar novo.

### Execução

Criar os ingredientes faltantes (arroz, açúcar, canela, cravo). Verificar cada um antes:

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%arroz%'
   UNION SELECT id, nome FROM ingredientes WHERE nome LIKE '%acucar%';"
```

Suponha que `ING-000002 Açúcar Refinado` já existe mas `arroz`, `canela`, `cravo` não.

Criar apenas os faltantes: `ING-000009-arroz-branco-v1.md`, `ING-000010-canela-em-pau-v1.md`, `ING-000011-cravo-da-india-v1.md`.

Criar a Receita referenciando os IDs existentes e os novos:
```yaml
ingredientes: [ING-000009, ING-000001, ING-000002, ING-000010, ING-000011]
#              arroz         leite       açúcar       canela       cravo
```

### O que o Grafo Mostra

```
REC-000003 ──[COMPOSITIONAL]──→ ING-000001  ← já existia, agora tem 2 receitas
           ──[COMPOSITIONAL]──→ ING-000002  ← já existia, agora tem 2 receitas
           ──[COMPOSITIONAL]──→ ING-000009  ← novo
           ...
```

A reutilização de `ING-000001` cria uma segunda aresta COMPOSITIONAL apontando para ele. Agora `ING-000001` é referenciado por `REC-000001` e `REC-000002` — exatamente o comportamento esperado.

---

## Exemplo 3: Corrigir uma Referência Quebrada

**Situação:** O FAA ou o importador reporta `referencia_quebrada: ING-000099` ao importar `REC-000003-arroz-doce-v1.md`.

### Diagnóstico

```bash
# Confirmar que ING-000099 não existe
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id FROM ingredientes WHERE id = 'ING-000099';"
# Retorna vazio

# Ver o arquivo com a referência quebrada
grep "ING-000099" dados/receitas/REC-000003-arroz-doce-v1.md
# ingredientes: [ING-000009, ING-000001, ING-000002, ING-000099]
```

`ING-000099` foi digitado quando o ID correto era `ING-000009` (canela).

### Correção

```bash
nano dados/receitas/REC-000003-arroz-doce-v1.md
# Corrigir: ING-000099 → ING-000009
# Atualizar: atualizado-em: 2026-06-27

scripts/importacao/importar.sh dados/receitas/REC-000003-arroz-doce-v1.md
# Importação deve passar sem erros

python3 scripts/auditoria/auditor-v1.py
# Sem referências quebradas

git commit -am "fix(rec): corrige referencia ING-000099 → ING-000009 em REC-000003"
```

---

## Exemplo 4: Resolver um Ciclo Estrutural

**Situação:** O FAA reporta:
```
❌ [DEP-002] Ciclo detectado: TEC-000001 -> EQP-000001 -> TEC-000001
    Arestas: STRUCTURAL
```

### Diagnóstico

```bash
python3 scripts/auditoria/auditor-v1.py entity TEC-000001
python3 scripts/auditoria/auditor-v1.py entity EQP-000001
```

Resultado: `TEC-000001` tem no frontmatter um campo `equipamento: EQP-000001`. E `EQP-000001` tem um campo `tecnica-principal: TEC-000001`. Ambas as referências são `STRUCTURAL` no frontmatter — um ciclo estrutural real.

### Correção

A questão semântica: `EQP-000001 (panela de fundo grosso)` não *depende estruturalmente* de `TEC-000001 (redução)`. Ela é frequentemente *usada com* essa técnica — uma relação informacional, não estrutural.

```bash
nano dados/equipamentos/EQP-000001-panela-fundo-grosso-v1.md
```

Remover `tecnica-principal: TEC-000001` do frontmatter. Se quiser preservar a informação, mencioná-la no corpo do texto:

```markdown
## Uso Típico
Frequentemente utilizada com a técnica de Redução (TEC-000001) por seu
aquecimento uniforme que evita pontos quentes.
```

Isso transforma a aresta de `STRUCTURAL` (frontmatter) para `INFORMATIONAL` (corpo). O ciclo não é mais crítico.

```bash
scripts/importacao/importar.sh dados/equipamentos/EQP-000001-panela-fundo-grosso-v1.md
python3 scripts/auditoria/auditor-v1.py
# [DEP-002] deve ter desaparecido ou mudado para INFO
git commit -am "fix(eqp): converte dependencia estrutural EQP→TEC para informacional"
```

---

## Exemplo 5: Atualizar uma Técnica Compartilhada por Múltiplas Receitas

**Situação:** `TEC-000001 Redução` está sendo usada por `REC-000001` e `REC-000003`. Você descobriu informações novas sobre pontos de atenção que afetam ambas.

### Verificação de Impacto

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT r.id, r.titulo FROM receitas r
   JOIN receita_tecnica rt ON rt.receita_id = r.id
   WHERE rt.tecnica_id = 'TEC-000001';"
# REC-000001 | Doce de Leite Artesanal
# REC-000003 | Arroz Doce
```

A técnica é compartilhada — a atualização beneficia todas as receitas que a usam automaticamente.

### Execução

```bash
nano dados/tecnicas/TEC-000001-reducao-v1.md
# Adicionar na seção "Pontos Críticos":
# - Açúcares com alto teor de frutose caramelizam antes da evaporação adequada
# Atualizar: atualizado-em: 2026-06-27

scripts/importacao/importar.sh dados/tecnicas/TEC-000001-reducao-v1.md
python3 scripts/auditoria/auditor-v1.py
git commit -am "feat(tec): adiciona ponto critico sobre caramelizacao em TEC-000001"
```

Nenhuma das receitas precisou ser editada — elas referenciavam `TEC-000001` e automaticamente "herdam" o conhecimento atualizado.

---

## Exemplo 6: Criar um Experimento Ligado a uma Receita

**Situação:** Após três execuções do Doce de Leite, você quer testar sistematicamente se temperatura mais alta no início acelera o processo sem comprometer o resultado.

### Execução

```bash
cp docs/01-dominio/templates/experimento-v1.md \
   dados/experimentos/EXP-000001-temperatura-inicial-doce-leite-v1.md
```

Frontmatter:
```yaml
---
id: EXP-000001
tipo: experimento
schema-version: 1
versao: 1
status: aberto
criado-em: 2026-06-27
atualizado-em: 2026-06-27
autor: nome-do-autor
receita-base-id: REC-000001
tags: [doce-de-leite, temperatura, tempo-preparo]
---
```

Conteúdo:
```markdown
# Experimento: Temperatura Inicial no Doce de Leite

## Hipótese
Iniciar o cozimento em fogo médio-alto (80% da potência) por 10 minutos antes
de reduzir para baixo reduz o tempo total sem comprometer textura ou sabor.

## Variáveis
- **Testada:** temperatura nos primeiros 10 min (baixo → médio-alto)
- **Mantidas:** proporções dos ingredientes, tempo total de observação

## Receita Base
REC-000001 — Doce de Leite Artesanal

## Critério de Sucesso
Tempo total ≤ 1h45min com avaliação de sabor ≥ 8/10 e textura ≥ 8/10
```

```bash
scripts/importacao/importar.sh dados/experimentos/EXP-000001-temperatura-inicial-doce-leite-v1.md
```

### Arestas Criadas

```
EXP-000001 ──[DERIVATION]──→ REC-000001
```

### Durante o Experimento

Cada preparo de teste é uma nova `EXE` com os desvios documentados:
```yaml
# EXE-000003 — preparo com temperatura alta no início
status: concluida
# desvios: temperatura inicial 80% por 10min conforme EXP-000001
```

### Concluindo

```bash
nano dados/experimentos/EXP-000001-temperatura-inicial-doce-leite-v1.md
# status: concluido (ou incorporado se o resultado vai para REC-000001-v2)
# Adicionar seção ## Resultado com referência às EXEs realizadas
```

---

## Exemplo 7: Registrar uma Execução Retrospectiva

**Situação:** Você fez Doce de Leite há três dias e esqueceu de registrar. Hoje quer registrar retrospectivamente.

### Por que isso é válido

O campo `data-execucao` é a data em que o **preparo ocorreu**, não quando o arquivo foi criado. `criado-em` é quando o arquivo foi criado hoje.

```yaml
---
id: EXE-000004
tipo: execucao
schema-version: 1
versao: 1
status: concluida
criado-em: 2026-06-27          ← hoje, data de criação do arquivo
atualizado-em: 2026-06-27
data-execucao: 2026-06-24      ← há três dias, quando o preparo ocorreu
autor: nome-do-autor
tags: [doce-de-leite, retrospectiva]
---
```

Registros retrospectivos são completamente válidos no SOE. O sistema preserva o conhecimento independentemente do momento em que é formalizado. Quanto mais cedo, mais detalhes você lembra — mas tarde é melhor que nunca.

```bash
scripts/importacao/importar.sh dados/execucoes/EXE-000004-doce-leite-execucao4-v1.md
git commit -am "feat(exe): registra retroativamente EXE-000004 preparo 2026-06-24"
```
