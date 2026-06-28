# Fluxo Completo — Sessão de Trabalho

> Uma sessão de trabalho do início ao fim. Leitura única recomendada antes de começar.

---

## Cenário

Você preparou um pão de queijo ontem, baseado em uma receita que ainda não está no sistema. Hoje vai registrar tudo.

---

## 1. Abrir o repositório e verificar o estado

```bash
cd /path/to/SOE-CCG
git status               # deve estar limpo
git pull                 # sincronizar se trabalhando com remoto

# Checar saúde inicial
python3 scripts/auditoria/auditor-v1.py
```

---

## 2. Planejar o que vai criar

Na sessão de hoje:
- 5 novos ingredientes (polvilho, queijo, ovo, óleo, sal já existe? verificar)
- 1 nova técnica (modelagem manual)
- 1 novo equipamento (forma antiaderente)
- 1 nova receita (REC)
- 1 execução de ontem (EXE)
- 1 observação sobre o resultado (OBS)

**Consultar próximos IDs disponíveis** em `docs/04-padroes/identificadores-v1.md`:
```
ING → último: ING-000004 → próximos: ING-000005 a ING-000009
TEC → último: TEC-000003 → próximo: TEC-000004
EQP → último: EQP-000002 → próximo: EQP-000003
REC → último: REC-000001 → próximo: REC-000002
EXE → último: EXE-000001 → próximo: EXE-000002
OBS → último: OBS-000001 → próximo: OBS-000002
```

---

## 3. Criar ingredientes (ING)

```bash
# Verificar quais já existem
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT id, nome FROM ingredientes WHERE nome LIKE '%sal%'
   UNION SELECT id, nome FROM ingredientes WHERE nome LIKE '%ovo%';"
```

Para cada ingrediente faltante:
```bash
cp docs/01-dominio/templates/ingrediente-v1.md \
   dados/ingredientes/ING-000005-polvilho-azedo-v1.md
# Editar → preencher frontmatter → importar
scripts/importacao/importar.sh dados/ingredientes/ING-000005-polvilho-azedo-v1.md
```

Repetir para: `ING-000006`, `ING-000007`, `ING-000008`, `ING-000009`.

---

## 4. Criar técnica e equipamento

```bash
cp docs/01-dominio/templates/tecnica-v1.md \
   dados/tecnicas/TEC-000004-modelagem-manual-v1.md
# Editar e importar

cp docs/01-dominio/templates/equipamento-v1.md \
   dados/equipamentos/EQP-000003-forma-antiaderente-v1.md
# Editar e importar
```

---

## 5. Criar a Receita

```bash
cp docs/01-dominio/templates/receita-v1.md \
   dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
```

Preencher frontmatter com todos os IDs corretos em `ingredientes`, `tecnicas`, `equipamentos`.

```bash
scripts/importacao/importar.sh dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md

# Verificar no banco
sqlite3 banco_de_dados/sqlite/soe-ccg.db \
  "SELECT source, target, kind FROM relacionamentos WHERE source = 'REC-000002';"
```

---

## 6. Registrar a execução de ontem

```bash
cp docs/01-dominio/templates/execucao-v1.md \
   dados/execucoes/EXE-000002-pao-de-queijo-execucao1-v1.md
```

Frontmatter: `receita-id: REC-000002`, `data-execucao: 2026-06-26` (ontem).

Preencher desvios, avaliações e métricas.

```bash
scripts/importacao/importar.sh dados/execucoes/EXE-000002-pao-de-queijo-execucao1-v1.md

# Promover receita de rascunho para testada
nano dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
# status: testada
scripts/importacao/importar.sh dados/receitas/REC-000002-pao-de-queijo-mineiro-v1.md
```

---

## 7. Registrar descoberta como Observação

```bash
cp docs/01-dominio/templates/observacao-v1.md \
   dados/observacoes/OBS-000002-queijo-temperatura-v1.md
# entidade-referenciada: EXE-000002
# relevancia: alta
# Conteúdo: o que foi aprendido
scripts/importacao/importar.sh dados/observacoes/OBS-000002-queijo-temperatura-v1.md
```

---

## 8. Atualizar controle de IDs

Abrir `docs/04-padroes/identificadores-v1.md` e atualizar a tabela:
```
ING → ING-000009
TEC → TEC-000004
EQP → EQP-000003
REC → REC-000002
EXE → EXE-000002
OBS → OBS-000002
```

---

## 9. Rodar FAA e verificar saúde

```bash
python3 scripts/auditoria/auditor-v1.py
```

Resultado esperado: `APROVADO`, sem novas falhas.

---

## 10. Commit da sessão

```bash
git add dados/
git add docs/04-padroes/identificadores-v1.md
git status  # revisar o que está sendo commitado

git commit -m "feat: sessao 2026-06-27 — REC-000002 pao-de-queijo + 5 ING + EXE + OBS"
git push origin main
```

---

## Resultado

```
✅ 5 ingredientes criados
✅ 1 técnica criada
✅ 1 equipamento criado
✅ 1 receita criada e importada
✅ 1 execução registrada
✅ 1 observação criada
✅ FAA aprovado
✅ Commit realizado
```

O conhecimento do pão de queijo — receita, preparo, aprendizado — está preservado, rastreável e consultável.
