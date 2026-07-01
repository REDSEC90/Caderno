"""Utilitários compartilhados — FAA v1."""

from pathlib import Path
import frontmatter


def ler_frontmatter(path: Path) -> dict:
    try:
        post = frontmatter.load(str(path))
        return dict(post.metadata)
    except Exception:
        return {}


def listar_md(diretorio: Path) -> list[Path]:
    if not diretorio.exists():
        return []
    return sorted(diretorio.glob("*.md"))


def extrair_ids_referenciados(metadata: dict, id_pattern) -> list[str]:
    ids = []
    for valor in metadata.values():
        if isinstance(valor, str) and id_pattern.match(valor):
            ids.append(valor)
        elif isinstance(valor, list):
            for item in valor:
                if isinstance(item, str) and id_pattern.match(item):
                    ids.append(item)
    return ids
