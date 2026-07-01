# FASE 2 — EXPANSÃO DO MODULECONTRACT

**Versão:** 1.0  
**Data:** 2026-07-01  
**Status:** Especificação (Implementação pendente)

---

## Objetivo

Expandir o `ModuleContract` atual com campos adicionais para transformá-lo em uma **identidade completa** do módulo.

---

## Implementação Proposta

### Arquivo: `kernel/contracts/module.py` (v2.0)

```python
"""Contrato declarativo para módulos registrados no microkernel."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


class ContractError(ValueError):
    """Erro de contrato detectado antes da inicialização de módulos."""


# Tipos auxiliares
CategoryType = Literal["kernel", "runtime", "application", "plugin", "tool"]
ModuleType = Literal["service", "library", "command", "daemon"]
StateType = Literal["experimental", "stable", "deprecated", "archived"]
LifecyclePolicyType = Literal["standard", "singleton", "transient"]


@dataclass(frozen=True)
class ModuleContract:
    """Descrição estrutural completa de um módulo."""
    
    # =========================================================================
    # IDENTIDADE (obrigatório)
    # =========================================================================
    
    name: str
    """Nome único do módulo em formato hierárquico (ex: 'runtime.parser')."""
    
    version: str = "1.0.0"
    """Versão semântica do módulo (SemVer 2.0)."""
    
    # =========================================================================
    # METADADOS (opcional)
    # =========================================================================
    
    author: str = ""
    """Autor ou time responsável pelo módulo."""
    
    description: str = ""
    """Descrição concisa do módulo (uma linha, ~100 chars)."""
    
    # =========================================================================
    # CATEGORIZAÇÃO (opcional)
    # =========================================================================
    
    category: CategoryType = "application"
    """Categoria do módulo: kernel, runtime, application, plugin, tool."""
    
    type: ModuleType = "library"
    """Tipo do módulo: service, library, command, daemon."""
    
    state: StateType = "stable"
    """Estado de maturidade: experimental, stable, deprecated, archived."""
    
    # =========================================================================
    # DEPENDÊNCIAS (obrigatório/opcional)
    # =========================================================================
    
    provides: tuple[str, ...] = field(default_factory=tuple)
    """Capabilities fornecidas (mínimo 1 obrigatório)."""
    
    requires: tuple[str, ...] = field(default_factory=tuple)
    """Capabilities requeridas (hard dependencies)."""
    
    optional_requires: tuple[str, ...] = field(default_factory=tuple)
    """Capabilities opcionais (soft dependencies)."""
    
    capabilities: dict[str, str] = field(default_factory=dict)
    """Mapa de capabilities com descrições."""
    
    # =========================================================================
    # EXECUÇÃO (opcional)
    # =========================================================================
    
    entrypoint: str | None = None
    """Caminho de importação do módulo (ex: 'codigo.parser')."""
    
    priority: int = 100
    """Prioridade de inicialização (0=crítico, 100=padrão, 999=baixa)."""
    
    lifecycle_policy: LifecyclePolicyType = "standard"
    """Política de ciclo de vida: standard, singleton, transient."""
    
    # =========================================================================
    # SEGURANÇA (futuro — Fase 9)
    # =========================================================================
    
    permissions: tuple[str, ...] = field(default_factory=tuple)
    """Permissões requeridas (ex: 'filesystem.read')."""
    
    checksum: str = ""
    """Hash SHA256 do módulo (integridade)."""
    
    signature: str = ""
    """Assinatura digital do contrato."""
    
    # =========================================================================
    # COMPATIBILIDADE (futuro — Fase 12)
    # =========================================================================
    
    compatibility: str = "1.0.0"
    """Versão mínima do Kernel requerida."""
    
    deprecation: str | None = None
    """Mensagem de descontinuação (se aplicável)."""
    
    # =========================================================================
    # VALIDAÇÃO
    # =========================================================================
    
    def validate(self) -> None:
        """Valida estrutura do contrato."""
        
        # Validações básicas (v1.0)
        if not self.name:
            raise ContractError("ModuleContract.name é obrigatório")
        
        if not self.version:
            raise ContractError(f"{self.name}: version é obrigatório")
        
        if not self.provides:
            raise ContractError(
                f"{self.name}: provides deve declarar ao menos uma capacidade"
            )
        
        # Validação de conflito provides/requires
        duplicated = set(self.provides).intersection(self.requires)
        if duplicated:
            names = ", ".join(sorted(duplicated))
            raise ContractError(
                f"{self.name}: capacidade simultaneamente provides/requires: {names}"
            )
        
        # Validações expandidas (v2.0)
        self._validate_semver()
        self._validate_category()
        self._validate_type()
        self._validate_state()
        self._validate_priority()
        self._validate_lifecycle_policy()
        self._validate_optional_requires()
        self._validate_capabilities()
    
    def _validate_semver(self) -> None:
        """Valida formato SemVer da versão."""
        parts = self.version.split(".")
        if len(parts) != 3:
            raise ContractError(
                f"{self.name}: version deve seguir SemVer (MAJOR.MINOR.PATCH)"
            )
        try:
            for part in parts:
                int(part)
        except ValueError:
            raise ContractError(
                f"{self.name}: version deve conter apenas números"
            ) from None
    
    def _validate_category(self) -> None:
        """Valida categoria do módulo."""
        valid = {"kernel", "runtime", "application", "plugin", "tool"}
        if self.category not in valid:
            raise ContractError(
                f"{self.name}: category inválida '{self.category}' "
                f"(válidas: {', '.join(sorted(valid))})"
            )
    
    def _validate_type(self) -> None:
        """Valida tipo do módulo."""
        valid = {"service", "library", "command", "daemon"}
        if self.type not in valid:
            raise ContractError(
                f"{self.name}: type inválido '{self.type}' "
                f"(válidos: {', '.join(sorted(valid))})"
            )
    
    def _validate_state(self) -> None:
        """Valida estado de maturidade."""
        valid = {"experimental", "stable", "deprecated", "archived"}
        if self.state not in valid:
            raise ContractError(
                f"{self.name}: state inválido '{self.state}' "
                f"(válidos: {', '.join(sorted(valid))})"
            )
    
    def _validate_priority(self) -> None:
        """Valida prioridade de inicialização."""
        if not (0 <= self.priority <= 999):
            raise ContractError(
                f"{self.name}: priority deve estar entre 0 e 999 (atual: {self.priority})"
            )
    
    def _validate_lifecycle_policy(self) -> None:
        """Valida política de ciclo de vida."""
        valid = {"standard", "singleton", "transient"}
        if self.lifecycle_policy not in valid:
            raise ContractError(
                f"{self.name}: lifecycle_policy inválida '{self.lifecycle_policy}' "
                f"(válidas: {', '.join(sorted(valid))})"
            )
    
    def _validate_optional_requires(self) -> None:
        """Valida que optional_requires não conflita com requires."""
        conflict = set(self.requires).intersection(self.optional_requires)
        if conflict:
            names = ", ".join(sorted(conflict))
            raise ContractError(
                f"{self.name}: capability em requires e optional_requires: {names}"
            )
    
    def _validate_capabilities(self) -> None:
        """Valida que capabilities mapeiam provides corretamente."""
        if self.capabilities:
            provided = set(self.provides)
            declared = set(self.capabilities.keys())
            extra = declared - provided
            if extra:
                names = ", ".join(sorted(extra))
                raise ContractError(
                    f"{self.name}: capabilities declaradas mas não em provides: {names}"
                )
```

