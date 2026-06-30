"""
Relatórios do FAA v1 — console e Markdown.
Exibe veredicto de baseline (APROVADO/REPROVADO) como decisão arquitetural central.
"""

from datetime import datetime
from models_v1 import AuditResult, MotorResult, Status
from config_v1 import ROOT, DOCS

_ICONE = {Status.PASS: "✅", Status.WARN: "⚠️ ", Status.FAIL: "❌"}
_COR   = {Status.PASS: "\033[92m", Status.WARN: "\033[93m", Status.FAIL: "\033[91m"}
_RESET = "\033[0m"


def _barra(motor: MotorResult) -> str:
    nome = motor.nome.ljust(20, ".")
    if not motor.resultados:
        return f"  {nome} SEM DADOS"
    f, a, pct = len(motor.falhas), len(motor.avisos), motor.pontuacao
    if f:
        tag = f"{_COR[Status.FAIL]}{f} falha(s){_RESET}"
    elif a:
        tag = f"{_COR[Status.WARN]}{a} aviso(s){_RESET}"
    else:
        tag = f"{_COR[Status.PASS]}OK{_RESET}"
    return f"  {nome} {tag}  ({pct:.1f}%)"


def imprimir_console(motores: list[MotorResult], pontuacao_geral: float) -> None:
    print()
    print("=" * 56)
    print("  SOE-CCG — Framework de Auditoria Arquitetural v1")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 56)
    print()

    for motor in motores:
        print(_barra(motor))

    print()
    cor_pct = _COR[Status.PASS] if pontuacao_geral >= 80 else _COR[Status.WARN]
    print(f"  Pontuação geral: {cor_pct}{pontuacao_geral:.1f}%{_RESET}")

    # Exibe decisão arquitetural do motor de baseline se disponível
    baseline_motor = next((m for m in motores if m.nome == "Baseline"), None)
    if baseline_motor and hasattr(baseline_motor, "_decisao"):
        d = baseline_motor._decisao
        cor = _COR[Status.PASS] if d.aprovado else _COR[Status.FAIL]
        veredicto = "APROVADO" if d.aprovado else "REPROVADO"
        print(f"  Decisão arquitetural: {cor}{veredicto}{_RESET}")
        print(f"  Baseline: {d.artefatos_presentes}/{d.artefatos_total} artefatos ({d.pontuacao_geral:.0f}%)")
        if d.grupos_reprovados:
            print(f"  Grupos bloqueantes: {', '.join(d.grupos_reprovados)}")
    else:
        total_falhas = sum(len(m.falhas) for m in motores)
        cor = _COR[Status.PASS] if total_falhas == 0 else _COR[Status.FAIL]
        print(f"  Sistema {cor}{'APROVADO' if total_falhas == 0 else 'REPROVADO'}{_RESET}")

    total_pass   = sum(sum(1 for r in m.resultados if r.status == Status.PASS) for m in motores)
    total_avisos = sum(len(m.avisos) for m in motores)
    total_falhas = sum(len(m.falhas) for m in motores)
    print()
    print(f"  ✅ {total_pass} verificações passaram")
    print(f"  ⚠️  {total_avisos} avisos")
    print(f"  ❌ {total_falhas} falhas")
    print()

    if total_falhas > 0 or total_avisos > 0:
        print("  Detalhes:")
        for motor in motores:
            for r in motor.resultados:
                if r.status != Status.PASS:
                    print(f"    {_ICONE[r.status]} [{r.id}] {r.titulo}")
                    for s in r.sugestoes:
                        print(f"         → {s}")
        print()


def gerar_markdown(motores: list[MotorResult], pontuacao_geral: float) -> None:
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_falhas = sum(len(m.falhas) for m in motores)
    total_avisos = sum(len(m.avisos) for m in motores)
    total_pass   = sum(sum(1 for r in m.resultados if r.status == Status.PASS) for m in motores)

    baseline_motor = next((m for m in motores if m.nome == "Baseline"), None)
    decisao = getattr(baseline_motor, "_decisao", None)
    status_geral = "✅ APROVADO" if (decisao.aprovado if decisao else total_falhas == 0) else "❌ REPROVADO"

    linhas = [
        "# Relatório de Auditoria Arquitetural — FAA v1",
        "",
        f"**Data:** {agora}  ",
        f"**Pontuação geral:** {pontuacao_geral:.1f}%  ",
        f"**Decisão arquitetural:** {status_geral}  ",
    ]

    if decisao:
        linhas += [
            f"**Baseline:** {decisao.artefatos_presentes}/{decisao.artefatos_total} artefatos ({decisao.pontuacao_geral:.0f}%)  ",
            "",
            "## Grupos de Maturidade",
            "",
            "| Grupo | % | Status |",
            "|-------|---|--------|",
        ]
        limiar_map = __import__("config_v1", fromlist=["LIMIAR_APROVACAO"]).LIMIAR_APROVACAO
        for grupo, pct in decisao.grupos.items():
            limiar = limiar_map.get(grupo, 80)
            icone = "✅" if pct >= limiar else ("⚠️" if pct >= limiar * 0.7 else "❌")
            linhas.append(f"| {grupo} | {pct:.0f}% | {icone} |")
        linhas.append("")

    linhas += [
        "## Resumo por Motor",
        "",
        "| Motor | Pontuação | Falhas | Avisos |",
        "|-------|-----------|--------|--------|",
    ]
    for motor in motores:
        linhas.append(f"| {motor.nome} | {motor.pontuacao:.1f}% | {len(motor.falhas)} | {len(motor.avisos)} |")

    linhas += [
        "",
        f"**Total:** {total_pass} ✅ · {total_avisos} ⚠️ · {total_falhas} ❌",
        "",
    ]

    for motor in motores:
        problemas = [r for r in motor.resultados if r.status != Status.PASS]
        if not problemas:
            continue
        linhas += [f"## {motor.nome}", ""]
        for r in problemas:
            linhas.append(f"- {_ICONE[r.status]} **[{r.id}]** {r.titulo}")
            for e in r.evidencias:
                linhas.append(f"  - Evidência: `{e}`")
            for s in r.sugestoes:
                linhas.append(f"  - Sugestão: {s}")
        linhas.append("")

    destino = DOCS / "99-referencias" / f"auditoria-v1-{datetime.now().strftime('%Y-%m-%d')}.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  Relatório salvo em: {destino.relative_to(ROOT)}")
