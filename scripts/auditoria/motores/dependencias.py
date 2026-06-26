"""
Motor 11 — Dependências
Monta o grafo de relacionamentos entre dados reais e detecta ciclos e dependências ocultas.
"""

import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent.parent))

from models import AuditResult, MotorResult, Status, Severidade
from config import ROOT, PREFIXOS, ID_PATTERN
from utils import ler_frontmatter, listar_md


def _coletar_grafo() -> dict[str, list[str]]:
    """Retorna {id: [ids_referenciados]}."""
    grafo: dict[str, list[str]] = {}
    for diretorio in PREFIXOS.values():
        for arquivo in listar_md(diretorio):
            meta = ler_frontmatter(arquivo)
            if not meta:
                continue
            id_proprio = str(meta.get("id", ""))
            if not ID_PATTERN.match(id_proprio):
                continue
            refs = []
            for chave, valor in meta.items():
                if chave == "id":
                    continue
                if isinstance(valor, str) and ID_PATTERN.match(valor):
                    refs.append(valor)
                elif isinstance(valor, list):
                    refs += [v for v in valor if isinstance(v, str) and ID_PATTERN.match(v)]
            grafo[id_proprio] = refs
    return grafo


def _detectar_ciclos(grafo: dict[str, list[str]]) -> list[list[str]]:
    """DFS simples para detectar ciclos. Retorna lista de ciclos encontrados."""
    ciclos = []
    visitados: set[str] = set()
    em_stack: set[str] = set()
    stack: list[str] = []

    def dfs(no: str):
        visitados.add(no)
        em_stack.add(no)
        stack.append(no)
        for vizinho in grafo.get(no, []):
            if vizinho not in visitados:
                dfs(vizinho)
            elif vizinho in em_stack:
                idx = stack.index(vizinho)
                ciclos.append(stack[idx:] + [vizinho])
        stack.pop()
        em_stack.discard(no)

    for no in grafo:
        if no not in visitados:
            dfs(no)
    return ciclos


def executar() -> MotorResult:
    resultado = MotorResult(nome="Dependências")
    grafo = _coletar_grafo()

    resultado.resultados.append(AuditResult(
        id="DEP-001", motor="Dependências",
        titulo=f"Grafo construído: {len(grafo)} nós, {sum(len(v) for v in grafo.values())} arestas",
        status=Status.PASS, severidade=Severidade.INFO,
    ))

    ciclos = _detectar_ciclos(grafo)
    if ciclos:
        for ciclo in ciclos:
            resultado.resultados.append(AuditResult(
                id="DEP-002", motor="Dependências",
                titulo=f"Ciclo detectado: {' → '.join(ciclo)}",
                status=Status.FAIL, severidade=Severidade.CRITICA,
                sugestoes=["Revisar relacionamentos para eliminar dependência circular"],
            ))
    else:
        resultado.resultados.append(AuditResult(
            id="DEP-002", motor="Dependências",
            titulo="Nenhum ciclo de dependência detectado",
            status=Status.PASS, severidade=Severidade.INFO,
        ))

    # Nós isolados: apenas entidades que DEVERIAM ter referências (Receita, Execução, Experimento)
    PREFIXOS_COM_REFS_ESPERADAS = {"REC", "EXE", "EXP"}
    referenciados = {ref for refs in grafo.values() for ref in refs}
    for no, refs in grafo.items():
        prefixo = no.split("-")[0]
        if prefixo not in PREFIXOS_COM_REFS_ESPERADAS:
            continue  # Ingredientes, técnicas, equipamentos e observações podem existir sozinhos
        if not refs and no not in referenciados:
            resultado.resultados.append(AuditResult(
                id="DEP-003", motor="Dependências",
                titulo=f"Registro isolado (sem referências): {no}",
                status=Status.WARN, severidade=Severidade.BAIXA,
                sugestoes=["Verificar se o registro tem relacionamentos não documentados"],
            ))

    return resultado
