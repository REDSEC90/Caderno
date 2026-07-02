#!/usr/bin/env bash
# SOE-CCG — Script de Verificação de Tipos
# Executa mypy com configuração strict

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Diretórios a verificar
TARGETS="kernel/ codigo/ scripts/faa/"

# Detecta mypy (venv ou sistema)
if [ -f "venv/bin/mypy" ]; then
    MYPY="venv/bin/mypy"
elif command -v mypy &> /dev/null; then
    MYPY="mypy"
else
    echo -e "${RED}❌ Erro: mypy não encontrado${NC}"
    echo "Instale com: make setup"
    echo "Ou: pip install mypy"
    exit 1
fi

echo -e "${BLUE}🔍 SOE-CCG — Verificação de Tipos${NC}"
echo ""

# Verifica se existe configuração mypy
if [ ! -f "pyproject.toml" ] && [ ! -f "mypy.ini" ]; then
    echo -e "${YELLOW}⚠️  Nenhuma configuração mypy encontrada${NC}"
    echo -e "${YELLOW}Usando configuração padrão${NC}"
    echo ""
fi

EXIT_CODE=0

# Executa mypy
echo -e "${BLUE}📝 Analisando tipos...${NC}"
if $MYPY $TARGETS --strict --pretty; then
    echo ""
    echo -e "${GREEN}✅ Verificação de tipos concluída com sucesso${NC}"
else
    EXIT_CODE=$?
    echo ""
    echo -e "${RED}❌ Erros de tipo encontrados${NC}"
    echo -e "${YELLOW}Corrija os problemas de tipo acima${NC}"
fi

exit $EXIT_CODE
