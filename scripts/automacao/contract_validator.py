"""Validador de Contratos — verifica se cada módulo de codigo/ respeita o contrato mínimo.

Contrato mínimo de um módulo:
  1. Docstring de módulo presente (com Contrato/Entrada/Saída)
  2. Type hints em todas as funções e métodos públicos
  3. Arquivo de teste correspondente em testes/unit/test_{modulo}.py
  4. Ao menos um documento em docs/ referenciando o módulo pelo nome

Uso:
  python3 scripts/automacao/contract_validator.py [--dir codigo/]
"""
from __future__ import annotations

import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path

from kernel.shared.paths import ROOT


@dataclass
class Violation:
    modulo: str
    regra:  str
    detalhe: str


@dataclass
class ContractReport:
    modulo:     str
    violations: list[Violation] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return len(self.violations) == 0


def _has_module_docstring(tree: ast.Module) -> bool:
    return (
        bool(tree.body)
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    )


def _public_functions(tree: ast.Module) -> list[ast.FunctionDef | ast.AsyncFunctionDef]:
    funcs: list[ast.FunctionDef | ast.AsyncFunctionDef] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith('_'):
                funcs.append(node)
    return funcs


def _has_full_annotations(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Retorna True se todos os args (exceto self/cls) e o retorno têm anotação."""
    args = func.args
    all_args = args.args + args.posonlyargs + args.kwonlyargs
    if args.vararg:
        all_args.append(args.vararg)
    if args.kwarg:
        all_args.append(args.kwarg)

    for arg in all_args:
        if arg.arg in ('self', 'cls'):
            continue
        if arg.annotation is None:
            return False

    return func.returns is not None


def check_module(path: Path, root: Path) -> ContractReport:
    """Verifica um único arquivo .py e retorna o ContractReport."""
    modulo = path.stem
    report = ContractReport(modulo=modulo)

    try:
        source = path.read_text(encoding='utf-8')
        tree   = ast.parse(source, filename=str(path))
    except Exception as exc:
        report.violations.append(Violation(modulo, 'parse_error', str(exc)))
        return report

    # Regra 1 — docstring de módulo
    if not _has_module_docstring(tree):
        report.violations.append(Violation(
            modulo, 'sem_docstring_modulo',
            f'{path.name} não possui docstring de módulo'
        ))

    # Regra 2 — type hints em funções públicas
    for func in _public_functions(tree):
        if not _has_full_annotations(func):
            report.violations.append(Violation(
                modulo, 'sem_type_hints',
                f'função pública `{func.name}` sem anotações completas em {path.name}'
            ))

    # Regra 3 — teste correspondente
    test_path = root / 'testes' / 'unit' / f'test_{modulo}.py'
    if not test_path.exists():
        report.violations.append(Violation(
            modulo, 'sem_teste_unitario',
            f'testes/unit/test_{modulo}.py não encontrado'
        ))

    # Regra 4 — referência em docs/
    docs_dir = root / 'docs'
    encontrado = False
    if docs_dir.exists():
        for doc in docs_dir.rglob('*.md'):
            if modulo in doc.read_text(encoding='utf-8', errors='ignore'):
                encontrado = True
                break
    if not encontrado:
        report.violations.append(Violation(
            modulo, 'sem_referencia_docs',
            f'nenhum documento em docs/ menciona o módulo `{modulo}`'
        ))

    return report


def validate_directory(codigo_dir: Path, root: Path) -> list[ContractReport]:
    """Valida todos os módulos públicos em codigo_dir."""
    _SKIP = {'__init__', '__main__', '__pycache__'}
    reports = []
    for py in sorted(codigo_dir.glob('*.py')):
        if py.stem in _SKIP:
            continue
        reports.append(check_module(py, root))
    return reports


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Valida contratos de módulos Python')
    parser.add_argument('--dir', default='codigo', help='Diretório a validar (relativo à raiz)')
    args = parser.parse_args(argv)

    codigo_dir = ROOT / args.dir
    if not codigo_dir.exists():
        print(f'[ERRO] Diretório não encontrado: {codigo_dir}', file=sys.stderr)
        return 2

    reports = validate_directory(codigo_dir, ROOT)
    total_violations = sum(len(r.violations) for r in reports)

    for report in reports:
        status = '✅' if report.ok else '❌'
        print(f'{status} {report.modulo}')
        for v in report.violations:
            print(f'   [{v.regra}] {v.detalhe}')

    print()
    ok_count = sum(1 for r in reports if r.ok)
    print(f'Resultado: {ok_count}/{len(reports)} módulos OK — {total_violations} violação(ões)')
    return 0 if total_violations == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
