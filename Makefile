# SOE-CCG — Makefile
# Interface unificada para automação do projeto

.PHONY: help setup test lint type audit pipeline clean build install
.DEFAULT_GOAL := help

# Configuração
VENV := venv
PYTHON := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
PYTEST := $(if $(wildcard $(VENV)/bin/pytest),$(VENV)/bin/pytest,pytest)
MYPY := $(if $(wildcard $(VENV)/bin/mypy),$(VENV)/bin/mypy,mypy)
RUFF := $(if $(wildcard $(VENV)/bin/ruff),$(VENV)/bin/ruff,ruff)
PIP := $(if $(wildcard $(VENV)/bin/pip),$(VENV)/bin/pip,pip)

help: ## Mostra esta ajuda
	@echo "SOE-CCG — Sistema de Conhecimento Gastronômico"
	@echo ""
	@echo "Comandos disponíveis:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup: ## Instala dependências e prepara ambiente
	@echo "🔧 Configurando ambiente..."
	@if [ ! -d "$(VENV)" ]; then \
		echo "📦 Criando ambiente virtual..."; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "📦 Instalando dependências..."
	@$(PIP) install --upgrade pip -q
	@$(PIP) install -r requirements-dev.txt -q 2>/dev/null || echo "⚠️  requirements-dev.txt não encontrado"
	@echo "✅ Ambiente configurado"
	@echo "💡 Ambiente virtual em: $(VENV)/"

lint: ## Executa linting e formatação
	@echo "🧹 Executando linting..."
	@./scripts/automacao/lint.sh

type: ## Executa verificação de tipos
	@echo "🔍 Verificando tipos..."
	@./scripts/automacao/type_check.sh

test: ## Executa todos os testes
	@echo "🧪 Executando testes..."
	@./scripts/automacao/test.sh

audit: ## Executa auditoria de qualidade (FAA)
	@echo "📊 Executando auditoria..."
	@./scripts/automacao/audit.sh

pipeline: ## Executa pipeline completo (CI/CD)
	@echo "🚀 Executando pipeline completo..."
	@./scripts/automacao/pipeline.sh

clean: ## Limpa arquivos temporários
	@echo "🧽 Limpando arquivos temporários..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@rm -f .coverage coverage.json htmlcov/ 2>/dev/null || true
	@echo "✅ Limpeza concluída"

build: lint type test audit ## Constrói o projeto (lint + type + test + audit)
	@echo "🏗️  Build completo executado"

install: setup build ## Instala o projeto localmente
	@echo "📦 Instalando SOE-CCG..."
	$(PYTHON) -m pip install -e .
	@echo "✅ SOE-CCG instalado"

# Aliases para compatibilidade
check: build ## Alias para 'build'
all: build ## Alias para 'build'
ci: pipeline ## Alias para 'pipeline'
