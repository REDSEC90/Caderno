# scripts/copia_seguranca — Backup e Recuperação

Este diretório contém scripts para backup e recuperação do banco de dados SQLite do SOE-CCG.

## Propósito

Garantir que nenhuma perda de dados ocorra durante operações de importação, migração ou falha inesperada.

**Princípio fundamental:** O Markdown em `dados/` é a fonte de verdade (ADR-0001). O banco SQLite é derivado e pode ser reconstruído a qualquer momento via `importar.sh`. Os backups do banco são uma conveniência operacional, não a fonte de verdade.

## Scripts Planejados (v0.9)

| Script | Propósito |
|--------|-----------|
| `backup.sh` | Cria cópia do banco com timestamp |
| `restore.sh` | Restaura banco a partir de um backup |
| `verify.sh` | Verifica integridade do backup (SHA-256) |

## Política de Retenção (a definir na v0.9)

- Manter últimos 7 backups diários
- Manter últimos 4 backups semanais
- Backups anteriores a 30 dias: remover automaticamente
- Localização padrão: `~/.soe-ccg/backups/` (fora do repositório)

## Uso (após implementação na v0.9)

```bash
# Criar backup
./scripts/copia_seguranca/backup.sh

# Verificar integridade
./scripts/copia_seguranca/verify.sh backups/soe-ccg-20260701.db

# Restaurar
./scripts/copia_seguranca/restore.sh backups/soe-ccg-20260701.db
```

## Alternativa sempre disponível

Como o Markdown é a fonte de verdade, o banco pode ser reconstruído sem backup:

```bash
./scripts/importacao/importar.sh
```
