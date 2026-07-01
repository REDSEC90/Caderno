# Plano de Execução — v0.9: Confiabilidade (REVISADO)

**Data de criação original:** 2026-07-01  
**Data de revisão:** 2026-07-01 19:30  
**Pré-requisito:** v0.8 completamente entregue (v0.8.0 + v0.8.1 + v0.8.2)  
**Objetivo:** Sistema robusto, seguro, resiliente e com recuperação garantida.

---

## Mudança de Escopo

### Antes (Plano Original)

**Nome:** v0.9 — Hardening

**Foco:** Apenas endurecer o sistema contra falhas

### Agora (Plano Revisado)

**Nome:** v0.9 — Confiabilidade

**Foco:** Hardening + Segurança + Performance + Resiliência

**Justificativa:** Após automação completa (v0.8), o sistema precisa de garantias operacionais abrangentes, não apenas tratamento de falhas.

---

## Estado Esperado ao Entrar na v0.9 (pós v0.8.2)

| Componente               | Estado Esperado                        |
|--------------------------|----------------------------------------|
| Arquitetura              | ✅ Congelada                           |
| Kernel                   | ✅ Estável (92% cobertura)             |
| Runtime Core             | ✅ Estável (97% cobertura)             |
| CLI                      | ✅ Testada (≥80% cobertura)            |
| Pipeline                 | ✅ Automatizado e reproduzível         |
| FAA contínuo             | ✅ Snapshots + diff + histórico        |
| Contratos                | ✅ Validados automaticamente           |
| Type hints               | ✅ Completos (mypy strict)             |
| Cobertura global         | ✅ ≥90%                                |
| Testes                   | ✅ ≥500 passando                       |
| Auto-registro            | ✅ Implementado                        |
| Segurança                | 🔴 Não tratada ainda                   |
| Recuperação de falhas    | 🔴 Não tratada ainda                   |
| Testes de carga          | 🔴 Não tratada ainda                   |
| Benchmarks               | 🔴 Não tratada ainda                   |
| Backup/Restore           | 🔴 Não tratada ainda                   |

---

## Áreas de Atuação da v0.9

### 1. Hardening

**Objetivo:** Sistema não falha silenciosamente, se recupera de erros graciosamente.

**Etapas:**
- Hardening do importador (transações atômicas, rollback, dry-run)
- Hardening do parser (limites, modo estrito, entradas patológicas)
- Validação de integridade de dados

### 2. Segurança

**Objetivo:** Sistema não executa código arbitrário nem expõe dados sensíveis.

**Etapas:**
- Sanitização de caminhos (sem symlinks fora do ROOT)
- Validação de IDs (padrão rigoroso)
- Validação de frontmatter (campos desconhecidos geram aviso)
- Auditoria de dependências externas

### 3. Performance

**Objetivo:** Sistema escala sem degradação.

**Etapas:**
- Benchmarks documentados
- Testes de carga (500+ entidades)
- Limites de desempenho definidos
- Monitoramento de performance

### 4. Resiliência

**Objetivo:** Sistema se recupera de falhas sem perda de dados.

**Etapas:**
- Backup automático do banco SQLite
- Restore verificado com integridade
- Recovery sem perda de dados
- Política de retenção de backups

### 5. Qualidade

**Objetivo:** Regressões são detectadas automaticamente.

**Etapas:**
- Suite de regressão completa
- Golden outputs do banco
- Testes de concorrência
- Testes de corrupção

---

## Etapas da v0.9

### Etapa 1 — Hardening do Importador

**Objetivo:** Garantir que falhas durante a importação não corrompem o banco de dados.

**Entregas:**
- Transações atômicas por entidade
  - Rollback parcial sem afetar entidades já importadas
  - Commit por entidade, não por batch
- Validação pré-importação
  - Rejeitar entidades com IDs duplicados sem sobrescrever
  - Validar schema antes de inserir
  - Validar foreign keys
- Log estruturado de erros
  - Rastreabilidade: entity_id, campo, motivo, timestamp
  - Formato JSON para parsing automático
