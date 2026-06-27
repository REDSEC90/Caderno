"""
Exemplo de regras customizadas para o FAA v2

Para adicionar novas regras:
1. Crie uma Rule com nome, severidade, função de validação e ação
2. Adicione à lista CUSTOM_RULES
3. Importe em core/rules.py e adicione a RULES
"""

from core.rules import Rule, Severity

# Exemplo: validar que arquivos de domínio tenham prefixo correto
def check_domain_prefix(node):
    if "docs/01-dominio/" in node.relative:
        valid_prefixes = ["entidade-", "contrato-", "template-", "glossario-", "catalogacao-", "linguagem-"]
        return any(node.path.name.startswith(p) for p in valid_prefixes) or node.path.name in ["README.md"]
    return True

# Exemplo: validar encoding UTF-8
def check_encoding(node):
    if node.path.suffix in {".md", ".txt"}:
        try:
            node.path.read_text(encoding="utf-8")
            return True
        except UnicodeDecodeError:
            return False
    return True

# Exemplo: validar tamanho de arquivo
def check_file_size(node):
    if node.path.suffix == ".md":
        size_mb = node.path.stat().st_size / (1024 * 1024)
        return size_mb < 2.0  # Max 2MB por arquivo .md
    return True

# Regras customizadas
CUSTOM_RULES = [
    Rule(
        "domain_naming",
        Severity.WARNING,
        check_domain_prefix,
        "Renomear com prefixo válido: entidade-, contrato-, template-"
    ),
    Rule(
        "utf8_encoding",
        Severity.CRITICAL,
        check_encoding,
        "Converter arquivo para UTF-8"
    ),
    Rule(
        "file_size_limit",
        Severity.WARNING,
        check_file_size,
        "Dividir arquivo em partes menores (<2MB)"
    ),
]

# Para ativar, adicione em core/rules.py:
# from plugins.custom_rules import CUSTOM_RULES
# RULES.extend(CUSTOM_RULES)
