"""
Motor 7 — Integridade Referencial
Verifica se todo ID referenciado em dados/ existe no sistema.
"""

from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, PREFIXOS, ID_PATTERN
from utils import ler_frontmatter, listar_md


def _coletar_ids_existentes() -> set[str]:
    ids: set[str] = set()
    for diretorio in PREFIXOS.values():
        for arquivo in listar_md(diretorio):
            meta = ler_frontmatter(arquivo)
            id_val = str(meta.get("id", ""))
            if ID_PATTERN.match(id_val):
                ids.add(id_val)
    return ids


def _ids_referenciados(meta: dict) -> list[str]:
    """Extrai todos os valores que parecem IDs de um frontmatter."""
    refs = []
    for chave, valor in meta.items():
        if chave == "id":
            continue
        if isinstance(valor, str) and ID_PATTERN.match(valor):
            refs.append(valor)
        elif isinstance(valor, list):
            for item in valor:
                if isinstance(item, str) and ID_PATTERN.match(item):
                    refs.append(item)
    return refs


def executar() -> MotorResult:
    resultado = MotorResult(nome="Integridade")
    existentes = _coletar_ids_existentes()

    for diretorio in PREFIXOS.values():
        for arquivo in listar_md(diretorio):
            meta = ler_frontmatter(arquivo)
            if not meta:
                continue
            rel = str(arquivo.relative_to(ROOT))

            for ref_id in _ids_referenciados(meta):
                if ref_id in existentes:
                    resultado.resultados.append(AuditResult(
                        id="INT-001", motor="Integridade",
                        titulo=f"Referência válida '{ref_id}' em {arquivo.name}",
                        status=Status.PASS, severidade=Severidade.INFO,
                        evidencias=[rel],
                    ))
                else:
                    resultado.resultados.append(AuditResult(
                        id="INT-002", motor="Integridade",
                        titulo=f"Referência quebrada '{ref_id}' em {arquivo.name}",
                        status=Status.FAIL, severidade=Severidade.CRITICA,
                        evidencias=[rel],
                        sugestoes=[f"Criar registro com id: {ref_id} ou corrigir a referência"],
                    ))

    return resultado
