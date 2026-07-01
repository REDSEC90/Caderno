"""Testes do contract_validator."""
from __future__ import annotations

import ast
import textwrap
from pathlib import Path

import pytest

from scripts.automacao.contract_validator import (
    ContractReport,
    Violation,
    _has_full_annotations,
    _has_module_docstring,
    _public_functions,
    check_module,
    validate_directory,
)


# ── helpers ──────────────────────────────────────────────────────────────────

def _parse(src: str) -> ast.Module:
    return ast.parse(textwrap.dedent(src))


def _func(src: str) -> ast.FunctionDef:
    tree = _parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            return node
    raise ValueError('nenhuma função encontrada')


# ── _has_module_docstring ─────────────────────────────────────────────────────

def test_has_module_docstring_presente():
    tree = _parse('"""Docstring."""\nx = 1')
    assert _has_module_docstring(tree) is True


def test_has_module_docstring_ausente():
    tree = _parse('x = 1')
    assert _has_module_docstring(tree) is False


def test_has_module_docstring_modulo_vazio():
    tree = _parse('')
    assert _has_module_docstring(tree) is False


# ── _has_full_annotations ─────────────────────────────────────────────────────

def test_annotations_completas():
    f = _func('def foo(x: int, y: str) -> bool: ...')
    assert _has_full_annotations(f) is True


def test_annotations_faltando_retorno():
    f = _func('def foo(x: int): ...')
    assert _has_full_annotations(f) is False


def test_annotations_faltando_arg():
    f = _func('def foo(x, y: str) -> bool: ...')
    assert _has_full_annotations(f) is False


def test_annotations_self_ignorado():
    f = _func('def foo(self, x: int) -> None: ...')
    assert _has_full_annotations(f) is True


def test_annotations_sem_args_com_retorno():
    f = _func('def foo() -> None: ...')
    assert _has_full_annotations(f) is True


# ── _public_functions ─────────────────────────────────────────────────────────

def test_public_functions_filtra_privadas():
    src = '''
def publica(x: int) -> int: ...
def _privada(x: int) -> int: ...
class C:
    def metodo(self) -> None: ...
    def _interno(self) -> None: ...
'''
    tree = _parse(src)
    funcs = _public_functions(tree)
    nomes = [f.name for f in funcs]
    assert 'publica' in nomes
    assert 'metodo' in nomes
    assert '_privada' not in nomes
    assert '_interno' not in nomes


# ── check_module (com tmp_path) ───────────────────────────────────────────────

def test_check_module_ok(tmp_path: Path):
    # módulo com docstring, type hints, teste e referência em docs
    codigo_dir = tmp_path / 'codigo'
    codigo_dir.mkdir()
    modulo = codigo_dir / 'meu_modulo.py'
    modulo.write_text(textwrap.dedent('''\
        """Módulo de exemplo.

        Contrato:
          Entrada: x int
          Saída: int
        """
        from __future__ import annotations


        def processar(x: int) -> int:
            """Processa x."""
            return x
    '''), encoding='utf-8')

    testes_dir = tmp_path / 'testes' / 'unit'
    testes_dir.mkdir(parents=True)
    (testes_dir / 'test_meu_modulo.py').write_text('# teste\n', encoding='utf-8')

    docs_dir = tmp_path / 'docs'
    docs_dir.mkdir()
    (docs_dir / 'ref.md').write_text('Veja meu_modulo para detalhes.\n', encoding='utf-8')

    report = check_module(modulo, tmp_path)
    assert report.ok, report.violations


def test_check_module_sem_docstring(tmp_path: Path):
    codigo_dir = tmp_path / 'codigo'
    codigo_dir.mkdir()
    modulo = codigo_dir / 'mod.py'
    modulo.write_text('x = 1\n', encoding='utf-8')

    # satisfaz regras 3 e 4
    (tmp_path / 'testes' / 'unit').mkdir(parents=True)
    (tmp_path / 'testes' / 'unit' / 'test_mod.py').write_text('', encoding='utf-8')
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs' / 'r.md').write_text('mod\n', encoding='utf-8')

    report = check_module(modulo, tmp_path)
    regras = [v.regra for v in report.violations]
    assert 'sem_docstring_modulo' in regras


def test_check_module_sem_teste(tmp_path: Path):
    codigo_dir = tmp_path / 'codigo'
    codigo_dir.mkdir()
    modulo = codigo_dir / 'mod2.py'
    modulo.write_text('"""Docstring."""\n', encoding='utf-8')
    (tmp_path / 'testes' / 'unit').mkdir(parents=True)
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs' / 'r.md').write_text('mod2\n', encoding='utf-8')

    report = check_module(modulo, tmp_path)
    regras = [v.regra for v in report.violations]
    assert 'sem_teste_unitario' in regras


def test_check_module_sem_referencia_docs(tmp_path: Path):
    codigo_dir = tmp_path / 'codigo'
    codigo_dir.mkdir()
    modulo = codigo_dir / 'mod3.py'
    modulo.write_text('"""Docstring."""\n', encoding='utf-8')
    (tmp_path / 'testes' / 'unit').mkdir(parents=True)
    (tmp_path / 'testes' / 'unit' / 'test_mod3.py').write_text('', encoding='utf-8')
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs' / 'outro.md').write_text('sem mencao\n', encoding='utf-8')

    report = check_module(modulo, tmp_path)
    regras = [v.regra for v in report.violations]
    assert 'sem_referencia_docs' in regras


# ── validate_directory ────────────────────────────────────────────────────────

def test_validate_directory_skip_dunder(tmp_path: Path):
    codigo_dir = tmp_path / 'codigo'
    codigo_dir.mkdir()
    (codigo_dir / '__init__.py').write_text('', encoding='utf-8')
    (codigo_dir / '__main__.py').write_text('', encoding='utf-8')
    (codigo_dir / 'mod.py').write_text('"""doc."""\n', encoding='utf-8')
    (tmp_path / 'testes' / 'unit').mkdir(parents=True)
    (tmp_path / 'docs').mkdir()

    reports = validate_directory(codigo_dir, tmp_path)
    nomes = [r.modulo for r in reports]
    assert '__init__' not in nomes
    assert '__main__' not in nomes
    assert 'mod' in nomes
