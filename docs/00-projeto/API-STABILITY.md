# API Stability Policy — Política de Estabilidade de API

**Versão:** 1.0  
**Data:** 2026-07-01  
**Aplicável a partir de:** v1.0.0  
**Status:** Compromisso Formal

---

## 🎯 Compromisso

O SOE-CCG se compromete a manter **estabilidade de API pública** entre releases dentro da mesma versão major.

**APIs públicas não terão breaking changes entre v1.0 e v2.0.**

---

## 📐 Definições

### API Pública

**Definição:** Toda interface (função, classe, módulo) destinada ao uso direto por usuários ou integradores externos.

**Identificação:**
- Documentada em `docs/05-desenvolvimento/API-PUBLICA-v1.md`
- Exportada em `__init__.py` de módulos públicos
- Não prefixada com `_` (underscore)
- Possui docstring completa
- Mencionada em exemplos ou tutoriais

**Exemplos:**
```python
# API Pública
from codigo import parse_directory, importar
from kernel import bootstrap_system, KernelEvent
```

---

### API Interna

**Definição:** Toda interface destinada ao uso interno do projeto.

**Identificação:**
- Prefixada com `_` (underscore simples = protected)
- Prefixada com `__` (duplo underscore = private)
- Não exportada em `__init__.py`
- Não documentada em docs de API pública
- Marcada com `@internal` em docstring (opcional)

**Exemplos:**
```python
# API Interna
from codigo.parser import _parse_frontmatter  # protected
from kernel.core.kernel import __validate_state  # private
```

---

### Breaking Change

**Definição:** Mudança que quebra compatibilidade com código existente.

**Exemplos de Breaking Changes:**
- Remover função pública
- Renomear função pública
- Mudar assinatura (remover/renomear parâmetros)
- Mudar tipo de retorno de forma incompatível
- Mudar comportamento observável de forma incompatível
- Remover classe pública
- Mover módulo público

**Exemplos de NÃO Breaking Changes:**
- Adicionar nova função
- Adicionar parâmetro opcional (com default)
- Adicionar campo em retorno (se tipo flexível)
- Melhorar mensagem de erro
- Otimizar performance
- Corrigir bugs

---

## 📋 Regras de Estabilidade

### API Pública (v1.0 → v2.0)

```
✅ PERMITIDO:
  • Adicionar novas funções
  • Adicionar parâmetros opcionais (com default)
  • Adicionar novos módulos
  • Adicionar novas classes
  • Deprecar (com aviso) para remoção em v2.0
  • Melhorar documentação
  • Otimizar implementação (mesma interface)
  • Corrigir bugs
  • Adicionar type hints (se antes não tinha)

❌ PROIBIDO:
  • Remover funções públicas
  • Renomear funções públicas
  • Mudar assinatura de forma incompatível
  • Mudar comportamento observável incompativelmente
  • Remover parâmetros (mesmo opcionais)
  • Renomear parâmetros
  • Mudar tipo de retorno incompativelmente
  • Mudar exceções lançadas incompativelmente
```

---

### API Interna (sem garantias)

```
✅ PERMITIDO:
  • Qualquer mudança, a qualquer momento
  • Remover funções
  • Renomear funções
  • Mudar assinaturas
  • Mudar comportamento
  • Remover módulos inteiros

⚠️  AVISO:
  • Se você usa API interna, código pode quebrar
  • Sem avisos de deprecação
  • Sem período de transição
```

---

## 📊 Tabela de Estabilidade

| Módulo/API | Tipo | Estabilidade | Breaking Changes Permitidos |
|------------|------|--------------|----------------------------|
| `codigo.parse_directory()` | Pública | Alta | Não (até v2.0) |
| `codigo.importar()` | Pública | Alta | Não (até v2.0) |
| `kernel.bootstrap_system()` | Pública | Alta | Não (até v2.0) |
| `kernel.KernelEvent` | Pública | Alta | Não (até v2.0) |
| `codigo.parser._parse_frontmatter()` | Interna | Nenhuma | Sim (a qualquer momento) |
| `kernel.core.kernel.__validate_state()` | Interna | Nenhuma | Sim (a qualquer momento) |

---

## 🔄 Processo de Deprecação

### Deprecar API Pública (para remoção em v2.0)

**Passo 1: Marcar como deprecated**
```python
import warnings

def funcao_antiga(param: str) -> str:
    """Função antiga (DEPRECATED).
    
    .. deprecated:: 1.2.0
        Use :func:`funcao_nova` em vez disso.
        Será removida em v2.0.
    
    Args:
        param: Parâmetro
    
    Returns:
        Resultado
    """
    warnings.warn(
        "funcao_antiga está deprecated e será removida em v2.0. "
        "Use funcao_nova em vez disso.",
        DeprecationWarning,
        stacklevel=2
    )
    return funcao_nova(param)
```

**Passo 2: Documentar no CHANGELOG**
```markdown
## [v1.2.0] — 2026-09-01

### Deprecated

- `codigo.funcao_antiga()` — Use `codigo.funcao_nova()` em vez disso.
  Será removida em v2.0.
```

