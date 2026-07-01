# Como Funciona o SOE-CCG — Guia Prático

**Data:** 2026-07-01  
**Objetivo:** Explicar o funcionamento completo do sistema do ponto de vista do usuário

---

## 🎯 O Que é o SOE-CCG

**SOE-CCG** = Sistema de Registro, Organização, Evolução e Consulta de Conhecimento Gastronômico

**Não é:**
- ❌ Um gerenciador de receitas comum
- ❌ Um app de culinária
- ❌ Um banco de dados de pratos

**É:**
- ✅ Um **motor de conhecimento gastronômico**
- ✅ Sistema para preservar conhecimento por décadas
- ✅ Base de dados científica da culinária

---

## 📚 Filosofia Central

### Princípio Fundamental

```
O conhecimento é permanente. A implementação é temporária.
```

**Isso significa:**
- Markdown é o formato canônico (arquivos de texto simples)
- SQLite é apenas para consultas rápidas
- Nenhuma informação vive **exclusivamente** no banco
- Você pode regenerar o banco a partir dos arquivos Markdown
- Em 20 anos, os Markdown ainda serão legíveis

### Separação de Conceitos

```
RECEITA = conhecimento (como fazer)
EXECUÇÃO = registro (o que aconteceu quando fiz)
```

**Exemplo:**
- **Receita de Doce de Leite** = conhecimento atemporal sobre como fazer
- **Execução de 2026-06-25** = o que aconteceu quando fiz naquele dia específico

---

## 🏗️ Entidades do Sistema

### 1. **Receita** (REC-NNNNNN)

**O que é:** Conhecimento estruturado sobre como preparar um prato

**Contém:**
- Lista de ingredientes (por ID)
- Técnicas necessárias (por ID)
- Equipamentos usados (por ID)
- Modo de preparo (texto)
- Informações (tempo, rendimento, dificuldade)

**Exemplo real:**
```
REC-000001: Doce de Leite Artesanal
- Ingredientes: ING-000001 (leite), ING-000002 (açúcar), ...
- Técnicas: TEC-000001 (redução), TEC-000003 (agitação contínua)
- Tempo: ~2h
- Rendimento: ~300g
```

---

### 2. **Ingrediente** (ING-NNNNNN)

**O que é:** Insumo reutilizável usado em receitas

**Contém:**
- Nome
- Classificação (tipo, categorias)
- Unidade padrão
- Descrição
- Substitutos comuns

**Exemplo real:**
```
ING-000001: Leite Integral
- Tipo: Laticínio
- Unidade: ml
- Origem: Animal (bovino)
- Substituto: leite de aveia (vegano)
```

**Por que usar IDs?**
- ✅ "Leite Integral" pode ter variações de grafia
- ✅ Centraliza informações (uma vez só)
- ✅ Permite evolução sem quebrar receitas antigas

---

### 3. **Técnica** (TEC-NNNNNN)

**O que é:** Método ou procedimento culinário

**Contém:**
- Nome
- Tipo (calor seco, calor úmido, etc)
- Descrição detalhada
- Pontos críticos
- Aplicações

**Exemplo real:**
```
TEC-000001: Redução
- Tipo: Calor úmido — concentração por evaporação
- Aplicações: doce de leite, caldas, molhos
- Ponto crítico: temperatura baixa e constante
```

**Por que separar técnicas?**
- ✅ Evita repetir a mesma explicação em 50 receitas
- ✅ Permite evoluir o conhecimento sobre a técnica
- ✅ Facilita encontrar todas as receitas que usam uma técnica

---

### 4. **Equipamento** (EQP-NNNNNN)

**O que é:** Utensílio ou aparelho usado no preparo

**Contém:**
- Nome
- Tipo
- Descrição
- Substitutos

**Exemplo real:**
```
EQP-000001: Panela de Fundo Grosso
- Tipo: Utensílio de cozimento
- Essencial para: receitas com açúcar (evita queima)
```

