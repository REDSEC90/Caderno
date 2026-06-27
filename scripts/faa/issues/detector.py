"""Detector e classificador de issues"""
from typing import List, Dict
from dataclasses import asdict
from core.rules import Issue, Severity, validate_node, RULES

def detect_issues(nodes, rules=RULES) -> List[Issue]:
    """Detecta todos os problemas no sistema"""
    all_issues = []
    
    for node in nodes:
        issues = validate_node(node, rules)
        all_issues.extend(issues)
    
    return all_issues

def classify_issues(issues: List[Issue]) -> Dict:
    """Classifica issues por severidade"""
    classified = {
        "critical": [],
        "warnings": [],
        "info": []
    }
    
    for issue in issues:
        issue_dict = asdict(issue)
        issue_dict["severity"] = issue.severity.value  # Enum -> string
        
        if issue.severity == Severity.CRITICAL:
            classified["critical"].append(issue_dict)
        elif issue.severity == Severity.WARNING:
            classified["warnings"].append(issue_dict)
        else:
            classified["info"].append(issue_dict)
    
    return {
        **classified,
        "counts": {
            "critical": len(classified["critical"]),
            "warnings": len(classified["warnings"]),
            "info": len(classified["info"])
        }
    }
