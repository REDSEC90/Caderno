#!/usr/bin/env bash
# SOE-CCG — Script de Linting e Formatação
# Executa ruff check e ruff format

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretórios a verificar
TARGETS="kernel/ codigo/ scripts/faa/ testes/"

# Detecta ruff (venv ou sistema)
if [ -f "venv/bin/ruff" ]; then
    RUFF="venv/bin/ruff"
elif command -v ruff &> /dev/null; then
    RUFF="ruff"
else
    echo -e "${RED}❌ Erro: ruff não encontrado${NC}"
    echo "Instale com: make setup"
    echo "Ou: pip install ruff"
    exit 1
fi

echo -e "${BLUE}🧹 SOE-CCG — Linting e Formatação${NC}"
echo ""

EXIT_CODE=0

# 1. Verificação de formatação
echo -e "${BLUE}📋 Verificando formatação...${NC}"
if $RUFF format --check $TARGETS; then
    echo -e "${GREEN}✅ Formatação OK${NC}"
else
    echo -e "${YELLOW}⚠️  Problemas de formatação encontrados${NC}"
    echo -e "${YELLOW}Execute 'ruff format $TARGETS' para corrigir${NC}"
    EXIT_CODE=1
fi
echo ""

# 2. Linting
echo -e "${BLUE}🔍 Executando linting...${NC}"
if $RUFF check $TARGETS; then
    echo -e "${GREEN}✅ Linting OK${NC}"
else
    echo -e "${RED}❌ Problemas de linting encontrados${NC}"
    echo -e "${YELLOW}Execute 'ruff check --fix $TARGETS' para corrigir automaticamente${NC}"
    EXIT_CODE=1
fi
echo ""

# Resultado final
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Linting concluído com sucesso${NC}"
else
    echo -e "${RED}❌ Linting falhou — corrija os problemas acima${NC}"
fi

exit $EXIT_CODE
