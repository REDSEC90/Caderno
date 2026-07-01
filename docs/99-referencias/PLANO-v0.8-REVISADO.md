# Plano de Execução — v0.8 (REVISADO): Escalabilidade + Automação

**Data de criação original:** 2026-07-01  
**Data de revisão:** 2026-07-01 19:30  
**Status:** v0.8.0 concluída, v0.8.1-v0.8.2 em planejamento  
**Objetivo:** Permitir que o sistema cresça com automação completa de engenharia, eliminando riscos de processo.

---

## Contexto da Revisão

### Estado Atual (v0.8.0)

| Componente               | Estado                                           |
|--------------------------|--------------------------------------------------|
| Arquitetura              | ✅ Congelada                                    |
| Kernel                   | ✅ Estável (92% cobertura)                      |
| Runtime Core             | ✅ Estável (97% cobertura)                      |
| Testes                   | ✅ 444/444 passando                             |
| Cobertura global         | ✅ 87%                                          |
| FAA                      | ✅ Operacional (score 93.78)                    |
| Observabilidade          | ✅ Implementada (diagnostics 100%)              |
| CLI                      | 🔴 0% cobertura                                 |
| Pipeline                 | 🔴 Manual                                       |
| CI/CD                    | 🔴 Ausente                                      |
| FAA contínuo             | 🔴 Sem snapshots/histórico                      |

**Conclusão:** O código é sólido. O risco é o processo.

---

## Mudança de Paradigma

### Antes (Plano Original v0.8)

Foco: adicionar features (type hints, docstrings, auto-registro)

**Risco:** Features sem garantia de qualidade contínua

### Agora (Plano Revisado v0.8)

Foco: **automação de engenharia antes de features**

**Benefício:** Toda mudança futura é automaticamente validada

---

## Razão da Reorganização

O projeto atingiu maturidade arquitetural:
- v0.5: Arquitetura congelada ✅
- v0.6: Consolidação ✅
- v0.7: Otimização Kernel ✅
- v0.8: 60% concluída ✅

**Neste patamar, o maior risco não é mais o código, mas o processo.**

Sem pipeline automatizado:
- ❌ Alguém pode esquecer testes
- ❌ Alguém pode esquecer FAA
- ❌ Alguém pode esquecer validações
- ❌ Alguém pode quebrar contratos
- ❌ Releases não são reproduzíveis

**Pipeline é o guardião da qualidade.**

---

## Nova Estrutura: v0.8.0 → v0.8.1 → v0.8.2

### v0.8.0 — Escalabilidade ✅ CONCLUÍDA

**Objetivo:** Cobertura de testes do runtime core

**Entregas:**
- [x] Testes unitários de `codigo/` (cobertura 45% → 73%)
- [x] `importador.py`: 0% → 92%
- [x] `parser.py`: 82% → 94%
- [x] 444/444 testes passando
- [x] Zero regressões

**Tag:** `v0.8.0` (2026-07-01)

---

### v0.8.1 — Automação de Engenharia 🔄 PRÓXIMA

**Objetivo:** Pipeline como guardião de qualidade + FAA contínuo + contratos automáticos

**Duração estimada:** 8-10 horas (1-2 dias)

#### Etapa 1 — Pipeline Unificado (Prioridade Máxima)

**Motivação:** Pipeline manual é o maior risco do projeto. Tudo depende dele.

**Entregas:**
- `scripts/automacao/pipeline.sh` — orquestrador principal
  ```bash
  #!/bin/bash
  # Pipeline oficial SOE-CCG v0.8.1
  
  echo "=== SOE-CCG Pipeline de Release ==="
  
  # 1. Lint
  ./scripts/automacao/lint.sh || exit 1
  
  # 2. Format check
  ./scripts/automacao/format_check.sh || exit 1
  
  # 3. Type check
  mypy --strict codigo/ kernel/ || exit 1
  
  # 4. Contract validation
  python scripts/automacao/contract_validator.py || exit 1
  
  # 5. Unit tests
  pytest testes/unit/ -v || exit 1
  
  # 6. Integration tests
  pytest testes/integration/ -v || exit 1
  
  # 7. Contract tests
  pytest testes/contract/ -v || exit 1
  
  # 8. FAA
  ./scripts/faa.sh --snapshot || exit 1
  
  # 9. Documentation validation
  python scripts/automacao/doc_validator.py || exit 1
  
  # 10. Changelog check
  python scripts/automacao/release_check.py || exit 1
  
  echo "✅ Pipeline concluído com sucesso"
  ```

