# FAA — Framework de Auditoria Arquitetural

> Como executar, interpretar e agir sobre os resultados da auditoria.

---

## O que é o FAA

O FAA é o sistema de verificação de saúde arquitetural do repositório inteiro. Enquanto o Parser/Resolver/Validador verificam arquivos individuais, o FAA verifica o sistema como um todo.

Ele responde sete perguntas fundamentais:
1. O que existe no sistema?
2. Está correto (em conformidade com os contratos)?
3. Está coerente com a filosofia?
4. Está completo (baseline mínimo)?
5. Está evoluindo corretamente?
6. O que está bloqueando?
7. Qual o estado global atual?

---

## Executando

```bash
# Auditoria completa
python3 scripts/auditoria/auditor-v1.py

# Motor específico
python3 scripts/auditoria/auditor-v1.py --motor baseline
python3 scripts/auditoria/auditor-v1.py --motor dados
python3 scripts/auditoria/auditor-v1.py --motor dependencias

# Estado atual persistido
python3 scripts/auditoria/auditor-v1.py state
python3 scripts/auditoria/auditor-v1.py state --json

# Inspecionar uma entidade
python3 scripts/auditoria/auditor-v1.py entity REC-000001

# Listar problemas
python3 scripts/auditoria/auditor-v1.py issues
python3 scripts/auditoria/auditor-v1.py issues --critical
```

---

## Os 12 Motores

| Motor | Verifica |
|-------|---------|
| `baseline` | Artefatos obrigatórios (ground truth) — é o motor de decisão |
| `estrutura` | Diretórios, nomenclatura, arquivos críticos |
| `filosofia` | Documentos fundacionais (constituição, axiomas, princípios) |
| `dominio` | Especificações, contratos, templates e esquemas por entidade |
| `cobertura` | Porcentagem de cobertura por tipo de artefato |
| `maturidade` | Pontuação por camada arquitetural |
| `semantica` | Termos obrigatórios/proibidos na linguagem oficial |
| `dados` | Frontmatter, IDs, estados e datas nos arquivos de `dados/` |
| `integridade` | Referências cruzadas entre registros |
| `padroes` | Nomenclatura, encoding, slug dos arquivos |
| `escalabilidade` | Limites de IDs e estrutura para crescimento |
| `dependencias` | Grafo de relacionamentos, ciclos, nós isolados |

---

## Interpretando o Resultado

```
  Pontuação geral: 94.2%
  Decisão arquitetural: REPROVADO
  Grupos bloqueantes: fundacao
```

**Score ≥ 90% mas REPROVADO** — há um artefato faltante em um grupo bloqueante. Geralmente um único arquivo ausente.

**Score < 80%** — múltiplos problemas. Verificar detalhes motor a motor.

**APROVADO** — todos os grupos bloqueantes passaram. O sistema está em conformidade.

---

## Catálogo de Falhas e Correções

### [BAS-001] / [BAS-002] — Artefato obrigatório ausente

```
⚠️  [BAS-001] Grupo 'fundacao': 86% (6/7) — limiar 100%
         → Ausente: visao → docs/00-projeto/visão-v1.md
```

**Ação:** Criar o arquivo apontado. Ver `docs/07-uso/03-validacao/07-resolucao-de-erros.md`.

### [DEP-002] — Ciclo detectado

```
❌ [DEP-002] Ciclo detectado: REC-000001 → OBS-000001 → EXE-000001 → REC-000001
```

**Análise:** Verificar se o ciclo é em arestas STRUCTURAL (erro real) ou INFORMATIONAL (pode ser válido).

```bash
python3 scripts/auditoria/auditor-v1.py entity REC-000001
python3 scripts/auditoria/auditor-v1.py entity OBS-000001
```

Se as arestas que formam o ciclo são todas INFORMATIONAL, o ciclo é semanticamente válido — referências cruzadas no corpo de documentos. Isso é um item pendente no motor de dependências (v0.9).

### [ERR-000] — Dependência Python ausente

```
❌ [ERR-000] Erro interno: No module named 'frontmatter'
```

**Ação:**
```bash
pip install python-frontmatter --break-system-packages
```

---

## Estado Persistido

Após cada auditoria, o FAA salva o estado em `docs/99-referencias/faa-state.json`. Esse arquivo é o kernel de estado do sistema — pode ser lido por agentes sem executar a auditoria.

```json
{
  "timestamp": "2026-06-27T09:00:00Z",
  "score": 94.2,
  "decision": "REPROVADO",
  "motors": { ... },
  "records": [...]
}
```

---

## Meta de Saúde

| Métrica | Meta | Mínimo aceitável |
|---------|------|-----------------|
| Score global | ≥ 90% | ≥ 80% |
| Falhas críticas | 0 | 0 |
| Grupos bloqueantes | 0 | 0 |
| Avisos | 0 | ≤ 3 |
