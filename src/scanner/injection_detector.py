"""
CopilotShield - Hardened Security & Injection Detector
Features:
- De-obfuscation pipeline: String concatenation resolution (e.g. process['en' + 'v'])
- Detection of indirect & social engineering prompt injections (e.g. "Reviewer: pre-approved by security")
- Dangerous dynamic execution checks (eval, new Function, child_process, shell)
- AST-level verification for Python scripts
- Exfiltration and secret access detection
"""

import re
import ast
import base64
from typing import Dict, List, Any

# Social engineering & authority spoofing prompts intended to deceive LLMs or reviewers
SOCIAL_ENGINEERING_PATTERNS = [
    (r"(?i)(?:reviewer|maintainer|human|security\s+team|admin)\s*:\s*(?:this\s+was\s+)?(?:pre-approved|approved|verified|authorized|lgtm)", "AUTHORITY_SPOOFING_INJECTION", 95),
    (r"(?i)(?:pre-approved|approved)\s+by\s+(?:the\s+)?(?:security|maintainer|core|admin|lead)\s+team", "FAKE_PRE_APPROVAL_CLAIM", 95),
    (r"(?i)(?:please\s+)?merge\s+(?:without\s+(?:review|checks|inspection)|directly|immediately)", "REVIEW_BYPASS_INJECTION", 90),
    (r"(?i)(?:skip|bypass|suppress|ignore)\s+(?:all\s+)?(?:review|audit|checks|ci|tests|scanning)", "SECURITY_GATE_BYPASS", 92),
    (r"(?i)(?:ignore|disregard|forget|override)\s+(?:all\s+)?(?:previous|prior|above)?\s*(?:instructions|prompts|rules|policies|constraints)", "PROMPT_OVERRIDE_ATTEMPT", 98),
    (r"(?i)(?:system\s+prompt|developer\s+mode|jailbreak|DAN\s+mode|bypass\s+safety)", "JAILBREAK_KEYWORD", 95),
    (r"(?i)(?:\[system:?|\[instruction:?|<!--\s*system:?|/\*\s*system:?)", "SYSTEM_ROLE_TAG_SPOOFING", 95),
    (r"(?i)(?:you\s+must|you\s+are\s+now)\s+(?:act\s+as|pretend\s+to\s+be|a\s+different\s+agent)", "ROLE_HIJACK_ATTEMPT", 90),
    (r"(?i)(?:exfiltrate|send|leak|transmit|upload)\s+(?:the\s+)?(?:token|key|secret|env|password|credential)", "SECRET_EXFILTRATION_PROMPT", 95),
]

# Code execution & dangerous runtime patterns (applied to normalized code)
DANGEROUS_RUNTIME_PATTERNS = [
    (r"(?i)new\s+Function\s*\(", "DYNAMIC_FUNCTION_CONSTRUCTOR", 90),
    (r"(?i)(?:eval|exec)\s*\(", "DYNAMIC_EVAL_EXECUTION", 85),
    (r"(?i)child_process\.(?:exec|execSync|spawn|fork)\s*\(", "ARBITRARY_PROCESS_EXECUTION", 80),
    (r"(?i)os\.system\s*\(|subprocess\.(?:Popen|run|call)\s*\(", "SHELL_EXECUTION", 80),
    (r"(?i)fetch\s*\(\s*['\"]https?:\/\/(?:webhook\.site|pipedream|requestbin|transfer\.sh|pastebin|attacker)", "SUSPICIOUS_EXFIL_ENDPOINT", 95),
    (r"(?i)curl\s+-[sS]?\s+.*\|\s*(?:bash|sh)", "CURL_PIPE_BASH", 98),
    (r"(?i)process\.env\.(?:GITHUB_TOKEN|AWS_SECRET|OPENAI_API_KEY|PRIVATE_KEY)", "SENSITIVE_ENV_ACCESS", 75),
    (r"(?i)process\[['\"]env['\"]\]\[['\"](?:GITHUB_TOKEN|AWS_SECRET|OPENAI_API_KEY|PRIVATE_KEY)['\"]\]", "SENSITIVE_ENV_INDEX_ACCESS", 75),
    (r"(?i)(?:require\(['\"]fs['\"]\)|fs)\.readFileSync\s*\(\s*['\"].*id_rsa", "SSH_KEY_READ_ATTEMPT", 99),
]