- Modo `--dry-run`
  - Simular importação sem persistir
  - Reportar o que seria feito
- Testes:
  - Cenários de falha controlada
  - Banco corrompido
  - Entidades inválidas
  - Rollback parcial
  - Idempotência

**Validação:**
- Falha em 1 entidade → outras não afetadas
- `--dry-run` não persiste nada
- Logs estruturados parseáveis
- Cobertura ≥ 95% em `importador.py`

---

### Etapa 2 — Hardening do Parser

**Objetivo:** Parser não deve travar nem produzir resultados silenciosamente errados em entradas malformadas.

**Entregas:**
- Limites de segurança
  - Arquivo > 1MB → aviso explícito
  - Arquivo > 10MB → rejeita
  - Profundidade de referências circulares > 100 → rejeita
- Frontmatter malformado
  - `ParseError` com localização precisa (linha, campo)
  - Mensagem de erro clara e acionável
- Corpo com loops de referência circulares
  - Detectado e reportado
  - Não trava o parser
- Modo estrito (`--strict`)
  - Qualquer aviso vira erro
  - Campos desconhecidos → erro
  - IDs inválidos → erro
- Testes:
  - Golden files de entradas patológicas: `testes/golden/pathological/`
  - Arquivo gigante
  - Frontmatter malformado
  - Referências circulares
  - Caracteres especiais
  - UTF-8 inválido

**Validação:**
- Parser nunca trava (timeout 10s)
- Modo estrito rejeita entradas suspeitas
- Mensagens de erro claras
- Cobertura ≥ 95% em `parser.py`

---

### Etapa 3 — Backup e Recuperação

**Objetivo:** O sistema deve ser capaz de se recuperar de falhas sem perda de dados.

**Entregas:**
- `scripts/copia_seguranca/backup.sh`
  - Cópia completa do banco SQLite com timestamp
  - Compressão opcional (gzip)
  - Verificação de integridade (SHA-256)
  - Rotação automática (política de retenção)
- `scripts/copia_seguranca/restore.sh`
  - Restaura a partir de um backup
  - Valida integridade antes de restaurar
  - Backup do banco atual antes de sobrescrever
- `scripts/copia_seguranca/verify.sh`
  - Verifica integridade do backup (hash SHA-256)
  - Testa restore em ambiente isolado
- `scripts/copia_seguranca/README.md`
  - Política de retenção definida
  - Procedimentos de backup e restore
  - Troubleshooting
- Testes:
  - Criar backup → verificar integridade
  - Corromper banco → restaurar → verificar integridade
  - Múltiplos backups → rotação automática

**Validação:**
- Backup funcional e verificado
- Restore recupera banco idêntico
- Política de retenção aplicada
- Documentação completa

---

### Etapa 4 — Testes de Regressão Completos

**Objetivo:** Garantir que nenhuma mudança futura quebra silenciosamente o comportamento existente.

**Entregas:**
- Suite de regressão: `testes/regression/`
  - Cenários end-to-end completos
  - Importar dataset completo → verificar banco resultante
  - Importar dataset após mudança de schema → verificar migração
  - Re-importar mesma entidade → verificar idempotência
- Golden outputs do banco: `testes/golden/db/`
  - Snapshots do banco para cada dataset
  - Schema esperado
  - Dados esperados
  - Relacionamentos esperados
- Comparador: `testes/regression/compare_db.py`
  - Diff entre banco gerado e golden output
  - Detecta:
    - Mudanças de schema
    - Mudanças de dados
    - Relacionamentos quebrados
    - Violações de integridade
- Integração com pipeline
  - Testes de regressão rodam automaticamente
  - Falha se diff != vazio

**Validação:**
- Re-importar dataset → diff vazio
- Mudar schema intencionalmente → diff detecta
- Pipeline inclui regressão

---

### Etapa 5 — Testes de Carga

**Objetivo:** Identificar limites de desempenho antes da v1.0.

**Entregas:**
- Dataset de stress: `testes/golden/large/`
  - 500+ entidades
  - 1000+ relacionamentos
  - Múltiplos tipos (receitas, ingredientes, técnicas, equipamentos)
