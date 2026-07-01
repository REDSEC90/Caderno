# API INTERNA DO KERNEL

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Documentada

---

## Definição

A **API Interna** consiste em funções, classes e interfaces utilizadas exclusivamente dentro do próprio Kernel.

Código externo ao Kernel **não deve** acessar esta API.

Mudanças na API interna **não** requerem RFC, desde que a API pública permaneça inalterada.

---

## 1. Bootstrap (Interno)

### `kernel.bootstrap.build_kernel()`

**Assinatura:**
```python
def build_kernel(extra_modules: tuple[ModuleContract, ...] = ()) -> MicroKernel
```

**Responsabilidade:** Constrói e configura o Kernel sem inicializá-lo.

**Uso:** Chamada por `bootstrap_system()`.

**Status:** Interno

---

### `kernel.bootstrap.ensure_project_root_on_path()`

**Assinatura:**
```python
def ensure_project_root_on_path() -> None
```

**Responsabilidade:** Garante que a raiz do projeto esteja no `sys.path`.

**Uso:** Chamada por `bootstrap_system()`.

**Status:** Interno

---

## 2. Lifecycle (Interno)

### `kernel.lifecycle.KernelLifecycle`

**Gerenciador interno do ciclo de vida.**

#### Métodos Internos

##### `__init__()`
```python
def __init__(self) -> None
```
Inicializa o gerenciador de lifecycle.

##### `initialize()`
```python
def initialize(self) -> None
```
Transição: `UNINITIALIZED → INITIALIZED`

##### `start()`
```python
def start(self) -> None
```
Transição: `INITIALIZED → RUNNING`

##### `stop()`
```python
def stop(self) -> None
```
Transição: `RUNNING → STOPPED`

##### `_transition(expected: LifecycleState, target: LifecycleState)`
```python
def _transition(self, expected: LifecycleState, target: LifecycleState) -> None
```
Valida e executa transição de estado.

**Levanta:** `LifecycleError` se transição inválida.

**Status:** Interno

---

## 3. Contracts (Interno)

### `kernel.contracts.validator.ValidationResult`

**Resultado de validação da arquitetura.**

#### Atributos

```python
issues: list[ValidationIssue]
```

#### Métodos Internos

##### `add(code: str, message: str, path: str | None, severity: str)`
```python
def add(self, code: str, message: str, path: str | None = None, severity: str = "error") -> None
```
Adiciona um problema à lista.

##### `errors() -> list[ValidationIssue]`
```python
@property
def errors(self) -> list[ValidationIssue]
```
Retorna apenas problemas com severidade "error".

##### `ok() -> bool`
```python
def ok(self) -> bool
```
Retorna `True` se não há erros.

##### `raise_for_errors()`
```python
def raise_for_errors(self) -> None
```
Levanta `ArchitectureValidationError` se houver erros.

**Status:** Interno

---

### `kernel.contracts.validator.ValidationIssue`

**Problema detectado na validação.**

```python
@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str
    path: str | None
    severity: str
```

**Status:** Interno

---

### Funções de Validação Internas

#### `_validate_kernel_docs(result: ValidationResult)`
Valida existência de `kernel-docs/`.

#### `_validate_default_registry(result: ValidationResult)`
Valida existência de `kernel/registry/module_registry.py`.

#### `_validate_single_root_source(root: Path, result: ValidationResult)`
Valida que há apenas uma raiz de código.

#### `_validate_kernel_isolation(root: Path, result: ValidationResult)`
Valida que o Kernel não importa de fora do Kernel.

#### `_validate_sys_path_adapters(root: Path, result: ValidationResult)`
Valida que não há manipulações de `sys.path` fora de adaptadores.

#### `_is_sys_path_insert(node: ast.AST) -> bool`
Verifica se um nó AST é uma manipulação de `sys.path`.

#### `_python_files(root: Path)`
Retorna todos os arquivos Python no projeto.

**Status:** Todas internas

---

## 4. Registry (Interno)

### Atributos Internos

```python
_modules: dict[str, ModuleContract]     # Mapa nome → contrato
_capabilities: dict[str, str]           # Mapa capability → nome do módulo
```

**Status:** Interno

---

## Convenções de Nomenclatura

### Público vs Interno

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Público | PascalCase / snake_case | `ModuleContract`, `bootstrap_system()` |
| Interno (função/método) | `_prefixo` | `_transition()`, `_validate_kernel_docs()` |
| Interno (atributo) | `_prefixo` | `_modules`, `_capabilities` |

### Regras

1. Tudo que começa com `_` é interno
2. Tudo sem `_` é público ou candidato a público
3. Classes começam com maiúscula
4. Funções e métodos começam com minúscula

---

## Resumo

| Componente | Classes Internas | Funções Internas | Atributos Internos |
|------------|------------------|------------------|--------------------|
| bootstrap  | 0                | 2                | 0                  |
| contracts  | 2                | 7                | 1                  |
| lifecycle  | 1                | 1                | 1                  |
| registry   | 0                | 0                | 2                  |
| **Total**  | **3**            | **10**           | **4**              |

---

## Política de Mudanças

A API interna pode ser modificada livremente, desde que:

1. A API pública permaneça inalterada
2. Os testes de contrato continuem passando
3. As regras arquiteturais sejam respeitadas

---

**Documento:** `FASE-0-API-INTERNA.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
