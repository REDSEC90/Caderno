"""Testes de integração — queries avançadas no ModuleRegistry.

Cobre: find_by_capability, find_by_category, find_by_type,
dependency_graph, health, stats, find_all e contracts().
"""
from __future__ import annotations

import pytest

from kernel.contracts.module import ModuleContract
from kernel.core.kernel import MicroKernel
from kernel.registry.module_registry import ModuleRegistry, RegistryError


# ---------------------------------------------------------------------------
# Helpers e fixtures
# ---------------------------------------------------------------------------

def _make(
    name: str,
    provides: tuple[str, ...] | None = None,
    requires: tuple[str, ...] = (),
    category: str = "runtime",
    module_type: str = "library",
    state: str = "stable",
) -> ModuleContract:
    cap = provides if provides is not None else (name.replace(".", "_"),)
    return ModuleContract(
        name=name,
        provides=cap,
        requires=requires,
        category=category,  # type: ignore[arg-type]
        type=module_type,   # type: ignore[arg-type]
        state=state,        # type: ignore[arg-type]
    )


def _build_registry() -> ModuleRegistry:
    """Registry com conjunto diversificado para testes de integração."""
    r = ModuleRegistry()
    r.register(_make("kernel.core",  provides=("core",),       category="kernel",  module_type="service"))
    r.register(_make("kernel.events", provides=("events",),    category="kernel",  module_type="library",  requires=("core",)))
    r.register(_make("runtime.parser",  provides=("parsing",), category="runtime", module_type="library"))
    r.register(_make("runtime.validator", provides=("validation",), category="runtime", module_type="service", requires=("parsing",)))
    r.register(_make("application.cli",   provides=("cli",),   category="application", module_type="command", requires=("parsing", "validation")))
    r.register(_make("plugin.export",     provides=("export",),category="plugin",  module_type="library", state="deprecated"))
    r.register(_make("tool.audit",        provides=("audit",), category="tool",    module_type="command", requires=("parsing", "validation")))
    r.register(_make("runtime.daemon",    provides=("daemon_svc",), category="runtime", module_type="daemon"))
    return r


# ---------------------------------------------------------------------------
# Teste 1 — find_by_capability()
# ---------------------------------------------------------------------------

class TestFindByCapability:
    def test_find_by_capability_retorna_provedor(self) -> None:
        r = _build_registry()
        results = r.find_by_capability("parsing")
        assert len(results) == 1
        assert results[0].name == "runtime.parser"

    def test_find_by_capability_core(self) -> None:
        r = _build_registry()
        results = r.find_by_capability("core")
        assert results[0].name == "kernel.core"

    def test_find_by_capability_inexistente_retorna_vazio(self) -> None:
        r = _build_registry()
        assert r.find_by_capability("nao_existe") == []

    def test_find_by_capability_retorna_lista(self) -> None:
        r = _build_registry()
        assert isinstance(r.find_by_capability("cli"), list)

    def test_find_by_capability_daemon(self) -> None:
        r = _build_registry()
        results = r.find_by_capability("daemon_svc")
        assert results[0].name == "runtime.daemon"

    def test_find_by_capability_registry_vazio(self) -> None:
        r = ModuleRegistry()
        assert r.find_by_capability("qualquer") == []


# ---------------------------------------------------------------------------
# Teste 2 — find_by_category()
# ---------------------------------------------------------------------------

class TestFindByCategory:
    def test_find_by_category_kernel(self) -> None:
        r = _build_registry()
        nomes = {c.name for c in r.find_by_category("kernel")}
        assert nomes == {"kernel.core", "kernel.events"}

    def test_find_by_category_runtime(self) -> None:
        r = _build_registry()
        nomes = {c.name for c in r.find_by_category("runtime")}
        assert nomes == {"runtime.parser", "runtime.validator", "runtime.daemon"}

    def test_find_by_category_application(self) -> None:
        r = _build_registry()
        results = r.find_by_category("application")
        assert len(results) == 1
        assert results[0].name == "application.cli"

    def test_find_by_category_plugin(self) -> None:
        r = _build_registry()
        results = r.find_by_category("plugin")
        assert results[0].name == "plugin.export"

    def test_find_by_category_tool(self) -> None:
        r = _build_registry()
        results = r.find_by_category("tool")
        assert results[0].name == "tool.audit"

    def test_find_by_category_sem_modulos_retorna_vazio(self) -> None:
        r = ModuleRegistry()
        r.register(_make("mod.a", category="kernel"))
        assert r.find_by_category("plugin") == []

    def test_find_by_category_retorna_lista_ordenada(self) -> None:
        r = _build_registry()
        results = r.find_by_category("runtime")
        nomes = [c.name for c in results]
        assert nomes == sorted(nomes)


