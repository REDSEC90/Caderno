#!/bin/bash
# Script de consolidação v0.5 → v1
# Baseado em análise FAA v2

set -e

PROJECT_ROOT="/home/redsec/Ambiente/SOE-CCG"
cd "$PROJECT_ROOT"

echo "════════════════════════════════════════"
echo "  Consolidação SOE-CCG v0.5 → v1"
echo "  Ferramenta: FAA v2"
echo "════════════════════════════════════════"
echo ""

# Função para consolidar arquivo
consolidate_file() {
    local file=$1
    local newfile="${file//-v0_5/-v1}"
    
    if [ ! -f "$file" ]; then
        echo "⚠️  Arquivo não encontrado: $file"
        return 1
    fi
    
    echo "📄 Processando: $file"
    echo "   → $newfile"
    
    # Renomear arquivo
    git mv "$file" "$newfile" 2>/dev/null || mv "$file" "$newfile"
    
    # Atualizar frontmatter se existir
    if head -n 1 "$newfile" | grep -q "^---$"; then
        sed -i 's/versao: 0\.5/versao: 1/' "$newfile"
        sed -i "s/atualizado-em: .*/atualizado-em: $(date +%Y-%m-%d)/" "$newfile"
    fi
    
    echo "   ✅ Consolidado"
    return 0
}

# Lote 1: Domínio core
echo ""
echo "═══ LOTE 1: DOMÍNIO CORE ═══"
echo ""

FILES_LOTE1=(
    "docs/01-dominio/template-especificacao-entidade-v0_5.md"
    "docs/01-dominio/template-contrato-v0_5.md"
    "docs/01-dominio/separacao-dominios-v0_5.md"
    "docs/01-dominio/linguagem-soe-ccg-v0_5.md"
    "docs/01-dominio/catalogacao-v0_5.md"
)

for file in "${FILES_LOTE1[@]}"; do
    consolidate_file "$file"
done

echo ""
echo "═══ VALIDAÇÃO FAA ═══"
./scripts/faa.sh validate --snapshot -q

echo ""
echo "═══ STATUS ATUALIZADO ═══"
./scripts/faa.sh status | head -20

echo ""
echo "════════════════════════════════════════"
echo "✅ Lote 1 concluído"
echo "════════════════════════════════════════"
