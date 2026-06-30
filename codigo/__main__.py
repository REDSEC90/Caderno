"""CLI do SOE-CCG — comandos: importar, validar, status.

Exit codes:
  0  — sucesso
  1  — erros de validação críticos ou erros de importação
  2  — uso incorreto (argumento inválido)
"""
from __future__ import annotations

import sys
from pathlib import Path

from kernel.bootstrap import bootstrap_system
from kernel.shared.paths import ROOT


def _cmd_importar(args: list[str]) -> int:
    from .parser import parse_directory
    from .resolvedor import resolver
    from .validador import validar
    from .importador import importar, DB_PATH

    dados = ROOT / 'dados'
    db    = Path(args[0]) if args else DB_PATH

    print(f'[importar] Parseando {dados} ...')
    grafo = parse_directory(dados)
    print(f'[importar] {len(grafo.entities)} entidades encontradas.')

    erros_ref = resolver(grafo)
    if erros_ref:
        for e in erros_ref:
            print(f'  [REF] {e.source} -> {e.target} ({e.kind}): {e.erro}', file=sys.stderr)

    issues = validar(grafo)
    criticos = [i for i in issues if i.severidade == 'CRITICO']
    for i in issues:
        prefix = {'CRITICO': '[ERRO]', 'AVISO': '[AVISO]', 'INFO': '[INFO]'}[i.severidade]
        dest   = sys.stderr if i.severidade == 'CRITICO' else sys.stdout
        print(f'  {prefix} {i.entity_id}: {i.mensagem}', file=dest)

    if criticos:
        print(f'[importar] ABORTADO — {len(criticos)} issue(s) crítico(s).', file=sys.stderr)
        return 1

    result = importar(grafo, db)
    print(f'[importar] Inseridos: {result.inseridos}  Atualizados: {result.atualizados}  '
          f'Erros: {len(result.erros)}')
    for e in result.erros:
        print(f'  [ERRO] {e}', file=sys.stderr)
    return 1 if result.erros else 0


def _cmd_validar(args: list[str]) -> int:
    from .parser import parse_directory
    from .resolvedor import resolver
    from .validador import validar

    dados = ROOT / 'dados'
    grafo = parse_directory(dados)
    erros_ref = resolver(grafo)

    for e in erros_ref:
        print(f'[REF] {e.source} -> {e.target}: {e.erro}')

    issues = validar(grafo)
    if not issues and not erros_ref:
        print('OK — sem issues.')
        return 0

    for i in issues:
        print(f'[{i.severidade}] {i.entity_id} ({i.tipo_issue}): {i.mensagem}')

    criticos = [i for i in issues if i.severidade == 'CRITICO']
    return 1 if (criticos or erros_ref) else 0


def _cmd_status(_args: list[str]) -> int:
    from .parser import parse_directory
    from .resolvedor import resolver
    from .validador import validar
    from collections import Counter

    dados = ROOT / 'dados'
    grafo = parse_directory(dados)
    erros_ref = resolver(grafo)
    issues = validar(grafo)

    tipos = Counter(e.tipo for e in grafo.entities.values())
    print(f'Entidades : {len(grafo.entities)}')
    for tipo, n in sorted(tipos.items()):
        print(f'  {tipo}: {n}')

    total_edges = sum(len(e.outgoing) for e in grafo.entities.values())
    print(f'Arestas   : {total_edges}')
    print(f'Refs quebradas: {len(erros_ref)}')

    sev = Counter(i.severidade for i in issues)
    print(f'Issues    : {dict(sev) or "nenhum"}')
    return 0


_COMMANDS = {
    'importar': _cmd_importar,
    'validar':  _cmd_validar,
    'status':   _cmd_status,
}

_HELP = """\
uso: python -m soe_ccg <comando> [opcoes]

Comandos:
  importar [db_path]  Parseia dados/ e importa para SQLite.
  validar             Valida o grafo sem importar.
  status              Exibe métricas do grafo.
"""


def main() -> None:
    bootstrap_system()

    argv = sys.argv[1:]
    if not argv or argv[0] in ('-h', '--help'):
        print(_HELP)
        sys.exit(0)

    cmd = argv[0]
    handler = _COMMANDS.get(cmd)
    if handler is None:
        print(f'Comando desconhecido: {cmd!r}\n{_HELP}', file=sys.stderr)
        sys.exit(2)

    sys.exit(handler(argv[1:]))


if __name__ == '__main__':
    main()
