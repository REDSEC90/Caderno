"""Audit Runner — executa o FAA e persiste snapshot em docs/99-referencias/snapshots/.

Uso:
  python3 scripts/automacao/audit_runner.py [--threshold 90]
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from kernel.shared.paths import ROOT
SNAPSHOTS_DIR = ROOT / 'docs' / '99-referencias' / 'snapshots'
FAA_STATE     = ROOT / 'docs' / '99-referencias' / 'faa-state.json'
THRESHOLD_DEFAULT = 90


def load_faa_state() -> dict:
    """Carrega o estado atual do FAA de faa-state.json."""
    if not FAA_STATE.exists():
        raise FileNotFoundError(f'faa-state.json não encontrado: {FAA_STATE}')
    return json.loads(FAA_STATE.read_text(encoding='utf-8'))


def build_snapshot(state: dict, threshold: int) -> dict:
    """Constrói o snapshot a partir do estado FAA."""
    metrics  = state.get('metrics', {})
    score    = metrics.get('score', 0.0)
    health   = metrics.get('health', 'UNKNOWN')
    decision = metrics.get('decision', 'UNKNOWN')
    issues   = state.get('issues', {})

    status = 'OK' if score >= threshold else 'DEGRADED'

    return {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'score':     score,
        'health':    health,
        'decision':  decision,
        'status':    status,
        'threshold': threshold,
        'metrics':   metrics,
        'issues':    issues,
    }


def save_snapshot(snapshot: dict) -> Path:
    """Persiste snapshot em SNAPSHOTS_DIR e retorna o caminho."""
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    ts   = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    path = SNAPSHOTS_DIR / f'faa-snapshot-{ts}.json'
    path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding='utf-8')
    return path


def run(threshold: int = THRESHOLD_DEFAULT) -> int:
    """Executa o audit runner. Retorna 0 se OK, 1 se DEGRADED."""
    try:
        state    = load_faa_state()
        snapshot = build_snapshot(state, threshold)
        path     = save_snapshot(snapshot)
    except Exception as exc:
        print(f'[audit_runner] ERRO: {exc}', file=sys.stderr)
        return 2

    score  = snapshot['score']
    status = snapshot['status']
    print(f'[audit_runner] Score: {score:.1f}  Status: {status}  Threshold: {threshold}')
    print(f'[audit_runner] Snapshot salvo: {path.relative_to(ROOT)}')

    if status == 'DEGRADED':
        print(f'[audit_runner] AVISO: score {score:.1f} < threshold {threshold}', file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description='Executa FAA e persiste snapshot')
    parser.add_argument('--threshold', type=int, default=THRESHOLD_DEFAULT,
                        help='Score mínimo para status OK (default: 90)')
    args = parser.parse_args(argv)
    return run(args.threshold)


if __name__ == '__main__':
    sys.exit(main())
