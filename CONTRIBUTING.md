# SOE-CCG — Guia de Desenvolvimento

> Guia rápido para desenvolvedores do SOE-CCG

## Setup Inicial

```bash
# Clone o repositório
git clone <repo-url>
cd SOE-CCG

# Instale dependências
make setup

# Ou manualmente:
pip install -r requirements.txt
pip install pytest pytest-cov mypy ruff
```

## Comandos Principais

### Desenvolvimento

```bash
make help          # Lista todos os comandos disponíveis
make lint          # Executa linting e formatação
make type          # Verifica tipos com mypy
make test          # Executa testes com cobertura
make audit         # Executa auditoria FAA
```

### Pipeline Completo

```bash
make pipeline      # Executa todas as verificações (CI/CD)
make build         # Alias para pipeline
make ci            # Alias para pipeline
```

### Limpeza

```bash
make clean         # Remove arquivos temporários e cache
```

## Workflow de Desenvolvimento

### 1. Antes de Commitar

```bash
# Execute o pipeline completo
make pipeline

# Se tudo passar, você está pronto para commitar
git add .
git commit -m "sua mensagem"
```

### 2. Criando um Release

```bash
# Release automático com validação
./scripts/automacao/release.sh 0.9.0

# Após revisar, faça push
git push origin main
git push origin v0.9.0
```

## Estrutura de Qualidade

### Metas de Qualidade

- **Cobertura de testes:** ≥95%
- **Score FAA:** ≥95/100
- **Type hints:** 100% (strict mode)
- **Linting:** Zero erros/warnings

### Ferramentas

| Ferramenta | Propósito | Configuração |
|------------|-----------|--------------|
| `pytest` | Testes unitários e cobertura | `pyproject.toml` |
| `mypy` | Verificação de tipos (strict) | `pyproject.toml` |
| `ruff` | Linting e formatação | `pyproject.toml` |
| `FAA` | Auditoria arquitetural | `scripts/faa/` |

## Scripts de Automação

Localizados em `scripts/automacao/`:

- `pipeline.sh` — Orquestrador completo (CI/CD)
- `lint.sh` — Linting com ruff
- `type_check.sh` — Verificação de tipos com mypy
- `test.sh` — Testes com pytest e cobertura
- `audit.sh` — Auditoria com FAA
- `release.sh` — Release automatizado

Todos os scripts podem ser executados diretamente ou via `Makefile`.

## Arquitetura de Testes

```
testes/
├── contract/     # Testes de contrato
├── unit/         # Testes unitários
├── integration/  # Testes de integração
├── e2e/          # Testes end-to-end
├── golden/       # Golden tests
└── cookbook/     # Testes de receitas reais
```

## Troubleshooting

### Pipeline falha no linting

```bash
# Corrija automaticamente
ruff check --fix kernel/ codigo/ scripts/faa/ testes/
ruff format kernel/ codigo/ scripts/faa/ testes/
```

### Pipeline falha em tipos

```bash
# Execute mypy diretamente para ver detalhes
mypy kernel/ codigo/ scripts/faa/ --strict --pretty
```

### Testes falham

```bash
# Execute testes específicos
pytest testes/unit/test_arquivo.py -v

# Execute com mais detalhes
pytest testes/ -vv --tb=long
```

## Contribuindo

1. Crie uma branch: `git checkout -b feature/minha-feature`
2. Faça mudanças e escreva testes
3. Execute `make pipeline` para validar
4. Commit: `git commit -m "feat: minha feature"`
5. Push e abra PR

## Convenções

### Commits

Seguimos [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — Nova funcionalidade
- `fix:` — Correção de bug
- `docs:` — Documentação
- `test:` — Adição/modificação de testes
- `refactor:` — Refatoração de código
- `chore:` — Tarefas de manutenção

### Código

- **Type hints:** Obrigatório em todas as funções públicas
- **Docstrings:** Obrigatório para funções/classes públicas
- **Testes:** Cobertura ≥95% para código novo
- **Formatação:** Deixe o ruff formatar automaticamente

## Links Úteis

- [Documentação completa](docs/)
- [Arquitetura](docs/02-arquitetura/)
- [Roadmap](ROADMAP-v1.0.md)
- [CHANGELOG](CHANGELOG.md)

---

**Versão atual:** v0.9.0  
**Status:** Beta — Em direção à v1.0
