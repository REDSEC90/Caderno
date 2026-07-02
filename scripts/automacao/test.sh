#!/usr/bin/env bash
# SOE-CCG — Script de Testes
# Executa pytest com cobertura

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 SOE-CCG — Execução de Testes${NC}"
echo ""

# Detecta pytest (venv ou sistema)
if [ -f "venv/bin/pytest" ]; then
    PYTEST="venv/bin/pytest"
elif command -v pytest &> /dev/null; then
    PYTEST="pytest"
else
    echo -e "${RED}❌ Erro: pytest não encontrado${NC}"
    echo "Instale com: make setup"
    echo "Ou: pip install pytest pytest-cov"
    exit 1
fi

# Detecta python (venv ou sistema)
if [ -f "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
else
    PYTHON="python3"
fi

EXIT_CODE=0

# Executa testes com cobertura
echo -e "${BLUE}📊 Executando testes com cobertura...${NC}"
echo ""

if $PYTEST \
    --cov=kernel \
    --cov=codigo \
    --cov-report=term-missing \
    --cov-report=json \
    --cov-report=html \
    -v \
    testes/; then
    
    echo ""
    echo -e "${GREEN}✅ Todos os testes passaram${NC}"
    
    # Extrai cobertura do coverage.json se disponível
    if [ -f "coverage.json" ]; then
        COVERAGE=$($PYTHON -c "import json; print(f\"{json.load(open('coverage.json'))['totals']['percent_covered']:.1f}\")" 2>/dev/null || echo "N/A")
        echo -e "${BLUE}📈 Cobertura total: ${COVERAGE}%${NC}"
        
        # Verifica meta de cobertura (95%)
        if command -v $PYTHON &> /dev/null && [ "$COVERAGE" != "N/A" ]; then
            MEETS_TARGET=$($PYTHON -c "print('true' if float('$COVERAGE') >= 95.0 else 'false')")
            if [ "$MEETS_TARGET" = "true" ]; then
                echo -e "${GREEN}✅ Meta de cobertura atingida (≥95%)${NC}"
            else
                echo -e "${YELLOW}⚠️  Meta de cobertura não atingida (objetivo: ≥95%)${NC}"
            fi
        fi
    fi
else
    EXIT_CODE=$?
    echo ""
    echo -e "${RED}❌ Alguns testes falharam${NC}"
fi

echo ""
echo -e "${BLUE}💡 Relatório HTML disponível em: htmlcov/index.html${NC}"

exit $EXIT_CODE
