"""Sistema de diagnóstico e observabilidade do Kernel."""
from kernel.diagnostics.doctor import run_diagnostics, DiagnosticReport
from kernel.diagnostics.inspector import inspect_kernel

__all__ = [
    "run_diagnostics",
    "DiagnosticReport",
    "inspect_kernel",
]
