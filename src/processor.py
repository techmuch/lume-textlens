import re
from typing import List, Dict, Any

class TextProcessor:
    def __init__(self, policy: str = "no-phi"):
        self.policy = policy
        # Simple regex for demo purposes:
        # SSN: \b\d{3}-\d{2}-\d{4}\b
        # Phone: \b\d{3}-\d{4}\b or \b\d{3}-\d{3}-\d{4}\b
        self.phi_patterns = {
            "Social Security Number": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
            "Phone Number": re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\d{3}[-.]?\d{4}\b")
        }

    def analyze(self, text: str) -> Dict[str, Any]:
        violations = []
        
        if self.policy == "no-phi" or self.policy == "biographical":
            for label, pattern in self.phi_patterns.items():
                for match in pattern.finditer(text):
                    violations.append({
                        "type": label,
                        "match": match.group(),
                        "start": match.start(),
                        "end": match.end(),
                        "reason": f"Contains potential {label}"
                    })
        
        return {
            "has_violation": len(violations) > 0,
            "violations": violations,
            "score": 1.0 if len(violations) == 0 else max(0.0, 1.0 - (len(violations) * 0.2)),
            "suggestions": ["Remove PHI from the text."] if len(violations) > 0 else []
        }
