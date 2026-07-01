"""Testes das receitas do Kernel Cookbook v1 — SOE-CCG.

Cada função de teste corresponde exatamente a uma receita do documento
docs/05-desenvolvimento/kernel-cookbook-v1.md.
"""
from __future__ import annotations

import pytest

# ---------------------------------------------------------------------------
# Receita 1: Registrar módulo custom
# ---------------------------------------------------------------------------


def test_receita1_registrar_modulo_custom() -> None:
    """Receita 1: criar ModuleContract completo, registrar e verificar queries."""
    from kernel.contracts.module import ModuleContract
    from kernel.core import MicroKernel

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

    kernel = MicroKernel()
    kernel.register(contrato)
    kernel.initialize()

    # Verificar via registry.get() (find_by_name)
    recuperado = kernel.registry.get("plugin.analisador")
    assert recuperado.name == "plugin.analisador"
    assert recuperado.version == "2.1.0"
    assert recuperado.author == "Time SOE"
    assert recuperado.category == "plugin"
    assert recuperado.type == "service"
    assert recuperado.state == "experimental"
    assert recuperado.priority == 50
    assert recuperado.lifecycle_policy == "singleton"
    assert "analisador" in recuperado.provides
    assert "nlp" in recuperado.provides

    # Verificar via find_by_capability()
    resultados = kernel.registry.find_by_capability("analisador")
    assert len(resultados) == 1
    assert resultados[0].name == "plugin.analisador"

    resultados_nlp = kernel.registry.find_by_capability("nlp")
    assert len(resultados_nlp) == 1
    assert resultados_nlp[0].name == "plugin.analisador"

    # Capability inexistente retorna lista vazia
    assert kernel.registry.find_by_capability("inexistente") == []


# ---------------------------------------------------------------------------
# Receita 2: Criar serviço e registrá-lo
# ---------------------------------------------------------------------------


def test_receita2_criar_e_registrar_servico() -> None:
    """Receita 2: definir serviço com health(), registrar e verificar saúde."""
    from kernel.contracts.module import ModuleContract
    from kernel.core import MicroKernel

    class CacheService:
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

    # Recuperar via get_service()
    servico = kernel.get_service("cache")
    assert servico is instancia
    assert servico.get("chave1") == "valor1"

    # Verificar all_health()
    saude = kernel.services.all_health()
    assert "cache" in saude
    info = saude["cache"]
    assert info["registered"] is True
    assert info["has_health_method"] is True
    assert info["health_result"]["healthy"] is True
    assert info["health_result"]["itens"] == 1
    assert info["error"] is None


# ---------------------------------------------------------------------------
# Receita 3: Assinar e publicar eventos
# ---------------------------------------------------------------------------


def test_receita3_assinar_e_publicar_eventos() -> None:
    """Receita 3: subscribe, publish, history e handlers_for."""
    from kernel.contracts.module import ModuleContract
    from kernel.core import MicroKernel
    from kernel.events.bus import KernelEvent

    kernel = MicroKernel()
    contrato = ModuleContract(name="runtime.demo", provides=("demo",))
    kernel.register(contrato)
    kernel.initialize()

    # subscribe()
    eventos_recebidos: list[tuple] = []

    def handler_registro(event: KernelEvent, data: dict) -> None:
        eventos_recebidos.append((event, data))

    def handler_estado(event: KernelEvent, data: dict) -> None:
        eventos_recebidos.append((event, data))

    kernel.events.subscribe(KernelEvent.MODULE_REGISTERED, handler_registro)
    kernel.events.subscribe(KernelEvent.STATE_CHANGED, handler_estado)

    # publish() com dados
    kernel.events.publish(
        KernelEvent.MODULE_REGISTERED,
        {"name": "plugin.teste", "version": "1.0.0"},
    )
    kernel.events.publish(
        KernelEvent.STATE_CHANGED,
        {"from": "initialized", "to": "running"},
    )

    # Verificar history()
    historico = kernel.events.history()
    assert any(e == KernelEvent.MODULE_REGISTERED for e, _ in historico)
    assert any(e == KernelEvent.STATE_CHANGED for e, _ in historico)

    # Filtrar histórico por tipo de evento
    historico_registro = kernel.events.history(KernelEvent.MODULE_REGISTERED)
    assert len(historico_registro) >= 1

    # Nosso dado específico deve estar no histórico
    nossos = [d for e, d in historico_registro if d.get("name") == "plugin.teste"]
    assert len(nossos) == 1
    assert nossos[0]["version"] == "1.0.0"

    # handlers_for()
    handlers_reg = kernel.events.handlers_for(KernelEvent.MODULE_REGISTERED)
    assert handler_registro in handlers_reg

    handlers_estado = kernel.events.handlers_for(KernelEvent.STATE_CHANGED)
    assert handler_estado in handlers_estado

    # Os handlers foram chamados
    recebidos_registro = [
        (e, d) for e, d in eventos_recebidos if e == KernelEvent.MODULE_REGISTERED
    ]
    assert len(recebidos_registro) >= 1

    recebidos_estado = [
        (e, d) for e, d in eventos_recebidos if e == KernelEvent.STATE_CHANGED
    ]
    assert len(recebidos_estado) >= 1