# ---------------------------------------------------------------------------
# Teste 3 — find_by_type()
# ---------------------------------------------------------------------------

class TestFindByType:
    def test_find_by_type_service(self) -> None:
        r = _build_registry()
        nomes = {c.name for c in r.find_by_type("service")}
        assert nomes == {"kernel.core", "runtime.validator"}

    def test_find_by_type_library(self) -> None:
        r = _build_registry()
        nomes = {c.name for c in r.find_by_type("library")}
        assert nomes == {"kernel.events", "runtime.parser", "plugin.export"}

    def test_find_by_type_command(self) -> None:
        r = _build_registry()
        nomes = {c.name for c in r.find_by_type("command")}
        assert nomes == {"application.cli", "tool.audit"}

    def test_find_by_type_daemon(self) -> None:
        r = _build_registry()
        results = r.find_by_type("daemon")
        assert len(results) == 1
        assert results[0].name == "runtime.daemon"

    def test_find_by_type_retorna_lista(self) -> None:
        r = _build_registry()
        assert isinstance(r.find_by_type("library"), list)

    def test_find_by_type_soma_total_modulos(self) -> None:
        r = _build_registry()
        total = (
            len(r.find_by_type("service"))
            + len(r.find_by_type("library"))
            + len(r.find_by_type("command"))
            + len(r.find_by_type("daemon"))
        )
        assert total == r.stats()["total_modules"]


# ---------------------------------------------------------------------------
# Teste 4 — dependency_graph()
# ---------------------------------------------------------------------------

class TestDependencyGraph:
    def test_dependency_graph_contem_todos_modulos(self) -> None:
        r = _build_registry()
        graph = r.dependency_graph()
        nomes_reg = {c.name for c in r.contracts()}
        assert set(graph.keys()) == nomes_reg

    def test_modulo_sem_deps_tem_lista_vazia(self) -> None:
        r = _build_registry()
        graph = r.dependency_graph()
        assert graph["kernel.core"] == []
        assert graph["runtime.parser"] == []

    def test_modulo_com_uma_dep(self) -> None:
        r = _build_registry()
        graph = r.dependency_graph()
        # kernel.events requer "core" → provido por kernel.core
        assert graph["kernel.events"] == ["kernel.core"]

    def test_modulo_com_multiplas_deps(self) -> None:
        r = _build_registry()
        graph = r.dependency_graph()
        # application.cli requer parsing + validation
        deps = graph["application.cli"]
        assert "runtime.parser" in deps
        assert "runtime.validator" in deps

    def test_dependency_graph_deps_ordenadas(self) -> None:
        r = _build_registry()
        graph = r.dependency_graph()
        for deps in graph.values():
            assert deps == sorted(deps)

    def test_dependency_graph_registry_vazio(self) -> None:
        r = ModuleRegistry()
        assert r.dependency_graph() == {}

    def test_dependency_graph_retorna_dict(self) -> None:
        r = _build_registry()
        assert isinstance(r.dependency_graph(), dict)


# ---------------------------------------------------------------------------
# Teste 5 — health() detecta dependência ausente
# ---------------------------------------------------------------------------

class TestHealth:
    def test_health_registry_completo_e_saudavel(self) -> None:
        r = _build_registry()
        h = r.health()
        assert h["healthy"] is True
        assert h["missing_dependencies"] == []

    def test_health_detecta_dependencia_ausente(self) -> None:
        r = ModuleRegistry()
        r.register(ModuleContract(name="mod.dep", provides=("dep",), requires=("cap_inexistente",)))
        h = r.health()
        assert h["healthy"] is False
        assert len(h["missing_dependencies"]) >= 1
        assert any("cap_inexistente" in msg for msg in h["missing_dependencies"])

    def test_health_total_modules_correto(self) -> None:
        r = _build_registry()
        h = r.health()
        assert h["total_modules"] == 8  # 8 módulos no _build_registry

    def test_health_detecta_deprecated(self) -> None:
        r = _build_registry()
        h = r.health()
        assert "plugin.export" in h["deprecated_modules"]

    def test_health_chaves_obrigatorias(self) -> None:
        r = _build_registry()
        h = r.health()
        for chave in ("healthy", "total_modules", "missing_dependencies",
                      "circular_dependencies", "deprecated_modules"):
            assert chave in h

    def test_health_registry_vazio_e_saudavel(self) -> None:
        r = ModuleRegistry()
        h = r.health()
        assert h["healthy"] is True
        assert h["total_modules"] == 0

    def test_health_multiplas_deps_ausentes(self) -> None:
        r = ModuleRegistry()
        r.register(ModuleContract(name="mod.a", provides=("a",), requires=("x", "y")))
        h = r.health()
        assert h["healthy"] is False
        assert len(h["missing_dependencies"]) == 2


