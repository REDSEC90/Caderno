#!/usr/bin/env bash
# lint.sh — ruff + mypy em codigo/ e kernel/
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
ERRORS=0

echo "── ruff ─────────────────────────────────────"
if command -v ruff &>/dev/null; then
    ruff check codigo/ kernel/ || ERRORS=$((ERRORS + 1))
else
    echo "[AVISO] ruff não instalado — pulando"
fi

echo ""
echo "── mypy (codigo/) ───────────────────────────"
$PYTHON -m mypy codigo/ --ignore-missing-imports || ERRORS=$((ERRORS + 1))

echo ""
echo "── mypy (kernel/) ───────────────────────────"
$PYTHON -m mypy kernel/ --ignore-missing-imports || ERRORS=$((ERRORS + 1))

if [ "$ERRORS" -gt 0 ]; then
    echo ""
    echo "❌  lint.sh: $ERRORS erro(s) encontrado(s)"
    exit 1
fi

echo ""
echo "✅  lint.sh: OK"
