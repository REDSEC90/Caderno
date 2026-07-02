#!/usr/bin/env bash
# SOE-CCG — Script de Auditoria de Qualidade
# Executa FAA (Framework de Auditoria Arquitetural)

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 SOE-CCG — Auditoria de Qualidade (FAA)${NC}"
echo ""

# Detecta python (venv ou sistema)
if [ -f "venv/bin/python3" ]; then
    PYTHON="venv/bin/python3"
else
    PYTHON="python3"
fi

# Verifica se o FAA existe
if [ ! -f "scripts/faa/__main__.py" ]; then
    echo -e "${RED}❌ Erro: FAA não encontrado em scripts/faa/${NC}"
    exit 1
fi

EXIT_CODE=0

# Executa FAA
echo -e "${BLUE}🔍 Executando análise arquitetural...${NC}"
echo ""

if $PYTHON -m scripts.faa; then
    echo ""
    echo -e "${GREEN}✅ Auditoria concluída${NC}"
    
    # Verifica se o relatório foi gerado
    if [ -f "faa-report.json" ]; then
        # Extrai score do relatório
        SCORE=$($PYTHON -c "import json; d=json.load(open('faa-report.json')); print(f\"{d.get('score', 0):.2f}\")" 2>/dev/null || echo "N/A")
        
        if [ "$SCORE" != "N/A" ]; then
            echo -e "${BLUE}🎯 Score FAA: ${SCORE}/100${NC}"
            
            # Verifica meta de qualidade (95%)
            MEETS_TARGET=$($PYTHON -c "print('true' if float('$SCORE') >= 95.0 else 'false')" 2>/dev/null || echo "false")
            if [ "$MEETS_TARGET" = "true" ]; then
                echo -e "${GREEN}✅ Meta de qualidade atingida (≥95)${NC}"
            else
                echo -e "${YELLOW}⚠️  Meta de qualidade não atingida (objetivo: ≥95)${NC}"
            fi
        fi
        
        echo -e "${BLUE}📄 Relatório completo: faa-report.json${NC}"
    fi
else
    EXIT_CODE=$?
    echo ""
    echo -e "${RED}❌ Auditoria falhou${NC}"
fi

exit $EXIT_CODE
