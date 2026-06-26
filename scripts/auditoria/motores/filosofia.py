"""
Motor 2 — Filosofia
Verifica presença e completude dos documentos filosóficos fundacionais.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT

AXIOMAS = ["Axioma 1", "Axioma 2", "Axioma 3", "Axioma 4", "Axioma 5"]
LEIS    = [f"Lei {i}" for i in range(1, 11)]  # "Lei 1" … "Lei 10" não estão no doc — usamos numeração
PRINCIPIOS_MINIMO = 8


def _verificar_secoes(path, secoes_esperadas, id_resultado, motor_nome, resultado):
    if not path.exists():
        resultado.resultados.append(AuditResult(
            id=id_resultado, motor=motor_nome,
            titulo=f"Arquivo ausente: {path.relative_to(ROOT)}",
            status=Status.FAIL, severidade=Severidade.CRITICA,
        ))
        return
    texto = path.read_text(encoding="utf-8")
    for secao in secoes_esperadas:
        status = Status.PASS if secao in texto else Status.FAIL
        sev    = Severidade.INFO if status == Status.PASS else Severidade.ALTA
        resultado.resultados.append(AuditResult(
            id=id_resultado, motor=motor_nome,
            titulo=f"{'Presente' if status == Status.PASS else 'Ausente'}: '{secao}' em {path.name}",
            status=status, severidade=sev,
            evidencias=[str(path.relative_to(ROOT))],
        ))


def executar() -> MotorResult:
    resultado = MotorResult(nome="Filosofia")

    # Axiomas em filosofia.md
    _verificar_secoes(
        DOCS / "00-projeto" / "filosofia.md",
        AXIOMAS, "FIL-001", "Filosofia", resultado,
    )

    # Leis em constituicao.md (verifica pela numeração no texto)
    constituicao = DOCS / "00-projeto" / "constituicao.md"
    if constituicao.exists():
        texto = constituicao.read_text(encoding="utf-8")
        leis_encontradas = sum(1 for i in range(1, 11) if f"{i}." in texto or f"Lei {i}" in texto)
        status = Status.PASS if leis_encontradas >= 10 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="FIL-002", motor="Filosofia",
            titulo=f"Constituição: {leis_encontradas}/10 leis encontradas",
            status=status, severidade=Severidade.INFO if status == Status.PASS else Severidade.MEDIA,
            evidencias=["docs/00-projeto/constituicao.md"],
        ))

    # Princípios
    principios = DOCS / "00-projeto" / "principios.md"
    if principios.exists():
        texto = principios.read_text(encoding="utf-8")
        count = texto.count("\n## ")
        status = Status.PASS if count >= PRINCIPIOS_MINIMO else Status.WARN
        resultado.resultados.append(AuditResult(
            id="FIL-003", motor="Filosofia",
            titulo=f"Princípios: {count} seções encontradas (mínimo {PRINCIPIOS_MINIMO})",
            status=status, severidade=Severidade.INFO if status == Status.PASS else Severidade.BAIXA,
        ))

    # Glossário existe e tem conteúdo
    glossario = DOCS / "00-projeto" / "glossario.md"
    if glossario.exists():
        linhas = len(glossario.read_text(encoding="utf-8").splitlines())
        status = Status.PASS if linhas > 20 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="FIL-004", motor="Filosofia",
            titulo=f"Glossário: {linhas} linhas",
            status=status, severidade=Severidade.INFO,
            evidencias=["docs/00-projeto/glossario.md"],
        ))

    return resultado
