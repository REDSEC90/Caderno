"""FAA v2 — Configuração central"""
import sys
from pathlib import Path
from dataclasses import dataclass
import re

_PROJECT_ROOT_FOR_IMPORT = Path(__file__).resolve().parents[2]
if str(_PROJECT_ROOT_FOR_IMPORT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT_FOR_IMPORT))

from kernel.shared.paths import ROOT

@dataclass
class FAAConfig:
    root: Path = ROOT
    
    # Diretórios críticos
    dirs_required = [
        "docs/00-projeto",
        "docs/01-dominio", 
        "docs/02-arquitetura",
        "docs/03-especificacoes",
        "docs/04-padroes",
        "dados",
        "banco_de_dados"
    ]
    
    # Arquivos fundacionais
    critical_files = [
        "docs/00-projeto/constituicao-v1.md",
        "docs/00-projeto/filosofia-v1.md",
        "docs/00-projeto/principios-v1.md",
        "docs/01-dominio/glossario-v1.md"
    ]
    
    # Padrões
    id_pattern = re.compile(r"^[A-Z]{3}-\d{6}$")
    versioned_pattern = re.compile(r"-v\d+\.md$")
    
    # Estado
    state_path: Path = ROOT / "docs/99-referencias/faa-state.json"
    snapshot_dir: Path = ROOT / "docs/99-referencias/snapshots"

CONFIG = FAAConfig()
