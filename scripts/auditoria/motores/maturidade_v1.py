"""
Motor Maturidade v1
Pontua cada camada arquitetural usando BASELINE_V1 (caminhos reais com sufixo de versão).
"""

from models_v1 import AuditResult, MotorResult, Status, Severidade
from config_v1 import BASELINE_V1, GRUPOS_BASELINE, LIMIAR_APROVACAO, PREFIXOS, ROOT


def _camada(id_audit, nome, chaves, resultado):
    itens = [(k, BASELINE_V1[k].exists()) for k in chaves if k in BASELINE_V1]
    presentes = sum(1 for _, e in itens if e)
    total = len(itens)
    pct = round(presentes / total * 100, 1) if total else 0.0
    limiar = LIMIAR_APROVACAO.get(nome, 80)
    st = Status.PASS if pct >= limiar else (Status.WARN if pct >= limiar * 0.7 else Status.FAIL)
    sev = Severidade.INFO if st == Status.PASS else (Severidade.MEDIA if st == Status.WARN else Severidade.ALTA)
    ausentes = [k for k, e in itens if not e]
    resultado.resultados.append(AuditResult(
        id=id_audit, motor="Maturidade",
        titulo=f"{nome}: {pct:.0f}% ({presentes}/{total})",
        status=st, severidade=sev,
        evidencias=[f"Presentes: {presentes}/{total}"],
        sugestoes=[f"Ausente: {a} → {BASELINE_V1[a].relative_to(ROOT)}" for a in ausentes],
    ))
    return pct


def executar() -> MotorResult:
    resultado = MotorResult(nome="Maturidade")
    pontuacoes = {}

    mapeamento = [
        ("MAT-001", "fundacao",              GRUPOS_BASELINE["fundacao"]),
        ("MAT-002", "arquitetura",            GRUPOS_BASELINE["arquitetura"]),
        ("MAT-003", "dominio_especificacoes", GRUPOS_BASELINE["dominio_especificacoes"]),
        ("MAT-004", "dominio_contratos",      GRUPOS_BASELINE["dominio_contratos"]),
        ("MAT-005", "dominio_templates",      GRUPOS_BASELINE["dominio_templates"]),
        ("MAT-006", "dominio_esquemas",       GRUPOS_BASELINE["dominio_esquemas"]),
        ("MAT-007", "governanca",             GRUPOS_BASELINE["governanca"]),
        ("MAT-008", "modelagem",              GRUPOS_BASELINE["modelagem"]),
        ("MAT-009", "linguagem_dominio",      GRUPOS_BASELINE["linguagem_dominio"]),
    ]
    for id_audit, nome, chaves in mapeamento:
        pontuacoes[nome] = _camada(id_audit, nome, chaves, resultado)

    # Dados canônicos — avalia diretamente (não está no BASELINE)
    com_dados = sum(1 for d in PREFIXOS.values() if d.exists() and any(d.glob("*.md")))
    pct_dados = round(com_dados / len(PREFIXOS) * 100, 1)
    st = Status.PASS if pct_dados >= 80 else (Status.WARN if pct_dados >= 50 else Status.FAIL)
    resultado.resultados.append(AuditResult(
        id="MAT-010", motor="Maturidade",
        titulo=f"dados_canonicos: {pct_dados:.0f}% ({com_dados}/{len(PREFIXOS)} entidades populadas)",
        status=st, severidade=Severidade.INFO if st == Status.PASS else Severidade.MEDIA,
    ))
    pontuacoes["dados_canonicos"] = pct_dados

    media = round(sum(pontuacoes.values()) / len(pontuacoes), 1)
    st_geral = Status.PASS if media >= 80 else (Status.WARN if media >= 50 else Status.FAIL)
    resultado.resultados.append(AuditResult(
        id="MAT-011", motor="Maturidade",
        titulo=f"Pontuação geral de maturidade: {media:.1f}%",
        status=st_geral, severidade=Severidade.INFO,
        evidencias=[f"{k}: {v:.0f}%" for k, v in pontuacoes.items()],
    ))

    return resultado
