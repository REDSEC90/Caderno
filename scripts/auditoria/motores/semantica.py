"""
Motor 8 — Semântica
Verifica se termos-chave do domínio têm definição consistente (presença no glossário e linguagem).
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

from models import AuditResult, MotorResult, Status, Severidade
from config import DOCS, ROOT

TERMOS_PROIBIDOS = ["deletar", "excluir", "gerenciador de receitas", "salvar", " usuário"]
TERMOS_OBRIGATORIOS = [
    "Ingrediente", "Técnica", "Equipamento", "Receita",
    "Execução", "Observação", "Experimento",
    "Registro", "Entidade", "Identificador", "Esquema", "Template",
]


def executar() -> MotorResult:
    resultado = MotorResult(nome="Semântica")

    linguagem = DOCS / "01-dominio" / "linguagem-soe-ccg.md"
    glossario = DOCS / "00-projeto" / "glossario.md"

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
                evidencias=["docs/01-dominio/linguagem-soe-ccg.md"],
            ))

        # Termos proibidos não aparecem fora de sua seção de proibição
        secao_proibidos = "## 2. Termos Proibidos"
        idx = texto.find(secao_proibidos)
        texto_fora = texto[:idx] + texto[idx + 500:] if idx > -1 else texto

        for termo in TERMOS_PROIBIDOS:
            if termo.lower() in texto_fora.lower():
                resultado.resultados.append(AuditResult(
                    id="SEM-002", motor="Semântica",
                    titulo=f"Termo proibido '{termo}' encontrado fora da seção de proibição",
                    status=Status.WARN, severidade=Severidade.MEDIA,
                    evidencias=["docs/01-dominio/linguagem-soe-ccg.md"],
                    sugestoes=["Verificar uso e substituir pelo termo correto"],
                ))
    else:
        resultado.resultados.append(AuditResult(
            id="SEM-003", motor="Semântica",
            titulo="Documento de linguagem oficial ausente",
            status=Status.FAIL, severidade=Severidade.CRITICA,
            sugestoes=["Criar docs/01-dominio/linguagem-soe-ccg.md"],
        ))

    # Glossário tem entradas suficientes?
    if glossario.exists():
        linhas = glossario.read_text(encoding="utf-8")
        entradas = linhas.count("**")  // 2  # cada entrada tem bold abertura + fechamento
        status = Status.PASS if entradas >= 20 else Status.WARN
        resultado.resultados.append(AuditResult(
            id="SEM-004", motor="Semântica",
            titulo=f"Glossário: ~{entradas} entradas encontradas",
            status=status, severidade=Severidade.INFO,
            evidencias=["docs/00-projeto/glossario.md"],
        ))

    return resultado
