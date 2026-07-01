"""Sistema de diagnóstico e observabilidade do Kernel."""
from kernel.diagnostics.doctor import (
    DiagnosticReport,
    print_diagnostics,
    run_diagnostics,
)
from kernel.diagnostics.inspector import (
    inspect_events,
    inspect_kernel,
    inspect_registry,
    inspect_services,
)

__all__ = [
    "DiagnosticReport",
    "run_diagnostics",
    "print_diagnostics",
    "inspect_kernel",
    "inspect_registry",
    "inspect_services",
    "inspect_events",
]
