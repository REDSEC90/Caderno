"""
Motor 6 — Dados v2
Corrige B-01: registra PASS explícito por arquivo válido e resumo final,
eliminando o falso-negativo "SEM DADOS" quando todos os registros são corretos.
Corrige B-07: datas aceitas como type date nativo do yaml (python-frontmatter).
"""

from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, PREFIXOS, METADADOS_OBRIGATORIOS, ESTADOS_VALIDOS, ID_PATTERN, DATE_PATTERN
from utils import ler_frontmatter, listar_md


def executar() -> MotorResult:
    resultado = MotorResult(nome="Dados")
    ids_vistos: set[str] = set()
    total_arquivos = 0
    total_validos = 0

    for prefixo, diretorio in PREFIXOS.items():
        for arquivo in listar_md(diretorio):
            total_arquivos += 1
            arquivo_valido = True
            meta = ler_frontmatter(arquivo)
            rel  = str(arquivo.relative_to(ROOT))

            if not meta:
                resultado.resultados.append(AuditResult(
                    id="DAD-001", motor="Dados",
                    titulo=f"Sem frontmatter: {rel}",
                    status=Status.FAIL, severidade=Severidade.ALTA,
                ))
                arquivo_valido = False
                continue

            for campo in METADADOS_OBRIGATORIOS:
                if campo not in meta or meta[campo] in (None, ""):
                    resultado.resultados.append(AuditResult(
                        id="DAD-002", motor="Dados",
                        titulo=f"Campo obrigatório ausente/vazio '{campo}': {rel}",
                        status=Status.FAIL, severidade=Severidade.ALTA,
                        evidencias=[rel],
                    ))
                    arquivo_valido = False

            id_val = str(meta.get("id", ""))
            if id_val:
                if not ID_PATTERN.match(id_val):
                    resultado.resultados.append(AuditResult(
                        id="DAD-003", motor="Dados",
                        titulo=f"ID inválido '{id_val}': {rel}",
                        status=Status.FAIL, severidade=Severidade.CRITICA,
                        evidencias=[rel],
                    ))
                    arquivo_valido = False
                elif not id_val.startswith(prefixo):
                    resultado.resultados.append(AuditResult(
                        id="DAD-004", motor="Dados",
                        titulo=f"ID com prefixo errado '{id_val}' (esperado {prefixo}-): {rel}",
                        status=Status.FAIL, severidade=Severidade.ALTA,
                        evidencias=[rel],
                    ))
                    arquivo_valido = False
                elif id_val in ids_vistos:
                    resultado.resultados.append(AuditResult(
                        id="DAD-005", motor="Dados",
                        titulo=f"ID duplicado '{id_val}': {rel}",
                        status=Status.FAIL, severidade=Severidade.CRITICA,
                        evidencias=[rel],
                    ))
                    arquivo_valido = False
                else:
                    ids_vistos.add(id_val)

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
                arquivo_valido = False

            for campo_data in ("criado-em", "atualizado-em"):
                val = meta.get(campo_data)
                val_str = str(val) if val is not None else ""
                if val_str and not DATE_PATTERN.match(val_str):
                    resultado.resultados.append(AuditResult(
                        id="DAD-007", motor="Dados",
                        titulo=f"Data inválida '{campo_data}={val_str}': {rel}",
                        status=Status.FAIL, severidade=Severidade.MEDIA,
                        evidencias=[rel],
                    ))
                    arquivo_valido = False

            if arquivo_valido:
                total_validos += 1
                resultado.resultados.append(AuditResult(
                    id="DAD-OK", motor="Dados",
                    titulo=f"Registro válido: {arquivo.name}",
                    status=Status.PASS, severidade=Severidade.INFO,
                    evidencias=[rel],
                ))

    resultado.resultados.append(AuditResult(
        id="DAD-SUM", motor="Dados",
        titulo=f"Resumo: {total_validos}/{total_arquivos} registros válidos",
        status=Status.PASS if total_validos == total_arquivos else Status.WARN,
        severidade=Severidade.INFO,
        evidencias=[f"IDs únicos: {len(ids_vistos)}"],
    ))

    return resultado
