"""Registry determinístico de módulos e dependências."""
from __future__ import annotations

import re
from collections import defaultdict, deque
from typing import Any

from kernel.contracts.module import (
    CategoryType,
    ContractError,
    ModuleContract,
    ModuleType,
    StateType,
)


class RegistryError(RuntimeError):
    """Erro de registro ou resolução de dependências."""


class ModuleRegistry:
    """Mantém contratos de módulos sem acoplar o kernel à implementação."""

    def __init__(self) -> None:
        self._modules: dict[str, ModuleContract] = {}
        self._providers: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Operações de escrita
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Consultas pontuais
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Consultas avançadas (Fase 4)
    # ------------------------------------------------------------------

    def find(self, name_pattern: str) -> list[ModuleContract]:
        """Busca módulos cujo nome casa com o padrão regex.

        Args:
            name_pattern: Expressão regular aplicada ao nome do módulo.

        Returns:
            Lista de contratos cujo nome satisfaz o padrão, ordenada
            alfabeticamente.

        Raises:
            RegistryError: Se o padrão regex for inválido.
        """
        try:
            compiled = re.compile(name_pattern)
        except re.error as exc:
            raise RegistryError(f"padrão regex inválido: {name_pattern!r}") from exc

        return [
            contract
            for name, contract in sorted(self._modules.items())
            if compiled.search(name)
        ]

    def find_by_category(self, category: CategoryType) -> list[ModuleContract]:
        """Busca módulos por categoria.

        Args:
            category: Categoria a filtrar ("kernel", "runtime", "application",
                      "plugin" ou "tool").

        Returns:
            Lista de contratos na categoria, ordenada alfabeticamente por nome.
        """
        return [
            contract
            for name, contract in sorted(self._modules.items())
            if contract.category == category
        ]

    def find_by_type(self, module_type: ModuleType) -> list[ModuleContract]:
        """Busca módulos por tipo.

        Args:
            module_type: Tipo a filtrar ("service", "library", "command" ou
                         "daemon").

        Returns:
            Lista de contratos do tipo, ordenada alfabeticamente por nome.
        """
        return [
            contract
            for name, contract in sorted(self._modules.items())
            if contract.type == module_type
        ]

    def find_by_capability(self, capability: str) -> list[ModuleContract]:
        """Busca módulos que fornecem (provides) a capability indicada.

        Args:
            capability: Nome exato da capability procurada.

        Returns:
            Lista de contratos que proveem a capability (0 ou 1 elemento,
            pois o registry impede duplicatas), ordenada por nome.
        """
        return [
            contract
            for name, contract in sorted(self._modules.items())
            if capability in contract.provides
        ]

    def find_by_state(self, state: StateType) -> list[ModuleContract]:
        """Busca módulos pelo estado de maturidade.

        Args:
            state: Estado a filtrar ("experimental", "stable", "deprecated"
                   ou "archived").

        Returns:
            Lista de contratos no estado, ordenada alfabeticamente por nome.
        """
        return [
            contract
            for name, contract in sorted(self._modules.items())
            if contract.state == state
        ]

    def dependency_graph(self) -> dict[str, list[str]]:
        """Retorna o grafo de dependências entre módulos.

        Cada chave é o nome de um módulo; o valor é a lista de nomes dos
        módulos dos quais ele depende diretamente (via ``requires``).

        Returns:
            Dicionário ``{módulo: [dependências diretas]}``.  Módulos sem
            dependências aparecem com lista vazia.
        """
        graph: dict[str, list[str]] = {}
        for name, contract in sorted(self._modules.items()):
            deps: list[str] = []
            for capability in contract.requires:
                provider = self._providers.get(capability)
                if provider is not None and provider != name:
                    if provider not in deps:
                        deps.append(provider)
            graph[name] = sorted(deps)
        return graph

    def health(self) -> dict[str, Any]:
        """Retorna o status de saúde do registry.

        Realiza as mesmas verificações de ``validate()`` mas em vez de
        levantar exceção, retorna um dicionário descritivo.

        Returns:
            Dicionário com as chaves:

            - ``healthy`` (bool) — True se sem problemas.
            - ``total_modules`` (int) — Número de módulos registrados.
            - ``missing_dependencies`` (list[str]) — Dependências ausentes.
            - ``circular_dependencies`` (list[str]) — Módulos em ciclo.
            - ``deprecated_modules`` (list[str]) — Módulos descontinuados.
        """
        missing: list[str] = []
        for contract in self._modules.values():
            for capability in contract.requires:
                if capability not in self._providers:
                    missing.append(f"{contract.name} requer {capability!r}")

        circular: list[str] = []
        try:
            self.resolve_order()
        except RegistryError as exc:
            msg = str(exc)
            if "circular" in msg:
                # Extrai os nomes do módulo da mensagem de erro
                circular = [
                    name.strip()
                    for name in msg.split(":", 1)[-1].split(",")
                ]

        deprecated = [
            contract.name
            for contract in self._modules.values()
            if contract.state == "deprecated"
        ]

        healthy = not missing and not circular

        return {
            "healthy": healthy,
            "total_modules": len(self._modules),
            "missing_dependencies": sorted(missing),
            "circular_dependencies": sorted(circular),
            "deprecated_modules": sorted(deprecated),
        }

    def stats(self) -> dict[str, int]:
        """Retorna estatísticas de contagem do registry.

        Returns:
            Dicionário com:

            - ``total_modules`` — Total de módulos registrados.
            - ``total_capabilities`` — Total de capabilities declaradas em
              ``provides`` (soma de todos os módulos).
            - ``by_category_kernel`` — Módulos na categoria "kernel".
            - ``by_category_runtime`` — Módulos na categoria "runtime".
            - ``by_category_application`` — Módulos na categoria "application".
            - ``by_category_plugin`` — Módulos na categoria "plugin".
            - ``by_category_tool`` — Módulos na categoria "tool".
            - ``by_type_service`` — Módulos do tipo "service".
            - ``by_type_library`` — Módulos do tipo "library".
            - ``by_type_command`` — Módulos do tipo "command".
            - ``by_type_daemon`` — Módulos do tipo "daemon".
            - ``by_state_stable`` — Módulos no estado "stable".
            - ``by_state_experimental`` — Módulos no estado "experimental".
            - ``by_state_deprecated`` — Módulos no estado "deprecated".
            - ``by_state_archived`` — Módulos no estado "archived".
        """
        modules = list(self._modules.values())
        total_caps = sum(len(c.provides) for c in modules)

        return {
            "total_modules": len(modules),
            "total_capabilities": total_caps,
            # por categoria
            "by_category_kernel": sum(1 for c in modules if c.category == "kernel"),
            "by_category_runtime": sum(1 for c in modules if c.category == "runtime"),
            "by_category_application": sum(1 for c in modules if c.category == "application"),
            "by_category_plugin": sum(1 for c in modules if c.category == "plugin"),
            "by_category_tool": sum(1 for c in modules if c.category == "tool"),
            # por tipo
            "by_type_service": sum(1 for c in modules if c.type == "service"),
            "by_type_library": sum(1 for c in modules if c.type == "library"),
            "by_type_command": sum(1 for c in modules if c.type == "command"),
            "by_type_daemon": sum(1 for c in modules if c.type == "daemon"),
            # por estado
            "by_state_stable": sum(1 for c in modules if c.state == "stable"),
            "by_state_experimental": sum(1 for c in modules if c.state == "experimental"),
            "by_state_deprecated": sum(1 for c in modules if c.state == "deprecated"),
            "by_state_archived": sum(1 for c in modules if c.state == "archived"),
        }

    # ------------------------------------------------------------------
    # Validação e ordenação
    # ------------------------------------------------------------------

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
