# SOE-CCG — Matriz de Rastreabilidade

**Versão:** 1.1  
**Data:** 2026-07-01  
**Status:** ATIVO  

> Rastreia cada lei/invariante do Kernel até sua implementação e cobertura de testes.

---

## Estrutura de rastreabilidade

```
Lei / Invariante
    ↓
Contrato formal
    ↓
Implementação
    ↓
Teste
```

---

## 1. Contratos de Módulo

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Todo módulo deve possuir contrato formal      | `CONTRACT_SCHEMA.md`                | `kernel/contracts/module.py`         | `test_microkernel.py`              | ✅ OK    |
| Contrato deve ser validado antes do registro  | `02_invariantes-v1.md` §1           | `kernel/contracts/validator.py`      | `test_contract_v2.py`              | ✅ OK    |
| Módulo sem contrato não pode ser registrado   | `01_regras_fundamentais-v1.md` §2   | `kernel/registry/module_registry.py` | `test_registry_v2.py`              | ✅ OK    |
| Contrato deve incluir nome, versão, tipo      | `CONTRACT_SCHEMA.md` §campos        | `kernel/contracts/module.py`         | `test_contract_v2.py`              | ✅ OK    |

---

## 2. Registry

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Registry é a única fonte de verdade dos módulos | `05_regras_kernel-v1.md` §1       | `kernel/registry/module_registry.py` | `test_registry_v2.py`              | ✅ OK    |
| Não pode existir módulo duplicado no registry | `02_invariantes-v1.md` §3           | `kernel/registry/module_registry.py` | `test_registry_v2.py`              | ✅ OK    |
| Registry suporta consulta por nome e tipo     | `FASE-4-RESUMO` (arquivado)         | `kernel/registry/module_registry.py` | `test_registry_v2.py`              | ✅ OK    |

---

## 3. Lifecycle

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Módulo segue ciclo de vida formal             | `kernel-docs/FASE-3-DIAGRAMA-LIFECYCLE.md` (arquivado) | `kernel/lifecycle/manager.py` | `test_lifecycle_v2.py`   | ✅ OK    |
| Transições de estado devem ser determinísticas | `02_invariantes-v1.md` §2          | `kernel/lifecycle/manager.py`        | `test_lifecycle_v2.py`             | ✅ OK    |
| Estado FAILED deve ser detectável             | `FASE-0-API-PUBLICA.md`             | `kernel/lifecycle/manager.py`        | `test_lifecycle_v2.py`             | ✅ OK    |

---

## 4. Eventos

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Módulos não se comunicam diretamente          | `04_regras_modulos-v1.md` §3        | `kernel/events/bus.py`               | `test_events_v1.py`                | ✅ OK    |
| Toda comunicação ocorre via EventBus          | `05_regras_kernel-v1.md` §4         | `kernel/events/bus.py`               | `test_events_v1.py`                | ✅ OK    |
| Eventos devem ser tipados                     | `FASE-0-API-INTERNA.md`             | `kernel/events/bus.py`               | `test_events_v1.py`                | ✅ OK    |

---

## 5. Serviços

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Serviços são separados de módulos             | `FASE-2-EXPANSAO-CONTRACT.md` §6    | `kernel/services/service_registry.py`| `test_services_v1.py`              | ✅ OK    |
| Serviços são registrados no ServiceRegistry   | `FASE-0-API-PUBLICA.md`             | `kernel/services/service_registry.py`| `test_services_v1.py`              | ✅ OK    |

---

## 6. Bootstrap

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Bootstrap é o único ponto de inicialização    | `FASE-1-RESPONSABILIDADES.md` §1    | `kernel/bootstrap.py`                | `test_microkernel.py`              | ✅ OK    |
| Bootstrap é determinístico                    | `02_invariantes-v1.md` §4           | `kernel/bootstrap.py`                | `test_microkernel.py`              | ✅ OK    |

---

## 7. Dependências

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Não podem existir dependências circulares     | `03_modelo_dependencias-v1.md` §2   | `kernel/registry/module_registry.py` | `test_registry_v2.py`              | ✅ OK    |
| Código depende do Kernel, nunca o contrário   | `FASE-1-CAMADAS.md` §hierarquia     | `kernel/` (estrutura)                | `test_kernel_validator_*`          | ✅ OK    |
| Kernel não importa de `codigo/`               | `FASE-1-MATRIZ-DEPENDENCIAS.md`     | `kernel/` (imports)                  | `test_kernel_validator_*`          | ✅ OK    |

---

