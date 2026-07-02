#!/usr/bin/env bash
# SOE-CCG — Instalador de Git Hooks
# Configura hooks locais para validação automática

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔧 SOE-CCG — Instalador de Git Hooks${NC}"
echo ""

# Verifica se está em um repositório git
if [ ! -d ".git" ]; then
    echo -e "${RED}❌ Erro: Não está em um repositório git${NC}"
    exit 1
fi

# Cria link simbólico para pre-commit
HOOK_SOURCE="$(pwd)/scripts/automacao/pre-commit"
HOOK_TARGET="$(pwd)/.git/hooks/pre-commit"

if [ -f "$HOOK_TARGET" ] || [ -L "$HOOK_TARGET" ]; then
    echo -e "${BLUE}⚠️  Hook pre-commit já existe${NC}"
    read -p "Substituir? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Instalação cancelada"
        exit 0
    fi
    rm "$HOOK_TARGET"
fi

# Cria link simbólico
ln -s "$HOOK_SOURCE" "$HOOK_TARGET"

echo -e "${GREEN}✅ Hook pre-commit instalado${NC}"
echo ""
echo -e "${BLUE}O que acontece agora:${NC}"
echo "  • Cada commit executará validação automática"
echo "  • Formatação será corrigida automaticamente"
echo "  • Linting será executado e problemas serão reportados"
echo ""
echo -e "${BLUE}Para desinstalar:${NC}"
echo "  rm .git/hooks/pre-commit"
echo ""
