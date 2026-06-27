# Scripts do SOE-CCG

## FAA — Framework de Auditoria Arquitetural

### FAA v2 (atual) — Sistema de governança arquitetural

**Localização:** `faa/`

Sistema de governança arquitetural contínua com capacidade de:
- Observar estado completo do sistema
- Detectar problemas automaticamente
- Gerar roadmap de ações priorizadas
- Manter histórico via snapshots

**Quick start:**
```bash
./faa.sh status    # Ver estado do sistema
./faa.sh plan      # Ver próximas ações
```

📖 Documentação completa: `faa/README.md`

---

### FAA v1 (legado) — Kernel de decisão arquitetural

**Localização:** `auditoria/`

Sistema de auditoria com 12 motores especializados.

**Quick start:**
```bash
cd auditoria
python3 auditor-v1.py
```

📖 Documentação: `auditoria/README.md`

---

## Migração v1 → v2

Consulte `faa/MIGRATION.md` para guia completo de migração.

**Resumo:**
- v1 = validação arquitetural
- v2 = governança contínua (valida + planeja + rastreia)

---

## Estrutura

```
scripts/
├── faa/              # FAA v2 (governança)
├── auditoria/        # FAA v1 (legado)
└── faa.sh           # Helper para executar FAA v2
```