- `scripts/automacao/lint.sh` — ruff em `codigo/` e `kernel/`
- `scripts/automacao/format_check.sh` — verifica formatação (ruff format --check)
- `scripts/automacao/release_check.py` — valida CHANGELOG.md

- `Makefile` atualizado:
  ```makefile
  .PHONY: test lint format audit pipeline release-check
  
  test:
      PYTHONPATH=. pytest -v
  
  lint:
      ./scripts/automacao/lint.sh
  
  format:
      ruff format codigo/ kernel/ scripts/ testes/
  
  format-check:
      ./scripts/automacao/format_check.sh
  
  audit:
      ./scripts/faa.sh
  
  pipeline:
      ./scripts/automacao/pipeline.sh
  
  release-check:
      python scripts/automacao/release_check.py
  ```

**Validação:**
- `make pipeline` roda do início ao fim sem erros
- Introduzir erro proposital → pipeline para no estágio correto
- Tempo de execução < 5 minutos

**Impacto:** Torna impossível fazer release sem passar por todas as validações.

---

#### Etapa 2 — Automação de Contratos

**Motivação:** SOE-CCG gira em torno de contratos. Validação manual é insustentável.

**Entregas:**
- Integrar `contract_validator.py` como motor FAA
- Novo motor: `scripts/faa/motores/contratos.py`
  - Valida que cada módulo público possui:
    - Docstring de contrato (Entrada/Saída/Erros)
    - Type hints completos
    - Teste unitário correspondente
    - Documento em `docs/` referenciando o módulo
  - Score baseado em conformidade
- `scripts/automacao/contract_validator.py` chama o motor
- Testes: `scripts/automacao/tests/test_contract_validator.py` (já existente)

**Validação:**
- Rodar contra `codigo/` e `kernel/` → zero violações (ou lista explícita de exceções)
- Motor integrado ao FAA
- Score de contratos ≥ 95%

**Impacto:** Contratos são validados automaticamente em cada pipeline run.

---

#### Etapa 3 — FAA Contínuo

**Motivação:** FAA sem histórico não detecta regressões. Precisa ser ferramenta de governança.

**Entregas:**
- `scripts/automacao/audit_runner.py`
  ```python
  """
  Executa FAA e persiste snapshot com timestamp.
  
  Snapshot: docs/99-referencias/snapshots/faa-YYYYMMDD-HHMMSS.json
  """
  ```
- Formato do snapshot:
  ```json
  {
    "version": "2.0",
    "timestamp": "2026-07-01T19:30:00Z",
    "commit": "d65301f",
    "score": 93.78,
    "metrics": { ... },
    "motors": { ... },
    "violations": [ ... ]
  }
  ```
- `scripts/automacao/audit_diff.py`
  ```python
  """
  Compara dois snapshots e lista regressões.
  
  Saída:
  - Mudança de score
  - Novas violações
  - Violações resolvidas
  - Mudanças por motor
  """
  ```
- `scripts/faa.sh --snapshot` integrado ao pipeline
- Diretório: `docs/99-referencias/snapshots/`
- Limiar configurável: score < 90 → pipeline falha

**Validação:**
- Gerar snapshot → arquivo válido criado
- Comparar dois snapshots → diff correto
- Score < 90 → pipeline falha

**Impacto:** FAA vira ferramenta de governança contínua com rastreabilidade.

---

#### Definição de Conclusão v0.8.1

