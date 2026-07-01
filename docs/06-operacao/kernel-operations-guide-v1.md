# Guia de Operação do Kernel — SOE-CCG

**Versão:** 1.0  
**Data:** 2026-07-01  
**Audiência:** Desenvolvedores integrando módulos com o Kernel

---

## Índice

1. [Inicialização do Kernel](#1-inicialização-do-kernel)
2. [Registrar Módulos](#2-registrar-módulos)
3. [Consultar o Registry](#3-consultar-o-registry)
4. [Usar Eventos](#4-usar-eventos)
5. [Registrar e Usar Serviços](#5-registrar-e-usar-serviços)
6. [Lifecycle Manual](#6-lifecycle-manual)
7. [Diagnóstico e Observabilidade](#7-diagnóstico-e-observabilidade)
8. [Troubleshooting Comum](#8-troubleshooting-comum)

---

## 1. Inicialização do Kernel

### `bootstrap_system()`

A forma padrão de inicializar o Kernel é via `bootstrap_system()`:

```python
from kernel.bootstrap import bootstrap_system

kernel = bootstrap_system()
# Kernel está em estado INITIALIZED e pronto para uso
```

**O que `bootstrap_system()` faz internamente:**

1. Garante que o `PROJECT_ROOT` está no `sys.path`
2. Cria uma instância de `MicroKernel`
3. Registra os 8 módulos padrão (`DEFAULT_MODULES`):
   - `kernel.paths` — fonte canônica de paths
   - `runtime.ir` — representação intermediária
   - `runtime.parser` — parser Markdown
   - `runtime.resolver` — resolvedor de referências
   - `runtime.validator` — validação estrutural
   - `runtime.importer` — importação para SQLite
   - `application.cli` — interface de linha de comando
   - `application.faa` — pipeline de auditoria
4. Chama `kernel.initialize()`, que:
   - Valida todos os contratos (`registry.validate()`)
   - Publica `CONTRACT_VALIDATED`
   - Resolve ordem de dependências (`registry.resolve_order()`)
   - Publica `DEPENDENCY_RESOLVED`
   - Transita lifecycle: `CREATED → INITIALIZED`
   - Publica `STATE_CHANGED`

**Estado resultante:** `LifecycleState.INITIALIZED`

### Módulos extras no bootstrap

Para registrar módulos adicionais junto com os padrões:

```python
from kernel.bootstrap import bootstrap_system
from kernel.contracts.module import ModuleContract

meu_modulo = ModuleContract(
    name="meu.modulo",
    provides=("minha_cap",),
    entrypoint="meu.pacote.modulo",
)

kernel = bootstrap_system(extra_modules=(meu_modulo,))
```

### Criação manual (sem módulos padrão)

```python
from kernel.core import MicroKernel

kernel = MicroKernel()
# Estado: CREATED — nenhum módulo registrado ainda
```

---

## 2. Registrar Módulos

### `ModuleContract` — campos

```python
from kernel.contracts.module import ModuleContract

contrato = ModuleContract(
    # Identidade (obrigatório)
    name="minha.ferramenta",          # Nome único hierárquico
    version="1.0.0",                  # SemVer MAJOR.MINOR.PATCH

    # Metadados (opcional)
    author="time-backend",
    description="Ferramenta de análise de receitas.",

    # Categorização (opcional, defaults abaixo)
    category="application",           # "kernel"|"runtime"|"application"|"plugin"|"tool"
    type="library",                   # "service"|"library"|"command"|"daemon"
    state="stable",                   # "experimental"|"stable"|"deprecated"|"archived"

    # Dependências (provides obrigatório)
    provides=("analise_receitas",),   # Capabilities fornecidas — mínimo 1
    requires=("ir",),                 # Hard dependencies (capabilities requeridas)
    optional_requires=("cache",),     # Soft dependencies

    # Execução (opcional)
    entrypoint="minha_app.analise",   # Caminho de importação Python
    priority=100,                     # 0=crítico, 100=padrão, 999=baixa
)
```

### Registrar via `kernel.register()`

```python
kernel.register(contrato)
# Publica KernelEvent.MODULE_REGISTERED automaticamente
```

**Regras:**
- `provides` deve ter ao menos 1 capability
- Não pode haver dois módulos com o mesmo `name`
- Não pode haver duas capabilities iguais em `provides` entre módulos distintos
- `requires` não pode conter capabilities que o próprio módulo fornece

**Erros possíveis:**

```python
from kernel.registry.module_registry import RegistryError

try:
    kernel.register(contrato)
except RegistryError as e:
    print(f"Erro de registro: {e}")
```

---

## 3. Consultar o Registry

O registry é acessível via `kernel.registry`.

### Busca por nome exato

```python
contrato = kernel.registry.get("runtime.parser")
print(contrato.name, contrato.version)
```

### Busca por padrão (regex)

```python
# Todos os módulos do namespace "runtime"
modulos = kernel.registry.find(r"^runtime\.")
for m in modulos:
    print(m.name)
```

### Busca por capability

```python
# Quem fornece "parser"?
provedores = kernel.registry.find_by_capability("parser")
# → [<ModuleContract name='runtime.parser'>]

# Quem é o provedor de uma capability?
contrato = kernel.registry.provider_for("ir")
```

### Busca por categoria

```python
# Todos os módulos de aplicação
apps = kernel.registry.find_by_category("application")

# Módulos do kernel
kernel_mods = kernel.registry.find_by_category("kernel")
```

Valores válidos: `"kernel"`, `"runtime"`, `"application"`, `"plugin"`, `"tool"`

### Busca por tipo

```python
servicos = kernel.registry.find_by_type("service")
bibliotecas = kernel.registry.find_by_type("library")
```

Valores válidos: `"service"`, `"library"`, `"command"`, `"daemon"`

### Busca por estado de maturidade

```python
experimentais = kernel.registry.find_by_state("experimental")
deprecados = kernel.registry.find_by_state("deprecated")
```

### Listar todos os contratos

```python
todos = kernel.registry.contracts()  # tuple[ModuleContract, ...]
for c in todos:
    print(c.name, c.version, c.state)
```

### Grafo de dependências

```python
grafo = kernel.registry.dependency_graph()
# → {"runtime.parser": ["runtime.ir"], "runtime.ir": [], ...}

for modulo, deps in grafo.items():
    if deps:
        print(f"{modulo} depende de: {', '.join(deps)}")
```

### Saúde do registry

```python
health = kernel.registry.health()
# {
#   "healthy": True,
#   "total_modules": 8,
#   "missing_dependencies": [],
#   "circular_dependencies": [],
#   "deprecated_modules": []
# }

if not health["healthy"]:
    for dep in health["missing_dependencies"]:
        print(f"Dependência ausente: {dep}")
```

### Estatísticas

```python
stats = kernel.registry.stats()
# {
#   "total_modules": 8,
#   "total_capabilities": 8,
#   "by_category_application": 2,
#   "by_category_runtime": 5,
#   "by_type_library": 8,
#   "by_state_stable": 8,
#   ...
# }
print(f"Total de módulos: {stats['total_modules']}")
print(f"Módulos estáveis: {stats['by_state_stable']}")
```

---

## 4. Usar Eventos

O barramento de eventos é acessível via `kernel.events`.

### Eventos disponíveis

```python
from kernel.events.bus import KernelEvent

# Todos os eventos do kernel:
# KernelEvent.MODULE_DISCOVERED    — módulo descoberto antes do registro
# KernelEvent.MODULE_REGISTERED    — contrato registrado com sucesso
# KernelEvent.MODULE_STARTED       — kernel entrou em RUNNING
# KernelEvent.MODULE_STOPPED       — kernel entrou em STOPPED
# KernelEvent.MODULE_FAILED        — kernel entrou em FAILED
# KernelEvent.CONTRACT_VALIDATED   — validate() bem-sucedido
# KernelEvent.DEPENDENCY_RESOLVED  — resolve_order() bem-sucedido
# KernelEvent.STATE_CHANGED        — transição de estado do lifecycle
# KernelEvent.SERVICE_REGISTERED   — serviço registrado
# KernelEvent.SERVICE_UNREGISTERED — serviço removido
```

### Assinar um evento

```python
from kernel.events.bus import KernelEvent

def ao_registrar_modulo(evento, dados):
    print(f"Módulo registrado: {dados['name']} v{dados['version']}")

kernel.events.subscribe(KernelEvent.MODULE_REGISTERED, ao_registrar_modulo)
```

O handler recebe sempre `(evento: KernelEvent, dados: dict[str, Any])`.

### Publicar um evento

```python
kernel.events.publish(
    KernelEvent.MODULE_DISCOVERED,
    {"name": "meu.modulo", "source": "discovery_scan"},
)
```

`publish()` retorna o número de handlers notificados.

### Cancelar assinatura

```python
kernel.events.unsubscribe(KernelEvent.MODULE_REGISTERED, ao_registrar_modulo)
```

### Consultar handlers registrados

```python
handlers = kernel.events.handlers_for(KernelEvent.MODULE_REGISTERED)
print(f"{len(handlers)} handler(s) para MODULE_REGISTERED")
```

### Histórico de eventos

```python
# Todos os eventos publicados
historico = kernel.events.history()

# Filtrado por tipo
mudancas = kernel.events.history(KernelEvent.STATE_CHANGED)
for evento, dados in mudancas:
    print(f"Estado: {dados['from']} → {dados['to']}")
```

### Estatísticas do barramento

```python
stats = kernel.events.stats()
print(f"Total publicados: {stats['total_events_published']}")
print(f"Total handlers: {stats['total_handlers']}")
print(f"MODULE_REGISTERED publicado: {stats['event_module_registered_published']} vez(es)")
```

---

## 5. Registrar e Usar Serviços

O registry de serviços é acessível via `kernel.services`.

**Serviço** = instância em memória pronta para consumo. Diferente de módulo (metadados estáticos).

### Registrar um serviço

```python
class MeuServico:
    def processar(self, dado):
        return dado.upper()

    def health(self):
        return {"healthy": True, "status": "ok"}

kernel.register_service("processador", MeuServico())
# Publica KernelEvent.SERVICE_REGISTERED automaticamente
```

### Recuperar um serviço

```python
svc = kernel.get_service("processador")
resultado = svc.processar("dados de entrada")
```

### Verificar existência

```python
if kernel.services.has_service("processador"):
    svc = kernel.get_service("processador")
```

### Listar serviços registrados

```python
nomes = kernel.services.list_services()  # lista alfabética
print(f"Serviços ativos: {nomes}")
```

### Saúde de um serviço

```python
health = kernel.services.service_health("processador")
# {
#   "name": "processador",
#   "registered": True,
#   "type": "MeuServico",
#   "uptime_seconds": 1.23,
#   "has_health_method": True,
#   "health_result": {"healthy": True, "status": "ok"},
#   "error": None
# }
```

### Saúde de todos os serviços

```python
todos_health = kernel.services.all_health()
for nome, info in todos_health.items():
    resultado = info.get("health_result")
    if resultado and not resultado.get("healthy", True):
        print(f"ATENÇÃO: serviço '{nome}' não está saudável")
```

### Estatísticas de serviços

```python
stats = kernel.services.stats()
# {
#   "total_services": 2,
#   "with_health_method": 1,
#   "without_health_method": 1
# }
```

### Remover um serviço

```python
kernel.unregister_service("processador")
# Publica KernelEvent.SERVICE_UNREGISTERED automaticamente
```

---

## 6. Lifecycle Manual

O estado do kernel é acessível via `kernel.state`.

### Estados e transições

```
CREATED
  └─► INITIALIZING → INITIALIZED
                        ├─► STARTING → RUNNING
                        │               ├─► PAUSING → PAUSED → RESUMING → RUNNING
                        │               └─► STOPPING → STOPPED → RESTARTING → INITIALIZED
                        └─► STOPPING → STOPPED → DISABLED
```

Estados estáveis: `CREATED`, `INITIALIZED`, `RUNNING`, `PAUSED`, `STOPPED`, `FAILED`, `DISABLED`

### Fluxo completo

```python
from kernel.bootstrap import bootstrap_system
from kernel.lifecycle import LifecycleState

kernel = bootstrap_system()
print(kernel.state)  # LifecycleState.INITIALIZED

kernel.start()
print(kernel.state)  # LifecycleState.RUNNING

kernel.stop()
print(kernel.state)  # LifecycleState.STOPPED

# Para reinicializar após STOPPED:
kernel.lifecycle.restart()
print(kernel.state)  # LifecycleState.INITIALIZED

kernel.start()
print(kernel.state)  # LifecycleState.RUNNING
```

### Verificar estado atual

```python
print(kernel.state.value)         # "running"
print(kernel.lifecycle.is_operational())   # True se RUNNING ou PAUSED
print(kernel.lifecycle.is_stable())        # True se em estado estável
print(kernel.lifecycle.is_terminal())      # True se DISABLED
```

### Verificar transição possível

```python
from kernel.lifecycle import LifecycleState

pode = kernel.lifecycle.can_transition_to(LifecycleState.RUNNING)
print(f"Pode ir para RUNNING: {pode}")
```

### Erros de lifecycle

```python
from kernel.lifecycle import LifecycleError

try:
    kernel.start()  # Chamar start() em RUNNING lança LifecycleError
except LifecycleError as e:
    print(f"Transição inválida: {e}")
```

**Atenção:** `kernel.start()` a partir de `STOPPED` lança `LifecycleError`. Primeiro chame `kernel.lifecycle.restart()` para voltar a `INITIALIZED`.

---

## 7. Diagnóstico e Observabilidade

O módulo `kernel.diagnostics` agrega informações de todos os componentes.

### Diagnóstico completo

```python
from kernel.diagnostics import run_diagnostics, print_diagnostics

kernel = bootstrap_system()
kernel.start()

report = run_diagnostics(kernel)

print(report.healthy)        # True se sem problemas
print(report.summary)        # "✅ Kernel: saudável" ou "⚠️ Kernel: N problema(s)"
print(report.kernel_state)   # Estado atual do lifecycle
print(report.issues)         # Lista de problemas detectados
```

### Imprimir relatório formatado

```python
print_diagnostics(report)
# ============================================================
# KERNEL DIAGNOSTICS REPORT
# ============================================================
#
# Estado do Kernel: running
#
# Registry:
#   - Total de módulos: 8
#   - Capabilities: 8
#   - Saudável: True
#
# Serviços:
#   - Total de serviços: 0
#   - Com health check: 0
#
# Eventos:
#   - Total de handlers: 0
#   - Total de publicações: 11
#
# ✅ Nenhum problema detectado
```

### Snapshot completo do estado

```python
from kernel.diagnostics import inspect_kernel

snapshot = inspect_kernel(kernel)
# {
#   "lifecycle": {"state": "running"},
#   "registry": {"contracts": [...], "dependency_graph": {...}, "health": {...}, "stats": {...}},
#   "services": {"list": [...], "health": {...}, "stats": {...}},
#   "events": {"handlers": {...}, "history_size": 11, "stats": {...}}
# }
```

### Inspecionar componentes individuais

```python
from kernel.diagnostics import inspect_registry, inspect_services, inspect_events

info_registry = inspect_registry(kernel)
print(f"Módulos registrados: {info_registry['total_modules']}")

info_services = inspect_services(kernel)
print(f"Serviços: {info_services['services']}")

info_events = inspect_events(kernel)
print(f"Histórico de eventos: {info_events['history_size']} entradas")
```

---

## 8. Troubleshooting Comum

### `RegistryError: módulo já registrado: <nome>`

**Causa:** Tentativa de registrar dois módulos com o mesmo `name`.  
**Solução:** Use nomes únicos. Siga a convenção `dominio.modulo` (ex: `runtime.parser`).

```python
# ❌ Errado
kernel.register(ModuleContract(name="parser", provides=("cap1",)))
kernel.register(ModuleContract(name="parser", provides=("cap2",)))  # RegistryError

# ✅ Correto
kernel.register(ModuleContract(name="runtime.parser", provides=("cap1",)))
kernel.register(ModuleContract(name="tools.parser_v2", provides=("cap2",)))
```

### `RegistryError: capacidade '<cap>' já é fornecida por '<modulo>'`

**Causa:** Dois módulos declaram a mesma capability em `provides`.  
**Solução:** Cada capability deve ter um único provedor.

### `ContractError: <nome>: provides deve declarar ao menos uma capacidade`

**Causa:** `ModuleContract` criado sem `provides`.  
**Solução:** Todo módulo deve declarar ao menos uma capability.

```python
# ✅ Correto
ModuleContract(name="meu.mod", provides=("minha_cap",))
```

### `RegistryError: dependências ausentes`

**Causa:** Um módulo em `requires` referencia uma capability sem provedor registrado.  
**Diagnóstico:**

```python
health = kernel.registry.health()
for dep in health["missing_dependencies"]:
    print(f"Ausente: {dep}")
```

**Solução:** Registre o módulo que provê a capability antes de chamar `initialize()`.

### `LifecycleError: Transição inválida: stopped → starting`

**Causa:** Chamada a `kernel.start()` após `kernel.stop()`.  
**Solução:** Após `stop()`, use `kernel.lifecycle.restart()` antes de `start()`:

```python
kernel.stop()
kernel.lifecycle.restart()   # STOPPED → INITIALIZED
kernel.start()               # INITIALIZED → RUNNING
```

### `ServiceError: serviço não registrado: '<nome>'`

**Causa:** `get_service()` chamado com nome inexistente.  
**Solução:** Verifique com `has_service()` antes, ou trate a exceção:

```python
from kernel.services.service_registry import ServiceError

try:
    svc = kernel.get_service("meu_servico")
except ServiceError:
    print("Serviço não encontrado — verifique o registro")
```

### `ValueError: handler já registrado para '<evento>'`

**Causa:** `subscribe()` chamado duas vezes com o mesmo handler para o mesmo evento.  
**Solução:** Use `unsubscribe()` antes de re-assinar, ou verifique `handlers_for()`:

```python
if meu_handler not in kernel.events.handlers_for(KernelEvent.MODULE_REGISTERED):
    kernel.events.subscribe(KernelEvent.MODULE_REGISTERED, meu_handler)
```

### Kernel com `healthy=False` sem motivo aparente

**Diagnóstico completo:**

```python
from kernel.diagnostics import run_diagnostics, print_diagnostics

report = run_diagnostics(kernel)
print_diagnostics(report)

# Checar cada categoria de problema:
print("Issues:", report.issues)
print("Deps ausentes:", report.registry_health["missing_dependencies"])
print("Deps circulares:", report.registry_health["circular_dependencies"])
print("Módulos deprecated:", report.registry_health["deprecated_modules"])
```

---

**Documento:** `docs/06-operacao/kernel-operations-guide-v1.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