- Benchmark: `scripts/manutencao/benchmark.py`
  - Mede tempo de:
    - Parse de 500+ arquivos
    - Resolução de dependências
    - Importação completa
    - Queries complexas
  - Compara com baseline
  - Gera relatório JSON
- Limites documentados: `docs/99-referencias/benchmark-v1.md`
  - Tempo máximo aceitável por operação
  - Uso de memória máximo
  - Throughput mínimo
- Monitoramento: integrar com FAA (motor de performance)

**Validação:**
- Benchmark roda em < 30s
- Tempo de parse < 10s para 500 entidades
- Uso de memória < 500MB
- Relatório gerado

---

### Etapa 6 — Segurança e Validação de Entrada

**Objetivo:** O sistema não deve executar conteúdo arbitrário nem expor dados sensíveis.

**Entregas:**
- Sanitização de caminhos
  - `parse_directory` não segue symlinks fora do ROOT
  - Detecta path traversal (../)
  - Rejeita caminhos absolutos suspeitos
- Validação de IDs
  - Rejeitar IDs com caracteres fora do padrão: `[A-Z]{3}\d{4}`
  - Rejeitar IDs com comprimento inválido
  - Validar prefixos por tipo de entidade
- Validação de frontmatter
  - Campos desconhecidos geram aviso (não são silenciados)
  - Valores suspeitos (código, scripts) rejeitados
- Auditoria de dependências
  - `scripts/manutencao/audit_deps.sh`
  - Lista dependências externas com versões
  - Verifica vulnerabilidades conhecidas (via `pip audit`)
  - Relatório: `docs/99-referencias/dependencias-auditadas.md`
- Testes:
  - Tentativa de path traversal
  - IDs maliciosos
  - Frontmatter com código

**Validação:**
- Path traversal bloqueado
- IDs inválidos rejeitados
- Campos suspeitos alertados
- Auditoria de deps funcional

---

### Etapa 7 — Testes de Concorrência

**Objetivo:** Sistema não corrompe dados em uso concorrente.

**Entregas:**
- `testes/concurrency/test_concurrent_import.py`
  - Múltiplos processos importando simultaneamente
  - Verifica integridade do banco após
- `testes/concurrency/test_concurrent_read.py`
  - Leitura durante escrita
  - Verifica consistência
- Locks de banco:
  - SQLite com timeout configurável
  - Retry automático em caso de lock
- Testes:
  - 10 processos importando diferentes entidades
  - 5 processos lendo + 5 escrevendo
  - Verificar integridade final

**Validação:**
- Banco íntegro após concorrência
- Nenhuma corrupção detectada
- Locks funcionando

---

### Etapa 8 — Validação Final e Release v0.9

**Entregas:**
- Rodar pipeline completo
- FAA score ≥ 94
- Todos os testes passando (target: ≥ 600)
- Cobertura global ≥ 92%
- Atualizar CHANGELOG.md com v0.9.0
- Criar `docs/99-referencias/v0.9-RESUMO-FINAL.md`
- Tag `v0.9.0`

**Validação:**
- 100% dos testes passando
- Backup/restore validado
- Benchmarks documentados
- Segurança auditada
- Pipeline < 5 minutos

---

## Critérios de Conclusão (Definition of Done)

A v0.9 será considerada concluída quando:

- [ ] Importador com transações atômicas e modo dry-run
- [ ] Parser com limites, modo estrito e golden pathological files
- [ ] Backup + restore + verify operacionais
- [ ] Suite de regressão com golden outputs do banco
- [ ] Benchmark documentado e integrado ao FAA
- [ ] Validação de entrada e sanitização completas
- [ ] Auditoria de dependências funcional
- [ ] Testes de concorrência validados
- [ ] FAA score ≥ 94
- [ ] Cobertura global ≥ 92%
- [ ] Todos os testes passando (≥ 600)
- [ ] Pipeline reproduzível < 5 minutos
- [ ] Tag `v0.9.0` criada

---

## Estimativas de Tempo