## 8. Pipeline de Código

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Pipeline obrigatório: INPUT→PARSER→IR→...     | `docs/02-arquitetura/fluxo-dados-v1.md` | `codigo/` (pipeline)             | `test_pipeline.py`                 | ✅ OK    |
| Parser produz IR válida                       | `ADR-0002-IR-ARESTAS-TIPADAS-v1.md` | `codigo/parser.py`, `codigo/ir.py`   | `test_parser.py`, `test_ir.py`     | ✅ OK    |
| Resolver não acessa storage diretamente       | `docs/02-arquitetura/fluxo-dados-v1.md` | `codigo/resolvedor.py`           | `test_resolvedor.py`               | ✅ OK    |
| Validador rejeita IR malformada               | `docs/04-padroes/validacao-v1.md`   | `codigo/validador.py`                | `test_validador.py`                | ✅ OK    |

---

## 9. Domínio de dados

| Lei / Invariante                              | Contrato                            | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------|-------------------------------------|--------------------------------------|------------------------------------|----------|
| Receita é especificação, não execução         | `especificacao-receita-v1.md` §1    | `dados/receitas/`                    | (golden files)                     | ✅ OK    |
| Execução referencia receita por ID            | `especificacao-execucao-v1.md` §3   | `dados/execucoes/`                   | (golden files)                     | ✅ OK    |
| Identificadores seguem padrão ENT-NNNNNN      | `identificadores-v1.md`             | `dados/` (arquivos)                  | (estrutural)                       | ✅ OK    |
| Markdown é fonte canônica                     | `filosofia-v1.md` §2                | `dados/` (arquivos .md)              | `test_golden.py`                   | ✅ OK    |
| SQLite é índice derivado, não fonte           | `ADR-0001-MOTOR-DE-CONHECIMENTO-v1.md` | `banco_de_dados/`                 | (estrutural)                       | ✅ OK    |

---

## 10. Observabilidade e Diagnóstico (v0.7)

| Lei / Invariante                                    | Contrato                                        | Implementação                        | Teste                              | Estado   |
|-----------------------------------------------------|-------------------------------------------------|--------------------------------------|------------------------------------|----------|
| Kernel deve ser inspecionável em tempo de execução  | `ADR-0003-OBSERVABILIDADE-KERNEL-v1.md`         | `kernel/diagnostics/inspector.py`    | `test_diagnostics.py`              | ✅ OK    |
| Health checks padronizados em todos os componentes  | `ADR-0003-OBSERVABILIDADE-KERNEL-v1.md`         | `kernel/diagnostics/doctor.py`       | `test_diagnostics.py`              | ✅ OK    |
| Diagnóstico agrega todos os componentes             | `ADR-0003-OBSERVABILIDADE-KERNEL-v1.md`         | `kernel/diagnostics/doctor.py`       | `test_diagnostics.py`              | ✅ OK    |
| Módulos deprecated aparecem nos avisos              | `ADR-0003-OBSERVABILIDADE-KERNEL-v1.md`         | `kernel/diagnostics/doctor.py`       | `test_diagnostics.py`              | ✅ OK    |
| Serviços com health falha aparecem nos issues       | `ADR-0003-OBSERVABILIDADE-KERNEL-v1.md`         | `kernel/diagnostics/doctor.py`       | `test_diagnostics.py`              | ✅ OK    |

---

## 11. Testes de Integração (v0.7)

| Cenário                                             | Escopo                                          | Arquivo de teste                                        | Estado   |
|-----------------------------------------------------|-------------------------------------------------|---------------------------------------------------------|----------|
| Ciclo completo bootstrap → start → stop             | Integração Kernel                               | `testes/integration/test_kernel_full_lifecycle.py`      | ✅ OK    |
| Propagação de eventos entre componentes             | Integração Events                               | `testes/integration/test_kernel_events_propagation.py`  | ✅ OK    |
| Services + Lifecycle integrado                      | Integração Services                             | `testes/integration/test_kernel_services_lifecycle.py`  | ✅ OK    |
| Queries avançadas no registry                       | Integração Registry                             | `testes/integration/test_kernel_registry_advanced.py`   | ✅ OK    |
| Receitas do cookbook são executáveis                | Cookbook                                        | `testes/cookbook/test_cookbook.py`                      | ✅ OK    |

---

## Legenda

| Símbolo | Significado                                    |
|---------|------------------------------------------------|
| ✅ OK   | Rastreado, implementado e testado              |
| ⚠️ PARCIAL | Implementado mas sem teste automático completo |
| ❌ ABERTO | Não implementado ou não testado               |

---

## Itens abertos para v0.8+

1. Testes de regressão ainda vazios (`testes/regression/`)
2. Golden files para `testes/golden/invalid/` e `testes/golden/minimal/`
3. Cobertura de testes de carga (prevista para v0.9)

---

**Documento:** `MATRIZ-RASTREABILIDADE.md`  
**Localização:** `docs/`  
**Versão:** 1.1  
**Data:** 2026-07-01  
**Status:** NORMATIVO
