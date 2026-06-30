"""
Motor Semântica v1
Usa BASELINE_V1 para resolver caminhos da linguagem e glossário.
"""

from models_v1 import AuditResult, MotorResult, Status, Severidade
from config_v1 import ROOT, BASELINE_V1

TERMOS_PROIBIDOS = ["deletar", "excluir", "gerenciador de receitas", "salvar", " usuário"]
TERMOS_OBRIGATORIOS = [
    "Ingrediente", "Técnica", "Equipamento", "Receita",
    "Execução", "Observação", "Experimento",
    "Registro", "Entidade", "Identificador", "Esquema", "Template",
]


def executar() -> MotorResult:
    resultado = MotorResult(nome="Semântica")

    linguagem = BASELINE_V1["linguagem"]
    glossario = BASELINE_V1["glossario"]

    if linguagem.exists():
        texto = linguagem.read_text(encoding="utf-8")
        for termo in TERMOS_OBRIGATORIOS:
            presente = termo in texto
            resultado.resultados.append(AuditResult(
                id="SEM-001", motor="Semântica",
                titulo=f"Termo '{termo}' {'definido' if presente else 'AUSENTE'} na linguagem oficial",
                status=Status.PASS if presente else Status.FAIL,
                severidade=Severidade.INFO if presente else Severidade.ALTA,
                evidencias=[str(linguagem.relative_to(ROOT))],
            ))
        idx = texto.find("## 2. Termos Proibidos")
        if idx > -1:
            prox = texto.find("\n## ", idx + 1)
            fim = prox if prox > -1 else len(texto)
            texto_fora = texto[:idx] + texto[fim:]
        else:
            texto_fora = texto
        for termo in TERMOS_PROIBIDOS:
            if termo.lower() in texto_fora.lower():
                resultado.resultados.append(AuditResult(
                    id="SEM-002", motor="Semântica",
                    titulo=f"Termo proibido '{termo}' encontrado fora da seção de proibição",
                    status=Status.WARN, severidade=Severidade.MEDIA,
                    evidencias=[str(linguagem.relative_to(ROOT))],
                    sugestoes=["Substituir pelo termo correto"],
                ))
    else:
        resultado.resultados.append(AuditResult(
            id="SEM-003", motor="Semântica",
            titulo=f"Documento de linguagem oficial ausente: {linguagem.relative_to(ROOT)}",
            status=Status.FAIL, severidade=Severidade.CRITICA,
            sugestoes=[f"Criar {linguagem.relative_to(ROOT)}"],
        ))

    if glossario.exists():
        entradas = sum(1 for l in glossario.read_text(encoding="utf-8").splitlines() if l.startswith("## "))
        st = Status.PASS if entradas >= 20 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="SEM-004", motor="Semântica",
            titulo=f"Glossário: ~{entradas} entradas",
            status=st, severidade=Severidade.INFO,
            evidencias=[str(glossario.relative_to(ROOT))],
        ))

    return resultado