---

## Mudanças em Relação à v1.0

### Campos Adicionados

1. ✅ `author` — Autor ou time
2. ✅ `category` — Categorização do módulo
3. ✅ `type` — Tipo de módulo
4. ✅ `state` — Estado de maturidade
5. ✅ `optional_requires` — Dependências opcionais
6. ✅ `capabilities` — Descrições de capabilities
7. ✅ `priority` — Prioridade de inicialização
8. ✅ `lifecycle_policy` — Política de ciclo de vida
9. ✅ `permissions` — Permissões (Fase 9)
10. ✅ `checksum` — Hash de integridade (Fase 9)
11. ✅ `signature` — Assinatura digital (Fase 9)
12. ✅ `compatibility` — Versão mínima do Kernel (Fase 12)
13. ✅ `deprecation` — Mensagem de descontinuação (Fase 12)

### Validações Adicionadas

1. ✅ Validação de SemVer
2. ✅ Validação de categoria
3. ✅ Validação de tipo
4. ✅ Validação de estado
5. ✅ Validação de prioridade (0-999)
6. ✅ Validação de lifecycle_policy
7. ✅ Validação de optional_requires (não pode conflitar com requires)
8. ✅ Validação de capabilities (deve mapear provides)

### Tipos Auxiliares

Adicionados tipos `Literal` para garantir type-safety:
- `CategoryType`
- `ModuleType`
- `StateType`
- `LifecyclePolicyType`

---

## Impacto

### Compatibilidade com v1.0

✅ **Retrocompatível**

Todos os campos novos têm valores padrão, então contratos v1.0 continuam funcionando:

```python
# v1.0 (ainda funciona)
ModuleContract(
    name="runtime.parser",
    version="1",
    provides=("parser",),
    requires=("ir",),
)

# v2.0 (expandido)
ModuleContract(
    name="runtime.parser",
    version="1.2.3",
    author="SOE-CCG Team",
    category="runtime",
    type="library",
    state="stable",
    provides=("parser",),
    requires=("ir",),
    capabilities={"parser": "Parse Markdown → KnowledgeGraph"},
    priority=100,
)
```

### Módulos Afetados

Nenhum módulo precisa ser modificado imediatamente.

Recomenda-se atualizar gradualmente para usar os novos campos.

---

## Cronograma de Implementação

| Etapa | Descrição | Status |
|-------|-----------|--------|
| 1 | Especificação completa | ✅ Esta fase |
| 2 | Implementação do código | ⏳ Próximo |
| 3 | Testes de validação | ⏳ Após implementação |
| 4 | Atualização de DEFAULT_MODULES | ⏳ Após testes |
| 5 | Documentação de migração | ⏳ Final da fase |

---

## Próximos Passos

1. Implementar código proposto em `kernel/contracts/module.py`
2. Adicionar testes para novos campos
3. Atualizar `DEFAULT_MODULES` em `bootstrap.py` com novos campos
4. Criar guia de migração para contratos existentes

---

**Documento:** `FASE-2-EXPANSAO-CONTRACT.md`  
**Versão:** 1.0  
**Data:** 2026-07-01
