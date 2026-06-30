# Troubleshooting — FAA

> Diagnóstico de falhas na auditoria arquitetural (`scripts/auditoria/auditor-v1.py`).

**O FAA verifica a saúde global do repositório — não apenas arquivos individuais.**  
Um sistema pode ter todos os arquivos corretos mas ainda ser reprovado pelo FAA se algum artefato obrigatório estiver ausente.

---

## Como executar o FAA

```bash
# Auditoria completa
python3 scripts/auditoria/auditor-v1.py

# Ver apenas falhas críticas
python3 scripts/auditoria/auditor-v1.py issues --critical

# Motor específico
python3 scripts/auditoria/auditor-v1.py --motor baseline
python3 scripts/auditoria/auditor-v1.py --motor dados
python3 scripts/auditoria/auditor-v1.py --motor dependencias

# Inspecionar uma entidade específica
python3 scripts/auditoria/auditor-v1.py entity REC-000001
```

---

## Interpretando o resultado

```
Pontuação geral: 94.2%
Decisão arquitetural: REPROVADO
Grupos bloqueantes: fundacao
```

| Situação | Significado |
|----------|-------------|
| Score ≥ 90% + APROVADO | Sistema em conformidade total |
| Score ≥ 90% + REPROVADO | Um artefato em grupo bloqueante está ausente. Um único arquivo. |
| Score < 80% | Múltiplos problemas. Verificar motor a motor. |
| Score < 50% | Sistema significativamente fora de conformidade |

---

## Problema 1: `[BAS-002] Sistema reprovado — artefato ausente`

**Sintoma:**
```
[BAS-002] CRITICAL: artefato ausente em grupo bloqueante
  → Criar: docs/00-projeto/visao-v1.md
  Grupo: fundacao
  Score sem este artefato: BLOQUEANTE
```

**Causa:** Um documento obrigatório do baseline não existe. O baseline define o mínimo que o repositório precisa ter.

**Diagnóstico:**
```bash
# Ver todos os artefatos que o baseline verifica
python3 scripts/auditoria/auditor-v1.py --motor baseline --verbose

# Verificar o que está faltando
python3 scripts/auditoria/auditor-v1.py issues --critical
```

**Solução:** Criar o arquivo indicado com conteúdo mínimo válido:
```bash
# Exemplo para docs/00-projeto/visao-v1.md
cat > docs/00-projeto/visao-v1.md << 'EOF'
# Visão do SOE-CCG

> Declaração de visão de longo prazo do sistema.

## Visão

Construir um repositório permanente de conhecimento culinário gastronômico,
independente de tecnologia, rastreável e evoluível.
EOF

git add docs/00-projeto/visao-v1.md
git commit -m "docs(projeto): cria visao-v1 para completar baseline"
```

Após criar, rodar o FAA novamente para confirmar que o bloqueio foi resolvido.

---

## Problema 2: `[DEP-002] Ciclo detectado`

**Sintoma:**
```
[DEP-002] ERROR: ciclo detectado no grafo de dependências
  REC-000001 → TEC-000001 → REC-000001
  Tipo de aresta no ciclo: STRUCTURAL
```

**Diagnóstico:**
```bash
# Inspecionar as entidades do ciclo
python3 scripts/auditoria/auditor-v1.py entity REC-000001
python3 scripts/auditoria/auditor-v1.py entity TEC-000001
```

**Interpretação:**

- Ciclo com arestas STRUCTURAL → **sempre erro** — um dos vínculos está semanticamente errado
- Ciclo com arestas INFORMATIONAL → **geralmente válido** — é uma menção cruzada entre entidades

**Solução para ciclo STRUCTURAL:**
Revisar os frontmatters. Técnicas não referenciam Receitas em campos estruturais. Se `TEC-000001` tem `receita-id: REC-000001` no frontmatter, isso está errado — esse campo é exclusivo de Execuções.

---

## Problema 3: `[DAD-001] Frontmatter inválido em dados/`

**Sintoma:**
```
[DAD-001] ERROR: frontmatter inválido
  dados/ingredientes/ING-000005-meu-ing-v1.md
  Campo 'criado-em' tem valor literal 'YYYY-MM-DD'
```

**Causa:** O template foi copiado mas os campos de data não foram preenchidos.

**Diagnóstico:**
```bash
grep "YYYY-MM-DD" dados/ingredientes/ING-000005-meu-ing-v1.md
```

**Solução:**
```bash
nano dados/ingredientes/ING-000005-meu-ing-v1.md
# Trocar YYYY-MM-DD pela data real: 2026-06-28
```

Campos com valores literais de template (`YYYY-MM-DD`, `[PREFIXO]-[NNNNNN]`, `nome-do-autor`) são rejeitados pelo FAA.

---

## Problema 4: `[EST-001] Arquivo em diretório errado`

**Sintoma:**
```
[EST-001] WARNING: arquivo com prefixo ING fora do diretório correto
  dados/receitas/ING-000005-meu-ing-v1.md ← errado
```

**Causa:** O arquivo foi criado no diretório errado.

**Solução:**
```bash
mv dados/receitas/ING-000005-meu-ing-v1.md \
   dados/ingredientes/ING-000005-meu-ing-v1.md
git add -A
git commit -m "fix(ing): move ING-000005 para diretório correto"
```

**Diretórios corretos por prefixo:**

| Prefixo | Diretório |
|---------|-----------|
| REC | `dados/receitas/` |
| ING | `dados/ingredientes/` |
| TEC | `dados/tecnicas/` |
| EQP | `dados/equipamentos/` |
| EXE | `dados/execucoes/` |
| OBS | `dados/observacoes/` |
| EXP | `dados/experimentos/` |

---

## Problema 5: Score < 80% sem causa óbvia

**Diagnóstico passo a passo:**

```bash
# 1. Ver quais motores estão falhando
python3 scripts/auditoria/auditor-v1.py

# 2. Rodar o motor com menor score isoladamente
python3 scripts/auditoria/auditor-v1.py --motor baseline
python3 scripts/auditoria/auditor-v1.py --motor dados
python3 scripts/auditoria/auditor-v1.py --motor estrutura

# 3. Ver todas as issues, não apenas críticas
python3 scripts/auditoria/auditor-v1.py issues

# 4. Inspecionar entidades suspeitas
python3 scripts/auditoria/auditor-v1.py entity [ID]
```

Resolver as issues críticas primeiro (CRITICAL), depois as de warning.

---

## Problema 6: `[ERR-000] No module named 'frontmatter'`

**Sintoma:** O FAA falha logo no início com erro de import.

**Solução:**
```bash
pip install python-frontmatter
# ou
pip install python-frontmatter --break-system-packages
```

---

## Próxima leitura

- Se o FAA aprova mas há erros no banco → [`05-sqlite-v1.md`](05-sqlite-v1.md)
- Guia completo do FAA → [`../03-validacao/05-faa-v1.md`](../03-validacao/05-faa-v1.md)
