"""
Motor 12 — Cobertura
Mede percentual de cobertura de contratos, templates, dados canônicos e documentação.
"""

from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT, ENTIDADES, PREFIXOS

_LIMIARES = {"critico": 60, "aviso": 80}


def _pct(encontrados: int, esperados: int) -> float:
    return (encontrados / esperados * 100) if esperados else 0.0


def _resultado_cobertura(id_audit, motor, titulo, encontrados, esperados, resultado):
    pct = _pct(encontrados, esperados)
    status = (
        Status.PASS if pct >= _LIMIARES["aviso"] else
        Status.WARN if pct >= _LIMIARES["critico"] else
        Status.FAIL
    )
    sev = Severidade.INFO if status == Status.PASS else (
        Severidade.MEDIA if status == Status.WARN else Severidade.ALTA
    )
    resultado.resultados.append(AuditResult(
        id=id_audit, motor=motor,
        titulo=f"{titulo}: {encontrados}/{esperados} ({pct:.0f}%)",
        status=status, severidade=sev,
    ))


def executar() -> MotorResult:
    resultado = MotorResult(nome="Cobertura")
    total = len(ENTIDADES)

    contratos = sum(
        1 for e in ENTIDADES
        if (DOCS / "01-dominio" / "contratos" / f"contrato-{e}-v1.md").exists()
    )
    _resultado_cobertura("COB-001", "Cobertura", "Contratos", contratos, total, resultado)

    templates = sum(
        1 for e in ENTIDADES
        if (DOCS / "01-dominio" / "templates" / f"{e}-v1.md").exists()
    )
    _resultado_cobertura("COB-002", "Cobertura", "Templates", templates, total, resultado)

    specs = sum(
        1 for e in ENTIDADES
        if (DOCS / "01-dominio" / f"especificacao-{e}-v1.md").exists()
    )
    _resultado_cobertura("COB-003", "Cobertura", "Especificações", specs, total, resultado)

    esquemas = sum(
        1 for e in ENTIDADES
        if (DOCS / "01-dominio" / "esquemas" / f"esquema-{e}-v1.md").exists()
    )
    _resultado_cobertura("COB-004", "Cobertura", "Esquemas", esquemas, total, resultado)

    politicas_esperadas = [
        "politica-templates-v1.md", "politica-esquemas-v1.md", "politica-arquivamento-v1.md",
        "politica-revisao-v1.md", "politica-conflito-v1.md",
        "identificadores-v1.md", "versionamento-v1.md", "metadados-v1.md",
    ]
    politicas = sum(1 for p in politicas_esperadas if (DOCS / "04-padroes" / p).exists())
    _resultado_cobertura("COB-005", "Cobertura", "Políticas de governança", politicas, len(politicas_esperadas), resultado)

    com_dados = sum(1 for d in PREFIXOS.values() if any(d.glob("*.md")))
    _resultado_cobertura("COB-006", "Cobertura", "Entidades com dados canônicos", com_dados, len(PREFIXOS), resultado)

    return resultado
