# scripts/instalacao — Instalação e Verificação de Ambiente

Este diretório contém scripts para preparar e verificar o ambiente do SOE-CCG.

## Propósito

Garantir que qualquer colaborador consiga configurar o ambiente do zero, de forma reprodutível, sem depender de conhecimento implícito.

## Critérios de Uso

- Executar apenas uma vez por ambiente (idempotente por segurança, mas não necessário)
- Não requer permissões de root para dependências Python
- Deve funcionar em Linux com Python ≥ 3.11

## Scripts Planejados (v1.0)

| Script | Propósito |
|--------|-----------|
| `instalar.sh` | Instala dependências e prepara o ambiente completo |
| `verificar.sh` | Verifica que o ambiente está correto (versões, dependências, banco) |

## Sequência de Onboarding (após v1.0)

```bash
# 1. Clonar repositório
git clone <repo> && cd SOE-CCG

# 2. Instalar dependências
./scripts/instalacao/instalar.sh

# 3. Verificar ambiente
./scripts/instalacao/verificar.sh

# 4. Rodar testes
python3 -m pytest testes/
```

## Dependências Externas

- Python ≥ 3.11
- python-frontmatter
- PyYAML
- pytest (desenvolvimento)
- mypy (desenvolvimento)
