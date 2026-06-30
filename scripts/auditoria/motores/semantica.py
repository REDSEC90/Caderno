"""
Motor 8 — Semântica
Verifica se termos-chave do domínio têm definição consistente (presença no glossário e linguagem).
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


def _sem_secao_termos_proibidos(texto: str) -> str:
    return re.sub(
        r"(?ms)^## 2\. Termos Proibidos.*?(?=^## \d+\.|\Z)",
        "",
        texto,
    )


def executar() -> MotorResult:
    resultado = MotorResult(nome="Semântica")

    linguagem = DOCS / "01-dominio" / "linguagem-soe-ccg-v1.md"
    glossario = DOCS / "00-projeto" / "glossario-v1.md"

    # Todos os termos obrigatórios definidos na linguagem oficial?
    if linguagem.exists():
        texto = linguagem.read_text(encoding="utf-8")
        for termo in TERMOS_OBRIGATORIOS:
            presente = termo in texto
            resultado.resultados.append(AuditResult(
                id="SEM-001", motor="Semântica",
                titulo=f"Termo '{termo}' definido na linguagem oficial",
                status=Status.PASS if presente else Status.FAIL,
                severidade=Severidade.INFO if presente else Severidade.ALTA,
                evidencias=["docs/01-dominio/linguagem-soe-ccg-v1.md"],
            ))

        # Termos proibidos não aparecem fora de sua seção de proibição.
        texto_fora = _sem_secao_termos_proibidos(texto)

        for termo in TERMOS_PROIBIDOS:
            if termo.lower() in texto_fora.lower():
                resultado.resultados.append(AuditResult(
                    id="SEM-002", motor="Semântica",
                    titulo=f"Termo proibido '{termo}' encontrado fora da seção de proibição",
                    status=Status.WARN, severidade=Severidade.MEDIA,
                    evidencias=["docs/01-dominio/linguagem-soe-ccg-v1.md"],
                    sugestoes=["Verificar uso e substituir pelo termo correto"],
                ))
    else:
        resultado.resultados.append(AuditResult(
            id="SEM-003", motor="Semântica",
            titulo="Documento de linguagem oficial ausente",
            status=Status.FAIL, severidade=Severidade.CRITICA,
            sugestoes=["Criar docs/01-dominio/linguagem-soe-ccg-v1.md"],
        ))

    # Glossário tem entradas suficientes?
    if glossario.exists():
        linhas = glossario.read_text(encoding="utf-8")
        entradas = len(re.findall(r"(?m)^##\s+\S+", linhas))
        status = Status.PASS if entradas >= 20 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="SEM-004", motor="Semântica",
            titulo=f"Glossário: ~{entradas} entradas encontradas",
            status=status, severidade=Severidade.INFO,
            evidencias=["docs/00-projeto/glossario-v1.md"],
        ))

    return resultado
