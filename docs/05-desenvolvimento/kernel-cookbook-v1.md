# Kernel Cookbook v1 — SOE-CCG Microkernel

> Receitas executáveis para as operações mais comuns do microkernel SOE-CCG.
> Cada receita é autocontida e corresponde a um teste em `testes/cookbook/test_cookbook.py`.

---

## Índice

1. [Registrar módulo custom](#receita-1-registrar-módulo-custom)
2. [Criar serviço e registrá-lo](#receita-2-criar-serviço-e-registrá-lo)
3. [Assinar e publicar eventos](#receita-3-assinar-e-publicar-eventos)
4. [Queries avançadas no registry](#receita-4-queries-avançadas-no-registry)
5. [Health check completo de todos os componentes](#receita-5-health-check-completo-de-todos-os-componentes)
6. [Lifecycle manual de um módulo](#receita-6-lifecycle-manual-de-um-módulo)

---

## Receita 1: Registrar módulo custom

**Objetivo:** Criar um `ModuleContract` com todos os campos relevantes,
registrá-lo no kernel e verificar a pesquisa por nome e por capability.

```python
from kernel.contracts.module import ModuleContract
from kernel.core import MicroKernel

# 1. Criar um ModuleContract com todos os campos
contrato = ModuleContract(
    name="plugin.analisador",
    version="2.1.0",
    author="Time SOE",
    description="Analisador semântico de entidades do grafo.",
    category="plugin",
    type="service",
    state="experimental",
    provides=("analisador", "nlp"),
    requires=(),
    optional_requires=("ir",),
    capabilities={
        "analisador": "Analisa entidades semânticas.",
        "nlp": "Processamento de linguagem natural.",
    },
    entrypoint="plugins.analisador",
    priority=50,
    lifecycle_policy="singleton",
)

# 2. Registrar via kernel.register()
kernel = MicroKernel()
kernel.register(contrato)
kernel.initialize()

# 3. Verificar via find_by_name() — usando registry.get()
recuperado = kernel.registry.get("plugin.analisador")
assert recuperado.name == "plugin.analisador"
assert recuperado.version == "2.1.0"
assert recuperado.author == "Time SOE"
assert recuperado.category == "plugin"
assert recuperado.type == "service"
assert recuperado.state == "experimental"
assert recuperado.priority == 50
assert recuperado.lifecycle_policy == "singleton"

# 4. Verificar via find_by_capability()
resultados = kernel.registry.find_by_capability("analisador")
assert len(resultados) == 1
assert resultados[0].name == "plugin.analisador"

resultados_nlp = kernel.registry.find_by_capability("nlp")
assert len(resultados_nlp) == 1
assert resultados_nlp[0].name == "plugin.analisador"
```

**Pontos-chave:**
- `ModuleContract` é um `dataclass(frozen=True)` — imutável após criação.
- `provides` deve conter ao menos uma capability (validado em `validate()`).
- `kernel.initialize()` chama `registry.validate()` e `registry.resolve_order()`.
- `find_by_capability(cap)` retorna lista de 0 ou 1 elemento (registry impede duplicatas).

---

## Receita 2: Criar serviço e registrá-lo

**Objetivo:** Definir uma classe de serviço com método `health()`, registrá-la
no kernel e verificar recuperação e saúde.

```python
from kernel.contracts.module import ModuleContract
from kernel.core import MicroKernel

# 1. Definir classe de serviço com método health()
class CacheService:
    """Serviço de cache em memória."""

    def __init__(self, capacidade: int = 100) -> None:
        self._store: dict = {}
        self._capacidade = capacidade

    def set(self, chave: str, valor) -> None:
        self._store[chave] = valor

    def get(self, chave: str):
        return self._store.get(chave)

    def health(self) -> dict:
        uso = len(self._store) / self._capacidade
        return {
            "healthy": uso < 1.0,
            "uso_percentual": uso * 100,
            "itens": len(self._store),
            "capacidade": self._capacidade,
        }

# 2. Registrar via kernel.register_service()
kernel = MicroKernel()
contrato = ModuleContract(
    name="runtime.cache",
    provides=("cache",),
    description="Serviço de cache em memória.",
)
kernel.register(contrato)
kernel.initialize()

instancia = CacheService(capacidade=50)
instancia.set("chave1", "valor1")
kernel.register_service("cache", instancia)

# 3. Recuperar via get_service()
servico = kernel.get_service("cache")
assert servico is instancia
assert servico.get("chave1") == "valor1"

# 4. Verificar all_health()
saude = kernel.services.all_health()
assert "cache" in saude
info = saude["cache"]
assert info["registered"] is True
assert info["has_health_method"] is True
assert info["health_result"]["healthy"] is True
assert info["health_result"]["itens"] == 1
assert info["error"] is None
```

**Pontos-chave:**
- `kernel.register_service(name, instance)` delega ao `ServiceRegistry` e publica `SERVICE_REGISTERED`.
- `kernel.get_service(name)` levanta `ServiceError` se o serviço não estiver registrado.
- `all_health()` chama `instance.health()` para cada serviço e captura exceções em `"error"`.
- Serviços sem método `health()` retornam `has_health_method=False` e `health_result=None`.

---

## Receita 3: Assinar e publicar eventos

**Objetivo:** Subscrever handlers a eventos do kernel, publicar eventos com dados
e verificar o histórico e os handlers registrados.

```python
from kernel.contracts.module import ModuleContract
from kernel.core import MicroKernel
from kernel.events.bus import KernelEvent

# Setup básico
kernel = MicroKernel()
contrato = ModuleContract(name="runtime.demo", provides=("demo",))
kernel.register(contrato)
kernel.initialize()

# 1. subscribe() para KernelEvent
eventos_recebidos: list[tuple] = []

def handler_registro(event: KernelEvent, data: dict) -> None:
    eventos_recebidos.append((event, data))

def handler_estado(event: KernelEvent, data: dict) -> None:
    eventos_recebidos.append((event, data))

kernel.events.subscribe(KernelEvent.MODULE_REGISTERED, handler_registro)
kernel.events.subscribe(KernelEvent.STATE_CHANGED, handler_estado)

# 2. publish() com dados
kernel.events.publish(
    KernelEvent.MODULE_REGISTERED,
    {"name": "plugin.teste", "version": "1.0.0"},
)
kernel.events.publish(
    KernelEvent.STATE_CHANGED,
    {"from": "initialized", "to": "running"},
)

# 3. Verificar history()
historico = kernel.events.history()
# O histórico inclui todos os eventos desde a criação do kernel
assert any(e == KernelEvent.MODULE_REGISTERED for e, _ in historico)
assert any(e == KernelEvent.STATE_CHANGED for e, _ in historico)

# Filtrar por tipo de evento
historico_registro = kernel.events.history(KernelEvent.MODULE_REGISTERED)
assert len(historico_registro) >= 1  # inclui os do initialize() + o nosso

# Verificar que os nossos dados chegaram
nossos = [d for e, d in historico_registro if d.get("name") == "plugin.teste"]
assert len(nossos) == 1
assert nossos[0]["version"] == "1.0.0"

# 4. Verificar handlers_for()
handlers = kernel.events.handlers_for(KernelEvent.MODULE_REGISTERED)
assert handler_registro in handlers

handlers_estado = kernel.events.handlers_for(KernelEvent.STATE_CHANGED)
assert handler_estado in handlers_estado

# Checar que os handlers receberam os eventos
eventos_de_registro = [(e, d) for e, d in eventos_recebidos if e == KernelEvent.MODULE_REGISTERED]
assert len(eventos_de_registro) >= 1
```

**Pontos-chave:**
- `subscribe(event, handler)` levanta `ValueError` se o mesmo handler já está registrado.
- `publish(event, data)` retorna o número de handlers notificados.
- `history(event=None)` sem argumento retorna todos; com argumento filtra por tipo.
- Handlers são chamados em ordem de subscrição; exceções individuais não interrompem a entrega.
- O kernel já publica eventos internamente durante `register()` e `initialize()`.

---

## Receita 4: Queries avançadas no registry

**Objetivo:** Explorar as APIs de busca do `ModuleRegistry` para filtrar módulos
por capability, categoria, tipo e visualizar o grafo de dependências.

```python
from kernel.contracts.module import ModuleContract
from kernel.core import MicroKernel

# Montar um registry com módulos variados
kernel = MicroKernel()

modulos = [
    ModuleContract(
        name="kernel.core",
        category="kernel",
        type="daemon",
        state="stable",
        provides=("core_api",),
    ),
    ModuleContract(
        name="runtime.parser",
        category="runtime",
        type="library",
        state="stable",
        provides=("parser",),
        requires=("core_api",),
    ),
    ModuleContract(
        name="runtime.validator",
        category="runtime",
        type="library",
        state="experimental",
        provides=("validator",),
        requires=("core_api",),
    ),
    ModuleContract(
        name="application.cli",
        category="application",
        type="command",
        state="stable",
        provides=("cli",),
        requires=("parser", "validator"),
    ),
]

for m in modulos:
    kernel.register(m)
kernel.initialize()

# 1. find_by_capability()
provedores = kernel.registry.find_by_capability("parser")
assert len(provedores) == 1
assert provedores[0].name == "runtime.parser"

sem_provedor = kernel.registry.find_by_capability("inexistente")
assert sem_provedor == []

# 2. find_by_category()
runtime_mods = kernel.registry.find_by_category("runtime")
nomes_runtime = [m.name for m in runtime_mods]
assert "runtime.parser" in nomes_runtime
assert "runtime.validator" in nomes_runtime
assert "application.cli" not in nomes_runtime

kernel_mods = kernel.registry.find_by_category("kernel")
assert len(kernel_mods) == 1
assert kernel_mods[0].name == "kernel.core"

# 3. find_by_type()
commands = kernel.registry.find_by_type("command")
assert len(commands) == 1
assert commands[0].name == "application.cli"

libraries = kernel.registry.find_by_type("library")
assert len(libraries) == 2

# 4. dependency_graph()
grafo = kernel.registry.dependency_graph()
assert isinstance(grafo, dict)
# cli depende de parser e validator
assert "runtime.parser" in grafo["application.cli"]
assert "runtime.validator" in grafo["application.cli"]
# parser depende de kernel.core
assert "kernel.core" in grafo["runtime.parser"]
# kernel.core não tem dependências
assert grafo["kernel.core"] == []
```

**Pontos-chave:**
- `find_by_category(cat)` aceita: `"kernel"`, `"runtime"`, `"application"`, `"plugin"`, `"tool"`.
- `find_by_type(type)` aceita: `"service"`, `"library"`, `"command"`, `"daemon"`.
- `dependency_graph()` mapeia nomes de módulos para lista de módulos dos quais dependem.
- Todos os métodos `find_*` retornam listas ordenadas alfabeticamente por nome.
- `find_by_capability()` retorna no máximo 1 elemento (o registry impede duplicatas de capability).

---

## Receita 5: Health check completo de todos os componentes

**Objetivo:** Executar verificações de saúde no registry, nos serviços e no
diagnóstico completo via `run_diagnostics()` e `print_diagnostics()`.

```python
from kernel.contracts.module import ModuleContract
from kernel.core import MicroKernel
from kernel.diagnostics.doctor import run_diagnostics, print_diagnostics

# Setup: kernel com módulo e serviço
kernel = MicroKernel()
contrato = ModuleContract(
    name="runtime.health_demo",
    provides=("health_demo",),
    description="Módulo para demonstração de health check.",
)
kernel.register(contrato)
kernel.initialize()

class MonitorService:
    def health(self) -> dict:
        return {"healthy": True, "latencia_ms": 12, "status": "ok"}

kernel.register_service("monitor", MonitorService())

# 1. registry.health()
reg_health = kernel.registry.health()
assert reg_health["healthy"] is True
assert isinstance(reg_health["total_modules"], int)
assert reg_health["total_modules"] >= 1
assert isinstance(reg_health["missing_dependencies"], list)
assert isinstance(reg_health["circular_dependencies"], list)
assert isinstance(reg_health["deprecated_modules"], list)

# 2. services.all_health()
svc_health = kernel.services.all_health()
assert "monitor" in svc_health
monitor_info = svc_health["monitor"]
assert monitor_info["registered"] is True
assert monitor_info["has_health_method"] is True
assert monitor_info["health_result"]["healthy"] is True
assert monitor_info["health_result"]["status"] == "ok"
assert monitor_info["error"] is None

# 3. run_diagnostics() — retorna DiagnosticReport
relatorio = run_diagnostics(kernel)
assert relatorio.kernel_state == kernel.state.value
assert isinstance(relatorio.registry_health, dict)
assert isinstance(relatorio.registry_stats, dict)
assert isinstance(relatorio.services_health, dict)
assert isinstance(relatorio.services_stats, dict)
assert isinstance(relatorio.events_stats, dict)
assert isinstance(relatorio.issues, list)
assert relatorio.healthy is True
assert "saudável" in relatorio.summary or relatorio.healthy

# 4. print_diagnostics() — saída formatada (não deve lançar exceção)
print_diagnostics(relatorio)
```

**Pontos-chave:**
- `registry.health()` retorna `{"healthy", "total_modules", "missing_dependencies", "circular_dependencies", "deprecated_modules"}`.
- `all_health()` chama `service_health()` para cada serviço registrado.
- `run_diagnostics(kernel)` agrega registry, services e events num `DiagnosticReport`.
- `DiagnosticReport.healthy` é `True` quando `issues` está vazio.
- `DiagnosticReport.summary` retorna `"✅ Kernel: saudável"` ou mensagem com contagem de problemas.
- `print_diagnostics(report)` imprime relatório formatado no stdout (não retorna nada útil).

---

## Receita 6: Lifecycle manual de um módulo

**Objetivo:** Percorrer o ciclo de vida completo do kernel — desde o bootstrap
até o stop — verificando o estado em cada etapa.

```python
from kernel.bootstrap import bootstrap_system
from kernel.contracts.module import ModuleContract
from kernel.lifecycle.manager import LifecycleState

# Módulo extra para adicionar ao bootstrap
modulo_extra = ModuleContract(
    name="plugin.lifecycle_demo",
    provides=("lifecycle_demo",),
    description="Módulo de demonstração do ciclo de vida.",
    category="plugin",
    state="experimental",
)

# 1. bootstrap_system() — cria e inicializa o kernel
kernel = bootstrap_system(extra_modules=(modulo_extra,))

# Após bootstrap, o kernel está em INITIALIZED
assert kernel.state == LifecycleState.INITIALIZED

# Verificar que o módulo extra foi registrado
recuperado = kernel.registry.get("plugin.lifecycle_demo")
assert recuperado.name == "plugin.lifecycle_demo"

# 2. kernel.start() — transita para RUNNING
kernel.start()
assert kernel.state == LifecycleState.RUNNING

# Em RUNNING o kernel é operacional
assert kernel.lifecycle.is_operational() is True
assert kernel.lifecycle.is_stable() is True

# 3. kernel.stop() — transita para STOPPED
kernel.stop()
assert kernel.state == LifecycleState.STOPPED

# Em STOPPED o kernel não é mais operacional
assert kernel.lifecycle.is_operational() is False
assert kernel.lifecycle.is_stable() is True
assert kernel.lifecycle.is_terminal() is False
```

**Pontos-chave:**
- `bootstrap_system(extra_modules=())` cria um kernel já inicializado (`INITIALIZED`).
- `kernel.start()` exige que o kernel esteja em `INITIALIZED`; transita por `STARTING → RUNNING`.
- `kernel.stop()` transita por `STOPPING → STOPPED` a partir de `RUNNING`, `PAUSED` ou `INITIALIZED`.
- `kernel.state` é um `LifecycleState` (enum); comparar com `LifecycleState.RUNNING`, etc.
- `lifecycle.is_operational()` retorna `True` apenas em `RUNNING` ou `PAUSED`.
- O kernel não pode chamar `start()` novamente após `STOPPED` sem `restart()`.

---

## Referência rápida de APIs

| Operação | API |
|---|---|
| Registrar módulo | `kernel.register(contract)` |
| Buscar módulo por nome | `kernel.registry.get(name)` |
| Buscar por capability | `kernel.registry.find_by_capability(cap)` |
| Buscar por categoria | `kernel.registry.find_by_category(cat)` |
| Buscar por tipo | `kernel.registry.find_by_type(type)` |
| Grafo de dependências | `kernel.registry.dependency_graph()` |
| Saúde do registry | `kernel.registry.health()` |
| Registrar serviço | `kernel.register_service(name, instance)` |
| Recuperar serviço | `kernel.get_service(name)` |
| Saúde de todos serviços | `kernel.services.all_health()` |
| Subscrever evento | `kernel.events.subscribe(event, handler)` |
| Publicar evento | `kernel.events.publish(event, data)` |
| Histórico de eventos | `kernel.events.history(event=None)` |
| Handlers por evento | `kernel.events.handlers_for(event)` |
| Diagnóstico completo | `run_diagnostics(kernel)` |
| Imprimir diagnóstico | `print_diagnostics(report)` |
| Bootstrap completo | `bootstrap_system(extra_modules=())` |
| Estado atual | `kernel.state` |
| Iniciar kernel | `kernel.start()` |
| Parar kernel | `kernel.stop()` |
