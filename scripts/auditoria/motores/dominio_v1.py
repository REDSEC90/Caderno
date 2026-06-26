"""
Motor Domínio v1
Verifica se cada entidade possui contrato, template, especificação e esquema.
Usa BASELINE_V1 para resolução de caminhos reais.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

from models_v1 import AuditResult, MotorResult, Status, Severidade
from config_v1 import ROOT, BASELINE_V1, ENTIDADES, CATALOGOS


def executar() -> MotorResult:
    resultado = MotorResult(nome="Domínio")

    for entidade in ENTIDADES:
        for artefato in ("especificacao", "contrato", "template", "esquema"):
            chave = f"{artefato}-{entidade}"
            if chave not in BASELINE_V1:
                continue
            caminho = BASELINE_V1[chave]
            existe = caminho.exists()
            resultado.resultados.append(AuditResult(
                id="DOM-001", motor="Domínio",
                titulo=f"{entidade}/{artefato}: {'presente' if existe else 'AUSENTE'}",
                status=Status.PASS if existe else Status.FAIL,
                severidade=Severidade.INFO if existe else Severidade.ALTA,
                evidencias=[str(caminho.relative_to(ROOT))],
                sugestoes=[] if existe else [f"Criar: {caminho.relative_to(ROOT)}"],
            ))

    # Catálogo de estados consolidado
    estados = BASELINE_V1["estados-todas-entidades"]
    existe = estados.exists()
    resultado.resultados.append(AuditResult(
        id="DOM-002", motor="Domínio",
        titulo=f"Catálogo de estados: {'presente' if existe else 'AUSENTE'}",
        status=Status.PASS if existe else Status.FAIL,
        severidade=Severidade.INFO if existe else Severidade.ALTA,
        evidencias=[str(estados.relative_to(ROOT))],
    ))

    # Mapa de relacionamentos
    mapa = BASELINE_V1["mapa-relacionamentos"]
    existe = mapa.exists()
    resultado.resultados.append(AuditResult(
        id="DOM-003", motor="Domínio",
        titulo=f"Mapa de relacionamentos: {'presente' if existe else 'AUSENTE'}",
        status=Status.PASS if existe else Status.FAIL,
        severidade=Severidade.INFO if existe else Severidade.ALTA,
        evidencias=[str(mapa.relative_to(ROOT))],
    ))

    return resultado
