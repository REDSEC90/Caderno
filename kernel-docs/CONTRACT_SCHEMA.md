# CONTRACT SCHEMA — ESPECIFICAÇÃO COMPLETA

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Normativo

---

## Objetivo

Este documento define **todos os campos obrigatórios e opcionais** de um `ModuleContract`.

O contrato é a **identidade oficial** de um módulo no Kernel.

---

## Campos do Contrato

### 1. `name` (obrigatório)

**Tipo:** `str`

**Descrição:** Nome único do módulo em formato hierárquico.

**Formato:** `categoria.nome` ou `categoria.subcategoria.nome`

**Exemplos:**
- `kernel.paths`
- `runtime.parser`
- `application.cli`

**Validação:**
- ✅ Não pode ser vazio
- ✅ Deve ser único no sistema
- ✅ Recomenda-se snake_case para componentes
- ✅ Recomenda-se categorização hierárquica

---

### 2. `version` (obrigatório)

**Tipo:** `str`

**Descrição:** Versão semântica do módulo.

**Formato:** `MAJOR.MINOR.PATCH` (SemVer 2.0)

**Exemplos:**
- `"1.0.0"` — Release inicial
- `"1.2.3"` — Versão com patches
- `"2.0.0"` — Breaking change

**Padrão:** `"1"`

**Validação:**
- ✅ Não pode ser vazio
- ✅ Recomenda-se SemVer completo

---

### 3. `provides` (obrigatório)

**Tipo:** `tuple[str, ...]`

**Descrição:** Capabilities (capacidades) fornecidas pelo módulo.

**Exemplos:**
- `("parser",)`
- `("ir", "graph")`
- `("logging", "metrics")`

**Validação:**
- ✅ Deve conter pelo menos uma capability
- ✅ Nenhuma capability pode estar simultaneamente em `provides` e `requires`
- ✅ Capabilities devem ser únicas no sistema (apenas um provedor)

---

### 4. `requires` (opcional)

**Tipo:** `tuple[str, ...]`

**Descrição:** Capabilities requeridas de outros módulos.

**Padrão:** `()`

**Exemplos:**
- `("ir",)`
- `("parser", "validator")`

**Validação:**
- ✅ Todas as capabilities devem ter provedor registrado
- ✅ Não pode haver dependências circulares
- ✅ Nenhuma capability pode estar simultaneamente em `provides` e `requires`

---

### 5. `entrypoint` (opcional)

**Tipo:** `str | None`

**Descrição:** Caminho de importação do módulo (formato Python).

**Formato:** `pacote.modulo` ou `pacote.subpacote.modulo`

**Exemplos:**
- `"kernel.shared.paths"`
- `"codigo.parser"`
- `"scripts.faa.faa"`

**Padrão:** `None`

**Validação:**
- ✅ Deve ser importável no momento de inicialização
- ✅ Recomenda-se especificar quando o módulo possui código executável

---

### 6. `description` (opcional)

**Tipo:** `str`

**Descrição:** Descrição concisa do módulo (uma linha).

**Padrão:** `""`

**Exemplos:**
- `"Parser Markdown para KnowledgeGraph."`
- `"Validação estrutural do grafo."`
- `"Fonte canônica de paths do projeto."`

**Validação:**
- ✅ Recomenda-se não exceder 100 caracteres
- ✅ Recomenda-se terminar com ponto

---

### 7. `author` (futuro — Fase 2+)

**Tipo:** `str`

**Descrição:** Autor ou time responsável pelo módulo.

**Formato:** `"Nome <email>"` ou `"Nome"`

**Exemplos:**
- `"SOE-CCG Team"`
- `"João Silva <joao@example.com>"`

**Padrão:** `""`

**Status:** Não implementado ainda

---

### 8. `category` (futuro — Fase 2+)

**Tipo:** `str`

**Descrição:** Categoria do módulo.

**Valores permitidos:**
- `"kernel"` — Componente do Kernel
- `"runtime"` — Motor de execução
- `"application"` — Aplicação
- `"plugin"` — Plugin externo
- `"tool"` — Ferramenta utilitária

