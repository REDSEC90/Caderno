#!/usr/bin/env bash
# SOE-CCG — Pipeline Completo de CI/CD
# Orquestrador que executa todas as etapas de verificação

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuração
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Contadores
TOTAL_STEPS=4
CURRENT_STEP=0
FAILED_STEPS=()

# Banner
echo -e "${CYAN}╔═══════════════════════════════════════╗${NC}"
echo -e "${CYAN}║  SOE-CCG — Pipeline de CI/CD v0.9.0  ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 Diretório: ${PROJECT_ROOT}${NC}"
echo -e "${BLUE}🎯 Etapas: ${TOTAL_STEPS}${NC}"
echo ""

# Função para executar etapa
run_step() {
    local step_name="$1"
    local step_script="$2"
    
    CURRENT_STEP=$((CURRENT_STEP + 1))
    
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}[${CURRENT_STEP}/${TOTAL_STEPS}] ${step_name}${NC}"
    echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    
    if bash "$SCRIPT_DIR/$step_script"; then
        echo -e "${GREEN}✅ ${step_name} — SUCESSO${NC}"
        echo ""
        return 0
    else
        echo -e "${RED}❌ ${step_name} — FALHOU${NC}"
        echo ""
        FAILED_STEPS+=("$step_name")
        return 1
    fi
}

# Timestamp inicial
START_TIME=$(date +%s)

# Etapa 1: Linting
run_step "Linting" "lint.sh" || true

# Etapa 2: Verificação de tipos
run_step "Verificação de Tipos" "type_check.sh" || true

# Etapa 3: Testes
run_step "Testes" "test.sh" || true

# Etapa 4: Auditoria
run_step "Auditoria (FAA)" "audit.sh" || true

# Timestamp final
END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

# Relatório final
echo -e "${CYAN}╔═══════════════════════════════════════╗${NC}"
echo -e "${CYAN}║        Relatório do Pipeline         ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════╝${NC}"
echo ""

if [ ${#FAILED_STEPS[@]} -eq 0 ]; then
    echo -e "${GREEN}✅ Pipeline concluído com SUCESSO${NC}"
    echo -e "${GREEN}🎉 Todas as ${TOTAL_STEPS} etapas passaram${NC}"
    EXIT_CODE=0
else
    echo -e "${RED}❌ Pipeline FALHOU${NC}"
    echo -e "${RED}⚠️  ${#FAILED_STEPS[@]} de ${TOTAL_STEPS} etapas falharam:${NC}"
    for step in "${FAILED_STEPS[@]}"; do
        echo -e "${RED}   • ${step}${NC}"
    done
    EXIT_CODE=1
fi

echo ""
echo -e "${BLUE}⏱️  Tempo total: ${DURATION}s${NC}"
echo ""

# Próximos passos em caso de falha
if [ $EXIT_CODE -ne 0 ]; then
    echo -e "${YELLOW}📋 Próximos passos:${NC}"
    echo -e "${YELLOW}   1. Revise os erros nas etapas falhadas acima${NC}"
    echo -e "${YELLOW}   2. Corrija os problemas identificados${NC}"
    echo -e "${YELLOW}   3. Execute novamente: make pipeline${NC}"
    echo ""
fi

exit $EXIT_CODE
