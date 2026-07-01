#!/bin/bash
# Consolidação Lote 2: Catálogos

set -e
PROJECT_ROOT="/home/redsec/Ambiente/SOE-CCG"
cd "$PROJECT_ROOT"

echo "═══ LOTE 2: CATÁLOGOS ═══"

FILES=(
    "docs/01-dominio/catalogos/categorias-v0_5.md"
    "docs/01-dominio/catalogos/catalogos-expandidos-v0_5.md"
    "docs/01-dominio/catalogos/tipos-equipamentos-v0_5.md"
    "docs/01-dominio/catalogos/tipos-tecnicas-v0_5.md"
    "docs/01-dominio/catalogos/tipos-ingredientes-v0_5.md"
    "docs/01-dominio/catalogos/estados-receita-v0_5.md"
    "docs/01-dominio/catalogos/unidades-medida-v0_5.md"
    "docs/01-dominio/catalogos/estados-todas-entidades-v0_5.md"
)

for file in "${FILES[@]}"; do
    newfile="${file//-v0_5/-v1}"
    echo "📄 $file → $newfile"
    git mv "$file" "$newfile" 2>/dev/null || mv "$file" "$newfile"
    [ -f "$newfile" ] && sed -i 's/versao: 0\.5/versao: 1/' "$newfile"
done

./scripts/faa.sh validate --snapshot -q
./scripts/faa.sh status | head -20

echo "✅ Lote 2 concluído - 8 catálogos consolidados"
