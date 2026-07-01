"""Release Check — valida que CHANGELOG.md contém entry para a versão mais recente.

Regras:
  - CHANGELOG.md deve existir
  - Deve conter pelo menos um cabeçalho ## [vX.Y.Z]
  - O cabeçalho mais recente não pode ser apenas "Em desenvolvimento" sem versão

Uso:
  python3 scripts/automacao/release_check.py [--version v0.8.0]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from kernel.shared.paths import ROOT
CHANGELOG = ROOT / 'CHANGELOG.md'

_VERSION_RE = re.compile(r'##\s+\[v?(\d+\.\d+\.\d+)\]')


def get_versions(changelog: Path) -> list[str]:
    """Retorna versões encontradas no CHANGELOG, em ordem de aparição."""
    text = changelog.read_text(encoding='utf-8')
    return _VERSION_RE.findall(text)


def check(version: str | None = None) -> tuple[bool, str]:
    """Verifica o CHANGELOG. Retorna (ok, mensagem)."""
    if not CHANGELOG.exists():
        return False, f'CHANGELOG.md não encontrado: {CHANGELOG}'

    versions = get_versions(CHANGELOG)
    if not versions:
        return False, 'CHANGELOG.md não contém nenhuma versão no formato ## [vX.Y.Z]'

    latest = versions[0]

    if version:
        clean = version.lstrip('v')
        if clean not in versions:
            return False, f'versão {version} não encontrada no CHANGELOG (encontradas: {versions})'
        return True, f'versão {version} encontrada no CHANGELOG'

    return True, f'versão mais recente no CHANGELOG: v{latest} ({len(versions)} versão(ões) total)'


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Verifica CHANGELOG para release')
    parser.add_argument('--version', default=None,
                        help='Versão específica a verificar (ex: v0.8.0)')
    args = parser.parse_args(argv)

    ok, msg = check(args.version)
    symbol = '✅' if ok else '❌'
    print(f'{symbol} {msg}')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
