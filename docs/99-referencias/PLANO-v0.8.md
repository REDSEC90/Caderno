# Plano de Execução — v0.8: Escalabilidade

**Data:** 2026-07-01  
**Objetivo:** Permitir que o sistema cresça — novos módulos, contratos, auditorias e integrações — sem aumentar exponencialmente o custo de manutenção.  
**Mecanismo principal:** Automação como suporte à escalabilidade.

---

## Estado Atual (v0.7.0)

| Componente               | Estado                                           |
|--------------------------|--------------------------------------------------|
| Arquitetura              | ✅ Congelada                                    |
| Kernel                   | ✅ Estável                                      |
| Observabilidade          | ✅ Implementada (kernel/diagnostics)            |
| Testes                   | ✅ 410/410 passando                             |
| Cobertura diagnostics    | ✅ 100%                                         |
| Cobertura codigo/        | 🔴 0% (parser, validador, importador)           |
| Type hints / docstrings  | 🟡 Parcial (contratos existem, hints ausentes)  |
| CI/CD                    | 🔴 Ausente                                      |
| Pipeline de release      | 🔴 Manual                                       |
| Automação de contratos   | 🔴 Ausente                                      |

**Conclusão:** O sistema funciona e é estável. O próximo desafio é garantir que o crescimento não quebre o que já existe.

---

## Por que Escalabilidade?

Após arquitetura congelada, Kernel estável e observabilidade implementada, o sistema saiu da fase de construção. O próximo desafio é crescimento sustentável:

- Novos módulos devem se integrar sem ambiguidade
- Novos contratos devem ser validados automaticamente
- Novos testes devem ser executados sem intervenção manual
- Nova documentação deve ser gerada a partir do código
- Novas auditorias devem rodar continuamente

**Automação é o mecanismo que viabiliza esse crescimento sem custo exponencial.**

---

## Etapas da v0.8

### Etapa 1 — Testes unitários do `codigo/`

**Objetivo:** Eliminar a lacuna de cobertura zero nos módulos centrais do runtime.

**Motivação:** `parser.py`, `validador.py`, `importador.py` e `ir.py` processam toda entidade do sistema. Sem testes unitários próprios, qualquer refatoração para suportar novos tipos de entidade é arriscada.

**Entregas:**
- `testes/unit/test_parser.py` — expandir com cobertura de `parse_file`, `_edges_from_frontmatter`, `_edges_from_body`, `ParseError`
- `testes/unit/test_validador.py` — expandir com cobertura de `validar`, `_detect_cycles`, todos os `EdgeKind`
- `testes/unit/test_importador.py` — criação, `_row_for` por tipo, arestas N:N, rollback
- `testes/unit/test_ir.py` — expandir com `KnowledgeGraph.resolve_edges`, todos os `EdgeKind`, `EdgeOrigin`

**Validação:**
- Cobertura ≥ 90% nos módulos `codigo/`
- Zero regressões nos 410 testes existentes

---

### Etapa 2 — Type hints e docstrings completos em `codigo/`

**Objetivo:** Eliminar dívida técnica nos módulos públicos do runtime antes de escalar.

**Motivação:** Type hints permitem validação estática. Docstrings padronizadas permitem geração automática de documentação. Sem ambos, escalar módulos significa aumentar a superfície de ambiguidade.

**Entregas:**
- `codigo/ir.py` — type hints completos em todas as classes e funções públicas
- `codigo/parser.py` — type hints + docstrings alinhadas com o contrato existente
- `codigo/validador.py` — type hints + docstrings alinhadas com o contrato existente
- `codigo/importador.py` — type hints + docstrings alinhadas com o contrato existente
- `codigo/resolvedor.py` — type hints + docstrings

**Validação:**
- `mypy` sem erros em `codigo/` (strict mode)
- Docstrings cobrem: entrada, saída, erros, pré-condições

---

### Etapa 3 — Automação de contratos

**Objetivo:** Sempre que um contrato mudar, validar automaticamente schema, documentação, testes e compatibilidade.

