"""Testes da Fase 4 — consultas avançadas do ModuleRegistry."""
from __future__ import annotations

import pytest

from kernel.contracts.module import ModuleContract
from kernel.registry import ModuleRegistry, RegistryError


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _build_registry() -> ModuleRegistry:
    """Registry com conjunto diversificado de módulos para testes."""
    registry = ModuleRegistry()

    registry.register(ModuleContract(
        name="kernel.core",
        category="kernel",
        type="service",
        state="stable",
        provides=("core",),
        description="Núcleo do kernel",
    ))
    registry.register(ModuleContract(
        name="kernel.events",
        category="kernel",
        type="library",
        state="experimental",
        provides=("events",),
        requires=("core",),
        description="Sistema de eventos do kernel",
    ))
    registry.register(ModuleContract(
        name="runtime.parser",
        category="runtime",
        type="library",
        state="stable",
        provides=("parsing",),
        description="Parser de entidades",
    ))
    registry.register(ModuleContract(
        name="runtime.validator",
        category="runtime",
        type="service",
        state="stable",
        provides=("validation",),
        requires=("parsing",),
        description="Validador de dados",
    ))
    registry.register(ModuleContract(
        name="application.cli",
        category="application",
        type="command",
        state="stable",
        provides=("cli",),
        requires=("parsing", "validation"),
        description="Interface de linha de comando",
    ))
    registry.register(ModuleContract(
        name="plugin.export",
        category="plugin",
        type="library",
        state="deprecated",
        provides=("export.csv",),
        requires=("parsing",),
        description="Exportação para CSV (descontinuado)",
    ))
    registry.register(ModuleContract(
        name="tool.audit",
        category="tool",
        type="command",
        state="stable",
        provides=("audit",),
        requires=("parsing", "validation"),
        description="Ferramenta de auditoria",
    ))

    return registry


@pytest.fixture()
def registry() -> ModuleRegistry:
    return _build_registry()


# ---------------------------------------------------------------------------
# find()
# ---------------------------------------------------------------------------

class TestFind:
    def test_find_por_prefixo(self, registry: ModuleRegistry) -> None:
        results = registry.find(r"^kernel\.")
        names = [c.name for c in results]
        assert "kernel.core" in names
        assert "kernel.events" in names
        assert "runtime.parser" not in names

    def test_find_por_sufixo(self, registry: ModuleRegistry) -> None:
        results = registry.find(r"\.parser$")
        assert len(results) == 1
        assert results[0].name == "runtime.parser"

    def test_find_sem_correspondencia(self, registry: ModuleRegistry) -> None:
        assert registry.find(r"nao.existe") == []

    def test_find_retorna_lista_ordenada(self, registry: ModuleRegistry) -> None:
        results = registry.find(r"kernel|runtime")
        names = [c.name for c in results]
        assert names == sorted(names)

    def test_find_registry_vazio(self) -> None:
        r = ModuleRegistry()
        assert r.find(r".*") == []

    def test_find_padrao_invalido_levanta_erro(self, registry: ModuleRegistry) -> None:
        with pytest.raises(RegistryError, match="padrão regex inválido"):
            registry.find(r"[inválido")

    def test_find_retorna_list_nao_tuple(self, registry: ModuleRegistry) -> None:
        result = registry.find(r".*")
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# find_by_category()
# ---------------------------------------------------------------------------

