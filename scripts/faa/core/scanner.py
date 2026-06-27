"""Scanner de arquivos do sistema"""
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
import re

@dataclass
class FileNode:
    path: Path
    relative: str
    category: str
    is_versioned: bool
    has_frontmatter: bool = False
    
def scan_tree(root: Path) -> List[FileNode]:
    """Escaneia árvore completa do projeto"""
    nodes = []
    
    for path in root.rglob("*"):
        if path.is_file() and not _ignore(path):
            nodes.append(_classify(path, root))
    
    return nodes

def _ignore(path: Path) -> bool:
    """Ignora arquivos de sistema"""
    ignore = {".git", "__pycache__", "node_modules", ".venv", ".kiro"}
    return any(p in ignore for p in path.parts)

def _classify(path: Path, root: Path) -> FileNode:
    """Classifica arquivo por categoria"""
    rel = str(path.relative_to(root))
    
    # Classificação por caminho
    if "docs/" in rel:
        cat = "documentation"
    elif "dados/" in rel:
        cat = "data"
    elif "banco_de_dados/" in rel:
        cat = "schema"
    elif "scripts/" in rel:
        cat = "automation"
    else:
        cat = "other"
    
    versioned = bool(re.search(r"-v\d+\.(md|sql)$", path.name))
    has_fm = path.suffix == ".md" and _has_frontmatter(path)
    
    return FileNode(path, rel, cat, versioned, has_fm)

def _has_frontmatter(path: Path) -> bool:
    """Detecta frontmatter YAML"""
    try:
        text = path.read_text(encoding="utf-8")
        return text.startswith("---\n")
    except:
        return False
