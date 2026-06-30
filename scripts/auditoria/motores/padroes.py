"""
Motor 9 — Padrões
Verifica nomenclatura de arquivos, encoding, formato de datas e convenções de IDs em dados/.
"""

import re
from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, PREFIXOS, ID_PATTERN
from utils import listar_md, ler_frontmatter

_NOME_DADOS = re.compile(r"^(REC|ING|TEC|EQP|EXE|OBS|EXP)-\d{6}-.+-v\d+\.md$")
_SLUG_OK    = re.compile(r"^[a-z0-9-]+$")


def executar() -> MotorResult:
    resultado = MotorResult(nome="Padrões")

    for prefixo, diretorio in PREFIXOS.items():
        for arquivo in listar_md(diretorio):
            rel = str(arquivo.relative_to(ROOT))

            # Nomenclatura do arquivo
            if not _NOME_DADOS.match(arquivo.name):
                resultado.resultados.append(AuditResult(
                    id="PAD-001", motor="Padrões",
                    titulo=f"Nome fora do padrão: {arquivo.name}",
                    status=Status.WARN, severidade=Severidade.MEDIA,
                    evidencias=[rel],
                    sugestoes=[f"Padrão: {prefixo}-NNNNNN-slug-vN.md"],
                ))
                continue

            # Slug em minúsculas e apenas hífens
            partes = arquivo.stem.split("-", 2)  # prefixo, nnnnnn, resto
            if len(partes) == 3:
                slug_versao = partes[2]  # "slug-v1"
                slug = re.sub(r"-v\d+$", "", slug_versao)
                if not _SLUG_OK.match(slug):
                    resultado.resultados.append(AuditResult(
                        id="PAD-002", motor="Padrões",
                        titulo=f"Slug com caracteres inválidos '{slug}': {arquivo.name}",
                        status=Status.WARN, severidade=Severidade.BAIXA,
                        evidencias=[rel],
                        sugestoes=["Use apenas letras minúsculas, números e hífens"],
                    ))

            # Encoding UTF-8
            try:
                arquivo.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                resultado.resultados.append(AuditResult(
                    id="PAD-003", motor="Padrões",
                    titulo=f"Encoding não é UTF-8: {arquivo.name}",
                    status=Status.FAIL, severidade=Severidade.ALTA,
                    evidencias=[rel],
                ))

            # ID no frontmatter bate com nome do arquivo
            meta = ler_frontmatter(arquivo)
            id_meta = str(meta.get("id", ""))
            id_nome = "-".join(arquivo.stem.split("-")[:2])  # ex: "REC-000001"
            if id_meta and id_nome and id_meta != id_nome:
                resultado.resultados.append(AuditResult(
                    id="PAD-004", motor="Padrões",
                    titulo=f"ID no frontmatter ('{id_meta}') difere do nome do arquivo ('{id_nome}'): {arquivo.name}",
                    status=Status.FAIL, severidade=Severidade.ALTA,
                    evidencias=[rel],
                ))

    return resultado