**Entregas:**
- `scripts/automacao/contract_validator.py` — verifica que cada módulo em `codigo/` possui:
  - Docstring de contrato (Entrada/Saída/Erros)
  - Type hints completos
  - Teste unitário correspondente em `testes/unit/`
  - Documento em `docs/` referenciando o módulo
- Integração com o FAA: novo motor `motores/contratos.py` no FAA
- Teste: `scripts/automacao/tests/test_contract_validator.py`

**Validação:**
- Rodar contra `codigo/` atual → zero violações após Etapas 1 e 2
- Rodar com módulo sem docstring → detectar e reportar

---

### Etapa 4 — Automação de auditorias (FAA contínuo)

**Objetivo:** FAA executando automaticamente em cada mudança, com histórico persistido.

**Entregas:**
- `scripts/automacao/audit_runner.py` — wrapper que executa FAA e persiste resultado em `docs/99-referencias/snapshots/`
- Formato do snapshot: `faa-snapshot-{datetime}.json` com score, motores, violações
- Comando: `./scripts/faa.sh --snapshot` salva resultado automaticamente
- Limiar configurável: se score < 90, sinalizar como DEGRADED no relatório
- `scripts/automacao/audit_diff.py` — compara dois snapshots e lista regressões

**Validação:**
- Rodar `audit_runner.py` → gerar snapshot válido
- Rodar `audit_diff.py` com dois snapshots → listar diferenças corretamente

---

### Etapa 5 — Pipeline de release

**Objetivo:** Substituir o processo manual de release por uma sequência automatizada e reprodutível.

**Pipeline alvo:**
```
commit
  ↓
lint (ruff / pylint)
  ↓
type check (mypy)
  ↓
contract validation
  ↓
unit tests
  ↓
integration tests
  ↓
FAA (score ≥ 90)
  ↓
document validation
  ↓
changelog check
  ↓
release
```

**Entregas:**
- `scripts/automacao/pipeline.sh` — executa todos os passos acima em sequência, para em qualquer falha
- `scripts/automacao/lint.sh` — ruff + mypy em `codigo/` e `kernel/`
- `scripts/automacao/release_check.py` — valida que CHANGELOG.md contém entry para a versão atual
- `Makefile` (ou atualizar existente) com targets: `make test`, `make lint`, `make audit`, `make release-check`

**Validação:**
- `./scripts/automacao/pipeline.sh` roda do início ao fim sem erros no estado atual
- Introduzir erro proposital → pipeline para no estágio correto

---

### Etapa 6 — Autodocumentação de módulos

**Objetivo:** Novo módulo adicionado ao `codigo/` ou `kernel/` gera automaticamente estrutura documental mínima.

**Entregas:**
- `scripts/automacao/doc_scaffold.py` — dado um módulo Python, gera:
  - `docs/05-desenvolvimento/{modulo}-contrato-v1.md` (template preenchido com docstrings)
  - Entry no `docs/INDICE-MESTRE.md`
  - Entry no `docs/MATRIZ-RASTREABILIDADE.md`
- Template de contrato: `docs/01-dominio/templates/template-contrato-modulo-v1.md`
- Teste: `scripts/automacao/tests/test_doc_scaffold.py`

**Validação:**
- Rodar contra `codigo/parser.py` → gerar documento coerente
- Documento gerado passa na validação do motor de contratos (Etapa 3)

---

### Etapa 7 — Registro automático no Kernel

**Objetivo:** Novos módulos se registram no Kernel sem configuração manual.

**Contexto:** Atualmente o bootstrap do Kernel é manual. Para escalar a quantidade de módulos, o registro deve ser declarativo e automático.

**Entregas:**
- Mecanismo de autodescoberta: módulos que implementam a interface `KernelModule` são registrados automaticamente no bootstrap
- `kernel/bootstrap.py` — atualizar para escanear `codigo/` e registrar módulos conformes
- Contrato de auto-registro: módulo deve declarar `MODULE_CONTRACT` no nível de módulo
- ADR-0004: decisão sobre mecanismo de auto-registro
- Testes: `testes/integration/test_kernel_autoregistry.py`

