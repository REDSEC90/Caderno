"""Orquestrador central do FAA v2"""
from pathlib import Path
from core.scanner import scan_tree
from core.rules import RULES
from engines.structure_engine import analyze_structure
from issues.detector import detect_issues, classify_issues
from planner.prioritizer import generate_plan, generate_roadmap
from planner.roadmap_engine import generate_roadmap as generate_roadmap_v2
from metrics.coverage import compute_metrics
from state.state_store import save_state, load_state, save_snapshot
from config import CONFIG

class FAA:
    """Framework de Auditoria Arquitetural v2"""
    
    def __init__(self, root: Path = CONFIG.root):
        self.root = root
        self.nodes = []
        self.structure = {}
        self.issues = {}
        self.plan = []
        self.metrics = {}
        self.state = {}
    
    def run(self, save_snapshot_flag: bool = False) -> dict:
        """Executa auditoria completa"""
        
        # 1. Coleta
        self.nodes = scan_tree(self.root)
        
        # 2. Estrutura
        self.structure = analyze_structure(self.nodes, self.root)
        
        # 3. Validação
        raw_issues = detect_issues(self.nodes, RULES)
        self.issues = classify_issues(raw_issues)
        
        # 4. Planejamento
        tasks = generate_plan(self.issues)
        self.plan = generate_roadmap(tasks)
        
        # 4.1 Roadmap estruturado (epics + tasks)
        self.roadmap = generate_roadmap_v2(self.issues)
        
        # 5. Métricas
        self.metrics = compute_metrics(self.nodes, self.issues, self.structure)
        
        # 6. Estado
        self.state = {
            "metrics": self.metrics,
            "structure": self.structure,
            "issues": self.issues,
            "plan": self.plan,
            "roadmap": self.roadmap
        }
        
        # 7. Persistência
        save_state(self.state, CONFIG.state_path)
        
        if save_snapshot_flag:
            save_snapshot(self.state, CONFIG.snapshot_dir)
        
        return self.state
    
    def status(self) -> dict:
        """Retorna status atual (lê do cache ou executa)"""
        cached = load_state(CONFIG.state_path)
        if cached and "metrics" in cached:
            return cached
        return self.run()