- [ ] Pipeline unificado executável em um comando (`make pipeline`)
- [ ] Pipeline roda em < 5 minutos
- [ ] Motor de contratos integrado ao FAA
- [ ] FAA com snapshots automáticos
- [ ] `audit_diff.py` funcional
- [ ] Makefile atualizado
- [ ] Todos os 444+ testes passando
- [ ] FAA score ≥ 90
- [ ] Tag `v0.8.1` criada

---

### v0.8.2 — Qualidade e Completude 🔄 PENDENTE

**Objetivo:** Eliminar lacunas críticas e elevar qualidade a nível de release

**Duração estimada:** 10-12 horas (2-3 dias)

#### Etapa 4 — Testes End-to-End da CLI

**Motivação:** CLI com 0% cobertura é a principal lacuna funcional. Interface do usuário não pode quebrar silenciosamente.

**Entregas:**
- `testes/e2e/test_cli.py` — testes end-to-end completos
  - Cenários:
    - `python -m codigo parse <dir>`
    - `python -m codigo import <file>`
    - `python -m codigo query <pattern>`
    - `python -m codigo export <output>`
    - Tratamento de erros (arquivo inexistente, formato inválido)
    - Saída padrão (stdout/stderr)
- Cobertura `codigo/__main__.py`: 0% → ≥80%
- Integração com pipeline (etapa de testes E2E)

**Validação:**
- Cobertura CLI ≥ 80%
- Todos os comandos testados
- Tratamento de erros validado
- Pipeline inclui testes E2E

**Impacto:** Elimina maior lacuna funcional do sistema.

---

#### Etapa 5 — Type Hints e Mypy Strict

**Motivação:** Type hints permitem validação estática. Mypy strict garante conformidade.

**Entregas:**
- Completar type hints em todos os módulos públicos:
  - `codigo/ir.py`
  - `codigo/parser.py`
  - `codigo/validador.py`
  - `codigo/importador.py`
  - `codigo/resolvedor.py`
  - `codigo/__main__.py`
- `mypy --strict codigo/ kernel/` → zero erros
- Pipeline enforça mypy strict

**Validação:**
- `mypy --strict` sem erros
- Pipeline falha se mypy falhar
- Type hints documentados nas docstrings

**Impacto:** Validação estática impede erros de tipo em tempo de desenvolvimento.

---

#### Etapa 6 — Autodocumentação

**Motivação:** Quando pipeline + contratos estão prontos, documentação se escreve sozinha.

**Entregas:**
- `scripts/automacao/doc_scaffold.py` — validar e expandir
  - Gera `docs/05-desenvolvimento/{modulo}-contrato-v1.md` a partir de docstrings
  - Entry automática no `docs/INDICE-MESTRE.md`
  - Entry automática no `docs/MATRIZ-RASTREABILIDADE.md`
- Template: `docs/01-dominio/templates/template-contrato-modulo-v1.md`
- Testes: `scripts/automacao/tests/test_doc_scaffold.py`

**Validação:**
- Rodar contra `codigo/parser.py` → documento válido gerado
- Documento passa na validação de contratos
- Integrado ao pipeline (opcional, apenas para novos módulos)

---

#### Etapa 7 — Auto-registro no Kernel

**Motivação:** Escalabilidade de módulos requer registro declarativo.

**Entregas:**
- Interface `KernelModule` para auto-registro
- `kernel/bootstrap.py` — autodescoberta de módulos com `MODULE_CONTRACT`
- Contrato de auto-registro: módulo declara `MODULE_CONTRACT` no nível de módulo
- ADR-0004: decisão sobre mecanismo de auto-registro
- Testes: `testes/integration/test_kernel_autoregistry.py`

**Validação:**
- Módulo com `MODULE_CONTRACT` → registrado automaticamente
- Módulo sem `MODULE_CONTRACT` → não registrado (sem erro)
- Testes de integração passando

---

#### Etapa 8 — Limpeza e Pendências Estruturais

**Motivação:** Apenas quando automação está completa, limpar pendências.

**Entregas:**
- **Diretórios vazios em `scripts/`:**
  - `scripts/manutencao/README.md` — propósito e critérios
  - `scripts/instalacao/README.md` + `instalar.sh` básico
  - `scripts/copia_seguranca/README.md` + estrutura básica
