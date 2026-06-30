"""
Motor 7 — Integridade v2
Corrige B-06: varre o corpo do arquivo Markdown em busca de IDs além do frontmatter,
tornando visíveis referências em tabelas, listas e texto corrido.
"""

import re
from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, PREFIXOS, ID_PATTERN
from utils import ler_frontmatter, listar_md

_ID_CORPO_RE = re.compile(r"\b(?:REC|ING|TEC|EQP|EXE|OBS|EXP|CAT)-\d{6}\b")


def _coletar_ids_existentes() -> set[str]:
    ids: set[str] = set()
    for diretorio in PREFIXOS.values():
        for arquivo in listar_md(diretorio):
            meta = ler_frontmatter(arquivo)
            id_val = str(meta.get("id", ""))
            if ID_PATTERN.match(id_val):
                ids.add(id_val)
    return ids


def _ids_frontmatter(meta: dict) -> list[str]:
    refs = []
    for chave, valor in meta.items():
        if chave == "id":
            continue
        if isinstance(valor, str) and ID_PATTERN.match(valor):
            refs.append(valor)
        elif isinstance(valor, list):
            refs += [v for v in valor if isinstance(v, str) and ID_PATTERN.match(v)]
    return refs


def _ids_corpo(arquivo, id_proprio: str) -> list[str]:
    """B-06: extrai IDs do corpo Markdown (após o bloco frontmatter)."""
    texto = arquivo.read_text(encoding="utf-8")
    partes = texto.split("---", 2)
    corpo = partes[2] if len(partes) >= 3 else texto
    encontrados = set(_ID_CORPO_RE.findall(corpo))
    encontrados.discard(id_proprio)
    return list(encontrados)


def executar() -> MotorResult:
    resultado = MotorResult(nome="Integridade")
    existentes = _coletar_ids_existentes()
    verificadas: set[tuple[str, str]] = set()

    for diretorio in PREFIXOS.values():
        for arquivo in listar_md(diretorio):
            meta = ler_frontmatter(arquivo)
            if not meta:
                continue
            rel = str(arquivo.relative_to(ROOT))
            id_proprio = str(meta.get("id", ""))

            refs_fm   = set(_ids_frontmatter(meta))
            refs_body = set(_ids_corpo(arquivo, id_proprio))
            todas = refs_fm | refs_body

            for ref_id in todas:
                chave = (id_proprio, ref_id)
                if chave in verificadas:
                    continue
                verificadas.add(chave)
                origem = "frontmatter" if ref_id in refs_fm else "corpo"

                if ref_id in existentes:
                    resultado.resultados.append(AuditResult(
                        id="INT-001", motor="Integridade",
                        titulo=f"Referência válida '{ref_id}' em {arquivo.name} ({origem})",
                        status=Status.PASS, severidade=Severidade.INFO,
                        evidencias=[rel],
                    ))
                else:
                    resultado.resultados.append(AuditResult(
                        id="INT-002", motor="Integridade",
                        titulo=f"Referência quebrada '{ref_id}' em {arquivo.name} ({origem})",
                        status=Status.FAIL, severidade=Severidade.CRITICA,
                        evidencias=[rel],
                        sugestoes=[f"Criar registro com id: {ref_id} ou corrigir a referência"],
                    ))

    return resultado
