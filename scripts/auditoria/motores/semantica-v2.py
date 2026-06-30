"""
Motor 8 — Semântica v2
Corrige B-02: contador de entradas do glossário usa headers ## em vez de pares de **
Corrige B-03: remoção da seção de termos proibidos usa próximo ## como delimitador real
"""

import re
from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT

TERMOS_PROIBIDOS = ["deletar", "excluir", "gerenciador de receitas", "salvar", " usuário"]
TERMOS_OBRIGATORIOS = [
    "Ingrediente", "Técnica", "Equipamento", "Receita",
    "Execução", "Observação", "Experimento",
    "Registro", "Entidade", "Identificador", "Esquema", "Template",
]

_PROX_SECAO_RE = re.compile(r"\n## ", re.MULTILINE)


def _texto_fora_da_secao_proibida(texto: str, titulo_secao: str) -> str:
    """B-03: remove a seção inteira até o próximo ##, não apenas 500 chars."""
    idx_inicio = texto.find(titulo_secao)
    if idx_inicio == -1:
        return texto
    match_fim = _PROX_SECAO_RE.search(texto, idx_inicio + len(titulo_secao))
    idx_fim = match_fim.start() if match_fim else len(texto)
    return texto[:idx_inicio] + texto[idx_fim:]


def _contar_entradas_glossario(texto: str) -> int:
    """B-02: conta headers ## em vez de pares de **."""
    return len(re.findall(r"^## .+", texto, re.MULTILINE))


def executar() -> MotorResult:
    resultado = MotorResult(nome="Semântica")

    linguagem = DOCS / "01-dominio" / "linguagem-soe-ccg-v1.md"
    glossario = DOCS / "00-projeto" / "glossario-v1.md"

    if linguagem.exists():
        texto = linguagem.read_text(encoding="utf-8")
        for termo in TERMOS_OBRIGATORIOS:
            presente = termo in texto
            resultado.resultados.append(AuditResult(
                id="SEM-001", motor="Semântica",
                titulo=f"Termo '{termo}' {'presente' if presente else 'AUSENTE'} na linguagem oficial",
                status=Status.PASS if presente else Status.FAIL,
                severidade=Severidade.INFO if presente else Severidade.ALTA,
                evidencias=[str(linguagem.relative_to(ROOT))],
            ))

        texto_fora = _texto_fora_da_secao_proibida(texto, "## 2. Termos Proibidos")
        for termo in TERMOS_PROIBIDOS:
            if termo.lower() in texto_fora.lower():
                resultado.resultados.append(AuditResult(
                    id="SEM-002", motor="Semântica",
                    titulo=f"Termo proibido '{termo}' fora da seção de proibição",
                    status=Status.WARN, severidade=Severidade.MEDIA,
                    evidencias=[str(linguagem.relative_to(ROOT))],
                    sugestoes=["Substituir pelo termo canônico do domínio"],
                ))
    else:
        resultado.resultados.append(AuditResult(
            id="SEM-003", motor="Semântica",
            titulo=f"Documento de linguagem oficial ausente: {linguagem.relative_to(ROOT)}",
            status=Status.FAIL, severidade=Severidade.CRITICA,
            sugestoes=[f"Criar {linguagem.relative_to(ROOT)}"],
        ))

    if glossario.exists():
        texto_gloss = glossario.read_text(encoding="utf-8")
        entradas = _contar_entradas_glossario(texto_gloss)
        status = Status.PASS if entradas >= 15 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="SEM-004", motor="Semântica",
            titulo=f"Glossário: {entradas} entradas encontradas",
            status=status, severidade=Severidade.INFO,
            evidencias=[str(glossario.relative_to(ROOT))],
            sugestoes=[] if status == Status.PASS else ["Glossário com menos de 15 entradas"],
        ))
    else:
        resultado.resultados.append(AuditResult(
            id="SEM-005", motor="Semântica",
            titulo=f"Glossário ausente: {glossario.relative_to(ROOT)}",
            status=Status.FAIL, severidade=Severidade.ALTA,
            sugestoes=[f"Criar {glossario.relative_to(ROOT)}"],
        ))

    return resultado
