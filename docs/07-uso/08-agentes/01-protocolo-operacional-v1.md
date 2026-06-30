# Protocolo Operacional — Agentes

> Contrato formal de como qualquer agente automatizado ou sistema de IA deve operar o SOE-CCG.

Este documento é normativo. Não é sugestão — é o protocolo que todo agente deve seguir sem exceção.

---

## O que é um agente neste contexto

Um agente é qualquer sistema automatizado que opera sobre o repositório sem interação humana direta. Isso inclui:
- Scripts de importação em lote
- Sistemas de IA que criam ou editam entidades
- Pipelines de CI/CD que modificam dados
- Qualquer automação que lê ou escreve em `dados/`

---

## Princípio fundamental

**O agente nunca é a fonte de verdade.**

O agente é um operador do sistema, não o sistema. Toda decisão de negócio (o que registrar, como classificar, qual status atribuir) pertence ao humano. O agente executa operações dentro das regras — não as define.

---

## Sequência obrigatória para qualquer operação de escrita

```
1. VERIFICAR → O que existe? O ID referenciado existe?
2. VALIDAR   → A operação é permitida? Respeita as regras?
3. EXECUTAR  → Escrever o arquivo Markdown
4. IMPORTAR  → Importar para o SQLite
5. VERIFICAR → O resultado está correto?
6. COMMITAR  → git add + git commit com mensagem descritiva
```

**Nunca pular etapas.** Uma operação sem verificação final pode introduzir dados corrompidos silenciosamente.

---

## Antes de qualquer operação: leitura do estado atual

```bash
# Estado do repositório
git status
git log --oneline -5

# Saúde do sistema
python3 scripts/auditoria/auditor-v1.py issues --critical

# IDs existentes por tipo
sqlite3 banco_de_dados/sqlite/soe-ccg.db "
  SELECT 'REC' as tipo, COUNT(*) FROM receitas UNION ALL
  SELECT 'ING', COUNT(*) FROM ingredientes UNION ALL
  SELECT 'TEC', COUNT(*) FROM tecnicas UNION ALL
  SELECT 'EQP', COUNT(*) FROM equipamentos UNION ALL
  SELECT 'EXE', COUNT(*) FROM execucoes UNION ALL
  SELECT 'OBS', COUNT(*) FROM observacoes UNION ALL
  SELECT 'EXP', COUNT(*) FROM experimentos;
"
```

---

## Verificação de existência antes de criar

**Obrigatório.** Criar duplicatas corrompe o grafo.

```bash
# Verificar por nome aproximado
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%[TERMO]%';"

# Verificar por arquivo
ls dados/ingredientes/ | grep -i "[slug]"

# Verificar por texto livre
grep -r "[NOME]" dados/ingredientes/ --include="*.md"
```

Se encontrar o conceito, **usar o ID existente**. Nunca criar um segundo.

---

## Obtenção de IDs

```bash
# Próximo ID disponível para cada tipo
sqlite3 banco_de_dados/sqlite/soe-ccg.db "
  SELECT MAX(id) FROM receitas;
  SELECT MAX(id) FROM ingredientes;
  SELECT MAX(id) FROM tecnicas;
  SELECT MAX(id) FROM equipamentos;
  SELECT MAX(id) FROM execucoes;
  SELECT MAX(id) FROM observacoes;
  SELECT MAX(id) FROM experimentos;
"
```

O próximo ID é: pegar o último, incrementar o número, manter 6 dígitos com zeros à esquerda.
`ING-000004` → `ING-000005`.

⚠️ Em operações concorrentes, verificar o ID novamente imediatamente antes de escrever o arquivo para evitar conflito.

---

## Validação antes de importar

```bash
# Verificar que o Parser consegue ler o arquivo
python3 codigo/parser-v1.py dados/[tipo]/[ID]-[slug]-v1.md

# Verificar que não há referências quebradas
python3 codigo/resolvedor-v1.py dados/[tipo]/[ID]-[slug]-v1.md
```

Se qualquer um desses falhar, **não importar**. Corrigir o arquivo e tentar novamente.

---

## Importação

```bash
# Importar arquivo individual
scripts/importacao/importar.sh dados/[tipo]/[ID]-[slug]-v1.md

# Verificar o resultado imediatamente após
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, [campo-principal] FROM [tabela] WHERE id = '[ID]';"
```

---

## Commit obrigatório após cada sessão de operações

```bash
git add dados/[tipo]/[ID]-[slug]-v1.md
git add docs/04-padroes/identificadores-v1.md
git commit -m "[tipo]([escopo]): [descrição clara da operação]"
```

Padrões de mensagem:
```
feat(ing): adiciona ING-000005 acucar-mascavo
feat(rec): cria REC-000002 pao-de-queijo-mineiro
feat(exe): registra EXE-000002 doce-de-leite 2026-06-28
fix(ing): corrige status de ING-000003 para ativo
chore(ing): arquiva ING-000006 duplicata de ING-000001
```

---

## Auditoria após operações

```bash
python3 scripts/auditoria/auditor-v1.py
```

Se o sistema estava `APROVADO` antes e ficou `REPROVADO` depois, a operação introduziu um problema. Identificar e corrigir antes de encerrar.

---

## Próxima leitura

- Regras invioláveis → [`02-invariantes-v1.md`](02-invariantes-v1.md)
- Sequências permitidas → [`03-sequencias-validas-v1.md`](03-sequencias-validas-v1.md)
- Referência de comandos → [`../07-referencia/comandos-v1.md`](../07-referencia/comandos-v1.md)