# ---------------------------------------------------------------------------
# Teste 6 — stats() contagens por category/type/state
# ---------------------------------------------------------------------------

class TestStats:
    def test_stats_total_modules(self) -> None:
        r = _build_registry()
        assert r.stats()["total_modules"] == 8

    def test_stats_por_categoria(self) -> None:
        r = _build_registry()
        s = r.stats()
        assert s["by_category_kernel"] == 2
        assert s["by_category_runtime"] == 3
        assert s["by_category_application"] == 1
        assert s["by_category_plugin"] == 1
        assert s["by_category_tool"] == 1

    def test_stats_por_tipo(self) -> None:
        r = _build_registry()
        s = r.stats()
        assert s["by_type_service"] == 2
        assert s["by_type_library"] == 3
        assert s["by_type_command"] == 2
        assert s["by_type_daemon"] == 1

    def test_stats_por_state(self) -> None:
        r = _build_registry()
        s = r.stats()
        assert s["by_state_stable"] == 7
        assert s["by_state_deprecated"] == 1
        assert s["by_state_experimental"] == 0
        assert s["by_state_archived"] == 0

    def test_stats_soma_categorias_igual_total(self) -> None:
        r = _build_registry()
        s = r.stats()
        soma = (s["by_category_kernel"] + s["by_category_runtime"]
                + s["by_category_application"] + s["by_category_plugin"]
                + s["by_category_tool"])
        assert soma == s["total_modules"]

    def test_stats_soma_tipos_igual_total(self) -> None:
        r = _build_registry()
        s = r.stats()
        soma = (s["by_type_service"] + s["by_type_library"]
                + s["by_type_command"] + s["by_type_daemon"])
        assert soma == s["total_modules"]

    def test_stats_soma_states_igual_total(self) -> None:
        r = _build_registry()
        s = r.stats()
        soma = (s["by_state_stable"] + s["by_state_experimental"]
                + s["by_state_deprecated"] + s["by_state_archived"])
        assert soma == s["total_modules"]

    def test_stats_todos_valores_sao_int(self) -> None:
        r = _build_registry()
        for v in r.stats().values():
            assert isinstance(v, int)


# ---------------------------------------------------------------------------
# Teste 7 — find_all (find com .*) e contracts()
# ---------------------------------------------------------------------------

class TestFindAllContracts:
    def test_find_all_retorna_todos_modulos(self) -> None:
        r = _build_registry()
        todos = r.find(r".*")
        assert len(todos) == 8

    def test_find_all_retorna_lista_ordenada(self) -> None:
        r = _build_registry()
        todos = r.find(r".*")
        nomes = [c.name for c in todos]
        assert nomes == sorted(nomes)

    def test_contracts_retorna_tuple_ordenada(self) -> None:
        r = _build_registry()
        contratos = r.contracts()
        assert isinstance(contratos, tuple)
        nomes = [c.name for c in contratos]
        assert nomes == sorted(nomes)

    def test_contracts_contem_todos_registrados(self) -> None:
        r = _build_registry()
        nomes_contratos = {c.name for c in r.contracts()}
        nomes_find = {c.name for c in r.find(r".*")}
        assert nomes_contratos == nomes_find

    def test_registrar_multiplos_e_verificar_find_all(self) -> None:
        r = ModuleRegistry()
        for i in range(5):
            r.register(ModuleContract(name=f"mod.m{i}", provides=(f"cap_{i}",)))
        todos = r.find(r".*")
        assert len(todos) == 5

    def test_find_por_prefixo_runtime(self) -> None:
        r = _build_registry()
        results = r.find(r"^runtime\.")
        nomes = {c.name for c in results}
        assert nomes == {"runtime.parser", "runtime.validator", "runtime.daemon"}

    def test_find_por_prefixo_kernel(self) -> None:
        r = _build_registry()
        results = r.find(r"^kernel\.")
        nomes = {c.name for c in results}
        assert nomes == {"kernel.core", "kernel.events"}