**Validação:**
- Criar módulo stub com `MODULE_CONTRACT` → registrado automaticamente no bootstrap
- Módulo sem `MODULE_CONTRACT` → não registrado (sem erro)
- Testes de integração passando

---

### Etapa 8 — Resolução das pendências estruturais

**Objetivo:** Fechar pendências abertas desde a auditoria de 2026-06-28 que afetam a qualidade do repositório.

**8a — Diretórios vazios em `scripts/`:**

| Diretório | Decisão |
|-----------|---------|
| `scripts/manutencao/` | Manter — adicionar `README.md` com propósito e critérios |
| `scripts/instalacao/` | Manter — adicionar `README.md` + `instalar.sh` básico |
| `scripts/copia_seguranca/` | Manter — adicionar `README.md` + `backup.sh` básico |

**8b — Atualização do INDICE-MESTRE e MATRIZ-RASTREABILIDADE:**
- Incluir `scripts/automacao/` na rastreabilidade
- Incluir novos ADRs (ADR-0004)
- Atualizar contagem de testes

**Validação:**
- Nenhum diretório de `scripts/` vazio sem `README.md`
- INDICE-MESTRE referencia todos os módulos novos

---

### Etapa 9 — Validação Final e Release v0.8

**Objetivo:** Garantir que v0.8 está completo e o sistema escala corretamente.

**Entregas:**
- Rodar pipeline completo: `./scripts/automacao/pipeline.sh`
- FAA score ≥ 90
- Todos os testes passando (target: ≥ 480)
- Atualizar CHANGELOG.md com v0.8.0
- Criar `docs/99-referencias/PLANO-v0.8-RESUMO.md` com o que foi entregue
- Tag `v0.8.0`

**Validação:**
- 100% dos testes passando
- Zero breaking changes na API pública do Kernel
- Pipeline de release executando do início ao fim

---

## Critérios de Conclusão (Definition of Done)

A v0.8 será considerada concluída quando:

- [ ] Cobertura ≥ 90% em `codigo/`
- [ ] `mypy` sem erros em `codigo/` e `kernel/` (strict)
- [ ] Motor de validação de contratos operacional
- [ ] FAA rodando automaticamente com snapshots persistidos
- [ ] Pipeline de release executável em um comando
- [ ] Scaffold de documentação funcional
- [ ] Auto-registro de módulos no Kernel implementado
- [ ] ADR-0004 criado
- [ ] Diretórios vazios em `scripts/` resolvidos
- [ ] INDICE-MESTRE e MATRIZ-RASTREABILIDADE atualizados
- [ ] Todos os testes passando (≥ 480)
- [ ] FAA score ≥ 90
- [ ] API pública inalterada (freeze respeitado)
- [ ] Tag v0.8.0 criada

---

## Ordem de Execução Recomendada

```
Etapa 1 → Etapa 2 → Etapa 3
                         ↓
              Etapa 4 ← Etapa 5
                    ↓
              Etapa 6 → Etapa 7
                    ↓
              Etapa 8 → Etapa 9
```

Etapas 1 e 2 são pré-requisito para Etapa 3 (contratos só podem ser validados automaticamente se type hints e testes existirem).  
Etapa 4 depende do FAA estar integrado ao pipeline (Etapa 5).  
Etapa 7 (auto-registro) depende dos contratos de módulo estarem definidos (Etapa 3).

---

## Roadmap após v0.8

**v0.9 — Hardening**
- Segurança, resiliência e recuperação de falhas
- Testes de carga e regressão completos
- Redução da superfície de risco

**v1.0 — Maturidade**
- Arquitetura imutável
- Contratos estáveis e auditados
- Documentação consolidada e processos reprodutíveis
- Baixa dívida técnica

---

**Documento:** `PLANO-v0.8.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
