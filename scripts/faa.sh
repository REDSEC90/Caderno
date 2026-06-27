#!/bin/bash
# Helper para executar FAA v2 de qualquer lugar

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAA_CLI="$SCRIPT_DIR/faa/faa"

cd "$SCRIPT_DIR/.." && python3 "$FAA_CLI" "$@"
