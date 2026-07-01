"""Doc Scaffold — gera estrutura documental mínima para um módulo Python.

Dado um módulo Python em codigo/ ou kernel/, gera:
  - docs/05-desenvolvimento/{modulo}-contrato-v1.md  (template preenchido com docstrings)
  - Entry no docs/INDICE-MESTRE.md
  - Entry no docs/MATRIZ-RASTREABILIDADE.md

Uso:
  python3 scripts/automacao/doc_scaffold.py codigo/parser.py
  python3 scripts/automacao/doc_scaffold.py --dry-run codigo/parser.py
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

from kernel.shared.paths import ROOT, DOCS

TEMPLATE = """\
# Contrato — `{modulo}`

**Módulo:** `{entrypoint}`
**Gerado por:** doc_scaffold v1
**Data:** {data}

---

## Descrição

{descricao}

---

## Contrato

| Campo       | Descrição                        |
|-------------|----------------------------------|
| Entrada     | *(preencher)*                    |
| Saída       | *(preencher)*                    |
| Erros       | *(preencher)*                    |
| Pré-cond.   | *(preencher)*                    |

---

## Funções Públicas

{funcoes}

---

## Referências

- Código-fonte: `{entrypoint}`
- Testes: `testes/unit/test_{modulo}.py`
"""


def _extract_module_info(path: Path) -> tuple[str, list[str]]:
    """Extrai (docstring_do_módulo, lista_de_funções_públicas) de um .py."""
    try:
        source = path.read_text(encoding='utf-8')
        tree   = ast.parse(source)
    except Exception:
        return '*(não disponível)*', []

    docstring = ''
    if (tree.body
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)):
        docstring = tree.body[0].value.value.strip()

    funcs: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith('_'):
                doc = ast.get_docstring(node) or ''
                sig = f'`{node.name}(...)` — {doc.splitlines()[0] if doc else "sem docstring"}'
                funcs.append(f'- {sig}')

    return docstring or '*(sem docstring de módulo)*', funcs


def scaffold(module_path: Path, dry_run: bool = False) -> list[Path]:
    """Gera os artefatos documentais para module_path. Retorna lista de arquivos criados/modificados."""
    from datetime import date

    modulo    = module_path.stem
    # entrypoint: converte path para notação de módulo Python
    rel       = module_path.relative_to(ROOT)
    entrypoint = '.'.join(rel.with_suffix('').parts)

    descricao, funcs = _extract_module_info(module_path)
    funcoes_md = '\n'.join(funcs) if funcs else '*(nenhuma função pública encontrada)*'

    # ── 1. Documento de contrato ───────────────────────────────────────────────
    dest_dir  = DOCS / '05-desenvolvimento'
    dest_file = dest_dir / f'{modulo}-contrato-v1.md'
    conteudo  = TEMPLATE.format(
        modulo=modulo,
        entrypoint=entrypoint,
        data=date.today().isoformat(),
        descricao=descricao.splitlines()[0] if descricao else '*(sem descrição)*',
        funcoes=funcoes_md,
    )

    created: list[Path] = []

    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
        if not dest_file.exists():
            dest_file.write_text(conteudo, encoding='utf-8')
            created.append(dest_file)
            print(f'[scaffold] Criado: {dest_file.relative_to(ROOT)}')
        else:
            print(f'[scaffold] Já existe: {dest_file.relative_to(ROOT)} — pulando')
    else:
        print(f'[dry-run] Criaria: {dest_file.relative_to(ROOT)}')
        created.append(dest_file)

    # ── 2. INDICE-MESTRE ──────────────────────────────────────────────────────
    indice = DOCS / 'INDICE-MESTRE.md'
    marker = f'`{entrypoint}`'
    if indice.exists():
        texto = indice.read_text(encoding='utf-8')
        if marker not in texto:
            entry = f'\n- {marker} — ver `docs/05-desenvolvimento/{modulo}-contrato-v1.md`'
            if not dry_run:
                indice.write_text(texto + entry, encoding='utf-8')
                print(f'[scaffold] INDICE-MESTRE atualizado com {marker}')
            else:
                print(f'[dry-run] Adicionaria ao INDICE-MESTRE: {marker}')
            created.append(indice)

    # ── 3. MATRIZ-RASTREABILIDADE ─────────────────────────────────────────────
    matriz = DOCS / 'MATRIZ-RASTREABILIDADE.md'
    if matriz.exists():
        texto = matriz.read_text(encoding='utf-8')
        if marker not in texto:
            entry = f'\n| {marker} | `testes/unit/test_{modulo}.py` | `docs/05-desenvolvimento/{modulo}-contrato-v1.md` |'
            if not dry_run:
                matriz.write_text(texto + entry, encoding='utf-8')
                print(f'[scaffold] MATRIZ-RASTREABILIDADE atualizada com {marker}')
            else:
                print(f'[dry-run] Adicionaria à MATRIZ: {marker}')
            created.append(matriz)

    return created


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Gera scaffold documental para um módulo')
    parser.add_argument('modulo', help='Caminho para o arquivo .py (ex: codigo/parser.py)')
    parser.add_argument('--dry-run', action='store_true', help='Mostra o que seria criado sem criar')
    args = parser.parse_args(argv)

    path = Path(args.modulo)
    if not path.is_absolute():
        path = ROOT / path

    if not path.exists():
        print(f'[ERRO] Arquivo não encontrado: {path}', file=sys.stderr)
        return 2

    created = scaffold(path, dry_run=args.dry_run)
    print(f'\n[scaffold] {len(created)} artefato(s) {"seria(m) gerado(s)" if args.dry_run else "gerado(s)"}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
