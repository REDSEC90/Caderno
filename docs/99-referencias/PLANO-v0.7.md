# Plano de Execução — v0.7: Fortalecimento do Kernel

**Data:** 2026-07-01  
**Objetivo:** Fortalecer APIs, documentação, integração e observabilidade do Kernel sem adicionar funcionalidades novas (freeze arquitetural mantido).

---

## Status Atual (v0.6.0)

| Componente       | Estado                                          |
|------------------|-------------------------------------------------|
| ModuleRegistry   | ✅ 14 métodos públicos + find/health/stats     |
| ServiceRegistry  | ✅ 9 métodos públicos + health                  |
| KernelEventBus   | ✅ 9 métodos públicos + stats/history           |
| LifecycleManager | ✅ 4 estados + transições                       |
| MicroKernel      | ✅ Integra registry, events, services, lifecycle|
| API Pública      | ✅ Documentada em FASE-0-API-PUBLICA.md         |
| API Interna      | ✅ Documentada em FASE-0-API-INTERNA.md         |
| Testes           | ✅ 226/226 passando                             |

**Conclusão:** As funcionalidades já existem. O fortalecimento deve focar em **integração, observabilidade e documentação técnica**.

---

## Etapas da v0.7

### Etapa 1 — Observabilidade: kernel.diagnostics

**Objetivo:** Criar módulo de diagnóstico unificado que agrega informações de todos os componentes.

**Entregas:**
- `kernel/diagnostics/__init__.py`
- `kernel/diagnostics/doctor.py` — agregador de health checks
- `kernel/diagnostics/inspector.py` — inspetor de estado do Kernel
- Comando: `kernel.diagnostics.doctor.run_diagnostics()` → relatório completo

**Validação:**
- Testes em `testes/contract/test_diagnostics.py`
- Relatório inclui: registry.health(), services.health(), events.stats(), lifecycle.state

---

### Etapa 2 — Guia de Operação do Kernel

**Objetivo:** Documentar operação completa do Kernel (não apenas API).

**Entregas:**
- `docs/06-operacao/kernel-operations-guide-v1.md`
  - Como inicializar o Kernel
  - Como registrar módulos
  - Como consultar registry (find/stats/health)
  - Como usar eventos (subscribe/publish)
  - Como usar serviços
  - Troubleshooting comum

**Validação:**
- Revisão manual da documentação
- Exemplos executáveis no guia

---

### Etapa 3 — Cookbook de Integrações

**Objetivo:** Exemplos práticos de uso do Kernel.

**Entregas:**
- `docs/05-desenvolvimento/kernel-cookbook-v1.md`
  - Exemplo 1: Registrar módulo custom
  - Exemplo 2: Criar serviço e registrá-lo
  - Exemplo 3: Assinar eventos do Kernel
  - Exemplo 4: Query complexa no registry (find_by_*)
  - Exemplo 5: Health check de todos os componentes
  - Exemplo 6: Lifecycle manual de um módulo

**Validação:**
- Todos os exemplos devem ser executáveis
- Criar `testes/cookbook/` com testes dos exemplos

---

### Etapa 4 — Ampliação de Testes de Integração

**Objetivo:** Garantir cobertura de cenários de integração entre componentes.

**Entregas:**
- `testes/integration/test_kernel_full_lifecycle.py`
  - Ciclo completo: bootstrap → register → initialize → start → stop
- `testes/integration/test_kernel_events_propagation.py`
  - Validar que todos os eventos esperados são publicados
- `testes/integration/test_kernel_services_lifecycle.py`
  - Integração services + lifecycle
- `testes/integration/test_kernel_registry_advanced.py`
  - Queries avançadas (find_by_capability, health, dependency_graph)

**Validação:**
- Mínimo 20 novos testes de integração
- 100% de cobertura dos métodos públicos de ModuleRegistry, ServiceRegistry, EventBus

---

### Etapa 5 — Atualização do INDICE-MESTRE e MATRIZ-RASTREABILIDADE

**Objetivo:** Incluir novos componentes (diagnostics) e novos testes.

**Entregas:**
- Atualizar `docs/INDICE-MESTRE.md` com `kernel/diagnostics`
- Atualizar `docs/MATRIZ-RASTREABILIDADE.md` com novos testes
- Adicionar seção de observabilidade na matriz

**Validação:**
- Revisão manual da consistência

---

### Etapa 6 — ADR-0003: Observabilidade do Kernel

**Objetivo:** Registrar decisão arquitetural sobre modelo de observabilidade.

**Entregas:**
- `docs/04-padroes/ADR-0003-OBSERVABILIDADE-KERNEL-v1.md`
  - Contexto: necessidade de inspeção de estado
  - Decisão: módulo diagnostics + APIs health/stats em cada componente
  - Consequências: overhead mínimo, APIs padronizadas
  - Alternativas consideradas

**Validação:**
- Revisão do formato ADR

---

### Etapa 7 — Validação Final e Release

**Objetivo:** Garantir que v0.7 está completo.

**Entregas:**
- Rodar todos os testes (target: ≥240 passando)
- Validar arquitetura (`test_kernel_validator_aprova_arquitetura_atual`)
- Atualizar CHANGELOG.md com v0.7.0
- Commit + tag `v0.7.0`

**Validação:**
- 100% dos testes passando
- Zero breaking changes na API pública
- Documentação sincronizada

---

## Critérios de Conclusão (Definition of Done)

A v0.7 será considerada concluída quando:

✅ Módulo `kernel/diagnostics` implementado e testado  
✅ Guia de operações do Kernel criado  
✅ Cookbook com 6+ exemplos executáveis  
✅ ≥20 novos testes de integração  
✅ Cobertura 100% dos métodos públicos de Registry/Services/Events  
✅ INDICE-MESTRE e MATRIZ atualizado  
✅ ADR-0003 criado  
✅ Todos os testes passando (≥240)  
✅ API pública inalterada (freeze respeitado)  
✅ Tag v0.7.0 criada  

---

## Roadmap após v0.7

**v0.8 — Automação**
- Validação automática de contratos
- Auditoria contínua
- Geração automática de documentação

**v0.9 — Hardening**
- Segurança
- Desempenho
- Testes de carga
- Testes de regressão completos

**v1.0 — Release de Produção**
- Arquitetura imutável
- Contratos estáveis
- APIs congeladas permanentemente
- Rastreabilidade completa
- Cobertura elevada (≥95% dos componentes críticos)

---

**Documento:** `PLANO-v0.7.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