**Padrão:** `"application"`

**Status:** Não implementado ainda

---

### 9. `type` (futuro — Fase 2+)

**Tipo:** `str`

**Descrição:** Tipo do módulo.

**Valores permitidos:**
- `"service"` — Serviço (longa duração)
- `"library"` — Biblioteca (sem estado)
- `"command"` — Comando (execução única)
- `"daemon"` — Daemon (background)

**Padrão:** `"library"`

**Status:** Não implementado ainda

---

### 10. `state` (futuro — Fase 2+)

**Tipo:** `str`

**Descrição:** Estado de maturidade do módulo.

**Valores permitidos:**
- `"experimental"` — Experimental (pode mudar)
- `"stable"` — Estável (API garantida)
- `"deprecated"` — Descontinuado (será removido)
- `"archived"` — Arquivado (somente leitura)

**Padrão:** `"stable"`

**Status:** Não implementado ainda

---

### 11. `capabilities` (futuro — Fase 2+)

**Tipo:** `dict[str, str]`

**Descrição:** Mapa de capabilities com descrições.

**Exemplo:**
```python
{
    "parser": "Parse Markdown para KnowledgeGraph",
    "validator": "Valida estrutura do grafo"
}
```

**Padrão:** `{}`

**Status:** Não implementado ainda

---

### 12. `optional_requires` (futuro — Fase 2+)

**Tipo:** `tuple[str, ...]`

**Descrição:** Capabilities opcionais (funcionalidade adicional se disponíveis).

**Exemplo:**
```python
optional_requires=("logging", "metrics")
```

**Padrão:** `()`

**Status:** Não implementado ainda

---

### 13. `priority` (futuro — Fase 2+)

**Tipo:** `int`

**Descrição:** Prioridade de inicialização (menor = primeiro).

**Valores:**
- `0` — Crítico (Kernel Core)
- `10` — Kernel Runtime
- `50` — Kernel Services
- `100` — Aplicações (padrão)
- `999` — Baixa prioridade

**Padrão:** `100`

**Status:** Não implementado ainda

---

### 14. `permissions` (futuro — Fase 9 — Segurança)

**Tipo:** `tuple[str, ...]`

**Descrição:** Permissões requeridas pelo módulo.

**Exemplos:**
- `("filesystem.read", "filesystem.write")`
- `("network.http", "network.https")`
- `("system.execute")`

**Padrão:** `()`

**Status:** Não implementado ainda

---

### 15. `checksum` (futuro — Fase 9 — Segurança)

**Tipo:** `str`

**Descrição:** Hash SHA256 do módulo (integridade).

**Formato:** Hexadecimal (64 caracteres)

**Exemplo:** `"a3b5c7d9e1f2..."`

**Padrão:** `""`

**Status:** Não implementado ainda

---

### 16. `signature` (futuro — Fase 9 — Segurança)

**Tipo:** `str`

**Descrição:** Assinatura digital do contrato.

**Formato:** Base64

**Padrão:** `""`

**Status:** Não implementado ainda

---

### 17. `compatibility` (futuro — Fase 12 — Versionamento)

**Tipo:** `str`

**Descrição:** Versão mínima do Kernel requerida.

**Formato:** `MAJOR.MINOR.PATCH`

**Exemplo:** `"1.0.0"`

**Padrão:** `"1.0.0"`

**Status:** Não implementado ainda

---

### 18. `deprecation` (futuro — Fase 12 — Versionamento)

**Tipo:** `str | None`

**Descrição:** Mensagem de descontinuação (se aplicável).

**Exemplo:** `"Este módulo será removido na v2.0. Use 'novo.modulo'."`

**Padrão:** `None`

**Status:** Não implementado ainda

---

### 19. `lifecycle_policy` (futuro — Fase 3 — Lifecycle)

**Tipo:** `str`

**Descrição:** Política de ciclo de vida.

