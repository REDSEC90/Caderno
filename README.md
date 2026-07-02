# SOE-CCG

> Sistema de Organização e Evolução de Conhecimento Gastronômico

[![CI/CD](https://github.com/seu-usuario/SOE-CCG/workflows/CI/badge.svg)](https://github.com/seu-usuario/SOE-CCG/actions)
[![Coverage](https://img.shields.io/badge/coverage-94%25-brightgreen.svg)](./coverage.json)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-GPL--3.0-blue.svg)](./LICENSE)

## 🎯 Visão

O SOE-CCG nasceu da necessidade de registrar, preservar, organizar, relacionar e evoluir conhecimento gastronômico durante muitos anos, independentemente da tecnologia utilizada para acessá-lo.

**Não é um gerenciador de receitas. É um motor de conhecimento gastronômico.**

## ⚡ Quick Start

```bash
# Clone e configure
git clone https://github.com/seu-usuario/SOE-CCG.git
cd SOE-CCG
make setup

# Execute testes
make test

# Valide qualidade
make pipeline
```

## 📚 Filosofia

O software não nasce pelo código. Nasce pelo conhecimento.

Toda implementação é consequência do domínio previamente definido.

```
Filosofia → Constituição → Governança → Especificações → Modelagem → Implementação → Interface
```

## 🎨 Princípios

* O conhecimento é permanente. A implementação é temporária.
* Markdown é o formato canônico.
* SQLite é apenas um mecanismo de consulta.
* Nenhuma informação deve existir exclusivamente no banco de dados.
* Todo registro possui identificador permanente.
* Relacionamentos utilizam identificadores, nunca nomes.

## 📊 Status

🟢 **v0.9.0 — Automação e Qualidade**

| Métrica | Status | Meta |
|---------|--------|------|
| Testes | 516/516 ✅ | 100% |
| Cobertura | 94% ✅ | ≥95% |
| FAA Score | 93.78 | ≥95 |
| Type Hints | Em progresso | 100% |

**Versão atual:** v0.9.0  
**Próxima release:** v1.0.0 (estável)

## 🚀 Comandos

```bash
make help          # Lista todos os comandos
make lint          # Linting e formatação
make type          # Verificação de tipos
make test          # Testes + cobertura
make audit         # Auditoria FAA
make pipeline      # CI/CD completo
make clean         # Limpa temporários
```

## 📁 Estrutura

```
SOE-CCG/
├── kernel/              # Motor central do sistema
├── codigo/              # Runtime e CLI
├── dados/               # Dados canônicos (Markdown)
├── banco_de_dados/      # Esquemas SQLite
├── docs/                # Documentação completa
│   ├── 00-projeto/      # Visão e constituição
│   ├── 01-dominio/      # Entidades e esquemas
│   ├── 02-arquitetura/  # Fluxo de dados
│   ├── 03-modelagem/    # Modelo ER
│   └── 04-padroes/      # Convenções
├── testes/              # Testes (contract, unit, integration, e2e)
├── scripts/             # Automação e utilitários
│   └── automacao/       # Pipeline CI/CD
└── recursos/            # Assets e templates
```

## 📖 Documentação

- **[Guia de Contribuição](CONTRIBUTING.md)** — Como desenvolver
- **[Roadmap](ROADMAP-v1.0.md)** — Caminho para v1.0
- **[CHANGELOG](CHANGELOG.md)** — Histórico de mudanças
- **[Como Funciona](COMO-FUNCIONA-SOE-CCG.md)** — Arquitetura detalhada
- **[Documentação Completa](docs/)** — Especificações técnicas

## 🔧 Desenvolvimento

```bash
# Instale git hooks
./scripts/automacao/install-hooks.sh

# Desenvolva com qualidade
make pipeline  # Valida antes de commitar

# Crie release
./scripts/automacao/release.sh 0.9.1
```

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guia completo.

## 🏗️ Arquitetura

O sistema segue arquitetura em camadas:

1. **Kernel** — Motor de conhecimento (tipos, validação, IR)
2. **Runtime** — Execução (parser, importador, resolvedor)
3. **CLI** — Interface de linha de comando
4. **Storage** — Persistência (Markdown + SQLite)

## 📊 Qualidade

- **Testes:** 516 testes (contract, unit, integration, e2e, golden, cookbook)
- **Cobertura:** 94% (meta: ≥95%)
- **Linting:** ruff (zero warnings)
- **Type checking:** mypy strict mode
- **Auditoria:** FAA (Framework de Auditoria Arquitetural)

## 🤝 Contribuindo

Contribuições são bem-vindas! Ver [CONTRIBUTING.md](CONTRIBUTING.md).

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Commit: `git commit -m "feat: minha feature"`
4. Push: `git push origin feature/minha-feature`
5. Abra um Pull Request

## 📜 Licença

[GPL-3.0-or-later](LICENSE)

## 📮 Contato

- **Issues:** [GitHub Issues](https://github.com/seu-usuario/SOE-CCG/issues)
- **Discussões:** [GitHub Discussions](https://github.com/seu-usuario/SOE-CCG/discussions)

---

**Desenvolvido com ❤️ e muito conhecimento gastronômico**