- **Atualização INDICE-MESTRE:**
  - Incluir `scripts/automacao/` completo
  - Incluir ADR-0004
  - Atualizar contagem de testes
- **Atualização MATRIZ-RASTREABILIDADE:**
  - Incluir novos testes E2E
  - Incluir pipeline
  - Incluir FAA contínuo

**Validação:**
- Nenhum diretório de `scripts/` vazio sem `README.md`
- INDICE-MESTRE referencia todos os módulos novos
- MATRIZ-RASTREABILIDADE atualizada

---

#### Etapa 9 — Release Candidate e Validação Final

**Entregas:**
- Rodar `make pipeline` → 100% sucesso
- FAA score ≥ 92
- Todos os testes passando (target: ≥ 500)
- Cobertura global ≥ 90%
- Atualizar CHANGELOG.md com v0.8.2
- Criar `docs/99-referencias/v0.8-RESUMO-FINAL.md`
- Tag `v0.8.2`

**Validação:**
- 100% dos testes passando
- Pipeline completo < 5 minutos
- Zero breaking changes na API pública
- Processo de release reproduzível

---

#### Definição de Conclusão v0.8.2

- [ ] CLI com ≥80% cobertura
- [ ] `mypy --strict` sem erros em `codigo/` e `kernel/`
- [ ] Scaffold de documentação validado
- [ ] Auto-registro de módulos implementado
- [ ] ADR-0004 criado
- [ ] Pendências estruturais resolvidas
- [ ] INDICE-MESTRE e MATRIZ-RASTREABILIDADE atualizados
- [ ] FAA score ≥ 92
- [ ] Cobertura global ≥ 90%
- [ ] Todos os testes passando (≥ 500)
- [ ] Pipeline reproduzível
- [ ] Tag `v0.8.2` criada

---

## Definição de Conclusão da v0.8 Completa

A v0.8 será considerada **completamente concluída** quando:

- [x] **v0.8.0** — Testes unitários runtime ✅
- [ ] **v0.8.1** — Automação de engenharia (pipeline + FAA + contratos)
- [ ] **v0.8.2** — Qualidade e completude (CLI + mypy + autodoc + autoregistro)

**Critérios finais:**
- [ ] Pipeline unificado operacional
- [ ] FAA contínuo com snapshots
- [ ] Contratos validados automaticamente
- [ ] CLI testada (≥80%)
- [ ] Type hints completos (mypy strict)
- [ ] Cobertura global ≥ 90%
- [ ] FAA score ≥ 92
- [ ] ≥ 500 testes passando
- [ ] Processo de release reproduzível
- [ ] Zero breaking changes

---

## Ordem de Execução Revisada

```
v0.8.0 ✅
   ↓
v0.8.1 (Automação)
   │
   ├─ 1. Pipeline unificado
   ├─ 2. Automação de contratos
   └─ 3. FAA contínuo
   ↓
v0.8.2 (Qualidade)
   │
   ├─ 4. CLI E2E
   ├─ 5. Mypy strict
   ├─ 6. Autodocumentação
   ├─ 7. Auto-registro
   ├─ 8. Limpeza
   └─ 9. Release Candidate
   ↓
v0.9 (Confiabilidade)
```

---

## Revisão da v0.9: Release de Confiabilidade

### Novo Escopo da v0.9

**Nome:** Confiabilidade (não apenas Hardening)

**Objetivo:** Sistema robusto, seguro, resiliente e com recuperação garantida.

**Pré-requisito:** v0.8 completamente concluída (automação + qualidade).

**Áreas:**
1. **Hardening**
   - Transações atômicas no importador
   - Validação de entrada rigorosa
   - Limites de segurança no parser

2. **Segurança**
   - Sanitização de caminhos
   - Validação de IDs
   - Auditoria de dependências

3. **Performance**
   - Benchmarks documentados
   - Testes de carga (500+ entidades)
   - Limites de desempenho definidos