---

### 5. **Execução** (EXE-NNNNNN)

**O que é:** Registro de quando você **realmente preparou** uma receita

**Contém:**
- ID da receita executada
- Data e hora
- Resultado (sucesso, parcial, falha)
- Métricas (tempo real, rendimento real, temperatura)
- Modificações feitas
- Avaliação

**Exemplo:**
```
EXE-000001: Execução de REC-000001 em 2026-06-25
- Tempo real: 2h15min (previsto: 2h)
- Rendimento: 285g (previsto: 300g)
- Modificações: usei fogo médio-baixo em vez de baixo
- Resultado: sucesso, mas ficou um pouco mais escuro
- Nota: da próxima vez, voltar ao fogo baixo
```

**Por que separar execução de receita?**
- ✅ Receita é conhecimento, execução é evidência
- ✅ Você pode executar a mesma receita 10 vezes
- ✅ Cada execução ensina algo novo
- ✅ Você pode comparar execuções para aprender

---

### 6. **Observação** (OBS-NNNNNN)

**O que é:** Nota, percepção ou descoberta sobre qualquer coisa

**Pode ser vinculada a:**
- Uma receita
- Um ingrediente
- Uma técnica
- Uma execução
- Um experimento

**Exemplo:**
```
OBS-000001: Papel do Bicarbonato no Doce de Leite
Vinculada a: REC-000001, ING-000004
Conteúdo:
  O bicarbonato de sódio tem dupla função:
  1. Previne coagulação das proteínas do leite
  2. Contribui para a cor âmbar (reação de Maillard)
  
  Fonte: pesquisa em livros de química culinária
  Data: 2026-06-26
```

**Por que observações são importantes?**
- ✅ Conhecimento informal que não cabe nos campos estruturados
- ✅ Registro de hipóteses
- ✅ Conexão entre teoria e prática
- ✅ Evolução do entendimento ao longo do tempo

---

### 7. **Experimento** (EXP-NNNNNN)

**O que é:** Tentativa deliberada de testar ou criar conhecimento novo

**Diferença de Receita:**
- Receita = conhecimento consolidado
- Experimento = conhecimento em formação

**Exemplo:**
```
EXP-000001: Doce de Leite com Coco
Objetivo: testar se leite de coco funciona em doce de leite
Status: em andamento
Hipótese: leite de coco + açúcar de coco pode criar doce cremoso
Tentativa 1: falhou (separou)
Tentativa 2: adicionei goma xantana (melhorou)
Próximo passo: testar com leite de coco integral
```

**Quando um experimento vira receita?**
- Quando você tem certeza suficiente para que outra pessoa possa repetir
- Quando o resultado é consistente
- Quando o conhecimento está consolidado

---

## 📁 Estrutura de Arquivos

### Como os Dados São Organizados

```
dados/
├── receitas/
│   ├── REC-000001-doce-de-leite-artesanal-v1.md
│   ├── REC-000002-pao-de-queijo-v1.md
│   └── ...
├── ingredientes/
│   ├── ING-000001-leite-integral-v1.md
│   ├── ING-000002-acucar-refinado-v1.md
│   └── ...
├── tecnicas/
│   ├── TEC-000001-reducao-v1.md
│   ├── TEC-000002-caramelizacao-v1.md
│   └── ...
├── equipamentos/
│   ├── EQP-000001-panela-fundo-grosso-v1.md
│   └── ...
├── execucoes/
│   ├── EXE-000001-doce-leite-2026-06-25-v1.md
│   └── ...
├── observacoes/
│   ├── OBS-000001-bicarbonato-doce-leite-v1.md
│   └── ...
└── experimentos/
    ├── EXP-000001-doce-leite-coco-v1.md
    └── ...
```

### Formato dos Arquivos (Markdown + YAML)

Todo arquivo tem duas partes:

**1. Frontmatter (metadados YAML):**
```yaml
---
id: REC-000001
tipo: receita
schema-version: 1
versao: 1
status: testada
criado-em: 2026-06-25
atualizado-em: 2026-06-26
autor: sistema
origem: receita artesanal tradicional
tags: [doce, brasileiro, laticinio]
ingredientes: [ING-000001, ING-000002]
tecnicas: [TEC-000001, TEC-000003]
equipamentos: [EQP-000001, EQP-000002]
---
```

**2. Conteúdo (Markdown):**
```markdown
# Doce de Leite Artesanal

## Descrição

Doce de leite produzido por redução lenta...

## Ingredientes

| ID | Nome | Quantidade | Unidade |
|----|------|------------|---------|
| ING-000001 | Leite Integral | 1000 | ml |
...
```

---

## 🔄 Fluxo de Uso

### Como Criar uma Nova Receita

**Passo 1: Garantir que ingredientes existem**

```bash
# Verificar se já existe
ls dados/ingredientes/ | grep leite

# Se não existir, criar
# Copiar template
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000010-leite-desnatado-v1.md

# Editar o arquivo
# Preencher id, nome, descrição, etc
```

**Passo 2: Garantir que técnicas existem**

```bash
# Mesmo processo para técnicas
ls dados/tecnicas/ | grep fermentacao

# Se necessário, criar
cp docs/01-dominio/templates/tecnica-v1.md \
   dados/tecnicas/TEC-000015-fermentacao-natural-v1.md
```

**Passo 3: Criar a receita**

```bash
# Copiar template
cp docs/01-dominio/templates/receita-v1.md \
   dados/receitas/REC-000042-pao-integral-v1.md

# Editar:
# - Frontmatter: id, status, tags
# - Ingredientes: listar IDs com quantidades
# - Técnicas: listar IDs
# - Modo de preparo: descrever passos
```

**Passo 4: Importar para o banco**

```bash
python -m codigo importar banco_de_dados/sqlite/soe.db
```

Isso vai:
1. Parsear todos os arquivos Markdown
2. Validar IDs e referências
3. Importar para SQLite
4. Criar relacionamentos

**Passo 5: Consultar**

```bash
# Consultar no banco (SQL)
sqlite3 banco_de_dados/sqlite/soe.db

SELECT r.titulo, i.nome, ri.quantidade, ri.unidade
FROM receitas r
JOIN receitas_ingredientes ri ON r.id = ri.receita_id
JOIN ingredientes i ON ri.ingrediente_id = i.id
WHERE r.id = 'REC-000001';
```

---

## 🔍 Relacionamentos

### Como as Entidades se Conectam

```
                    ┌─────────────┐
                    │  RECEITA    │
                    │ REC-000001  │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
      referencia      referencia      referencia
           │               │               │
   ┌───────▼──────┐ ┌─────▼──────┐ ┌─────▼──────┐
   │ INGREDIENTE  │ │  TÉCNICA   │ │ EQUIPAMENTO│
   │ ING-000001   │ │ TEC-000001 │ │ EQP-000001 │
   └──────────────┘ └────────────┘ └────────────┘
           │
           │
      possui execução
           │
   ┌───────▼──────┐
   │  EXECUÇÃO    │
   │ EXE-000001   │
   │ 2026-06-25   │
   └──────┬───────┘
          │
     pode ter observações
          │
   ┌──────▼──────┐
   │ OBSERVAÇÃO  │
   │ OBS-000001  │
   └─────────────┘
```

### Tipos de Relacionamentos

**1. Composicional (N:N)**
- Receita → Ingredientes (uma receita usa vários, um ingrediente aparece em várias)
- Receita → Técnicas
- Receita → Equipamentos

**2. Estrutural (1:N)**
- Receita → Execuções (uma receita pode ter várias execuções)
- Execução → Observações

**3. Derivação (1:N)**
- Receita base → Receita derivada (variações)
- Experimento → Receita (experimento bem-sucedido origina receita)

**4. Informacional (flexível)**
- Observação pode se conectar a qualquer entidade

