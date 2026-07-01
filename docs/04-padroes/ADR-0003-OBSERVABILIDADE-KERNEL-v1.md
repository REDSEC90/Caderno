# ADR-0003 — Observabilidade do Kernel

**Status:** ACEITO  
**Data:** 2026-07-01  
**Versão:** 1.0  
**Autores:** time SOE-CCG  

---

## Contexto

Com o Kernel estabilizado na v0.6.0 (ModuleRegistry, ServiceRegistry, KernelEventBus, LifecycleManager, MicroKernel — 226 testes, 100% passando), surgiu a necessidade de **inspecionar o estado interno do sistema em tempo de execução** sem depender de logs externos ou instrumentação ad hoc.

Os problemas concretos que motivaram esta decisão:

1. **Diagnóstico de dependências quebradas** — não havia forma programática de verificar se todas as dependências estavam resolvidas sem provocar exceções
2. **Saúde de serviços** — `ServiceRegistry` expunha `service_health()` por serviço, mas não havia agregação global
3. **Visibilidade de eventos** — `KernelEventBus` mantinha histórico, mas não havia ponto único de consulta
4. **Detecção de módulos deprecados** — o registry rastreava `deprecated_modules` em `health()`, mas nada consumia essa informação sistematicamente
5. **Debugging integrado** — ao detectar comportamento inesperado, o desenvolvedor precisava consultar cada componente separadamente

---

## Decisão

Criar o módulo `kernel/diagnostics/` com dois componentes:

### `doctor.py` — Agregador de health checks

Função principal: `run_diagnostics(kernel) → DiagnosticReport`

- Agrega `registry.health()`, `services.all_health()`, `events.stats()` e `lifecycle.state` em um único objeto
- Classifica problemas em `issues` (lista de strings descritivas)
- Propriedade `healthy` (bool) para verificação rápida
- Propriedade `summary` para exibição humana
- Função auxiliar `print_diagnostics(report)` para output formatado no terminal

### `inspector.py` — Inspetor de estado

Funções: `inspect_kernel()`, `inspect_registry()`, `inspect_services()`, `inspect_events()`

- Retorna snapshots completos do estado interno como dicionários Python
- Não modifica o estado — somente leitura
- Adequado para serialização, logging, debugging

### Critério de "saudável"

Um `DiagnosticReport` é considerado `healthy=True` quando:
- Nenhuma dependência ausente no registry (`missing_dependencies == []`)
- Nenhuma dependência circular (`circular_dependencies == []`)
- Nenhum serviço com `health_result.healthy == False`

Módulos deprecados **geram aviso** mas **não marcam healthy=False** — são listados em `issues` como informativos, pois deprecação não impede operação.

---

## Alternativas Consideradas

### Alternativa A: Decorators de health em cada componente

Adicionar método `health()` padronizado em `ModuleRegistry`, `ServiceRegistry`, `KernelEventBus` e `KernelLifecycle` e expô-los individualmente.

**Rejeitada porque:**
- Já existem (`registry.health()`, `services.all_health()`, `events.stats()`) — só faltava agregação
- Não resolve o problema de visão unificada
- Aumenta acoplamento de quem consome (precisa conhecer cada componente)

### Alternativa B: Middleware de observabilidade (decorators/proxies)

Envolver cada componente em um proxy que registra todas as chamadas.

**Rejeitada porque:**
- Viola o freeze arquitetural — precisaria modificar as interfaces existentes
- Overhead em chamadas de produção
- Complexidade excessiva para o nível de observabilidade necessário

### Alternativa C: Sistema de métricas externo (Prometheus, StatsD)

Integrar com sistema de métricas externo.

**Rejeitada porque:**
- Dependência externa não alinhada com a filosofia de independência do SOE-CCG
- Overkill para o tamanho atual do sistema
- Pode ser considerado em v1.0+ como módulo opcional

### Alternativa D: Logging estruturado

Instrumentar todos os componentes com `logging` estruturado e analisar os logs.

**Rejeitada como solução primária porque:**
- Não é programaticamente consultável sem parsing
- Não oferece snapshot de estado — apenas histórico de eventos
- Pode coexistir como complemento, não como substituto

---

## Consequências

### Positivas

- **Zero overhead em produção** quando não usado — `run_diagnostics()` é chamado sob demanda
- **API padronizada** — um único ponto de entrada para todos os diagnósticos
- **Sem breaking changes** — módulo adicional, não modifica nenhuma interface existente
- **Testável** — 35 testes com 100% de cobertura de `kernel/diagnostics/`
- **Extensível** — novos componentes podem ser incorporados ao `DiagnosticReport` sem quebrar a API

### Negativas / Limitações

- **Snapshot, não streaming** — `run_diagnostics()` captura estado no instante da chamada; estado pode mudar entre chamadas
- **Sem alertas proativos** — o módulo não monitora continuamente nem dispara alertas; requer chamada explícita
- **Saúde de serviços depende de implementação** — serviços sem método `health()` aparecem com `health_result=None`, não como `healthy=False`

---

## Estrutura implementada

```
kernel/
└── diagnostics/
    ├── __init__.py       — exporta: run_diagnostics, DiagnosticReport,
    │                                print_diagnostics, inspect_kernel,
    │                                inspect_registry, inspect_services,
    │                                inspect_events
    ├── doctor.py         — DiagnosticReport, run_diagnostics(), print_diagnostics()
    └── inspector.py      — inspect_kernel(), inspect_registry(),
                            inspect_services(), inspect_events()
```

### Uso mínimo

```python
from kernel.bootstrap import bootstrap_system
from kernel.diagnostics import run_diagnostics, print_diagnostics

kernel = bootstrap_system()
kernel.start()

report = run_diagnostics(kernel)

if not report.healthy:
    print_diagnostics(report)
    raise RuntimeError(f"Kernel não está saudável: {report.issues}")
```

---

## Rastreabilidade

| Item                        | Referência                                          |
|-----------------------------|-----------------------------------------------------|
| Implementação               | `kernel/diagnostics/doctor.py`, `inspector.py`      |
| Testes                      | `testes/contract/test_diagnostics.py` (35 testes)   |
| Cobertura                   | 100% de `kernel/diagnostics/`                       |
| Índice mestre               | `docs/INDICE-MESTRE.md` — seção 4a e 8              |
| Matriz de rastreabilidade   | `docs/MATRIZ-RASTREABILIDADE.md` — seção 10         |
| Guia de uso                 | `docs/06-operacao/kernel-operations-guide-v1.md` §7 |
| Cookbook                    | `docs/05-desenvolvimento/kernel-cookbook-v1.md` §5  |

---

**Documento:** `ADR-0003-OBSERVABILIDADE-KERNEL-v1.md`  
**Localização:** `docs/04-padroes/`  
**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** ACEITO