# ---------------------------------------------------------------------------
# Receita 4: Queries avançadas no registry
# ---------------------------------------------------------------------------


def test_receita4_queries_avancadas_registry() -> None:
    """Receita 4: find_by_capability, find_by_category, find_by_type, dependency_graph."""
    from kernel.contracts.module import ModuleContract
    from kernel.core import MicroKernel

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

    # find_by_capability()
    provedores = kernel.registry.find_by_capability("parser")
    assert len(provedores) == 1
    assert provedores[0].name == "runtime.parser"

    assert kernel.registry.find_by_capability("inexistente") == []

    # find_by_category()
    runtime_mods = kernel.registry.find_by_category("runtime")
    nomes_runtime = [m.name for m in runtime_mods]
    assert "runtime.parser" in nomes_runtime
    assert "runtime.validator" in nomes_runtime
    assert "application.cli" not in nomes_runtime

    kernel_mods = kernel.registry.find_by_category("kernel")
    assert len(kernel_mods) == 1
    assert kernel_mods[0].name == "kernel.core"

    # find_by_type()
    commands = kernel.registry.find_by_type("command")
    assert len(commands) == 1
    assert commands[0].name == "application.cli"

    libraries = kernel.registry.find_by_type("library")
    assert len(libraries) == 2
    nomes_lib = [m.name for m in libraries]
    assert "runtime.parser" in nomes_lib
    assert "runtime.validator" in nomes_lib

    # dependency_graph()
    grafo = kernel.registry.dependency_graph()
    assert isinstance(grafo, dict)
    assert "runtime.parser" in grafo["application.cli"]
    assert "runtime.validator" in grafo["application.cli"]
    assert "kernel.core" in grafo["runtime.parser"]
    assert "kernel.core" in grafo["runtime.validator"]
    assert grafo["kernel.core"] == []


# ---------------------------------------------------------------------------
# Receita 5: Health check completo de todos os componentes
# ---------------------------------------------------------------------------


def test_receita5_health_check_completo() -> None:
    """Receita 5: registry.health, all_health, run_diagnostics, print_diagnostics."""
    from kernel.contracts.module import ModuleContract
    from kernel.core import MicroKernel
    from kernel.diagnostics.doctor import DiagnosticReport, print_diagnostics, run_diagnostics

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

    # 3. run_diagnostics() com DiagnosticReport
    relatorio = run_diagnostics(kernel)
    assert isinstance(relatorio, DiagnosticReport)
    assert relatorio.kernel_state == kernel.state.value
    assert isinstance(relatorio.registry_health, dict)
    assert isinstance(relatorio.registry_stats, dict)
    assert isinstance(relatorio.services_health, dict)
    assert isinstance(relatorio.services_stats, dict)
    assert isinstance(relatorio.events_stats, dict)
    assert isinstance(relatorio.issues, list)
    assert relatorio.healthy is True
    assert isinstance(relatorio.summary, str)
    assert len(relatorio.summary) > 0

    # 4. print_diagnostics() — não deve lançar exceção
    print_diagnostics(relatorio)


# ---------------------------------------------------------------------------
# Receita 6: Lifecycle manual de um módulo
# ---------------------------------------------------------------------------


def test_receita6_lifecycle_manual() -> None:
    """Receita 6: bootstrap_system, start, stop, verificar kernel.state em cada etapa."""
    from kernel.bootstrap import bootstrap_system
    from kernel.contracts.module import ModuleContract
    from kernel.lifecycle.manager import LifecycleState

    modulo_extra = ModuleContract(
        name="plugin.lifecycle_demo",
        provides=("lifecycle_demo",),
        description="Módulo de demonstração do ciclo de vida.",
        category="plugin",
        state="experimental",
    )

    # 1. bootstrap_system() — inicializa o kernel
    kernel = bootstrap_system(extra_modules=(modulo_extra,))

    # Após bootstrap: INITIALIZED
    assert kernel.state == LifecycleState.INITIALIZED

    # O módulo extra foi registrado
    recuperado = kernel.registry.get("plugin.lifecycle_demo")
    assert recuperado.name == "plugin.lifecycle_demo"

    # 2. kernel.start() → RUNNING
    kernel.start()
    assert kernel.state == LifecycleState.RUNNING
    assert kernel.lifecycle.is_operational() is True
    assert kernel.lifecycle.is_stable() is True

    # 3. kernel.stop() → STOPPED
    kernel.stop()
    assert kernel.state == LifecycleState.STOPPED
    assert kernel.lifecycle.is_operational() is False
    assert kernel.lifecycle.is_stable() is True
    assert kernel.lifecycle.is_terminal() is False
