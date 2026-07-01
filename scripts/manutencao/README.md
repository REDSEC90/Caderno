# scripts/manutencao — Manutenção do Sistema

Este diretório contém scripts de manutenção operacional do SOE-CCG.

## Propósito

Scripts para operações periódicas que mantêm a saúde do sistema:

- Limpeza de artefatos temporários
- Verificação de integridade do banco de dados
- Benchmark de desempenho
- Relatórios de métricas operacionais

## Critérios de Uso

Scripts neste diretório devem:

- Ser idempotentes (executar N vezes produz o mesmo resultado)
- Não modificar dados canônicos em `dados/`
- Não fazer commit nem push automaticamente
- Registrar log de execução em `docs/99-referencias/`

## Scripts Planejados (v0.9)

| Script | Propósito |
|--------|-----------|
| `benchmark.py` | Mede tempo de parse, resolução e importação |
| `audit_deps.sh` | Lista dependências externas com versões |
| `verify_db.sh` | Verifica integridade do banco SQLite |

## Uso

```bash
# Exemplo (após implementação na v0.9)
./scripts/manutencao/benchmark.py
./scripts/manutencao/verify_db.sh
```
