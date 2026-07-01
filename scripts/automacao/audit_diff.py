"""Audit Diff — compara dois snapshots FAA e lista regressões.

Uso:
  python3 scripts/automacao/audit_diff.py <snapshot_anterior> <snapshot_novo>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from kernel.shared.paths import ROOT


def load_snapshot(path: Path) -> dict:
    """Carrega um snapshot JSON."""
    return json.loads(path.read_text(encoding='utf-8'))


def diff_snapshots(old: dict, new: dict) -> dict:
    """Compara dois snapshots e retorna um relatório de diferenças."""
    score_old = old.get('score', 0.0)
    score_new = new.get('score', 0.0)
    delta     = score_new - score_old

    regressions: list[str] = []
    improvements: list[str] = []

    if delta < 0:
        regressions.append(f'score: {score_old:.1f} → {score_new:.1f} (Δ{delta:+.1f})')
    elif delta > 0:
        improvements.append(f'score: {score_old:.1f} → {score_new:.1f} (Δ{delta:+.1f})')

    health_old = old.get('health', '')
    health_new = new.get('health', '')
    if health_old != health_new:
        msg = f'health: {health_old} → {health_new}'
        if health_new in ('WARNING', 'ERROR', 'DEGRADED'):
            regressions.append(msg)
        else:
            improvements.append(msg)

    status_old = old.get('status', '')
    status_new = new.get('status', '')
    if status_old != status_new:
        msg = f'status: {status_old} → {status_new}'
        if status_new == 'DEGRADED':
            regressions.append(msg)
        else:
            improvements.append(msg)

    # issues críticas
    issues_old = old.get('issues', {}).get('critical', [])
    issues_new = new.get('issues', {}).get('critical', [])
    new_criticals = [i for i in issues_new if i not in issues_old]
    resolved      = [i for i in issues_old if i not in issues_new]

    for i in new_criticals:
        regressions.append(f'nova issue crítica: {i}')
    for i in resolved:
        improvements.append(f'issue crítica resolvida: {i}')

    return {
        'timestamp_old': old.get('timestamp', '?'),
        'timestamp_new': new.get('timestamp', '?'),
        'score_old':     score_old,
        'score_new':     score_new,
        'delta':         delta,
        'regressions':   regressions,
        'improvements':  improvements,
        'status':        'REGRESSION' if regressions else ('IMPROVED' if improvements else 'STABLE'),
    }


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    if len(argv) != 2:
        print('Uso: audit_diff.py <snapshot_anterior> <snapshot_novo>', file=sys.stderr)
        return 2

    old_path = Path(argv[0])
    new_path = Path(argv[1])

    for p in (old_path, new_path):
        if not p.exists():
            print(f'[ERRO] Arquivo não encontrado: {p}', file=sys.stderr)
            return 2

    old = load_snapshot(old_path)
    new = load_snapshot(new_path)
    result = diff_snapshots(old, new)

    print(f'Comparando snapshots:')
    print(f'  Anterior : {result["timestamp_old"]}  (score {result["score_old"]:.1f})')
    print(f'  Novo     : {result["timestamp_new"]}  (score {result["score_new"]:.1f})')
    print(f'  Delta    : {result["delta"]:+.1f}')
    print(f'  Status   : {result["status"]}')

    if result['regressions']:
        print('\nRegressões:')
        for r in result['regressions']:
            print(f'  ⚠ {r}')

    if result['improvements']:
        print('\nMelhorias:')
        for i in result['improvements']:
            print(f'  ✓ {i}')

    if not result['regressions'] and not result['improvements']:
        print('\nNenhuma diferença detectada.')

    return 1 if result['status'] == 'REGRESSION' else 0


if __name__ == '__main__':
    sys.exit(main())
