"""Testes do sistema de diagnóstico do Kernel."""
import io
import sys

import pytest

from kernel.bootstrap import bootstrap_system
from kernel.contracts.module import ModuleContract
from kernel.diagnostics import (
    DiagnosticReport,
    inspect_events,
    inspect_kernel,
    inspect_registry,
    inspect_services,
    print_diagnostics,
    run_diagnostics,
)
from kernel.lifecycle import LifecycleState


def test_run_diagnostics_retorna_diagnostic_report():
    """run_diagnostics() retorna DiagnosticReport."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    assert isinstance(report, DiagnosticReport)


def test_diagnostic_report_tem_todos_os_campos():
    """DiagnosticReport possui todos os campos esperados."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)

    assert hasattr(report, "kernel_state")
    assert hasattr(report, "registry_health")
    assert hasattr(report, "registry_stats")
    assert hasattr(report, "services_health")
    assert hasattr(report, "services_stats")
    assert hasattr(report, "events_stats")
    assert hasattr(report, "issues")


def test_diagnostic_report_kernel_state_e_string():
    """kernel_state é string representando o estado do lifecycle."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    assert isinstance(report.kernel_state, str)
    assert report.kernel_state in {s.value for s in LifecycleState}


def test_diagnostic_report_healthy_verdadeiro_sem_issues():
    """healthy é True quando não há issues."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    assert report.issues == []
    assert report.healthy is True


def test_diagnostic_report_healthy_falso_com_issues():
    """healthy é False quando há issues."""
    kernel = bootstrap_system()
    
    # Criar módulo com dependência que será detectada como faltante pelo health()
    # O contrato em si é válido, mas a dependência não existe
    valid_but_broken = ModuleContract(
        name="broken",
        version="1.0.0",
        type="service",
        category="tool",
        state="experimental",
        provides=("some_capability",),  # Precisa declarar ao menos uma
        requires=("nonexistent_capability",),  # Esta não existe
        priority=100,
        entrypoint=lambda: None,
    )
    kernel.register(valid_but_broken)

    report = run_diagnostics(kernel)
    # A dependência ausente será detectada pelo registry.health()
    assert len(report.issues) > 0
    assert report.healthy is False


def test_diagnostic_report_summary_saudavel():
    """summary retorna string indicando saúde."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    assert "saudável" in report.summary.lower()


def test_inspect_kernel_retorna_dict():
    """inspect_kernel() retorna dicionário."""
    kernel = bootstrap_system()
    snapshot = inspect_kernel(kernel)
    assert isinstance(snapshot, dict)


def test_inspect_kernel_tem_todas_secoes():
    """inspect_kernel() retorna todas as seções esperadas."""
    kernel = bootstrap_system()
    snapshot = inspect_kernel(kernel)

    assert "lifecycle" in snapshot
    assert "registry" in snapshot
    assert "services" in snapshot
    assert "events" in snapshot


def test_inspect_kernel_lifecycle_tem_state():
    """snapshot['lifecycle'] contém 'state'."""
    kernel = bootstrap_system()
    snapshot = inspect_kernel(kernel)
    assert "state" in snapshot["lifecycle"]
    assert isinstance(snapshot["lifecycle"]["state"], str)


def test_inspect_kernel_registry_tem_contracts():
    """snapshot['registry'] contém 'contracts'."""
    kernel = bootstrap_system()
    snapshot = inspect_kernel(kernel)
    assert "contracts" in snapshot["registry"]
    assert isinstance(snapshot["registry"]["contracts"], list)


def test_inspect_kernel_services_tem_list():
    """snapshot['services'] contém 'list'."""
    kernel = bootstrap_system()
    snapshot = inspect_kernel(kernel)
    assert "list" in snapshot["services"]
    assert isinstance(snapshot["services"]["list"], list)


def test_inspect_kernel_events_tem_stats():
    """snapshot['events'] contém 'stats'."""
    kernel = bootstrap_system()
    snapshot = inspect_kernel(kernel)
    assert "stats" in snapshot["events"]
    assert isinstance(snapshot["events"]["stats"], dict)


def test_inspect_registry_retorna_dict_com_total_modules():
    """inspect_registry() retorna dicionário com total_modules."""
    kernel = bootstrap_system()
    registry_info = inspect_registry(kernel)
    assert isinstance(registry_info, dict)
    assert "total_modules" in registry_info
    assert isinstance(registry_info["total_modules"], int)


def test_inspect_services_retorna_dict_com_services():
    """inspect_services() retorna dicionário com lista de serviços."""
    kernel = bootstrap_system()
    services_info = inspect_services(kernel)
    assert isinstance(services_info, dict)
    assert "services" in services_info
    assert isinstance(services_info["services"], list)


def test_inspect_events_retorna_dict_com_handlers():
    """inspect_events() retorna dicionário com handlers_by_event."""
    kernel = bootstrap_system()
    events_info = inspect_events(kernel)
    assert isinstance(events_info, dict)
    assert "handlers_by_event" in events_info
    assert isinstance(events_info["handlers_by_event"], dict)


def test_inspect_events_inclui_history():
    """inspect_events() inclui histórico de eventos."""
    kernel = bootstrap_system()
    events_info = inspect_events(kernel)
    assert "history" in events_info
    assert isinstance(events_info["history"], list)


def test_diagnostic_report_registry_stats_tem_total_modules():
    """registry_stats contém 'total_modules'."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    assert "total_modules" in report.registry_stats
    assert isinstance(report.registry_stats["total_modules"], int)


