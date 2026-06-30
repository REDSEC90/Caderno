"""
Motor Cobertura v1
Mede percentual de cobertura por tipo de artefato usando BASELINE_V1.
"""

from models_v1 import AuditResult, MotorResult, Status, Severidade
from config_v1 import BASELINE_V1, ENTIDADES, PREFIXOS

_LIMIARES = {"critico": 60, "aviso": 80}


def _cob(id_audit, titulo, encontrados, esperados, resultado):
    pct = (encontrados / esperados * 100) if esperados else 0.0
    st = (
        Status.PASS if pct >= _LIMIARES["aviso"] else
        Status.WARN if pct >= _LIMIARES["critico"] else
        Status.FAIL
    )
    sev = Severidade.INFO if st == Status.PASS else (
        Severidade.MEDIA if st == Status.WARN else Severidade.ALTA
    )
    resultado.resultados.append(AuditResult(
        id=id_audit, motor="Cobertura",
        titulo=f"{titulo}: {encontrados}/{esperados} ({pct:.0f}%)",
        status=st, severidade=sev,
    ))


def executar() -> MotorResult:
    resultado = MotorResult(nome="Cobertura")
    n = len(ENTIDADES)

    for tipo, id_audit in [
        ("especificacao", "COB-001"),
        ("contrato",      "COB-002"),
        ("template",      "COB-003"),
        ("esquema",       "COB-004"),
    ]:
        count = sum(
            1 for e in ENTIDADES
            if BASELINE_V1.get(f"{tipo}-{e}", None) and BASELINE_V1[f"{tipo}-{e}"].exists()
        )
        _cob(id_audit, tipo.capitalize() + "s", count, n, resultado)

    governanca_chaves = [
        "politica-templates", "politica-esquemas", "politica-arquivamento",
        "politica-revisao", "politica-conflito",
        "identificadores", "versionamento", "metadados",
    ]
    gov = sum(1 for k in governanca_chaves if BASELINE_V1[k].exists())
    _cob("COB-005", "Políticas de governança", gov, len(governanca_chaves), resultado)

    com_dados = sum(1 for d in PREFIXOS.values() if d.exists() and any(d.glob("*.md")))
    _cob("COB-006", "Entidades com dados canônicos", com_dados, len(PREFIXOS), resultado)

    return resultado
