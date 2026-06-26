# FAA v1 — Framework de Auditoria Arquitetural

> Kernel de estado arquitetural do SOE-CCG

## O que é

O FAA v1 é um sistema de auditoria e observabilidade arquitetural que:

- **Valida** o projeto contra regras arquiteturais definidas
- **Indexa** todos os registros de conhecimento em `dados/`
- **Persiste** o estado do sistema em JSON consumível por agentes
- **Reporta** problemas críticos e avisos organizados por motor

## Uso

### Auditoria completa (padrão)

```bash
python3 auditor-v1.py
```

Executa os 12 motores, indexa registros, persiste estado em `faa-state.json`.

### Auditoria de um motor específico

```bash
python3 auditor-v1.py --motor baseline
python3 auditor-v1.py --motor semantica
```

### Gerar relatório Markdown

```bash
python3 auditor-v1.py --relatorio
```

Cria `docs/99-referencias/auditoria-v1-YYYY-MM-DD.md`.

### Consultar estado (sem rodar auditoria)

```bash
python3 auditor-v1.py state            # resumo visual
python3 auditor-v1.py state --json     # JSON puro para agentes
```

Lê o último snapshot de `faa-state.json`.

### Inspecionar um registro

```bash
python3 auditor-v1.py entity REC-000001
```

Exibe metadados, links, tags, status de validação.

### Listar problemas

```bash
python3 auditor-v1.py issues             # todos
python3 auditor-v1.py issues --critical  # apenas críticos
```

## Estrutura do `faa-state.json`

```json
{
  "timestamp": "2026-06-26T20:56:03+00:00",
  "score": 100.0,
  "decision": "APPROVED",
  "trend": "improving",
  "baseline": {
    "present": 71,
    "total": 71,
    "pct": 100.0,
    "groups": { "fundacao": 100.0, ... },
    "missing": []
  },
  "domains": {
    "Baseline": 100.0,
    "Estrutura": 100.0,
    ...
  },
  "issues": {
    "critical": [],
    "warnings": [],
    "counts": { "critical": 0, "warnings": 0 }
  },
  "index": [
    {
      "id": "REC-000001",
      "tipo": "receita",
      "versao": "1",
      "status": "testada",
      "path": "dados/receitas/REC-000001-...",
      "nome_valido": true,
      "metadados_ok": true,
      "links": ["ING-000001", "TEC-000001", ...],
      "tags": ["doce", "brasileiro"]
    },
    ...
  ]
}
```

## Motores

| Motor | Função |
|-------|--------|
| **baseline** | Decisão arquitetural global — compara contra BASELINE_V1 |
| **estrutura** | Diretórios obrigatórios, nomenclatura de arquivos |
| **filosofia** | Documentos fundacionais (constituição, princípios) |
| **dominio** | Cobertura de artefatos por entidade (esquemas, contratos) |
| **cobertura** | % de registros por tipo |
| **maturidade** | Pontuação por camada arquitetural |
| **semantica** | Termos obrigatórios/proibidos, glossário |
| **dados** | Frontmatter, IDs, estados válidos |
| **integridade** | Referências entre registros |
| **padroes** | Nomenclatura, encoding, slugs |
| **escalabilidade** | Limites de IDs, crescimento |
| **dependencias** | Grafo de relacionamentos, ciclos |

## Consumo por agentes

Um agente LLM pode:

1. Executar `python3 auditor-v1.py` uma vez
2. Ler `docs/99-referencias/faa-state.json`
3. Obter:
   - Score global do sistema
   - Decisão (APPROVED/REPROVADO)
   - Tendência (improving/stable/degrading)
   - Lista completa de problemas críticos
   - Índice de todos os registros com metadados

**Sem ler arquivos manualmente.**

## Exit codes

- `0` — sistema aprovado, sem problemas críticos
- `1` — sistema reprovado ou problemas críticos encontrados

## Filosofia

O FAA não é um linter de código. É um **kernel de consciência arquitetural** que responde:

- O sistema está coerente com sua filosofia?
- O baseline está completo?
- Os registros estão íntegros e conectados?
- O que está bloqueando a evolução?

É a **fonte da verdade sobre o estado do projeto** para agentes autônomos.