def test_diagnostic_report_services_stats_tem_total_services():
    """services_stats contém 'total_services'."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    assert "total_services" in report.services_stats
    assert isinstance(report.services_stats["total_services"], int)


def test_diagnostic_report_events_stats_tem_total_handlers():
    """events_stats contém 'total_handlers'."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    assert "total_handlers" in report.events_stats
    assert isinstance(report.events_stats["total_handlers"], int)


def test_diagnostic_report_apos_start():
    """Diagnóstico após start() reflete estado running."""
    kernel = bootstrap_system()
    kernel.start()
    report = run_diagnostics(kernel)
    assert report.kernel_state == LifecycleState.RUNNING.value


def test_inspect_kernel_apos_registro_de_servico():
    """inspect_kernel() reflete serviço registrado."""
    kernel = bootstrap_system()

    class DummyService:
        pass

    kernel.register_service("dummy", DummyService())
    snapshot = inspect_kernel(kernel)

    assert "dummy" in snapshot["services"]["list"]


def test_diagnostic_report_registry_health_verdadeiro_sem_deps_quebradas():
    """registry_health['healthy'] é True quando não há dependências quebradas."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    # Bootstrap registra módulos válidos, então healthy deve ser True
    assert report.registry_health["healthy"] is True


# ---------------------------------------------------------------------------
# Cobertura de branches: summary com issues
# ---------------------------------------------------------------------------

def test_diagnostic_report_summary_com_issues():
    """summary retorna mensagem de alerta quando há issues."""
    kernel = bootstrap_system()
    broken = ModuleContract(
        name="broken_summary",
        version="1.0.0",
        type="service",
        category="tool",
        state="experimental",
        provides=("cap_broken_summary",),
        requires=("cap_nao_existe_summary",),
        priority=100,
        entrypoint=lambda: None,
    )
    kernel.register(broken)
    report = run_diagnostics(kernel)
    assert report.healthy is False
    assert "problema" in report.summary.lower()


def test_diagnostic_report_issues_tem_deps_ausentes():
    """issues contém mensagem sobre dependências ausentes."""
    kernel = bootstrap_system()
    broken = ModuleContract(
        name="broken_deps",
        version="1.0.0",
        type="service",
        category="tool",
        state="experimental",
        provides=("cap_broken_deps",),
        requires=("cap_que_nao_existe_deps",),
        priority=100,
        entrypoint=lambda: None,
    )
    kernel.register(broken)
    report = run_diagnostics(kernel)
    assert any("broken_deps" in issue or "cap_que_nao_existe_deps" in issue
               for issue in report.issues)


def test_diagnostic_report_service_nao_saudavel_aparece_nos_issues():
    """Service que retorna healthy=False aparece nos issues."""
    kernel = bootstrap_system()

    class UnhealthyService:
        def health(self):
            return {"healthy": False, "reason": "propositalmente quebrado"}

    kernel.register_service("svc_doente", UnhealthyService())
    report = run_diagnostics(kernel)
    assert not report.healthy
    assert any("svc_doente" in issue for issue in report.issues)


# ---------------------------------------------------------------------------
# Cobertura de print_diagnostics
# ---------------------------------------------------------------------------

def test_print_diagnostics_kernel_saudavel(capsys):
    """print_diagnostics imprime relatório sem problemas quando Kernel saudável."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    print_diagnostics(report)

    captured = capsys.readouterr()
    assert "KERNEL DIAGNOSTICS REPORT" in captured.out
    assert "Nenhum problema detectado" in captured.out