def deobfuscate_string_concatenation(code_line: str) -> str:
    """
    Resolves basic string concatenations:
    e.g. process['en' + 'v'] -> process['env']
    e.g. 'c' + 'u' + 'r' + 'l' -> 'curl'
    """
    # Pattern matching 'foo' + 'bar' or "foo" + "bar"
    pattern = r"(['\"][^'\"]*?['\"])\s*\+\s*(['\"][^'\"]*?['\"])"
    prev = None
    curr = code_line
    # Loop to handle multiple chained concatenations 'a' + 'b' + 'c'
    while curr != prev:
        prev = curr
        def replacer(m):
            s1 = m.group(1)[1:-1]
            s2 = m.group(2)[1:-1]
            quote = m.group(1)[0]
            return f"{quote}{s1}{s2}{quote}"
        curr = re.sub(pattern, replacer, curr)
    
    # Normalize bracket notation process['env'] -> process.env
    curr = re.sub(r"process\s*\[\s*['\"]env['\"]\s*\]", "process.env", curr)
    return curr

def check_python_ast(code: str) -> List[Dict[str, Any]]:
    """Inspects Python code via true AST parsing for malicious nodes."""
    findings = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings  # Not valid Python or is a diff snippet

    for node in ast.walk(tree):
        # 1. Calls to eval(), exec()
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec", "__import__"):
                findings.append({
                    "category": "DANGEROUS_CODE",
                    "rule_id": f"AST_PYTHON_{node.func.id.upper()}",
                    "line": getattr(node, "lineno", 0),
                    "risk_score": 90,
                    "severity": "CRITICAL",
                    "evidence": f"AST Call to dangerous built-in {node.func.id}()"
                })
            # 2. Subprocess calls
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr in ("system", "popen", "spawn") and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                    findings.append({
                        "category": "DANGEROUS_CODE",
                        "rule_id": "AST_PYTHON_OS_SYSTEM",
                        "line": getattr(node, "lineno", 0),
                        "risk_score": 85,
                        "severity": "HIGH",
                        "evidence": f"AST Call to os.{node.func.attr}()"
                    })
    return findings

def scan_content(content: str, filename: str = "diff.patch") -> Dict[str, Any]:
    """Scans code/diff using de-obfuscation, social engineering detection, and AST."""
    issues = []
    lines = content.splitlines()

    # 1. Check for Social Engineering & Prompt Injection across all lines/comments
    for line_num, line in enumerate(lines, 1):
        for pattern, rule_id, risk in SOCIAL_ENGINEERING_PATTERNS:
            if re.search(pattern, line):
                issues.append({
                    "category": "PROMPT_INJECTION",
                    "rule_id": rule_id,
                    "line": line_num,
                    "risk_score": risk,
                    "severity": "CRITICAL" if risk >= 85 else "HIGH",
                    "evidence": line.strip()[:140]
                })

    # 2. De-obfuscate and scan for dangerous code in added/modified lines
    for line_num, line in enumerate(lines, 1):
        check_line = line
        if line.startswith("-"):
            continue
        if line.startswith("+"):
            check_line = line[1:]

        # Run de-obfuscation
        normalized_line = deobfuscate_string_concatenation(check_line)

        for pattern, rule_id, risk in DANGEROUS_RUNTIME_PATTERNS:
            if re.search(pattern, normalized_line):
                issues.append({
                    "category": "DANGEROUS_CODE",
                    "rule_id": rule_id,
                    "line": line_num,
                    "risk_score": risk,
                    "severity": "CRITICAL" if risk >= 85 else "HIGH",
                    "evidence": check_line.strip()[:140] + (f" (De-obfuscated: {normalized_line.strip()[:100]})" if normalized_line != check_line else "")
                })

    # 3. If Python file, run AST inspection
    if filename.endswith(".py"):
        ast_issues = check_python_ast(content)
        issues.extend(ast_issues)

    max_risk = max([i["risk_score"] for i in issues], default=0)
    has_injection = any(i["category"] == "PROMPT_INJECTION" for i in issues)
    has_dangerous_code = any(i["category"] == "DANGEROUS_CODE" for i in issues)

    return {
        "file": filename,
        "is_safe": len(issues) == 0,
        "max_risk_score": max_risk,
        "total_issues": len(issues),
        "has_prompt_injection": has_injection,
        "has_dangerous_code": has_dangerous_code,
        "findings": issues
    }
