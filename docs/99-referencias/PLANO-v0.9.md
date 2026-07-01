# Plano de Execução — v0.9: Hardening

**Data:** 2026-07-01  
**Objetivo:** Endurecer o sistema contra falhas, reduzir superfície de risco e garantir recuperação sem perda de dados.  
**Pré-requisito:** v0.8 entregue (escalabilidade e automação operacionais).

---

## Estado Esperado ao Entrar na v0.9 (pós v0.8)

| Componente               | Estado Esperado                        |
|--------------------------|----------------------------------------|
| Arquitetura              | ✅ Congelada                           |
| Kernel                   | ✅ Estável + auto-registro             |
| Automação                | ✅ Pipeline de release operacional     |
| Cobertura `codigo/`      | ✅ ≥ 90%                               |
| Type hints               | ✅ Completos (mypy strict)             |
| FAA contínuo             | ✅ Snapshots automáticos               |
| Segurança                | 🔴 Não tratada ainda                   |
| Recuperação de falhas    | 🔴 Não tratada ainda                   |
| Testes de carga          | 🔴 Não tratada ainda                   |

---

## Etapas da v0.9

### Etapa 1 — Hardening do importador

**Objetivo:** Garantir que falhas durante a importação não corrompem o banco de dados.

**Entregas:**
- Transações atômicas por entidade (rollback parcial sem afetar entidades já importadas)
- Validação pré-importação: rejeitar entidades com IDs duplicados sem sobrescrever sem aviso
- Log estruturado de erros com rastreabilidade (entity_id, campo, motivo)
- Modo `--dry-run`: simular importação sem persistir
- Testes: cenários de falha controlada, banco corrompido, entidades inválidas

---

### Etapa 2 — Hardening do parser

**Objetivo:** Parser não deve travar nem produzir resultados silenciosamente errados em entradas malformadas.

**Entregas:**
- Limites de segurança: arquivo > 1MB → aviso explícito
- Frontmatter malformado → `ParseError` com localização precisa (linha, campo)
- Corpo com loops de referência circulares → detectado e reportado
- Modo estrito (`--strict`): qualquer aviso vira erro
- Testes: golden files de entradas patológicas (`testes/golden/pathological/`)

---

### Etapa 3 — Backup e recuperação

**Objetivo:** O sistema deve ser capaz de se recuperar de falhas sem perda de dados.

**Entregas:**
- `scripts/copia_seguranca/backup.sh` — cópia completa do banco SQLite com timestamp
- `scripts/copia_seguranca/restore.sh` — restaura a partir de um backup
- `scripts/copia_seguranca/verify.sh` — verifica integridade do backup (hash SHA-256)
- Política de retenção: definida em `scripts/copia_seguranca/README.md`
- Teste: criar backup → corromper banco → restaurar → verificar integridade

---

### Etapa 4 — Testes de regressão completos

**Objetivo:** Garantir que nenhuma mudança futura quebra silenciosamente o comportamento existente.

**Entregas:**
- Suite de regressão: `testes/regression/` com cenários end-to-end completos
  - Importar dataset completo → verificar banco resultante
  - Importar dataset após mudança de schema → verificar migração
  - Re-importar mesma entidade → verificar idempotência
- Golden outputs do banco: `testes/golden/db/` com snapshots do banco para cada dataset
- Comparador: `testes/regression/compare_db.py` — diff entre banco gerado e golden output

---

### Etapa 5 — Testes de carga

**Objetivo:** Identificar limites de desempenho antes da v1.0.

**Entregas:**
- Dataset de stress: `testes/golden/large/` com 500+ entidades
- Benchmark: `scripts/manutencao/benchmark.py` — mede tempo de parse, resolução e importação
- Limites documentados: tempo máximo aceitável por operação
- Relatório: `docs/99-referencias/benchmark-v1.md`

---

### Etapa 6 — Segurança e validação de entrada

**Objetivo:** O sistema não deve executar conteúdo arbitrário nem expor dados sensíveis.

**Entregas:**
- Sanitização de caminhos: `parse_directory` não segue symlinks fora do ROOT
- Validação de IDs: rejeitar IDs com caracteres fora do padrão definido
- Validação de frontmatter: campos desconhecidos geram aviso (não são silenciados)
- Auditoria de dependências: `scripts/manutencao/audit_deps.sh` — lista dependências externas com versões

---

### Etapa 7 — Validação Final e Release v0.9

**Entregas:**
- Rodar pipeline completo
- FAA score ≥ 92
- Todos os testes passando (target: ≥ 550)
- Atualizar CHANGELOG.md com v0.9.0
- Tag `v0.9.0`

---

## Critérios de Conclusão (Definition of Done)

- [ ] Importador com transações atômicas e modo dry-run
- [ ] Parser com limites e modo estrito
- [ ] Backup + restore + verify operacionais
- [ ] Suite de regressão com golden outputs
- [ ] Benchmark documentado
- [ ] Validação de entrada e sanitização
- [ ] FAA score ≥ 92
- [ ] Todos os testes passando (≥ 550)
- [ ] Tag v0.9.0 criada

---

**Documento:** `PLANO-v0.9.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