class TestFindByCategory:
    def test_categoria_kernel(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_category("kernel")
        names = {c.name for c in results}
        assert names == {"kernel.core", "kernel.events"}

    def test_categoria_runtime(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_category("runtime")
        names = {c.name for c in results}
        assert names == {"runtime.parser", "runtime.validator"}

    def test_categoria_application(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_category("application")
        assert len(results) == 1
        assert results[0].name == "application.cli"

    def test_categoria_plugin(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_category("plugin")
        assert len(results) == 1
        assert results[0].name == "plugin.export"

    def test_categoria_tool(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_category("tool")
        assert len(results) == 1
        assert results[0].name == "tool.audit"

    def test_categoria_sem_modulos(self) -> None:
        r = ModuleRegistry()
        r.register(ModuleContract(name="x", category="kernel", provides=("x",)))
        assert r.find_by_category("tool") == []

    def test_retorna_lista_ordenada(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_category("kernel")
        names = [c.name for c in results]
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# find_by_type()
# ---------------------------------------------------------------------------

class TestFindByType:
    def test_tipo_service(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_type("service")
        names = {c.name for c in results}
        assert names == {"kernel.core", "runtime.validator"}

    def test_tipo_library(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_type("library")
        names = {c.name for c in results}
        assert names == {"kernel.events", "runtime.parser", "plugin.export"}

    def test_tipo_command(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_type("command")
        names = {c.name for c in results}
        assert names == {"application.cli", "tool.audit"}

    def test_tipo_daemon_sem_modulos(self, registry: ModuleRegistry) -> None:
        assert registry.find_by_type("daemon") == []

    def test_retorna_lista(self, registry: ModuleRegistry) -> None:
        assert isinstance(registry.find_by_type("service"), list)


# ---------------------------------------------------------------------------
# find_by_capability()
# ---------------------------------------------------------------------------

class TestFindByCapability:
    def test_capability_existente(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_capability("parsing")
        assert len(results) == 1
        assert results[0].name == "runtime.parser"

    def test_capability_inexistente(self, registry: ModuleRegistry) -> None:
        assert registry.find_by_capability("nao_existe") == []

    def test_capability_retorna_provedor_correto(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_capability("validation")
        assert results[0].name == "runtime.validator"

    def test_retorna_lista(self, registry: ModuleRegistry) -> None:
        assert isinstance(registry.find_by_capability("core"), list)


# ---------------------------------------------------------------------------
# find_by_state()
# ---------------------------------------------------------------------------

class TestFindByState:
    def test_state_stable(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_state("stable")
        names = {c.name for c in results}
        assert names == {
            "kernel.core",
            "runtime.parser",
            "runtime.validator",
            "application.cli",
            "tool.audit",
        }

    def test_state_experimental(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_state("experimental")
        assert len(results) == 1
        assert results[0].name == "kernel.events"

    def test_state_deprecated(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_state("deprecated")
        assert len(results) == 1
        assert results[0].name == "plugin.export"

    def test_state_archived_sem_modulos(self, registry: ModuleRegistry) -> None:
        assert registry.find_by_state("archived") == []

    def test_retorna_lista_ordenada(self, registry: ModuleRegistry) -> None:
        results = registry.find_by_state("stable")
        names = [c.name for c in results]
        assert names == sorted(names)


# ---------------------------------------------------------------------------
# dependency_graph()
# ---------------------------------------------------------------------------

class TestDependencyGraph:
    def test_grafo_contem_todos_modulos(self, registry: ModuleRegistry) -> None:
        graph = registry.dependency_graph()
        assert set(graph.keys()) == {
            "kernel.core",
            "kernel.events",
            "runtime.parser",
            "runtime.validator",
            "application.cli",
            "plugin.export",
            "tool.audit",
        }

    def test_modulo_sem_deps_tem_lista_vazia(self, registry: ModuleRegistry) -> None:
        graph = registry.dependency_graph()
        assert graph["kernel.core"] == []
        assert graph["runtime.parser"] == []

    def test_modulo_com_uma_dep(self, registry: ModuleRegistry) -> None:
        graph = registry.dependency_graph()
        assert graph["kernel.events"] == ["kernel.core"]
        assert graph["runtime.validator"] == ["runtime.parser"]

    def test_modulo_com_multiplas_deps(self, registry: ModuleRegistry) -> None:
        graph = registry.dependency_graph()
        # application.cli requer parsing e validation
        assert graph["application.cli"] == ["runtime.parser", "runtime.validator"]

    def test_deps_ordenadas_alfabeticamente(self, registry: ModuleRegistry) -> None:
        graph = registry.dependency_graph()
        for deps in graph.values():
            assert deps == sorted(deps)

    def test_grafo_registry_vazio(self) -> None:
        r = ModuleRegistry()
        assert r.dependency_graph() == {}

    def test_retorna_dict(self, registry: ModuleRegistry) -> None:
        assert isinstance(registry.dependency_graph(), dict)


# ---------------------------------------------------------------------------
# health()
# ---------------------------------------------------------------------------

class TestHealth:
    def test_registry_saudavel(self, registry: ModuleRegistry) -> None:
        h = registry.health()
        assert h["healthy"] is True
        assert h["missing_dependencies"] == []
        assert h["circular_dependencies"] == []

    def test_health_total_modules(self, registry: ModuleRegistry) -> None:
        h = registry.health()
        assert h["total_modules"] == 7

    def test_health_detecta_deprecated(self, registry: ModuleRegistry) -> None:
        h = registry.health()
        assert "plugin.export" in h["deprecated_modules"]

    def test_health_dependencia_ausente(self) -> None:
        r = ModuleRegistry()
        r.register(ModuleContract(name="a", provides=("a",), requires=("x",)))
        h = r.health()
        assert h["healthy"] is False
        assert len(h["missing_dependencies"]) == 1
        assert "x" in h["missing_dependencies"][0]

    def test_health_retorna_dict(self, registry: ModuleRegistry) -> None:
        h = registry.health()
        assert isinstance(h, dict)
        for chave in ("healthy", "total_modules", "missing_dependencies",
                      "circular_dependencies", "deprecated_modules"):
            assert chave in h

    def test_health_registry_vazio(self) -> None:
        h = ModuleRegistry().health()
        assert h["healthy"] is True
        assert h["total_modules"] == 0
        assert h["deprecated_modules"] == []


# ---------------------------------------------------------------------------
# stats()
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_total_modules(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        assert s["total_modules"] == 7

    def test_stats_total_capabilities(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        # Cada módulo declara exatamente 1 capability → total = 7
        assert s["total_capabilities"] == 7

    def test_stats_por_categoria(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        assert s["by_category_kernel"] == 2
        assert s["by_category_runtime"] == 2
        assert s["by_category_application"] == 1
        assert s["by_category_plugin"] == 1
        assert s["by_category_tool"] == 1

    def test_stats_por_tipo(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        assert s["by_type_service"] == 2
        assert s["by_type_library"] == 3
        assert s["by_type_command"] == 2
        assert s["by_type_daemon"] == 0

    def test_stats_por_state(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        assert s["by_state_stable"] == 5
        assert s["by_state_experimental"] == 1
        assert s["by_state_deprecated"] == 1
        assert s["by_state_archived"] == 0

    def test_stats_soma_categorias_igual_total(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        soma = (
            s["by_category_kernel"]
            + s["by_category_runtime"]
            + s["by_category_application"]
            + s["by_category_plugin"]
            + s["by_category_tool"]
        )
        assert soma == s["total_modules"]

    def test_stats_soma_tipos_igual_total(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        soma = (
            s["by_type_service"]
            + s["by_type_library"]
            + s["by_type_command"]
            + s["by_type_daemon"]
        )
        assert soma == s["total_modules"]

    def test_stats_soma_states_igual_total(self, registry: ModuleRegistry) -> None:
        s = registry.stats()
        soma = (
            s["by_state_stable"]
            + s["by_state_experimental"]
            + s["by_state_deprecated"]
            + s["by_state_archived"]
        )
        assert soma == s["total_modules"]

    def test_stats_registry_vazio(self) -> None:
        s = ModuleRegistry().stats()
        assert s["total_modules"] == 0
        assert s["total_capabilities"] == 0

    def test_stats_retorna_dict(self, registry: ModuleRegistry) -> None:
        assert isinstance(registry.stats(), dict)

    def test_stats_todos_valores_sao_int(self, registry: ModuleRegistry) -> None:
        for v in registry.stats().values():
            assert isinstance(v, int)


# ---------------------------------------------------------------------------
# Compatibilidade retroativa — operações existentes
# ---------------------------------------------------------------------------

class TestRetrocompatibilidade:
    """Garante que as consultas novas não quebraram as existentes."""

    def test_register_e_get(self, registry: ModuleRegistry) -> None:
        contract = registry.get("runtime.parser")
        assert contract.name == "runtime.parser"

    def test_provider_for(self, registry: ModuleRegistry) -> None:
        contract = registry.provider_for("parsing")
        assert contract.name == "runtime.parser"

    def test_validate_sem_erro(self, registry: ModuleRegistry) -> None:
        registry.validate()  # não deve levantar

    def test_resolve_order_retorna_ordem_topologica(
        self, registry: ModuleRegistry
    ) -> None:
        ordered = registry.resolve_order()
        names = [c.name for c in ordered]
        # kernel.core deve vir antes de kernel.events
        assert names.index("kernel.core") < names.index("kernel.events")
        # runtime.parser deve vir antes de runtime.validator
        assert names.index("runtime.parser") < names.index("runtime.validator")

    def test_contracts_retorna_tuple_ordenada(self, registry: ModuleRegistry) -> None:
        contracts = registry.contracts()
        assert isinstance(contracts, tuple)
        names = [c.name for c in contracts]
        assert names == sorted(names)