**Passo 3: Adicionar ao Migration Guide**
```markdown
# Migration Guide: v1.x → v2.0

## Remoções

### `codigo.funcao_antiga()`

**Removido em:** v2.0.0  
**Deprecated desde:** v1.2.0

**Antes:**
```python
from codigo import funcao_antiga
resultado = funcao_antiga("param")
```

**Depois:**
```python
from codigo import funcao_nova
resultado = funcao_nova("param")
```
```

**Passo 4: Manter por pelo menos 2 minor releases**

- Deprecated em v1.2.0
- Mantém em v1.3.0, v1.4.0, ...
- Remove apenas em v2.0.0

---

## 🚨 Exceções

### Quando Breaking Changes São Permitidos Antes de v2.0

**1. Bugfix Crítico de Segurança**

Se manter API atual representa risco de segurança:
- Documentar extensivamente
- Fornecer migration path
- Anunciar amplamente
- Incrementar minor version (v1.x.0 → v1.y.0)

**2. API Experimental**

Se API foi marcada como "experimental" desde o início:
- Pode mudar entre minor releases
- Deve ser claramente marcada em docstring:
  ```python
  def experimental_feature():
      """Feature experimental.
      
      .. warning::
          Esta API é experimental e pode mudar
          entre releases minor sem aviso prévio.
      """
  ```

**3. Correção de Bug Comportamental Grave**

Se comportamento atual é:
- Claramente incorreto
- Quebra princípios do sistema
- Causa perda de dados

Então:
- Documentar como bugfix (não breaking change)
- Explicar comportamento antigo e novo
- Fornecer workaround se possível

---

## 📚 Documentação de API Pública

### Documento Canônico

**Local:** `docs/05-desenvolvimento/API-PUBLICA-v1.md`

**Conteúdo:**
```markdown
# API Pública do SOE-CCG — v1.0

Todas as APIs listadas aqui são públicas e estáveis.

**Garantia:** Sem breaking changes até v2.0.

## Módulo: codigo

### parse_directory(path: Path) -> KnowledgeGraph

Parseia diretório e retorna grafo de conhecimento.

**Estável desde:** v1.0.0  
**Status:** Estável

...
```

---

## 🔍 Validação de Estabilidade

### Ferramentas

**1. API Compatibility Checker**

```bash
# scripts/automacao/check-api-compat.sh

# Compara API pública entre v1.x.0 e v1.y.0
# Detecta breaking changes
# Falha build se breaking change encontrado
```

**2. Testes de Compatibilidade**

```python
# testes/compatibility/test_api_v1.py

def test_parse_directory_signature_unchanged():
    """Valida que assinatura não mudou desde v1.0."""
    import inspect
    from codigo import parse_directory
    
    sig = inspect.signature(parse_directory)
    assert str(sig) == "(path: Path) -> KnowledgeGraph"
```

---

## 🎓 Exemplos

### ✅ Mudança Compatível

**v1.0.0:**
```python
def importar(grafo: KnowledgeGraph, db: Path) -> ImportResult:
    """Importa grafo para banco."""
    ...
```

**v1.1.0:**
```python
def importar(
    grafo: KnowledgeGraph,
    db: Path,
    dry_run: bool = False  # NOVO: parâmetro opcional
) -> ImportResult:
    """Importa grafo para banco.
    
    Args:
        grafo: Grafo de conhecimento
        db: Caminho do banco
        dry_run: Se True, simula sem persistir (novo em v1.1.0)
    """
    ...
```

**Por que é compatível:**
- Parâmetro é opcional (tem default)
- Código antigo continua funcionando:
  ```python
  importar(grafo, db)  # funciona em v1.0 e v1.1
  ```

---

### ❌ Mudança Incompatível (PROIBIDA)

**v1.0.0:**
```python
def importar(grafo: KnowledgeGraph, db: Path) -> ImportResult:
    ...
```

**v1.1.0 (PROIBIDO):**
```python
def importar(grafo: KnowledgeGraph, db: Path, mode: str) -> ImportResult:
    # ❌ BREAKING: parâmetro obrigatório adicionado
    ...
```

**Por que é incompatível:**
- Parâmetro é obrigatório (sem default)
- Código antigo quebra:
  ```python
  importar(grafo, db)  # funcionava em v1.0, falha em v1.1
  ```

---

## ✨ Filosofia

> "API pública é um contrato. Não quebramos contratos."

> "Se você depreca hoje, remove apenas em v2.0."

> "API interna pode mudar. API pública não pode (até v2.0)."

> "Estabilidade gera confiança. Confiança gera adoção."

---

## 📖 Referências

- `docs/05-desenvolvimento/API-PUBLICA-v1.md` — Lista de APIs públicas
- `docs/00-projeto/VERSIONING.md` — Política de versionamento
- `docs/00-projeto/RELEASE-GATE-v1.md` — Critérios de release
- Semantic Versioning: https://semver.org/

---

**Documento:** `API-STABILITY.md`  
**Tipo:** Compromisso Formal  
**Autoridade:** Máxima  
**Vigência:** v1.0.0 → indefinido