---

## 🛠️ Templates

### Para Que Servem os Templates

**Localização:** `docs/01-dominio/templates/`

**Templates disponíveis:**
- `receita-v1.md`
- `ingrediente-v1.md`
- `tecnica-v1.md`
- `equipamento-v1.md`
- `execucao-v1.md`
- `observacao-v1.md`
- `experimento-v1.md`

**Como usar:**

```bash
# 1. Copiar template
cp docs/01-dominio/templates/receita-v1.md \
   dados/receitas/REC-000XXX-nome-v1.md

# 2. Substituir placeholders
# - REC-000000 → REC-000XXX (próximo ID disponível)
# - [Título] → nome real
# - YYYY-MM-DD → data atual
# - Preencher todos os campos

# 3. Salvar e importar
python -m codigo importar
```

---

## 📊 Sistema de IDs

### Padrão de Identificadores

Formato: `TIPO-NNNNNN`

**Tipos:**
- `REC-` — Receita
- `ING-` — Ingrediente
- `TEC-` — Técnica
- `EQP-` — Equipamento
- `EXE-` — Execução
- `OBS-` — Observação
- `EXP-` — Experimento

**Números:**
- Sequencial: 000001, 000002, 000003, ...
- Sem lacunas
- Não reutilizável (deletar não libera ID)

**Por que IDs permanentes?**
- ✅ Markdown pode ser renomeado sem quebrar referências
- ✅ Permite versionamento (`-v1.md`, `-v2.md`)
- ✅ Facilita importação incremental
- ✅ Rastreabilidade histórica

---

## 🔄 Versionamento

### Como Evoluir Receitas

**Cenário:** Receita melhorou após 5 execuções

**Processo:**

```bash
# 1. Criar nova versão
cp dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md \
   dados/receitas/REC-000001-doce-de-leite-artesanal-v2.md

# 2. Editar v2
# - Atualizar frontmatter: versao: 2
# - Atualizar atualizado-em
# - Modificar ingredientes/processo
# - Adicionar nota: "v2: baseado em execuções EXE-000001 a EXE-000005"

# 3. Manter v1 como histórico
# (não deletar, apenas parar de usar)

# 4. Importar
python -m codigo importar
```

**No banco:**
- Ambas versões existem
- Queries pegam a versão mais recente por padrão
- Histórico preservado

---

## 🎯 Status das Entidades

### Ciclo de Vida

**Receita:**
- `rascunho` — ainda não testada
- `testada` — executada pelo menos uma vez com sucesso
- `validada` — executada múltiplas vezes, consistente
- `arquivada` — obsoleta, mantida apenas para histórico

**Ingrediente/Técnica/Equipamento:**
- `ativo` — em uso
- `descontinuado` — não usar em novas receitas
- `arquivado` — mantido apenas para histórico

**Experimento:**
- `planejado` — ainda não iniciado
- `em-andamento` — sendo testado
- `concluido` — finalizado (sucesso ou falha)
- `abandonado` — interrompido

---

## 📝 Tags

### Sistema de Classificação

**Tags são livres, mas organizadas:**

**Exemplos de tags:**
- Tipo de prato: `doce`, `salgado`, `bebida`
- Origem: `brasileiro`, `italiano`, `asiatico`
- Ocasião: `festa`, `dia-a-dia`, `especial`
- Características: `vegano`, `sem-gluten`, `rapido`
- Categoria: `laticinios`, `panificacao`, `confeitaria`

**No arquivo:**
```yaml
tags: [doce, brasileiro, laticinio, conserva]
```

**Uso:**
```bash
# Buscar todas as receitas de doce
grep -l "tags:.*doce" dados/receitas/*.md

# Ou consultar no banco
SELECT * FROM receitas WHERE tags LIKE '%doce%';
```

---

## 🚀 Comandos do CLI

### Interface de Linha de Comando

