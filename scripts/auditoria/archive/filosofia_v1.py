"""
Motor Filosofia v1
Verifica presença e completude dos documentos filosóficos fundacionais.
Usa BASELINE_V1 para resolução de caminhos.
"""

from models_v1 import AuditResult, MotorResult, Status, Severidade
from config_v1 import ROOT, BASELINE_V1

AXIOMAS     = ["Axioma 1", "Axioma 2", "Axioma 3", "Axioma 4", "Axioma 5"]
MIN_PRINCIPIOS = 8


def executar() -> MotorResult:
    resultado = MotorResult(nome="Filosofia")

    filosofia = BASELINE_V1["filosofia"]
    if not filosofia.exists():
        resultado.resultados.append(AuditResult(
            id="FIL-001", motor="Filosofia",
            titulo=f"Arquivo ausente: {filosofia.relative_to(ROOT)}",
            status=Status.FAIL, severidade=Severidade.CRITICA,
        ))
        return resultado

    texto = filosofia.read_text(encoding="utf-8")
    for axioma in AXIOMAS:
        presente = axioma in texto
        resultado.resultados.append(AuditResult(
            id="FIL-001", motor="Filosofia",
            titulo=f"{'Presente' if presente else 'Ausente'}: '{axioma}' em {filosofia.name}",
            status=Status.PASS if presente else Status.FAIL,
            severidade=Severidade.INFO if presente else Severidade.ALTA,
            evidencias=[str(filosofia.relative_to(ROOT))],
        ))

    constituicao = BASELINE_V1["constituicao"]
    if constituicao.exists():
        texto_c = constituicao.read_text(encoding="utf-8")
        leis = sum(1 for i in range(1, 11) if f"Lei {i}" in texto_c or f"{i}." in texto_c)
        st = Status.PASS if leis >= 10 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="FIL-002", motor="Filosofia",
            titulo=f"Constituição: {leis}/10 leis encontradas",
            status=st, severidade=Severidade.INFO if st == Status.PASS else Severidade.MEDIA,
            evidencias=[str(constituicao.relative_to(ROOT))],
        ))

    principios = BASELINE_V1["principios"]
    if principios.exists():
        count = principios.read_text(encoding="utf-8").count("\n## ")
        st = Status.PASS if count >= MIN_PRINCIPIOS else Status.WARN
        resultado.resultados.append(AuditResult(
            id="FIL-003", motor="Filosofia",
            titulo=f"Princípios: {count} seções (mínimo {MIN_PRINCIPIOS})",
            status=st, severidade=Severidade.INFO if st == Status.PASS else Severidade.BAIXA,
            evidencias=[str(principios.relative_to(ROOT))],
        ))

    glossario = BASELINE_V1["glossario"]
    if glossario.exists():
        linhas = len(glossario.read_text(encoding="utf-8").splitlines())
        st = Status.PASS if linhas > 20 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="FIL-004", motor="Filosofia",
            titulo=f"Glossário: {linhas} linhas",
            status=st, severidade=Severidade.INFO,
            evidencias=[str(glossario.relative_to(ROOT))],
        ))

    return resultado
