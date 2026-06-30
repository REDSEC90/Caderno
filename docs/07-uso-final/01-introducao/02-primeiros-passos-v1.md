# Primeiros Passos

> Do zero ao primeiro registro funcionando. Você vai ver o sistema rodando nos primeiros 5 minutos.

**Tempo estimado:** 15–20 minutos  
**Pré-requisitos:** nenhum — só Python 3.10+ e git instalados

---

## O que você vai fazer

```
Clonar o repositório
       ↓
Ver os dados que já existem
       ↓
Rodar o pipeline nos dados existentes
       ↓
Ver o banco funcionando
       ↓
Criar seu primeiro registro
       ↓
Commitar
```

---

## Passo 1 — Clonar e entrar no repositório

```bash
git clone <url-do-repositorio> SOE-CCG
cd SOE-CCG
```

```
# Resultado esperado:
Cloning into 'SOE-CCG'...
done.
```

---

## Passo 2 — Instalar a única dependência

```bash
pip install python-frontmatter
```

✅ Verificar:
```bash
python3 -c "import frontmatter; print('OK')"
```

```
# Resultado esperado:
OK
```

---

## Passo 3 — Ver o que já existe no sistema

Antes de qualquer configuração, explore os dados seed que já estão no repositório:

```bash
ls dados/receitas/
ls dados/ingredientes/
ls dados/tecnicas/
```

```
# Resultado esperado:
dados/receitas/:
  REC-000001-doce-de-leite-artesanal-v1.md

dados/ingredientes/:
  ING-000001-leite-integral-v1.md
  ING-000002-acucar-refinado-v1.md
  ING-000003-sal-refinado-v1.md
  ING-000004-bicarbonato-sodio-v1.md

dados/tecnicas/:
  TEC-000001-reducao-v1.md
  TEC-000002-caramelizacao-v1.md
  TEC-000003-agitacao-continua-v1.md
```

Abra um dos arquivos para entender como o sistema armazena conhecimento:

```bash
cat dados/receitas/REC-000001-doce-de-leite-artesanal-v1.md
```

Você vai ver um cabeçalho YAML (frontmatter) seguido de conteúdo Markdown. O frontmatter é onde ficam os metadados e os relacionamentos.

---

## Passo 4 — Inicializar o banco SQLite

```bash
mkdir -p banco_de_dados/sqlite

sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  < banco_de_dados/esquemas/schema-sqlite-v1.sql

echo "Banco criado:"
sqlite3 banco_de_dados/sqlite/soe-ccg.db ".tables"
```

```
# Resultado esperado:
Banco criado:
equipamentos     execucoes        experimentos     ingredientes
observacoes      receita_equipamento  receita_ingrediente  receita_tecnica
receitas         relacionamentos  tecnicas
```

---

## Passo 5 — Rodar o pipeline nos dados existentes

Agora vamos processar todos os arquivos Markdown e popular o banco:

```bash
python3 -m codigo
```

```
# Resultado esperado:
[PARSER]    Processando dados/ingredientes/ING-000001-leite-integral-v1.md
[PARSER]    Processando dados/ingredientes/ING-000002-acucar-refinado-v1.md
[PARSER]    Processando dados/ingredientes/ING-000003-sal-refinado-v1.md
[PARSER]    Processando dados/ingredientes/ING-000004-bicarbonato-sodio-v1.md
[PARSER]    Processando dados/tecnicas/TEC-000001-reducao-v1.md
...
[RESOLVER]  13 entidades, 0 referências quebradas
[VALIDADOR] 0 ciclos detectados
[IMPORTADOR] 13 entidades importadas para o SQLite
```

✅ O pipeline processou todos os arquivos sem erros.

---

## Passo 6 — Verificar que o banco está populado

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, titulo, status FROM receitas;"
```

```
# Resultado esperado:
REC-000001|Doce de Leite Artesanal|testada
```

```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes ORDER BY id;"
```

```
# Resultado esperado:
ING-000001|Leite Integral
ING-000002|Açúcar Refinado
ING-000003|Sal Refinado
ING-000004|Bicarbonato de Sódio
```

---

## Passo 7 — Rodar a auditoria (FAA)

O FAA verifica a saúde geral do repositório:

```bash
python3 scripts/auditoria/auditor-v1.py
```

```
# Resultado esperado num repositório saudável:
  Pontuação geral: 90%+
  Decisão arquitetural: APROVADO
```

Se houver falhas, consulte [`09-troubleshooting/06-faa-v1.md`](../09-troubleshooting/06-faa-v1.md).

---

## Passo 8 — Seu primeiro registro

Agora você vai criar um ingrediente novo do zero para validar que o pipeline completo funciona.

**Verificar que não existe:**
```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%mascavo%';"
```

```
# Resultado esperado (vazio = não existe, podemos criar):
(nenhum resultado)
```

**Criar o arquivo:**
```bash
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000005-acucar-mascavo-v1.md
```

**Editar o frontmatter** (abra com seu editor):
```yaml
---
id: ING-000005
tipo: ingrediente
schema-version: 1
versao: 1
status: ativo
criado-em: 2026-06-28
atualizado-em: 2026-06-28
autor: seu-nome
tags: [acucar, adocante, basico]
---

# Açúcar Mascavo

## Informações
- **Tipo:** Adoçante
- **Unidade padrão:** g

## Descrição
Açúcar não refinado com melaço incorporado. Sabor mais intenso e levemente caramelizado.
```

**Importar:**
```bash
scripts/importacao/importar.sh dados/ingredientes/ING-000005-acucar-mascavo-v1.md
```

```
# Resultado esperado:
[OK] ING-000005 importado com sucesso
```

**Verificar:**
```bash
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE id = 'ING-000005';"
```

```
# Resultado esperado:
ING-000005|Açúcar Mascavo
```

✅ Se o SELECT retornou o ingrediente, o pipeline completo está funcionando.

---

## Passo 9 — Atualizar o controle de IDs e commitar

```bash
# Atualizar a tabela de controle de IDs
# (edite docs/04-padroes/identificadores-v1.md e marque ING-000005 como último)

git add dados/ingredientes/ING-000005-acucar-mascavo-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "feat(ing): adiciona ING-000005 acucar-mascavo"
```

---

## Próximos passos

Agora que você viu o sistema funcionando de ponta a ponta:

- **Entender a mentalidade:** [`01-introducao/03-como-pensar-no-soe-v1.md`](03-como-pensar-no-soe-v1.md)
- **Ver uma sessão completa:** [`05-fluxos/07-fluxo-completo-v1.md`](../05-fluxos/07-fluxo-completo-v1.md)
- **Criar uma receita agora:** [`10-cookbook/02-criar-receita-v1.md`](../10-cookbook/02-criar-receita-v1.md)

---

## Problemas comuns nesta etapa

| Problema | Causa | Solução |
|----------|-------|---------|
| `No module named 'frontmatter'` | Dependência não instalada | `pip install python-frontmatter` |
| `sqlite3: no such file or directory` | sqlite3 não está no PATH | Instalar: `sudo apt install sqlite3` (Linux) ou `brew install sqlite3` (Mac) |
| Pipeline não encontra arquivos | Não está na raiz do repositório | `cd SOE-CCG` e tentar novamente |
| FAA reprovado no primeiro run | Arquivo de baseline ausente | Ver [`09-troubleshooting/06-faa-v1.md`](../09-troubleshooting/06-faa-v1.md) |