4. **Resiliência**
   - Backup automático
   - Restore verificado
   - Recovery sem perda de dados
   - Testes de corrupção
   - Testes de recuperação

5. **Qualidade**
   - Suite de regressão completa
   - Golden outputs do banco
   - Testes de concorrência

**Entrega:** Sistema com garantia de confiabilidade operacional.

---

## Roadmap Revisado

```
v0.5 — Arquitetura          ✅
  ↓
v0.6 — Consolidação         ✅
  ↓
v0.7 — Otimização Kernel    ✅
  ↓
v0.8 — Escalabilidade + Automação  🔄 60%
  ├─ v0.8.0 — Runtime        ✅
  ├─ v0.8.1 — Engenharia     🔄 Próxima
  └─ v0.8.2 — Qualidade      ⏸️  Pendente
  ↓
v0.9 — Confiabilidade       ⏸️  Aguardando v0.8
  ↓
v1.0 — Produto Maduro       ⏸️  Aguardando v0.9
```

---

## Estimativas de Tempo

| Release | Duração Estimada | Esforço |
|---------|------------------|---------|
| v0.8.0  | ✅ Concluído     | 6-8h    |
| v0.8.1  | 1-2 dias         | 8-10h   |
| v0.8.2  | 2-3 dias         | 10-12h  |
| **v0.8 Total** | **4-5 dias** | **24-30h** |
| v0.9    | 5-7 dias         | 30-40h  |
| v1.0    | 3-5 dias         | 20-30h  |

---

## Próxima Ação Imediata

### Para iniciar v0.8.1:

```bash
# 1. Criar estrutura de pipeline
mkdir -p scripts/automacao/
touch scripts/automacao/pipeline.sh
touch scripts/automacao/lint.sh
touch scripts/automacao/format_check.sh
touch scripts/automacao/release_check.py

# 2. Tornar executáveis
chmod +x scripts/automacao/*.sh

# 3. Criar estrutura de snapshots
mkdir -p docs/99-referencias/snapshots/

# 4. Atualizar Makefile
# (editar manualmente)
```

---

## Princípios da Revisão

1. **Pipeline primeiro** — guardião de qualidade
2. **Automação antes de features** — processo > código
3. **Contratos como governança** — arquitetura validada continuamente
4. **Releases reproduzíveis** — zero ambiguidade
5. **Não avançar sem base sólida** — v0.9 só com v0.8 completa

---

## Mudanças em Relação ao Plano Original

| Aspecto | Plano Original | Plano Revisado |
|---------|---------------|----------------|
| Estrutura | v0.8 única | v0.8.0 + v0.8.1 + v0.8.2 |
| Prioridade #1 | Type hints | Pipeline |
| Prioridade #2 | Contratos | Contratos (mantido) |
| Prioridade #3 | FAA | FAA contínuo (mantido) |
| Prioridade #4 | Pipeline | CLI (elevado) |
| Prioridade #5 | Autodoc | Type hints (rebaixado) |
| v0.9 Escopo | Hardening | Confiabilidade (expandido) |
| Critério de conclusão | Features | Automação + Qualidade |

---

## Justificativa das Mudanças

### Por que Pipeline primeiro?

- **Risco máximo:** Processo manual permite esquecimentos
- **Impacto máximo:** Valida tudo automaticamente
- **Habilitador:** Outras features dependem dele

### Por que CLI antes de Type Hints?

- **CLI:** Interface do usuário, 0% cobertura → risco funcional
- **Type Hints:** Melhora qualidade do código, mas não muda comportamento

### Por que dividir v0.8 em 3 releases menores?

- **Clareza:** Separar automação de features
- **Entregas incrementais:** Cada release tem valor isolado
- **Rastreabilidade:** Mudanças menores, mais fácil de reverter

---

**Documento:** `PLANO-v0.8-REVISADO.md`  
**Versão:** 2.0  
**Data de criação:** 2026-07-01  
**Data de revisão:** 2026-07-01 19:30  
**Aprovado por:** Revisão estratégica do processo de engenharia