**Valores permitidos:**
- `"standard"` — Ciclo padrão (CREATED → INITIALIZED → RUNNING → STOPPED)
- `"singleton"` — Instância única
- `"transient"` — Instância temporária

**Padrão:** `"standard"`

**Status:** Não implementado ainda

---

## Schema Resumido

### Estado Atual (v1.0)

```python
@dataclass(frozen=True)
class ModuleContract:
    name: str                          # obrigatório
    version: str = "1"                 # obrigatório (padrão: "1")
    provides: tuple[str, ...] = ()     # obrigatório (mínimo 1)
    requires: tuple[str, ...] = ()     # opcional
    entrypoint: str | None = None      # opcional
    description: str = ""              # opcional
```

### Estado Futuro (v2.0 — após Fase 2)

```python
@dataclass(frozen=True)
class ModuleContract:
    # Identidade
    name: str
    version: str = "1.0.0"
    author: str = ""
    description: str = ""
    
    # Categorização
    category: str = "application"
    type: str = "library"
    state: str = "stable"
    
    # Dependências
    provides: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    optional_requires: tuple[str, ...] = ()
    capabilities: dict[str, str] = field(default_factory=dict)
    
    # Execução
    entrypoint: str | None = None
    priority: int = 100
    lifecycle_policy: str = "standard"
    
    # Segurança (Fase 9)
    permissions: tuple[str, ...] = ()
    checksum: str = ""
    signature: str = ""
    
    # Compatibilidade (Fase 12)
    compatibility: str = "1.0.0"
    deprecation: str | None = None
```

---

## Validações

### Validações Atuais (v1.0)

1. ✅ `name` não pode ser vazio
2. ✅ `version` não pode ser vazio
3. ✅ `provides` deve ter ao menos uma capability
4. ✅ Nenhuma capability pode estar em `provides` e `requires` simultaneamente

### Validações Futuras (v2.0+)

5. ✅ `version` deve seguir SemVer
6. ✅ `category` deve ser um dos valores permitidos
7. ✅ `type` deve ser um dos valores permitidos
8. ✅ `state` deve ser um dos valores permitidos
9. ✅ `priority` deve estar entre 0 e 999
10. ✅ `checksum` deve ser SHA256 válido (se especificado)
11. ✅ `signature` deve ser válida (se especificada)
12. ✅ `compatibility` deve seguir SemVer
13. ✅ `lifecycle_policy` deve ser um dos valores permitidos

---

## Evolução do Schema

| Fase | Campos Adicionados | Status |
|------|-------------------|--------|
| Inicial | `name`, `version`, `provides`, `requires`, `entrypoint`, `description` | ✅ Implementado |
| Fase 2 | `author`, `category`, `type`, `state`, `capabilities`, `optional_requires`, `priority` | 🔄 Esta fase |
| Fase 3 | `lifecycle_policy` | ⏳ Futuro |
| Fase 9 | `permissions`, `checksum`, `signature` | ⏳ Futuro |
| Fase 12 | `compatibility`, `deprecation` | ⏳ Futuro |

---

## Exemplo Completo (Futuro)

```python
ModuleContract(
    # Identidade
    name="runtime.parser",
    version="1.2.3",
    author="SOE-CCG Team <team@soe-ccg.org>",
    description="Parser Markdown para KnowledgeGraph.",
    
    # Categorização
    category="runtime",
    type="library",
    state="stable",
    
    # Dependências
    provides=("parser",),
    requires=("ir",),
    optional_requires=("logging",),
    capabilities={
        "parser": "Parse Markdown → KnowledgeGraph"
    },
    
    # Execução
    entrypoint="codigo.parser",
    priority=100,
    lifecycle_policy="standard",
    
    # Segurança
    permissions=("filesystem.read",),
    checksum="a3b5c7d9e1f2...",
    signature="LS0tLS1CRU...",
    
    # Compatibilidade
    compatibility="1.0.0",
    deprecation=None
)
```

---

**Documento:** `CONTRACT_SCHEMA.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
