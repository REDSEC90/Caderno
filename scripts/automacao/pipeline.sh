#!/usr/bin/env bash
# pipeline.sh — Pipeline de release do SOE-CCG
# Executa: lint → type check → contract validation → unit tests →
#           integration tests → FAA → changelog check
# Para em qualquer falha.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python3}"
OK="✅"
FAIL="❌"
SEP="────────────────────────────────────────"

step() {
    echo ""
    echo "$SEP"
    echo "▶ $1"
    echo "$SEP"
}

pass() { echo "$OK  $1"; }
fail() { echo "$FAIL $1"; exit 1; }

# ── 1. Lint ───────────────────────────────────────────────────────────────────
step "1/7 — Lint (ruff / pylint)"
if command -v ruff &>/dev/null; then
    ruff check codigo/ kernel/ && pass "ruff OK" || fail "ruff encontrou erros"
else
    echo "    [AVISO] ruff não encontrado — pulando"
fi

# ── 2. Type check ─────────────────────────────────────────────────────────────
step "2/7 — Type check (mypy)"
$PYTHON -m mypy codigo/ --ignore-missing-imports && pass "mypy OK" || fail "mypy encontrou erros"

# ── 3. Validação de contratos ─────────────────────────────────────────────────
step "3/7 — Validação de contratos"
$PYTHON scripts/automacao/contract_validator.py && pass "contratos OK" || fail "violações de contrato encontradas"

# ── 4. Testes unitários ───────────────────────────────────────────────────────
step "4/7 — Testes unitários"
$PYTHON -m pytest testes/unit/ -q --tb=short && pass "unit tests OK" || fail "testes unitários falharam"

# ── 5. Testes de integração ───────────────────────────────────────────────────
step "5/7 — Testes de integração"
$PYTHON -m pytest testes/integration/ testes/contract/ testes/cookbook/ -q --tb=short && pass "integration tests OK" || fail "testes de integração falharam"

# ── 6. FAA ────────────────────────────────────────────────────────────────────
step "6/7 — FAA (score ≥ 90)"
$PYTHON scripts/automacao/audit_runner.py --threshold 90 && pass "FAA OK" || fail "FAA score abaixo do threshold"

# ── 7. Changelog check ───────────────────────────────────────────────────────
step "7/7 — Changelog check"
$PYTHON scripts/automacao/release_check.py && pass "changelog OK" || fail "changelog sem entry para versão atual"

echo ""
echo "$SEP"
echo "✅  Pipeline concluído com sucesso."
echo "$SEP"
