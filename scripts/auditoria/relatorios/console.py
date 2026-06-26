"""
Módulo de relatórios do FAA.
Gera saída no terminal (console) e relatório Markdown em docs/99-referencias/.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

from datetime import datetime
from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, DOCS

_ICONE = {Status.PASS: "✅", Status.WARN: "⚠️ ", Status.FAIL: "❌"}
_COR   = {Status.PASS: "\033[92m", Status.WARN: "\033[93m", Status.FAIL: "\033[91m"}
_RESET = "\033[0m"


def _barra_status(motor: MotorResult) -> str:
    nome = motor.nome.ljust(20, ".")
    if not motor.resultados:
        return f"  {nome} SEM DADOS"
    falhas  = len(motor.falhas)
    avisos  = len(motor.avisos)
    pct     = motor.pontuacao
    if falhas:
        tag = f"{_COR[Status.FAIL]}{falhas} falha(s){_RESET}"
    elif avisos:
        tag = f"{_COR[Status.WARN]}{avisos} aviso(s){_RESET}"
    else:
        tag = f"{_COR[Status.PASS]}OK{_RESET}"
    return f"  {nome} {tag}  ({pct:.1f}%)"


def imprimir_console(motores: list[MotorResult], pontuacao_geral: float) -> None:
    print()
    print("=" * 50)
    print("  SOE Architectural Audit — FAA")
    print(f"  Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 50)
    print()

    for motor in motores:
        print(_barra_status(motor))

    print()
    print(f"  Pontuação geral: {_COR[Status.PASS] if pontuacao_geral >= 80 else _COR[Status.WARN]}{pontuacao_geral:.1f}%{_RESET}")

    total_falhas  = sum(len(m.falhas)  for m in motores)
    total_avisos  = sum(len(m.avisos)  for m in motores)
    total_pass    = sum(sum(1 for r in m.resultados if r.status == Status.PASS) for m in motores)

    status_geral = "APROVADO" if total_falhas == 0 else "REPROVADO"
    cor = _COR[Status.PASS] if total_falhas == 0 else _COR[Status.FAIL]
    print(f"  Sistema {cor}{status_geral}{_RESET}")
    print()
    print(f"  ✅ {total_pass} verificações passaram")
    print(f"  ⚠️  {total_avisos} avisos")
    print(f"  ❌ {total_falhas} falhas críticas")
    print()

    if total_falhas > 0 or total_avisos > 0:
        print("  Detalhes:")
        for motor in motores:
            problemas = [r for r in motor.resultados if r.status != Status.PASS]
            for r in problemas:
                icone = _ICONE[r.status]
                print(f"    {icone} [{r.id}] {r.titulo}")
                for s in r.sugestoes:
                    print(f"         → {s}")
        print()


def gerar_markdown(motores: list[MotorResult], pontuacao_geral: float) -> None:
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_falhas = sum(len(m.falhas) for m in motores)
    total_avisos = sum(len(m.avisos) for m in motores)
    total_pass   = sum(sum(1 for r in m.resultados if r.status == Status.PASS) for m in motores)
    status_geral = "✅ APROVADO" if total_falhas == 0 else "❌ REPROVADO"

    linhas = [
        f"# Relatório de Auditoria Arquitetural — FAA",
        f"",
        f"**Data:** {agora}  ",
        f"**Pontuação geral:** {pontuacao_geral:.1f}%  ",
        f"**Status:** {status_geral}  ",
        f"",
        f"| Motor | Pontuação | Falhas | Avisos |",
        f"|-------|-----------|--------|--------|",
    ]
    for motor in motores:
        linhas.append(
            f"| {motor.nome} | {motor.pontuacao:.1f}% | {len(motor.falhas)} | {len(motor.avisos)} |"
        )

    linhas += [
        f"",
        f"**Total:** {total_pass} ✅ · {total_avisos} ⚠️ · {total_falhas} ❌",
        f"",
    ]

    for motor in motores:
        problemas = [r for r in motor.resultados if r.status != Status.PASS]
        if not problemas:
            continue
        linhas.append(f"## {motor.nome}")
        linhas.append("")
        for r in problemas:
            icone = _ICONE[r.status]
            linhas.append(f"- {icone} **[{r.id}]** {r.titulo}")
            for e in r.evidencias:
                linhas.append(f"  - Evidência: `{e}`")
            for s in r.sugestoes:
                linhas.append(f"  - Sugestão: {s}")
        linhas.append("")

    destino = DOCS / "99-referencias" / f"auditoria-{datetime.now().strftime('%Y-%m-%d')}.md"
    destino.write_text("\n".join(linhas), encoding="utf-8")
    print(f"  Relatório salvo em: {destino.relative_to(ROOT)}")
