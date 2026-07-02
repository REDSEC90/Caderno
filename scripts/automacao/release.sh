#!/usr/bin/env bash
# SOE-CCG — Script de Release Automatizado
# Cria nova versão com validação completa

set -euo pipefail

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Função de ajuda
usage() {
    echo "Uso: $0 <versão> [--skip-tests]"
    echo ""
    echo "Exemplos:"
    echo "  $0 0.9.0          # Release normal com testes"
    echo "  $0 0.9.1 --skip-tests  # Release sem testes (usar com cautela)"
    echo ""
    exit 1
}

# Verifica argumentos
if [ $# -lt 1 ]; then
    usage
fi

VERSION="$1"
SKIP_TESTS=false

if [ $# -gt 1 ] && [ "$2" = "--skip-tests" ]; then
    SKIP_TESTS=true
fi

# Valida formato da versão (semver)
if ! [[ "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
    echo -e "${RED}❌ Erro: Versão inválida: $VERSION${NC}"
    echo "Use formato semver: X.Y.Z ou X.Y.Z-suffix"
    exit 1
fi

# Banner
echo -e "${CYAN}╔═══════════════════════════════════════╗${NC}"
echo -e "${CYAN}║      SOE-CCG — Release v${VERSION}       ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════╝${NC}"
echo ""

# Verifica se está no git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Erro: Não está em um repositório git${NC}"
    exit 1
fi

# Verifica se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}❌ Erro: Há mudanças não commitadas${NC}"
    echo "Commit ou descarte as mudanças antes do release"
    git status --short
    exit 1
fi

# Verifica se a tag já existe
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo -e "${RED}❌ Erro: Tag v$VERSION já existe${NC}"
    exit 1
fi

# Verifica branch atual
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${BLUE}📍 Branch atual: $CURRENT_BRANCH${NC}"
echo ""

# Executa pipeline se não foi pulado
if [ "$SKIP_TESTS" = false ]; then
    echo -e "${BLUE}🔍 Executando pipeline de validação...${NC}"
    echo ""
    
    if ! make pipeline; then
        echo ""
        echo -e "${RED}❌ Pipeline falhou — release cancelado${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${GREEN}✅ Pipeline passou${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠️  AVISO: Testes pulados (--skip-tests)${NC}"
    echo ""
fi

# Atualiza versão no pyproject.toml
echo -e "${BLUE}📝 Atualizando versão no pyproject.toml...${NC}"
if [ -f "pyproject.toml" ]; then
    sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml
    echo -e "${GREEN}✅ Versão atualizada${NC}"
else
    echo -e "${YELLOW}⚠️  pyproject.toml não encontrado${NC}"
fi
echo ""

# Cria entrada no CHANGELOG
echo -e "${BLUE}📋 Atualizando CHANGELOG.md...${NC}"
if [ -f "CHANGELOG.md" ]; then
    DATE=$(date +%Y-%m-%d)
    
    # Cria backup
    cp CHANGELOG.md CHANGELOG.md.bak
    
    # Adiciona nova seção no topo (após o cabeçalho)
    {
        head -n 5 CHANGELOG.md
        echo ""
        echo "## [v${VERSION}] — ${DATE}"
        echo ""
        echo "### Adicionado"
        echo ""
        echo "- Pipeline de automação completo (Makefile + scripts)"
        echo "- Scripts: lint.sh, type_check.sh, test.sh, audit.sh, pipeline.sh"
        echo "- Configuração pyproject.toml com mypy, ruff, pytest"
        echo ""
        echo "### Melhorado"
        echo ""
        echo "- Processo de release automatizado"
        echo "- Integração com CI/CD"
        echo ""
        tail -n +6 CHANGELOG.md
    } > CHANGELOG.md.new
    
    mv CHANGELOG.md.new CHANGELOG.md
    rm CHANGELOG.md.bak
    
    echo -e "${GREEN}✅ CHANGELOG atualizado${NC}"
else
    echo -e "${YELLOW}⚠️  CHANGELOG.md não encontrado${NC}"
fi
echo ""

# Commit das mudanças de release
echo -e "${BLUE}💾 Criando commit de release...${NC}"
git add pyproject.toml CHANGELOG.md 2>/dev/null || true
git commit -m "chore: release v${VERSION}" || echo "Nenhuma mudança para commitar"
echo -e "${GREEN}✅ Commit criado${NC}"
echo ""

# Cria tag
echo -e "${BLUE}🏷️  Criando tag v${VERSION}...${NC}"
git tag -a "v${VERSION}" -m "Release v${VERSION}"
echo -e "${GREEN}✅ Tag criada${NC}"
echo ""

# Relatório final
echo -e "${CYAN}╔═══════════════════════════════════════╗${NC}"
echo -e "${CYAN}║          Release Concluído           ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✅ Release v${VERSION} criado com sucesso${NC}"
echo ""
echo -e "${BLUE}📋 Próximos passos:${NC}"
echo -e "${BLUE}   1. Revise as mudanças: git show v${VERSION}${NC}"
echo -e "${BLUE}   2. Push do commit: git push origin ${CURRENT_BRANCH}${NC}"
echo -e "${BLUE}   3. Push da tag: git push origin v${VERSION}${NC}"
echo ""
echo -e "${YELLOW}⚠️  O release foi criado localmente mas NÃO foi enviado ao remoto${NC}"
echo ""