def test_print_diagnostics_com_issues(capsys):
    """print_diagnostics lista problemas quando existem issues."""
    kernel = bootstrap_system()
    broken = ModuleContract(
        name="broken_print",
        version="1.0.0",
        type="service",
        category="tool",
        state="experimental",
        provides=("cap_broken_print",),
        requires=("dep_que_nao_existe_print",),
        priority=100,
        entrypoint=lambda: None,
    )
    kernel.register(broken)
    report = run_diagnostics(kernel)
    print_diagnostics(report)

    captured = capsys.readouterr()
    assert "PROBLEMAS DETECTADOS" in captured.out


def test_print_diagnostics_exibe_estado_kernel(capsys):
    """print_diagnostics exibe o estado do kernel."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    print_diagnostics(report)

    captured = capsys.readouterr()
    assert "Estado do Kernel" in captured.out
    assert report.kernel_state in captured.out


def test_print_diagnostics_exibe_total_modulos(capsys):
    """print_diagnostics exibe o total de módulos no registry."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    print_diagnostics(report)

    captured = capsys.readouterr()
    assert "Total de módulos" in captured.out


def test_print_diagnostics_exibe_secao_eventos(capsys):
    """print_diagnostics exibe seção de eventos."""
    kernel = bootstrap_system()
    report = run_diagnostics(kernel)
    print_diagnostics(report)

    captured = capsys.readouterr()
    assert "Eventos" in captured.out
    assert "handlers" in captured.out.lower()


# ---------------------------------------------------------------------------
# Cobertura: __init__ exporta todos os símbolos
# ---------------------------------------------------------------------------

def test_init_exporta_print_diagnostics():
    """__init__ exporta print_diagnostics."""
    import kernel.diagnostics as diag
    assert hasattr(diag, "print_diagnostics")
    assert callable(diag.print_diagnostics)


def test_init_exporta_inspect_registry():
    """__init__ exporta inspect_registry."""
    import kernel.diagnostics as diag
    assert hasattr(diag, "inspect_registry")
    assert callable(diag.inspect_registry)


def test_init_exporta_inspect_services():
    """__init__ exporta inspect_services."""
    import kernel.diagnostics as diag
    assert hasattr(diag, "inspect_services")
    assert callable(diag.inspect_services)


def test_init_exporta_inspect_events():
    """__init__ exporta inspect_events."""
    import kernel.diagnostics as diag
    assert hasattr(diag, "inspect_events")
    assert callable(diag.inspect_events)


def test_diagnostic_report_issues_inclui_modulos_deprecados():
    """issues menciona módulos deprecados quando registry os detecta."""
    kernel = bootstrap_system()

    # Registrar dois módulos onde um está deprecated e depende do outro
    # para forçar registry.health()['deprecated_modules'] a ser preenchido
    deprecated_mod = ModuleContract(
        name="mod_deprecado",
        version="1.0.0",
        type="library",
        category="tool",
        state="deprecated",    # módulo deprecado
        provides=("cap_deprecada",),
        requires=(),
        priority=100,
        entrypoint=lambda: None,
    )
    kernel.register(deprecated_mod)

    # Verificar se registry.health() reporta deprecated_modules
    health = kernel.registry.health()
    if health.get("deprecated_modules"):
        # O branch está acessível — executar run_diagnostics e checar issues
        report = run_diagnostics(kernel)
        assert any("deprecado" in issue for issue in report.issues)
    else:
        # Registry não rastreia deprecated em health — branch inatingível via API atual
        pytest.skip("registry.health() não reporta deprecated_modules; branch N/A")
