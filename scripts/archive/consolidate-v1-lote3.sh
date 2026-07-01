#!/bin/bash
# Consolidação Lote 3: Arquitetura + Dev + Ops

set -e
PROJECT_ROOT="/home/redsec/Ambiente/SOE-CCG"
cd "$PROJECT_ROOT"

echo "═══ LOTE 3: ARQUITETURA + DEV + OPS ═══"

FILES=(
    "docs/02-arquitetura/diagrama-mestre-v0_5.md"
    "docs/05-desenvolvimento/padroes-desenvolvimento-v0_5.md"
    "docs/05-desenvolvimento/casos-de-uso-v0_5.md"
    "docs/06-operacao/guia-operacao-v0_5.md"
)

for file in "${FILES[@]}"; do
    newfile="${file//-v0_5/-v1}"
    echo "📄 $file → $newfile"
    git mv "$file" "$newfile" 2>/dev/null || mv "$file" "$newfile"
    [ -f "$newfile" ] && sed -i 's/versao: 0\.5/versao: 1/' "$newfile"
done

./scripts/faa.sh validate --snapshot -q
./scripts/faa.sh status | head -20

echo "✅ Lote 3 concluído - 4 arquivos consolidados"
