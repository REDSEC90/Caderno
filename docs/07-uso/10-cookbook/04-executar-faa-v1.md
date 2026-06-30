# Cookbook — Executar o FAA

> Como rodar a auditoria arquitetural e interpretar os resultados.

**O FAA deve ser executado ao final de cada sessão de trabalho.**  
Ele verifica a saúde global do repositório, não apenas arquivos individuais.

---

## Execução básica

```bash
python3 scripts/auditoria/auditor-v1.py
```

```
# Resultado esperado (sistema saudável):
  Pontuação geral: 94.2%
  Decisão arquitetural: APROVADO

  Motores:
  ✓ baseline       100% — todos os artefatos obrigatórios presentes
  ✓ estrutura       98% — nomenclatura e diretórios corretos
  ✓ filosofia       90% — documentos fundacionais presentes
  ✓ dominio         95% — especificações e contratos completos
  ✓ cobertura       85% — cobertura por tipo de artefato
  ✓ maturidade      92% — pontuação por camada
  ✓ semantica       96% — linguagem oficial em uso
  ✓ dados           98% — frontmatters válidos
  ✓ integridade     90% — referências cruzadas ok
  ✓ padroes         99% — nomenclatura de arquivos
  ✓ escalabilidade 100% — limites de ID ok
  ✓ dependencias    88% — grafo sem ciclos problemáticos
```

---

## Ver apenas problemas críticos

```bash
python3 scripts/auditoria/auditor-v1.py issues --critical
```

Use isso quando quiser resolver problemas rápido sem ler o relatório completo.

---

## Motor específico

Quando souber qual área tem problema:

```bash
# Verificar apenas os dados (frontmatters, IDs, datas)
python3 scripts/auditoria/auditor-v1.py --motor dados

# Verificar apenas as dependências (referências, ciclos)
python3 scripts/auditoria/auditor-v1.py --motor dependencias

# Verificar apenas o baseline (artefatos obrigatórios)
python3 scripts/auditoria/auditor-v1.py --motor baseline
```

---

## Inspecionar uma entidade específica

```bash
python3 scripts/auditoria/auditor-v1.py entity REC-000001
```

```
# Resultado esperado:
Entidade: REC-000001
Tipo: receita
Status: testada

Arestas de saída (outgoing):
  → ING-000001  COMPOSITIONAL  FRONTMATTER
  → ING-000002  COMPOSITIONAL  FRONTMATTER
  → ING-000003  COMPOSITIONAL  FRONTMATTER
  → ING-000004  COMPOSITIONAL  FRONTMATTER
  → TEC-000001  COMPOSITIONAL  FRONTMATTER
  → TEC-000003  COMPOSITIONAL  FRONTMATTER
  → EQP-000001  COMPOSITIONAL  FRONTMATTER
  → EQP-000002  COMPOSITIONAL  FRONTMATTER

Arestas de entrada (incoming):
  ← EXE-000001  STRUCTURAL  FRONTMATTER
```

---

## Verificar estado salvo

```bash
# Estado atual persistido
python3 scripts/auditoria/auditor-v1.py state

# Em JSON (para processamento)
python3 scripts/auditoria/auditor-v1.py state --json
```

---

## Interpretando os resultados

### Score ≥ 90% + APROVADO
```
Pontuação geral: 94.2%
Decisão arquitetural: APROVADO
```
Sistema em conformidade. Prosseguir com o trabalho.

### Score ≥ 90% + REPROVADO
```
Pontuação geral: 93.1%
Decisão arquitetural: REPROVADO
Grupos bloqueantes: fundacao
```
Score alto mas algum artefato obrigatório está ausente. Geralmente um único arquivo. Ver [`09-troubleshooting/06-faa-v1.md`](../09-troubleshooting/06-faa-v1.md#problema-1).

### Score < 80%
Múltiplos problemas. Rodar motor a motor para identificar onde:
```bash
for motor in baseline estrutura dados dependencias; do
  echo "=== $motor ==="
  python3 scripts/auditoria/auditor-v1.py --motor $motor 2>&1 | tail -3
done
```

---

## Rotina recomendada de sessão

```bash
# Início da sessão — estado inicial
python3 scripts/auditoria/auditor-v1.py

# ... trabalho ...

# Após cada importação importante
python3 scripts/auditoria/auditor-v1.py issues --critical

# Final da sessão — verificação completa
python3 scripts/auditoria/auditor-v1.py
git add [arquivos]
git commit -m "[tipo]([escopo]): [descrição]"
```

---

## Problemas comuns

| Situação | O que fazer |
|----------|-------------|
| REPROVADO com score alto | Ver qual grupo está bloqueando e criar o artefato ausente |
| Score < 80% | Resolver issues críticas primeiro, depois warnings |
| Ciclo detectado | Ver `entity` das entidades no ciclo para entender o tipo de aresta |
| `No module named 'frontmatter'` | `pip install python-frontmatter` |

Para diagnóstico detalhado: [`09-troubleshooting/06-faa-v1.md`](../09-troubleshooting/06-faa-v1.md)
