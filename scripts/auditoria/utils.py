"""Utilitários compartilhados entre motores."""

from pathlib import Path
import frontmatter


def ler_frontmatter(path: Path) -> dict:
    """Lê e retorna o frontmatter YAML de um arquivo Markdown. Retorna {} em caso de erro."""
    try:
        post = frontmatter.load(str(path))
        return dict(post.metadata)
    except Exception:
        return {}


def listar_md(diretorio: Path) -> list[Path]:
    """Lista todos os arquivos .md em um diretório (não recursivo)."""
    if not diretorio.exists():
        return []
    return sorted(diretorio.glob("*.md"))


def extrair_ids_referenciados(metadata: dict) -> list[str]:
    """Extrai todos os valores que parecem IDs (padrão PREFIXO-NNNNNN) de um frontmatter."""
    import re
    from config import ID_PATTERN
    ids = []
    for valor in metadata.values():
        if isinstance(valor, str) and ID_PATTERN.match(valor):
            ids.append(valor)
        elif isinstance(valor, list):
            for item in valor:
                if isinstance(item, str) and ID_PATTERN.match(item):
                    ids.append(item)
    return ids