**Status — ver resumo do sistema:**
```bash
python -m codigo status

# Saída:
# Entidades: 42
#   receita: 15
#   ingrediente: 20
#   tecnica: 5
#   equipamento: 2
# Arestas: 87
# Issues: nenhum
```

**Validar — verificar consistência:**
```bash
python -m codigo validar

# Verifica:
# - IDs duplicados
# - Referências quebradas (ING-999 que não existe)
# - Ciclos estruturais
# - Issues críticos
```

**Importar — atualizar banco:**
```bash
python -m codigo importar [caminho/do/banco.db]

# Processa:
# 1. Parseia todos os Markdown em dados/
# 2. Valida schema e referências
# 3. Insere/atualiza no SQLite
# 4. Cria relacionamentos
# 5. Reporta erros
```

---

## 📊 Banco de Dados

### SQLite como Cache

**Localização:** `banco_de_dados/sqlite/soe.db`

**Estrutura:**

```sql
-- Tabelas principais
CREATE TABLE receitas (...)
CREATE TABLE ingredientes (...)
CREATE TABLE tecnicas (...)
CREATE TABLE equipamentos (...)
CREATE TABLE execucoes (...)
CREATE TABLE observacoes (...)
CREATE TABLE experimentos (...)

-- Tabelas de relacionamento (N:N)
CREATE TABLE receitas_ingredientes (...)
CREATE TABLE receitas_tecnicas (...)
CREATE TABLE receitas_equipamentos (...)
```

**Importante:**
- ⚠️ Banco é **regenerável** a partir dos Markdown
- ⚠️ Não editar banco diretamente (editar Markdown e reimportar)
- ⚠️ Banco é para **consultas**, não para armazenamento primário

**Consultas úteis:**

```sql
-- Receitas usando um ingrediente
SELECT r.titulo
FROM receitas r
JOIN receitas_ingredientes ri ON r.id = ri.receita_id
WHERE ri.ingrediente_id = 'ING-000001';

-- Técnicas mais usadas
SELECT t.nome, COUNT(*) as uso
FROM tecnicas t
JOIN receitas_tecnicas rt ON t.id = rt.tecnica_id
GROUP BY t.id
ORDER BY uso DESC;
```

---

## 🔄 Workflow Completo

### Do Markdown ao Banco e de Volta

```
1. CRIAÇÃO (Markdown)
   └─> Editar: dados/receitas/REC-000042-pao-v1.md

2. VALIDAÇÃO (CLI)
   └─> python -m codigo validar
       └─> Verifica: IDs, refs, schema

3. IMPORTAÇÃO (CLI → SQLite)
   └─> python -m codigo importar
       └─> Parser → Validator → Importer → DB

4. CONSULTA (SQL)
   └─> sqlite3 banco_de_dados/sqlite/soe.db
       └─> SELECT, JOIN, aggregations

5. EVOLUÇÃO (Markdown)
   └─> Editar Markdown novamente
       └─> Reimportar
           └─> Banco reflete mudanças
```

---

## 🎓 Casos de Uso Práticos

### Exemplo 1: Adicionar Nova Receita

```bash
# Passo 1: Verificar ingredientes necessários
ls dados/ingredientes/ | grep farinha

# Passo 2: Criar ingredientes faltantes
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000025-farinha-trigo-integral-v1.md

# Editar ING-000025
# ...

# Passo 3: Criar receita
cp docs/01-dominio/templates/receita-v1.md \
   dados/receitas/REC-000042-pao-integral-v1.md

# Editar REC-000042
# - Frontmatter: id, status, tags
# - Ingredientes: [ING-000025, ING-000001, ...]
# - Modo de preparo: ...

# Passo 4: Validar
python -m codigo validar

# Passo 5: Importar
python -m codigo importar
```

### Exemplo 2: Registrar Execução

