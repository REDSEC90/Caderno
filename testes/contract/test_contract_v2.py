"""Testes para ModuleContract v2.0 (campos expandidos)."""
from __future__ import annotations

import pytest

from kernel.contracts.module import ContractError, ModuleContract


def test_contract_v2_com_todos_campos():
    """Contrato v2.0 completo deve validar."""
    contract = ModuleContract(
        name="test.module",
        version="1.2.3",
        author="Test Author",
        description="Test module",
        category="application",
        type="library",
        state="stable",
        provides=("test_cap",),
        requires=(),
        optional_requires=("optional_cap",),
        capabilities={"test_cap": "Test capability"},
        entrypoint="test.module",
        priority=100,
        lifecycle_policy="standard",
        permissions=("filesystem.read",),
        checksum="abc123",
        signature="xyz789",
        compatibility="1.0.0",
        deprecation=None,
    )
    contract.validate()  # Não deve levantar exceção


def test_contract_v1_ainda_funciona():
    """Contratos v1.0 devem continuar funcionando (retrocompatibilidade)."""
    contract = ModuleContract(
        name="test.module",
        version="1",
        provides=("test_cap",),
        requires=(),
        entrypoint="test.module",
        description="Test",
    )
    contract.validate()  # Não deve levantar exceção


def test_category_invalida():
    """Categoria inválida deve levantar ContractError."""
    contract = ModuleContract(
        name="test.module",
        category="invalid_category",
        provides=("test_cap",),
    )
    with pytest.raises(ContractError, match="category inválida"):
        contract.validate()


def test_type_invalido():
    """Tipo inválido deve levantar ContractError."""
    contract = ModuleContract(
        name="test.module",
        type="invalid_type",
        provides=("test_cap",),
    )
    with pytest.raises(ContractError, match="type inválido"):
        contract.validate()


def test_state_invalido():
    """Estado inválido deve levantar ContractError."""
    contract = ModuleContract(
        name="test.module",
        state="invalid_state",
        provides=("test_cap",),
    )
    with pytest.raises(ContractError, match="state inválido"):
        contract.validate()


def test_priority_fora_do_range():
    """Priority fora do range 0-999 deve levantar ContractError."""
    contract = ModuleContract(
        name="test.module",
        priority=1000,
        provides=("test_cap",),
    )
    with pytest.raises(ContractError, match="priority deve estar entre 0 e 999"):
        contract.validate()


def test_lifecycle_policy_invalida():
    """Lifecycle policy inválida deve levantar ContractError."""
    contract = ModuleContract(
        name="test.module",
        lifecycle_policy="invalid_policy",
        provides=("test_cap",),
    )
    with pytest.raises(ContractError, match="lifecycle_policy inválida"):
        contract.validate()


def test_optional_requires_conflita_com_requires():
    """Optional requires não pode estar em requires."""
    contract = ModuleContract(
        name="test.module",
        provides=("test_cap",),
        requires=("cap1",),
        optional_requires=("cap1",),
    )
    with pytest.raises(ContractError, match="capability em requires e optional_requires"):
        contract.validate()


def test_capabilities_com_chave_nao_em_provides():
    """Capabilities deve mapear apenas provides."""
    contract = ModuleContract(
        name="test.module",
        provides=("cap1",),
        capabilities={"cap1": "Valid", "cap2": "Invalid (not in provides)"},
    )
    with pytest.raises(ContractError, match="capabilities declaradas mas não em provides"):
        contract.validate()


def test_semver_relaxado_aceita_versao_simples():
    """Versões simples como '1' devem ser aceitas (compatibilidade v1.0)."""
    contract = ModuleContract(
        name="test.module",
        version="1",
        provides=("test_cap",),
    )
    contract.validate()  # Não deve levantar exceção


def test_semver_aceita_major_minor():
    """Versões MAJOR.MINOR devem ser aceitas."""
    contract = ModuleContract(
        name="test.module",
        version="1.2",
        provides=("test_cap",),
    )
    contract.validate()  # Não deve levantar exceção


def test_semver_aceita_major_minor_patch():
    """Versões MAJOR.MINOR.PATCH devem ser aceitas."""
    contract = ModuleContract(
        name="test.module",
        version="1.2.3",
        provides=("test_cap",),
    )
    contract.validate()  # Não deve levantar exceção


def test_semver_rejeita_formato_invalido():
    """Versões com formato inválido devem ser rejeitadas."""
    contract = ModuleContract(
        name="test.module",
        version="1.2.3.4",
        provides=("test_cap",),
    )
    with pytest.raises(ContractError, match="version deve seguir SemVer"):
        contract.validate()


def test_semver_rejeita_nao_numerico():
    """Versões com caracteres não-numéricos devem ser rejeitadas."""
    contract = ModuleContract(
        name="test.module",
        version="1.2.a",
        provides=("test_cap",),
    )
    with pytest.raises(ContractError, match="version deve conter apenas números"):
        contract.validate()


def test_valores_padrao_sao_validos():
    """Valores padrão devem passar na validação."""
    contract = ModuleContract(
        name="test.module",
        provides=("test_cap",),
    )
    contract.validate()
    
    # Verificar valores padrão
    assert contract.version == "1.0.0"
    assert contract.author == ""
    assert contract.description == ""
    assert contract.category == "application"
    assert contract.type == "library"
    assert contract.state == "stable"
    assert contract.optional_requires == ()
    assert contract.capabilities == {}
    assert contract.entrypoint is None
    assert contract.priority == 100
    assert contract.lifecycle_policy == "standard"
    assert contract.permissions == ()
    assert contract.checksum == ""
    assert contract.signature == ""
    assert contract.compatibility == "1.0.0"
    assert contract.deprecation is None
