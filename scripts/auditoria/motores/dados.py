"""
Motor 6 — Dados (Conhecimento)
Percorre dados/ e verifica IDs, metadados, estados, referências e duplicidades.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, PREFIXOS, METADADOS_OBRIGATORIOS, ESTADOS_VALIDOS, ID_PATTERN, DATE_PATTERN
from utils import ler_frontmatter, listar_md


def executar() -> MotorResult:
    resultado = MotorResult(nome="Dados")
    ids_vistos: set[str] = set()

    for prefixo, diretorio in PREFIXOS.items():
        for arquivo in listar_md(diretorio):
            meta = ler_frontmatter(arquivo)
            rel  = str(arquivo.relative_to(ROOT))

            if not meta:
                resultado.resultados.append(AuditResult(
                    id="DAD-001", motor="Dados",
                    titulo=f"Sem frontmatter: {rel}",
                    status=Status.FAIL, severidade=Severidade.ALTA,
                ))
                continue

            # Metadados obrigatórios
            for campo in METADADOS_OBRIGATORIOS:
                if campo not in meta or meta[campo] in (None, ""):
                    resultado.resultados.append(AuditResult(
                        id="DAD-002", motor="Dados",
                        titulo=f"Campo obrigatório ausente/vazio '{campo}': {rel}",
                        status=Status.FAIL, severidade=Severidade.ALTA,
                        evidencias=[rel],
                    ))

            # Formato do ID
            id_val = str(meta.get("id", ""))
            if id_val:
                if not ID_PATTERN.match(id_val):
                    resultado.resultados.append(AuditResult(
                        id="DAD-003", motor="Dados",
                        titulo=f"ID inválido '{id_val}': {rel}",
                        status=Status.FAIL, severidade=Severidade.CRITICA,
                        evidencias=[rel],
                    ))
                # Prefixo correto
                elif not id_val.startswith(prefixo):
                    resultado.resultados.append(AuditResult(
                        id="DAD-004", motor="Dados",
                        titulo=f"ID com prefixo errado '{id_val}' (esperado {prefixo}-): {rel}",
                        status=Status.FAIL, severidade=Severidade.ALTA,
                        evidencias=[rel],
                    ))
                # Unicidade
                elif id_val in ids_vistos:
                    resultado.resultados.append(AuditResult(
                        id="DAD-005", motor="Dados",
                        titulo=f"ID duplicado '{id_val}': {rel}",
                        status=Status.FAIL, severidade=Severidade.CRITICA,
                        evidencias=[rel],
                    ))
                else:
                    ids_vistos.add(id_val)

            # Status válido
            tipo  = str(meta.get("tipo", ""))
            stval = str(meta.get("status", ""))
            if tipo in ESTADOS_VALIDOS and stval not in ESTADOS_VALIDOS[tipo]:
                resultado.resultados.append(AuditResult(
                    id="DAD-006", motor="Dados",
                    titulo=f"Status inválido '{stval}' para '{tipo}': {rel}",
                    status=Status.FAIL, severidade=Severidade.ALTA,
                    evidencias=[rel],
                    sugestoes=[f"Valores aceitos: {ESTADOS_VALIDOS[tipo]}"],
                ))

            # Formato de datas
            for campo_data in ("criado-em", "atualizado-em"):
                val = str(meta.get(campo_data, ""))
                if val and not DATE_PATTERN.match(val):
                    resultado.resultados.append(AuditResult(
                        id="DAD-007", motor="Dados",
                        titulo=f"Data inválida '{campo_data}={val}': {rel}",
                        status=Status.FAIL, severidade=Severidade.MEDIA,
                        evidencias=[rel],
                    ))

    return resultado
