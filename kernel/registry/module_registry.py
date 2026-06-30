"""Registry determinístico de módulos e dependências."""
from __future__ import annotations

from collections import defaultdict, deque

from kernel.contracts.module import ContractError, ModuleContract


class RegistryError(RuntimeError):
    """Erro de registro ou resolução de dependências."""


class ModuleRegistry:
    """Mantém contratos de módulos sem acoplar o kernel à implementação."""

    def __init__(self) -> None:
        self._modules: dict[str, ModuleContract] = {}
        self._providers: dict[str, str] = {}

    def register(self, contract: ModuleContract) -> None:
        try:
            contract.validate()
        except ContractError as exc:
            raise RegistryError(str(exc)) from exc

        if contract.name in self._modules:
            raise RegistryError(f"módulo já registrado: {contract.name}")

        for capability in contract.provides:
            owner = self._providers.get(capability)
            if owner is not None:
                raise RegistryError(
                    f"capacidade {capability!r} já é fornecida por {owner!r}"
                )

        self._modules[contract.name] = contract
        for capability in contract.provides:
            self._providers[capability] = contract.name

    def get(self, name: str) -> ModuleContract:
        try:
            return self._modules[name]
        except KeyError as exc:
            raise RegistryError(f"módulo não registrado: {name}") from exc

    def provider_for(self, capability: str) -> ModuleContract:
        owner = self._providers.get(capability)
        if owner is None:
            raise RegistryError(f"capacidade sem provedor registrado: {capability}")
        return self._modules[owner]

    def validate(self) -> None:
        missing: list[str] = []
        for contract in self._modules.values():
            for capability in contract.requires:
                if capability not in self._providers:
                    missing.append(f"{contract.name} requer {capability}")
        if missing:
            raise RegistryError("dependências ausentes: " + "; ".join(sorted(missing)))
        self.resolve_order()

    def resolve_order(self) -> list[ModuleContract]:
        dependencies: dict[str, set[str]] = {name: set() for name in self._modules}
        dependents: dict[str, set[str]] = defaultdict(set)

        for name, contract in self._modules.items():
            for capability in contract.requires:
                provider = self._providers.get(capability)
                if provider is None:
                    raise RegistryError(f"{name} requer capacidade ausente: {capability}")
                if provider == name:
                    continue
                dependencies[name].add(provider)
                dependents[provider].add(name)

        ready = deque(sorted(name for name, deps in dependencies.items() if not deps))
        ordered: list[str] = []

        while ready:
            name = ready.popleft()
            ordered.append(name)
            for dependent in sorted(dependents[name]):
                dependencies[dependent].remove(name)
                if not dependencies[dependent]:
                    ready.append(dependent)

        if len(ordered) != len(self._modules):
            cycle = ", ".join(sorted(name for name, deps in dependencies.items() if deps))
            raise RegistryError(f"dependência circular detectada: {cycle}")

        return [self._modules[name] for name in ordered]

    def contracts(self) -> tuple[ModuleContract, ...]:
        return tuple(self._modules[name] for name in sorted(self._modules))
