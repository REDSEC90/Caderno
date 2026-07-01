"""
Motor Baseline v1 — Decisão Arquitetural
========================================
Compara o estado real do sistema contra a BASELINE_V1 (ground truth oficial).
É o único motor que emite APROVADO / REPROVADO com contexto global.

Lógica:
  - Para cada grupo de artefatos, calcula % de presença.
  - Compara com LIMIAR_APROVACAO do grupo.
  - Sistema APROVADO somente se TODOS os grupos atingem seu limiar.
"""

from models_v1 import AuditResult, MotorResult, Status, Severidade, DecisaoArquitetural
from config_v1 import ROOT, BASELINE_V1, GRUPOS_BASELINE, LIMIAR_APROVACAO


def executar() -> MotorResult:
    resultado = MotorResult(nome="Baseline")
    pontuacoes_grupos: dict[str, float] = {}
    grupos_reprovados: list[str] = []
    ausentes: list[str] = []

    for grupo, chaves in GRUPOS_BASELINE.items():
        presentes = [k for k in chaves if BASELINE_V1[k].exists()]
        faltando  = [k for k in chaves if not BASELINE_V1[k].exists()]
        ausentes.extend(faltando)

        pct = round(len(presentes) / len(chaves) * 100, 1) if chaves else 100.0
        limiar = LIMIAR_APROVACAO.get(grupo, 100)
        pontuacoes_grupos[grupo] = pct

        if pct >= limiar:
            st, sev = Status.PASS, Severidade.INFO
        elif pct >= limiar * 0.7:
            st, sev = Status.WARN, Severidade.MEDIA
            grupos_reprovados.append(grupo)
        else:
            st, sev = Status.FAIL, Severidade.ALTA
            grupos_reprovados.append(grupo)

        resultado.resultados.append(AuditResult(
            id="BAS-001", motor="Baseline",
            titulo=f"Grupo '{grupo}': {pct:.0f}% ({len(presentes)}/{len(chaves)}) — limiar {limiar}%",
            status=st, severidade=sev,
            evidencias=[f"Presente: {k}" for k in presentes],
            sugestoes=[f"Ausente: {k} → {BASELINE_V1[k].relative_to(ROOT)}" for k in faltando],
        ))

    total = len(BASELINE_V1)
    presentes_total = sum(1 for p in BASELINE_V1.values() if p.exists())
    pct_geral = round(presentes_total / total * 100, 1)
    aprovado = len(grupos_reprovados) == 0

    # Veredicto global
    resultado.resultados.append(AuditResult(
        id="BAS-002", motor="Baseline",
        titulo=(
            f"SISTEMA {'APROVADO' if aprovado else 'REPROVADO'} — "
            f"Cobertura baseline: {presentes_total}/{total} ({pct_geral:.0f}%)"
        ),
        status=Status.PASS if aprovado else Status.FAIL,
        severidade=Severidade.INFO if aprovado else Severidade.CRITICA,
        evidencias=[f"{k}: {v:.0f}%" for k, v in pontuacoes_grupos.items()],
        sugestoes=(
            []
            if aprovado
            else [f"Grupo bloqueante: {g}" for g in grupos_reprovados]
               + [f"Criar: {BASELINE_V1[a].relative_to(ROOT)}" for a in ausentes]
        ),
    ))

    # Armazena decisão no MotorResult para uso pelo agregador
    resultado._decisao = DecisaoArquitetural(
        aprovado=aprovado,
        pontuacao_geral=pct_geral,
        grupos=pontuacoes_grupos,
        grupos_reprovados=grupos_reprovados,
        artefatos_ausentes=ausentes,
        artefatos_presentes=presentes_total,
        artefatos_total=total,
    )

    return resultado