```bash
# Após preparar REC-000001
cp docs/01-dominio/templates/execucao-v1.md \
   dados/execucoes/EXE-000023-doce-leite-2026-07-01-v1.md

# Editar:
---
id: EXE-000023
receita_id: REC-000001
data: 2026-07-01
resultado: sucesso
tempo_real: 2h10min
rendimento_real: 295g
---

# Observações:
- Usei panela nova (melhor distribuição de calor)
- Ponto atingido em menos tempo
- Cor mais uniforme que em EXE-000001
```

### Exemplo 3: Adicionar Observação

```bash
cp docs/01-dominio/templates/observacao-v1.md \
   dados/observacoes/OBS-000015-sal-no-doce-v1.md

# Editar:
---
id: OBS-000015
vinculada_a: [REC-000001, ING-000003]
---

# Papel do Sal no Doce de Leite

Descobri que o sal (ING-000003) não é apenas realçador de sabor.
Em concentrações pequenas (< 0,5%), ele:
1. Retarda caramelização (controle de cor)
2. Realça percepção de doçura
3. Equilibra sabor (evita enjoativo)

Fonte: Execuções EXE-000001 a EXE-000023
Testar: versão sem sal na próxima execução
```

---

## 🔍 Busca e Descoberta

### Como Encontrar Informação

**1. Grep nos Markdown:**
```bash
# Receitas com chocolate
grep -ri "chocolate" dados/receitas/

# Ingredientes fermentados
grep -ri "fermentação" dados/ingredientes/
```

**2. SQL no banco:**
```sql
-- Receitas doces com tempo < 1h
SELECT titulo, tempo_preparo
FROM receitas
WHERE tags LIKE '%doce%'
  AND tempo_preparo < 60;

-- Ingredientes nunca usados
SELECT i.nome
FROM ingredientes i
LEFT JOIN receitas_ingredientes ri ON i.id = ri.ingrediente_id
WHERE ri.ingrediente_id IS NULL;
```

**3. Status do sistema:**
```bash
# Visão geral
python -m codigo status

# Validar consistência
python -m codigo validar
```

---

## 🎯 Resumo: Por Que o SOE-CCG é Diferente

### Comparação com Gerenciadores Comuns

| Aspecto | Gerenciador Comum | SOE-CCG |
|---------|-------------------|---------|
| Formato | Banco proprietário | Markdown (texto puro) |
| Durabilidade | Anos | Décadas |
| Conhecimento | Misturado | Separado (receita ≠ execução) |
| Evolução | Sobrescrever | Versionamento |
| Relacionamentos | Básicos | Grafo completo |
| Objetivo | Organizar receitas | Evoluir conhecimento |
| Perda de dados | Alto risco | Baixo risco (texto puro) |
| Exportação | Limitada | Total (já está em Markdown) |

---

## 📚 Documentação Adicional

**Para usuários:**
- `docs/01-dominio/entidades-v1.md` — Definição das entidades
- `docs/01-dominio/templates/` — Templates prontos
- `docs/04-padroes/` — Convenções de nomenclatura

**Para desenvolvedores:**
- `docs/02-arquitetura/` — Arquitetura do sistema
- `docs/03-modelagem/` — Modelo de dados
- `kernel-docs/` — Documentação do Kernel

**Para entender filosofia:**
- `docs/00-projeto/constituicao-v1.md` — Princípios fundamentais
- `docs/00-projeto/filosofia-v1.md` — Filosofia do sistema

---

## ✨ Conclusão

O SOE-CCG é um sistema pensado para **longo prazo**.

**Você não está apenas guardando receitas.**  
**Você está construindo uma biblioteca de conhecimento gastronômico que pode durar décadas.**

Cada entidade é isolada, versionada, rastreável.  
Cada relacionamento é explícito.  
Cada evolução é documentada.  
Cada execução ensina algo novo.

**O conhecimento é permanente. A implementação é temporária.**

---

**Documento:** `COMO-FUNCIONA-SOE-CCG.md`  
**Versão:** 1.0  
**Data:** 2026-07-01  
**Público:** Usuários e desenvolvedores do sistema