| Etapa | Duração Estimada | Esforço |
|-------|------------------|---------|
| 1. Hardening Importador   | 1 dia      | 6-8h   |
| 2. Hardening Parser       | 1 dia      | 6-8h   |
| 3. Backup/Restore         | 1 dia      | 5-7h   |
| 4. Regressão              | 1-2 dias   | 8-10h  |
| 5. Testes de Carga        | 1 dia      | 5-7h   |
| 6. Segurança              | 1 dia      | 6-8h   |
| 7. Concorrência           | 1 dia      | 4-6h   |
| 8. Validação Final        | 0.5 dia    | 3-4h   |
| **Total**                 | **7-9 dias** | **43-58h** |

---

## Ordem de Execução

```
Etapa 1 (Hardening Importador)
   ↓
Etapa 2 (Hardening Parser)
   ↓
Etapa 3 (Backup/Restore)
   ↓
Etapa 4 (Regressão)
   ↓
Etapa 5 (Testes de Carga) ← paralelo → Etapa 6 (Segurança)
   ↓                                          ↓
   └────────────────────────────────────────→
                      ↓
            Etapa 7 (Concorrência)
                      ↓
            Etapa 8 (Validação Final)
```

---

## Áreas de Confiabilidade Cobertas

| Área | Cobertura v0.9 |
|------|----------------|
| **Hardening** | ✅ Importador + Parser |
| **Segurança** | ✅ Sanitização + Validação + Auditoria |
| **Performance** | ✅ Benchmarks + Testes de Carga |
| **Resiliência** | ✅ Backup + Restore + Recovery |
| **Qualidade** | ✅ Regressão + Concorrência |
| **Observabilidade** | ✅ Logs estruturados + Monitoramento |

---

## Mudanças em Relação ao Plano Original

| Aspecto | Plano Original | Plano Revisado |
|---------|---------------|----------------|
| Nome | Hardening | Confiabilidade |
| Escopo | Apenas hardening | Hardening + Segurança + Performance + Resiliência |
| Etapas | 7 | 8 |
| Foco | Falhas | Garantias operacionais |
| Testes | ~550 | ≥600 |
| Cobertura | ≥90% | ≥92% |
| FAA Score | ≥92 | ≥94 |
| Duração | 5-7 dias | 7-9 dias |

---

## Próxima Ação Imediata (após v0.8.2)

```bash
# Criar estrutura de testes
mkdir -p testes/regression/
mkdir -p testes/concurrency/
mkdir -p testes/golden/large/
mkdir -p testes/golden/pathological/
mkdir -p testes/golden/db/

# Criar estrutura de backup
mkdir -p scripts/copia_seguranca/
touch scripts/copia_seguranca/backup.sh
touch scripts/copia_seguranca/restore.sh
touch scripts/copia_seguranca/verify.sh
touch scripts/copia_seguranca/README.md
chmod +x scripts/copia_seguranca/*.sh

# Criar estrutura de benchmark
touch scripts/manutencao/benchmark.py
chmod +x scripts/manutencao/benchmark.py
```

---

## Princípios da Revisão

1. **Confiabilidade é multidimensional** — não apenas hardening
2. **Garantias operacionais** — backup, restore, recovery
3. **Performance documentada** — benchmarks e limites
4. **Segurança por design** — sanitização e validação
5. **Regressões detectadas automaticamente** — golden outputs

---

## Preparação para v1.0

Após v0.9 concluída, o sistema terá:
- ✅ Arquitetura madura e congelada
- ✅ Automação completa de engenharia
- ✅ Qualidade elevada (≥92% cobertura)
- ✅ Confiabilidade operacional garantida
- ✅ Processo de release reproduzível

**v1.0 será apenas:**
- Documentação final consolidada
- Auditoria externa
- Release Notes
- Anúncio público

---

**Documento:** `PLANO-v0.9-REVISADO.md`  
**Versão:** 2.0  
**Data de criação:** 2026-07-01  
**Data de revisão:** 2026-07-01 19:30  
**Aprovado por:** Revisão estratégica do escopo de confiabilidade
