"""Doctor: agregador de health checks e diagnósticos do Kernel."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class DiagnosticReport:
    """Relatório completo de diagnóstico do Kernel."""

    kernel_state: str
    registry_health: dict[str, Any]
    registry_stats: dict[str, int]
    services_health: dict[str, dict[str, Any]]
    services_stats: dict[str, int]
    events_stats: dict[str, int]
    issues: list[str] = field(default_factory=list)

    @property
    def healthy(self) -> bool:
        """Retorna True se não há problemas críticos."""
        return len(self.issues) == 0

    @property
    def summary(self) -> str:
        """Retorna resumo textual do diagnóstico."""
        if self.healthy:
            return "✅ Kernel: saudável"
        return f"⚠️ Kernel: {len(self.issues)} problema(s) detectado(s)"


def run_diagnostics(kernel) -> DiagnosticReport:
    """Executa diagnóstico completo do Kernel.

    Args:
        kernel: Instância de MicroKernel a ser inspecionada.

    Returns:
        DiagnosticReport com estado completo do sistema.
    """
    issues = []

    # Registry
    registry_health = kernel.registry.health()
    registry_stats = kernel.registry.stats()

    if not registry_health["healthy"]:
        # Agregar problemas detectados no registry
        issues.extend(registry_health.get("missing_dependencies", []))
        issues.extend(registry_health.get("circular_dependencies", []))
        if registry_health.get("deprecated_modules"):
            issues.append(f"{len(registry_health['deprecated_modules'])} módulo(s) deprecado(s)")

    # Services
    services_health = kernel.services.all_health()
    services_stats = kernel.services.stats()

    for service_name, health in services_health.items():
        if not health["healthy"]:
            issues.append(f"Service '{service_name}' não está saudável")

    # Events
    events_stats = kernel.events.stats()

    # Lifecycle
    kernel_state = kernel.state.value

    return DiagnosticReport(
        kernel_state=kernel_state,
        registry_health=registry_health,
        registry_stats=registry_stats,
        services_health=services_health,
        services_stats=services_stats,
        events_stats=events_stats,
        issues=issues,
    )


def print_diagnostics(report: DiagnosticReport) -> None:
    """Imprime relatório de diagnóstico formatado.

    Args:
        report: DiagnosticReport a ser impresso.
    """
    print("=" * 60)
    print("KERNEL DIAGNOSTICS REPORT")
    print("=" * 60)
    print()

    print(f"Estado do Kernel: {report.kernel_state}")
    print()

    print("Registry:")
    print(f"  - Total de módulos: {report.registry_stats['total_modules']}")
    print(f"  - Capabilities: {report.registry_stats['total_capabilities']}")
    print(f"  - Saudável: {report.registry_health['healthy']}")
    print()

    print("Serviços:")
    print(f"  - Total de serviços: {report.services_stats['total_services']}")
    print(f"  - Com health check: {report.services_stats['with_health_check']}")
    print()

    print("Eventos:")
    print(f"  - Total de handlers: {report.events_stats['total_handlers']}")
    print(f"  - Total de publicações: {report.events_stats['total_published']}")
    print()

    if report.issues:
        print("⚠️ PROBLEMAS DETECTADOS:")
        for i, issue in enumerate(report.issues, 1):
            print(f"  {i}. {issue}")
    else:
        print("✅ Nenhum problema detectado")

    print()
    print("=" * 60)


__all__ = [
    "DiagnosticReport",
    "run_diagnostics",
    "print_diagnostics",
]
