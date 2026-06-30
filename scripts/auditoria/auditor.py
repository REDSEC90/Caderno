#!/usr/bin/env python3
"""
FAA — Framework de Auditoria Arquitetural do SOE-CCG
=====================================================
Nunca modifica o projeto. Apenas analisa, mede, valida e reporta.

Uso:
    python auditor.py              # auditoria completa
    python auditor.py --motor estrutura
    python auditor.py --motor integridade
    python auditor.py --relatorio  # gera relatório Markdown
"""

import sys
import argparse
from pathlib import Path

_PROJECT_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT_FOR_IMPORT))

from kernel.bootstrap import bootstrap_system
from kernel.shared.paths import SCRIPTS_AUDITORIA

bootstrap_system()

# Adapter temporário até scripts/auditoria virar pacote importável.
if str(SCRIPTS_AUDITORIA) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_AUDITORIA))

from models import MotorResult, Status
from relatorios.console import imprimir_console, gerar_markdown

# Registro de todos os motores disponíveis
from motores import (
    estrutura, filosofia, dominio, templates, contratos,
    dados, integridade, semantica, padroes, escalabilidade,
    dependencias, cobertura, maturidade,
)

MOTORES: dict[str, object] = {
    "estrutura":    estrutura,
    "filosofia":    filosofia,
    "dominio":      dominio,
    "templates":    templates,
    "contratos":    contratos,
    "dados":        dados,
    "integridade":  integridade,
    "semantica":    semantica,
    "padroes":      padroes,
    "escalabilidade": escalabilidade,
    "dependencias": dependencias,
    "cobertura":    cobertura,
    "maturidade":   maturidade,
}


def executar_motores(nomes: list[str]) -> list[MotorResult]:
    resultados = []
    for nome in nomes:
        motor = MOTORES.get(nome)
        if motor is None:
            print(f"  Motor desconhecido: {nome}")
            continue
        try:
            resultados.append(motor.executar())
        except Exception as e:
            from models import AuditResult, Severidade
            mr = MotorResult(nome=nome.capitalize())
            mr.resultados.append(AuditResult(
                id="ERR-000", motor=nome,
                titulo=f"Erro interno no motor: {e}",
                status=Status.FAIL, severidade=Severidade.CRITICA,
            ))
            resultados.append(mr)
    return resultados


def pontuacao_geral(motores: list[MotorResult]) -> float:
    if not motores:
        return 0.0
    return round(sum(m.pontuacao for m in motores) / len(motores), 1)


def main():
    parser = argparse.ArgumentParser(
        description="FAA — Framework de Auditoria Arquitetural do SOE-CCG"
    )
    parser.add_argument(
        "--motor", metavar="NOME",
        help=f"Executar apenas um motor. Disponíveis: {', '.join(MOTORES)}",
    )
    parser.add_argument(
        "--relatorio", action="store_true",
        help="Gerar relatório Markdown em docs/99-referencias/",
    )
    args = parser.parse_args()

    nomes = [args.motor] if args.motor else list(MOTORES.keys())
    resultados = executar_motores(nomes)
    pct = pontuacao_geral(resultados)

    imprimir_console(resultados, pct)

    if args.relatorio:
        gerar_markdown(resultados, pct)

    # Exit code não-zero se houver falhas (útil para CI)
    falhas = sum(len(m.falhas) for m in resultados)
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
