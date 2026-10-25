"""
CopilotShield - Hardened Security & Injection Detector
Comprehensive Multi-Vector Defense:
- Zero-width character detection & normalization (Trojan Source & hidden prompts)
- Advanced De-obfuscation: String concatenation, String.fromCharCode evaluation, Array joins, Base64 payload decoding
- Multi-language prompt injection & authority spoofing (English & German)
- Dangerous dynamic runtime & execution checks (standalone eval/exec vs safe method calls)
- process.env mass-dumping and sensitive credential exfiltration
- Split SSH key access & secret harvesting
- AST-level verification for Python scripts (os.system, __import__)
- npm lifecycle script backdoors (postinstall/preinstall in package.json)
- Typosquatted dependencies detection (npm & PyPI)
- Hardcoded backdoor accounts & authentication bypasses
- GitHub Actions workflow tampering
- False-alarm mitigation for doc files, test fixtures, regex.exec(), and db.exec()
"""

import re
import ast
import base64
import os
from typing import Dict, List, Any, Tuple, Optional

# Zero-width / invisible Unicode characters used for prompt injection / Trojan Source obfuscation
ZERO_WIDTH_REGEX = re.compile(r"[\u200B\u200C\u200D\uFEFF\u200E\u200F\u202A-\u202E\u2060-\u2064]")

# Known typosquats across npm and PyPI
TYPOSQUAT_MAP = {
    "crossenv": "cross-env",
    "lodashs": "lodash",
    "loadash": "lodash",
    "reqeusts": "requests",
    "requets": "requests",
    "requeests": "requests",
    "colourama": "colorama",
    "colorama-v2": "colorama",
    "crypto": "cryptography (or built-in node crypto; standalone 'crypto' npm package is deprecated/insecure)",
    "discord-py": "discord.py",
    "dateutil-python": "python-dateutil",
    "python-datetime": "datetime",
    "urllib": "urllib3 (standard lib 'urllib' is not a PyPI package)",
    "urllib33": "urllib3",
    "expresss": "express",
    "expres": "express",
    "react-domm": "react-dom",
    "dotenvv": "dotenv"
}

# Cyrillic and Greek Homoglyph Translation Map for Anti-Evasion
HOMOGLYPH_TRANSLATION = str.maketrans({
    # Cyrillic lowercase & uppercase
    'а': 'a', 'А': 'A',
    'е': 'e', 'Е': 'E',
    'о': 'o', 'О': 'O',
    'р': 'p', 'Р': 'P',
    'с': 'c', 'С': 'C',
    'у': 'y', 'У': 'Y',
    'х': 'x', 'Х': 'X',
    'і': 'i', 'І': 'I',
    'ї': 'i', 'Ї': 'I',
    'ј': 'j', 'Ј': 'J',
    'ѕ': 's', 'Ѕ': 'S',
    'п': 'n', 'П': 'N',
    'в': 'b', 'В': 'B',
    'т': 't', 'Т': 'T',
    'к': 'k', 'К': 'K',
    'м': 'm', 'М': 'M',
    'н': 'h', 'Н': 'H',
    # Greek homoglyphs
    'α': 'a', 'Α': 'A',
    'ο': 'o', 'Ο': 'O',
    'ρ': 'p', 'Ρ': 'P',
    'ν': 'v', 'Ν': 'N',
    'ε': 'e', 'Ε': 'E',
    'ι': 'i', 'Ι': 'I',
    'κ': 'k', 'Κ': 'K',
    'τ': 't', 'Τ': 'T',
})

def normalize_homoglyphs(text: str) -> Tuple[str, bool]:
    """Translates visual homoglyphs (Cyrillic/Greek) to Latin ASCII equivalents."""
    normalized = text.translate(HOMOGLYPH_TRANSLATION)
    return normalized, normalized != text

# English & German Social Engineering & Prompt Injections
SOCIAL_ENGINEERING_PATTERNS = [
    # English authority spoofing & review overrides (including "AI reviewer: approve")
    (r"(?i)(?:ai\s+reviewer|copilot|ai|llm|assistant|reviewer|maintainer|human|security\s+team|admin)\s*:\s*(?:please\s+)?(?:approve|approved|pre-approved|verified|authorized|lgtm|merge)", "AUTHORITY_SPOOFING_INJECTION", 95),
    (r"(?i)(?:pre-approved|approved)\s+by\s+(?:the\s+)?(?:security|maintainer|core|admin|lead|team)", "FAKE_PRE_APPROVAL_CLAIM", 95),
    (r"(?i)(?:please\s+)?merge\s+(?:without\s+(?:review|checks|inspection)|directly|immediately|this\s+pr)", "REVIEW_BYPASS_INJECTION", 90),
    (r"(?i)(?:skip|bypass|suppress|ignore)\s+(?:all\s+)?(?:review|audit|checks|ci|tests|scanning|safety)", "SECURITY_GATE_BYPASS", 92),
    (r"(?i)(?:ignore|disregard|forget|override)\s+(?:all\s+)?(?:previous|prior|above)?\s*(?:instructions|prompts|rules|policies|constraints|context)", "PROMPT_OVERRIDE_ATTEMPT", 98),
    (r"(?i)(?:system\s+prompt|developer\s+mode|jailbreak|DAN\s+mode|bypass\s+safety)", "JAILBREAK_KEYWORD", 95),
    (r"(?i)(?:\[system:?|\[instruction:?|<!--\s*system:?|/\*\s*system:?|<\|im_start\|>|<\|system\|>)", "SYSTEM_ROLE_TAG_SPOOFING", 95),
    (r"(?i)(?:you\s+must|you\s+are\s+now)\s+(?:act\s+as|pretend\s+to\s+be|a\s+different\s+agent)", "ROLE_HIJACK_ATTEMPT", 90),
    (r"(?i)(?:exfiltrate|send|leak|transmit|upload)\s+(?:the\s+)?(?:token|key|secret|env|password|credential)", "SECRET_EXFILTRATION_PROMPT", 95),
    
    # German Language Injections & Social Engineering
    (r"(?i)(?:ignoriere|vergiss|uebergehe|übergehe|verwerfe)\s+(?:alle\s+)?(?:vorherigen|bisherigen)?\s*(?:anweisungen|regeln|prompts|befehle|instruktionen)", "GERMAN_PROMPT_OVERRIDE_ATTEMPT", 98),
    (r"(?i)(?:ueberpruefer|überprüfer|pruefer|prüfer|sicherheitsteam|admin|ai\s+pruefer|ai\s+prüfer)\s*:\s*(?:bitte\s+)?(?:genehmigt|freigegeben|bestaetigt|bestätigt|akzeptiert|lgtm|genehmigen|freigeben)", "GERMAN_AUTHORITY_SPOOFING", 95),
    (r"(?i)(?:bitte\s+)?(?:ohne\s+(?:pruefung|prüfung|review|kontrolle)|direkt|sofort)\s+(?:zusammenfuehren|zusammenführen|mergen)", "GERMAN_REVIEW_BYPASS", 90),
    (r"(?i)(?:systemaufforderung|entwicklermodus|sicherheitspruefung\s+umgehen|sicherheitsprüfung\s+umgehen)", "GERMAN_JAILBREAK_KEYWORD", 95),
    (r"(?i)(?:du\s+musst\s+jetzt|handle\s+als|agiere\s+als)\s+(?:ein\s+anderer\s+agent|ohne\s+einschraenkungen|ohne\s+einschränkungen)", "GERMAN_ROLE_HIJACK", 90),
    (r"(?i)(?:senden|uebertragen|übertragen|exfiltrieren|leaken)\s+(?:das\s+)?(?:token|geheimnis|passwort|schluessel|schlüssel|anmeldedaten)", "GERMAN_EXFILTRATION_PROMPT", 95),
]

# Code execution & dangerous runtime patterns (applied to normalized code)
DANGEROUS_RUNTIME_PATTERNS = [
    # Shell download & pipe to shell (matches any flags, bare curl/wget, and sudo)
    (r"(?i)(?:bash|sh|zsh|dash)\s+-c\s+['\"].*?\$\((?:curl|wget)", "SHELL_DOWNLOAD_EXECUTE", 98),
    (r"(?i)\$\((?:curl|wget)\s+[^)]+\)", "COMMAND_SUBSTITUTION_DOWNLOAD", 95),
    (r"(?i)`(?:curl|wget)\s+[^`]+`", "COMMAND_SUBSTITUTION_DOWNLOAD", 95),
    (r"(?i)(?:curl|wget)\b[^|;\n]+\|\s*(?:sudo\s+)?(?:bash|sh|zsh|dash|python\d?|perl|ruby)", "CURL_PIPE_BASH", 98),
    (r"(?i)(?:eval|source)\s+['\"`]?\$\((?:curl|wget)", "EVAL_DOWNLOAD_EXECUTION", 98),
    
    # Reverse shells
    (r"(?i)(?:/dev/tcp|/dev/udp)/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/\d+|/dev/tcp/[a-zA-Z0-9_.-]+/\d+", "REVERSE_SHELL_DEV_TCP", 99),
    (r"(?i)(?:nc|ncat|netcat)\s+.*?-e\s*(?:/bin/sh|/bin/bash|sh|bash|cmd(?:\.exe)?|powershell)", "REVERSE_SHELL_NETCAT", 99),
    (r"(?i)bash\s+-i\s+>&?\s*/dev/tcp/", "REVERSE_SHELL_BASH", 99),
    (r"(?i)socat\s+exec:.*?tcp:", "REVERSE_SHELL_SOCAT", 99),
    
    # Sensitive file harvesting (/etc/passwd, ~/.aws/credentials, ~/.kube/config)
    (r"(?i)(?:readFileSync|readFile|open|createReadStream|\bcat\b|\bhead\b|\btail\b)\s*\(?.*?(?:/etc/passwd|/etc/shadow|/etc/sudoers|\.aws|\.kube|\.netrc|credentials)", "SENSITIVE_FILE_HARVESTING", 98),
    (r"(?i)path\.join\s*\(.*?['\"]\.aws['\"].*?['\"]credentials['\"]", "AWS_CREDENTIALS_PATH_CONSTRUCTION", 98),
    (r"(?i)(?:/etc/passwd|/etc/shadow|\.aws.*?credentials|\.aws/config|\.kube/config|\.netrc)", "SENSITIVE_FILE_LITERAL", 95),
    
    # .env harvesting & exfiltration
    (r"(?i)(?:readFileSync|readFile|open|createReadStream)\s*\(.*['\"]\.env(?:\.[a-zA-Z0-9]+)?['\"]", "DOTENV_FILE_ACCESS", 90),
    (r"(?i)(?:fetch|axios|http|requests\.(?:post|put)|curl)\s*\(?.*\.env", "DOTENV_EXFILTRATION", 95),
    (r"(?i)cat\s+\.env\s*\|\s*(?:curl|wget|nc)", "DOTENV_SHELL_EXFILTRATION", 95),
    
    # Python __import__ dangerous execution (Python __import__('os').system)
    (r"(?i)(?<![\w.])__import__\s*\(\s*['\"](?:os|subprocess|sys|shutil|pty|builtins)['\"]\s*\)\s*\.(?:system|popen|call|check_output|run|exec)", "PYTHON_DYNAMIC_IMPORT_EXEC", 95),
    (r"(?i)(?<![\w.])__import__\s*\(\s*['\"]os['\"]\s*\)", "PYTHON_IMPORT_OS_DYNAMIC", 90),
    (r"(?i)getattr\s*\(\s*(?:__builtins__|builtins|os|sys|subprocess)\s*,\s*['\"](?:exec|eval|system|popen|__import__|spawn)['\"]", "PYTHON_DYNAMIC_GETATTR_EXEC", 95),
    
    # Dynamic constructor & execution
    (r"(?i)new\s+Function\s*\(", "DYNAMIC_FUNCTION_CONSTRUCTOR", 90),
    (r"(?i)(?:child_process|require\s*\(\s*['\"]child_process['\"]\s*\))\s*\.\s*(?:exec|execSync|spawn|fork|execFile)\s*\(", "ARBITRARY_PROCESS_EXECUTION", 90),
    (r"(?i)(?:const|let|var)\s*\{[^}]*(?:exec|execSync|spawn|fork)[^}]*\}\s*=\s*require\s*\(\s*['\"]child_process['\"]\s*\)", "ARBITRARY_PROCESS_IMPORT", 85),
    (r"(?i)import\s*\{[^}]*(?:exec|execSync|spawn|fork)[^}]*\}\s*from\s*['\"]child_process['\"]", "ARBITRARY_PROCESS_IMPORT", 85),
    
    # Dangerous shell execution (targets os.system/popen or subprocess with shell=True or string commands; safe subprocess.run([...]) is allowed)
    (r"(?i)os\.(?:system|popen|spawn)\s*\(", "OS_SYSTEM_EXECUTION", 85),
    (r"(?i)subprocess\.(?:Popen|run|call|check_output)\s*\([^)]*shell\s*=\s*(?:True|1)", "SUBPROCESS_SHELL_TRUE", 85),
    (r"(?i)subprocess\.(?:Popen|run|call|check_output)\s*\(\s*['\"][^'\",\]\n]+['\"]\s*[,)]", "SUBPROCESS_STRING_COMMAND", 85),
    
    # Standalone eval/exec (uses negative lookbehind to avoid false alarms like regex.exec or db.exec)
    (r"(?<![\w.])eval\s*\(", "DYNAMIC_EVAL_EXECUTION", 85),
    (r"(?<![\w.])exec\s*\(", "DYNAMIC_EXEC_EXECUTION", 85),
    
    # process.env mass dumping & exfiltration
    (r"(?i)JSON\.stringify\s*\(\s*process\.env\s*\)", "DUMPING_PROCESS_ENV", 95),
    (r"(?i)Object\.(?:entries|keys|values)\s*\(\s*process\.env\s*\)", "DUMPING_PROCESS_ENV", 95),
    (r"(?i)console\.(?:log|dir|table|error)\s*\(\s*process\.env\s*\)", "DUMPING_PROCESS_ENV", 90),
    (r"(?i)util\.inspect\s*\(\s*process\.env\s*\)", "DUMPING_PROCESS_ENV", 90),
    (r"(?i)(?:fetch|axios|http)\s*\([^)]*process\.env", "ENV_NETWORK_EXFILTRATION", 95),
    (r"(?i)dict\s*\(\s*os\.environ\s*\)", "PYTHON_ENV_DUMP", 95),
    
    # process['env'] bracket evasion
    (r"(?i)process\s*\[\s*['\"]env['\"]\s*\]", "BRACKET_PROCESS_ENV_ACCESS", 85),
    
    # Sensitive env individual access
    (r"(?i)process\.env\.(?:GITHUB_TOKEN|AWS_SECRET|OPENAI_API_KEY|PRIVATE_KEY|DATABASE_URL|SECRET_KEY)", "SENSITIVE_ENV_ACCESS", 75),
    (r"(?i)process\[['\"]env['\"]\]\[['\"](?:GITHUB_TOKEN|AWS_SECRET|OPENAI_API_KEY|PRIVATE_KEY|DATABASE_URL)['\"]\]", "SENSITIVE_ENV_INDEX_ACCESS", 75),
    
    # Suspicious exfiltration endpoints
    (r"(?i)fetch\s*\(\s*['\"]https?:\/\/(?:webhook\.site|pipedream|requestbin|transfer\.sh|pastebin|attacker|ngrok)", "SUSPICIOUS_EXFIL_ENDPOINT", 95),
    (r"(?i)curl\s+.*?https?:\/\/(?:webhook\.site|pipedream|requestbin|transfer\.sh|pastebin|attacker|ngrok)", "SUSPICIOUS_EXFIL_ENDPOINT", 95),
    
    # Split SSH-key path & secret file harvesting
    (r"(?i)(?:readFileSync|readFile|open|createReadStream)\s*\(.*?(?:id_rsa|id_ed25519|id_ecdsa|id_dsa|\.ssh)", "SSH_KEY_READ_ATTEMPT", 99),
    (r"(?i)path\.join\s*\(.*?['\"]\.ssh['\"].*?['\"]id_", "SSH_KEY_PATH_CONSTRUCTION", 99),
    (r"(?i)\.ssh.*?id_(?:rsa|ed25519|ecdsa|dsa)", "SSH_KEY_PATH_LITERAL", 99),
    
    # Hardcoded backdoor user / auth bypass
    (r"(?i)(?:username|user|user_id|login|email|account)\s*(?:===?|==)\s*['\"](?:backdoor|admin_override|root_override|emergency_admin|superuser_bypass)['\"]", "HARDCODED_BACKDOOR_USER", 95),
    (r"(?i)(?:password|pass|secret|auth_token)\s*(?:===?|==)\s*['\"](?:backdoor|masterpass|override123|skeletonkey)['\"]", "HARDCODED_BACKDOOR_PASSWORD", 95),
    (r"(?i)if\s*\([^)]*(?:===?|==)\s*['\"]backdoor['\"]\s*\)\s*return\s+true", "AUTH_BYPASS_BACKDOOR", 95),
]

def deobfuscate_escapes(code_line: str) -> Tuple[str, List[str]]:
    """
    Evaluates hex escapes (\\x65\\x76\\x61\\x6c) and unicode escapes (\\u0065\\u0076\\u0061\\u006c).
    Returns (transformed_line, list_of_decoded_suspicious_tokens).
    """
    sensitive_found = []
    
    def hex_replacer(m):
        raw = m.group(0)
        try:
            s = re.sub(r"\\x([0-9a-fA-F]{2})", lambda h: chr(int(h.group(1), 16)), raw)
            s = re.sub(r"\\u([0-9a-fA-F]{4})", lambda u: chr(int(u.group(1), 16)), s)
            inner = s[1:-1].lower()
            if any(term in inner for term in ("eval", "exec", "system", "popen", "spawn", "curl", "wget", "sh", "bash", "process.env", "id_rsa", "passwd")):
                sensitive_found.append(inner)
            return s
        except Exception:
            return raw

    pattern = r"['\"](?:\\x[0-9a-fA-F]{2}|\\u[0-9a-fA-F]{4}|[^'\"\\])*['\"]"
    transformed = re.sub(pattern, hex_replacer, code_line)
    return transformed, sensitive_found

def deobfuscate_string_concatenation(code_line: str) -> Tuple[str, bool]:
    """
    Resolves string concatenations:
    e.g. process['en' + 'v'] -> process['env']
    e.g. 'c' + 'u' + 'r' + 'l' -> 'curl'
    e.g. 'id_' + 'rsa' -> 'id_rsa'
    Returns (transformed_line, had_obfuscated_env).
    """
    had_env_concat = bool(
        re.search(r"process\s*\[\s*['\"]en['\"]\s*\+\s*['\"]v['\"]\s*\]", code_line, re.I)
        or re.search(r"['\"]en['\"]\s*\+\s*['\"]v['\"]", code_line, re.I)
    )
    pattern = r"(['\"][^'\"]*?['\"])\s*\+\s*(['\"][^'\"]*?['\"])"
    prev = None
    curr = code_line
    while curr != prev:
        prev = curr
        def replacer(m):
            s1 = m.group(1)[1:-1]
            s2 = m.group(2)[1:-1]
            quote = m.group(1)[0]
            return f"{quote}{s1}{s2}{quote}"
        curr = re.sub(pattern, replacer, curr)
    
    if re.search(r"process\s*\[\s*['\"]env['\"]\s*\]", curr, re.I) and not re.search(r"process\s*\[\s*['\"]env['\"]\s*\]", code_line, re.I):
        had_env_concat = True

    # Normalize bracket notation process['env'] -> process.env
    curr = re.sub(r"process\s*\[\s*['\"]env['\"]\s*\]", "process.env", curr, flags=re.I)
    return curr, had_env_concat

def deobfuscate_from_char_code(code_line: str) -> Tuple[str, Optional[str]]:
    """
    Evaluates String.fromCharCode(101, 118, 97, 108) -> 'eval'.
    Returns (transformed_line, decoded_content_if_any).
    """
    pattern = r"String\.fromCharCode\s*\(\s*([\d\s,]+)\s*\)"
    decoded_payload = None
    curr = code_line
    for match in re.finditer(pattern, code_line):
        try:
            codes = [int(c.strip()) for c in match.group(1).split(",") if c.strip()]
            decoded = "".join(chr(c) for c in codes)
            decoded_payload = decoded
            curr = curr.replace(match.group(0), f'"{decoded}"')
        except Exception:
            pass
    return curr, decoded_payload

def deobfuscate_array_joins(code_line: str) -> str:
    """
    Evaluates array joins e.g. ['.s', 'sh', 'id_rsa'].join('/') -> '.ssh/id_rsa'
    or ['cu', 'rl'].join('') -> 'curl'
    """
    pattern = r"\[\s*((?:['\"][^'\"]*['\"]\s*,\s*)+['\"][^'\"]*['\"])\s*\]\.join\s*\(\s*['\"]([^'\"]*)['\"]\s*\)"
    def replacer(m):
        elements_raw = m.group(1)
        sep = m.group(2)
        elements = [s.strip()[1:-1] for s in elements_raw.split(",") if s.strip()]
        joined = sep.join(elements)
        return f'"{joined}"'
    return re.sub(pattern, replacer, code_line)

def inspect_base64_payloads(code_line: str) -> List[Dict[str, Any]]:
    """
    Detects base64 execution pipelines and scans inline base64 string literals
    for concealed malicious payloads. (Does not flag benign cryptographic base64 decoding).
    """
    findings = []
    # Check for direct decode-and-execute combinations
    b64_exec_patterns = [
        (r"(?i)(?:eval|exec)\s*\([^)]*(?:base64\.b64decode|atob|Buffer\.from)", "BASE64_DECODE_AND_EXEC"),
        (r"base64\s+-d\s*\|\s*(?:bash|sh)", "BASE64_SHELL_PIPELINE"),
        (r"echo\s+['\"][A-Za-z0-9+/=]{16,}['\"]\s*\|\s*base64\s+-d", "BASE64_ECHO_PIPELINE"),
    ]
    for pat, rule in b64_exec_patterns:
        if re.search(pat, code_line):
            findings.append({
                "category": "DANGEROUS_CODE",
                "rule_id": rule,
                "risk_score": 95,
                "severity": "CRITICAL",
                "evidence": f"Base64 execution pipeline detected: {code_line.strip()[:120]}"
            })

    # Search for long base64 string literals and inspect decoded content
    b64_literal_pattern = r"['\"]([A-Za-z0-9+/]{20,}={0,2})['\"]"
    for match in re.finditer(b64_literal_pattern, code_line):
        b64_str = match.group(1)
        try:
            decoded = base64.b64decode(b64_str).decode("utf-8", errors="ignore")
            # If decoded text contains shell or exfiltration commands
            suspicious = ["curl", "wget", "bash", "exec", "eval", "process.env", "os.system", "id_rsa", "/bin/sh", "powershell", "/etc/passwd"]
            if any(s in decoded.lower() for s in suspicious):
                findings.append({
                    "category": "DANGEROUS_CODE",
                    "rule_id": "BASE64_OBFUSCATED_PAYLOAD",
                    "risk_score": 95,
                    "severity": "CRITICAL",
                    "evidence": f"Decoded Base64 payload reveals malicious command: {decoded.strip()[:100]}"
                })
        except Exception:
            pass
    return findings

def check_python_ast(code: str) -> List[Dict[str, Any]]:
    """Inspects Python code via AST parsing for dynamic calls and __import__."""
    findings = []
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return findings

    for node in ast.walk(tree):
        # 1. Calls to eval(), exec(), __import__()
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ("eval", "exec", "__import__"):
                    findings.append({
                        "category": "DANGEROUS_CODE",
                        "rule_id": f"AST_PYTHON_{node.func.id.upper()}",
                        "line": getattr(node, "lineno", 0),
                        "risk_score": 90,
                        "severity": "CRITICAL",
                        "evidence": f"AST Call to dangerous built-in {node.func.id}()"
                    })
                elif node.func.id == "getattr" and len(node.args) >= 2:
                    target_name = node.args[0].id if isinstance(node.args[0], ast.Name) else ""
                    attr_val = node.args[1].value if isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str) else ""
                    if target_name in ("__builtins__", "builtins", "os", "sys", "subprocess") and attr_val in ("eval", "exec", "system", "popen", "__import__", "spawn"):
                        findings.append({
                            "category": "DANGEROUS_CODE",
                            "rule_id": "AST_PYTHON_GETATTR_EXEC",
                            "line": getattr(node, "lineno", 0),
                            "risk_score": 95,
                            "severity": "CRITICAL",
                            "evidence": f"AST Call to dangerous getattr({target_name}, '{attr_val}')"
                        })
            # 2. Chained calls: __import__('os').system(...)
            elif isinstance(node.func, ast.Attribute):
                val = node.func.value
                if isinstance(val, ast.Call) and isinstance(val.func, ast.Name) and val.func.id == "__import__":
                    findings.append({
                        "category": "DANGEROUS_CODE",
                        "rule_id": "AST_PYTHON_DYNAMIC_IMPORT_EXEC",
                        "line": getattr(node, "lineno", 0),
                        "risk_score": 95,
                        "severity": "CRITICAL",
                        "evidence": f"AST Call to __import__(...).{node.func.attr}()"
                    })
                # Subprocess / os calls
                elif isinstance(val, ast.Name) and val.id == "os" and node.func.attr in ("system", "popen", "spawn"):
                    findings.append({
                        "category": "DANGEROUS_CODE",
                        "rule_id": "AST_PYTHON_OS_SYSTEM",
                        "line": getattr(node, "lineno", 0),
                        "risk_score": 85,
                        "severity": "HIGH",
                        "evidence": f"AST Call to os.{node.func.attr}()"
                    })
                elif isinstance(val, ast.Name) and val.id == "subprocess" and node.func.attr in ("Popen", "run", "call", "check_output"):
                    has_shell_true = any(
                        kw.arg == "shell" and (
                            (isinstance(kw.value, ast.Constant) and bool(kw.value.value))
                        )
                        for kw in node.keywords
                    )
                    is_raw_string = False
                    if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        is_raw_string = True
                    if has_shell_true or is_raw_string:
                        findings.append({
                            "category": "DANGEROUS_CODE",
                            "rule_id": "AST_PYTHON_SUBPROCESS_SHELL",
                            "line": getattr(node, "lineno", 0),
                            "risk_score": 85,
                            "severity": "HIGH",
                            "evidence": f"AST Call to subprocess.{node.func.attr}() with {'shell=True' if has_shell_true else 'string command'}"
                        })
    return findings

def check_npm_package_json(added_lines: List[str]) -> List[Dict[str, Any]]:
    """Inspects package.json changes for postinstall/preinstall lifecycle backdoors and typosquats."""
    findings = []
    content = "\n".join(added_lines)
    
    # Check lifecycle scripts: postinstall, preinstall, install
    lifecycle_pattern = r'["\'](postinstall|preinstall|install)["\']\s*:\s*["\']([^"\']+)["\']'
    for match in re.finditer(lifecycle_pattern, content):
        hook = match.group(1)
        cmd = match.group(2)
        # Check if hook invokes shell, curl, wget, or remote execution
        if re.search(r"(?:curl|wget|bash|sh|node\s+-e|eval|powershell|http:\/\/|https:\/\/)", cmd, re.I):
            findings.append({
                "category": "DANGEROUS_CODE",
                "rule_id": "NPM_POSTINSTALL_BACKDOOR",
                "line": 1,
                "risk_score": 98,
                "severity": "CRITICAL",
                "evidence": f"Malicious npm {hook} script detected: {cmd[:100]}"
            })

    # Check for typosquatted dependencies
    dep_pattern = r'["\']([a-zA-Z0-9@_/-]+)["\']\s*:\s*["\'][^"\']+["\']'
    for match in re.finditer(dep_pattern, content):
        pkg = match.group(1).lower().strip()
        if pkg in TYPOSQUAT_MAP:
            findings.append({
                "category": "DANGEROUS_CODE",
                "rule_id": "TYPOSQUATTED_DEPENDENCY",
                "line": 1,
                "risk_score": 90,
                "severity": "CRITICAL",
                "evidence": f"Typosquatted package '{pkg}' detected (Legitimate: {TYPOSQUAT_MAP[pkg]})"
            })
    return findings

def check_workflow_tampering(filename: str, added_lines: List[str]) -> List[Dict[str, Any]]:
    """Inspects GitHub Actions workflow modifications for privilege escalation or tampering."""
    findings = []
    is_workflow = (
        ".github/workflows" in filename.replace("\\", "/") 
        or ".github/actions" in filename.replace("\\", "/")
        or filename in ("action.yml", "action.yaml")
    )
    if not is_workflow:
        return findings

    # Flag workflow modification itself
    findings.append({
        "category": "DANGEROUS_CODE",
        "rule_id": "TAMPERED_WORKFLOW",
        "line": 1,
        "risk_score": 95,
        "severity": "CRITICAL",
        "evidence": f"PR modifies GitHub Actions workflow or action file: {filename}"
    })

    content = "\n".join(added_lines)
    # Check for dangerous patterns in workflow: pull_request_target with untrusted checkout, secret dumping
    if re.search(r"pull_request_target", content):
        findings.append({
            "category": "DANGEROUS_CODE",
            "rule_id": "DANGEROUS_WORKFLOW_TRIGGER",
            "line": 1,
            "risk_score": 98,
            "severity": "CRITICAL",
            "evidence": "Workflow introduces 'pull_request_target' trigger (high risk for secret exfiltration)"
        })
    if re.search(r"echo\s+.*?secrets\.", content):
        findings.append({
            "category": "DANGEROUS_CODE",
            "rule_id": "WORKFLOW_SECRET_EXFILTRATION",
            "line": 1,
            "risk_score": 99,
            "severity": "CRITICAL",
            "evidence": "Workflow attempts to echo/dump GitHub secrets"
        })
    return findings

def split_diff_by_files(diff_text: str) -> List[Tuple[str, List[str], List[Tuple[int, str]]]]:
    """
    Parses a git diff into individual files.
    Returns list of tuples: (filename, added_raw_lines, [(line_no, added_line)])
    """
    files = []
    current_file = "diff.patch"
    current_added_lines = []
    current_indexed_lines = []

    lines = diff_text.splitlines()
    for idx, line in enumerate(lines, 1):
        if line.startswith("diff --git"):
            if current_added_lines or current_file != "diff.patch":
                files.append((current_file, current_added_lines, current_indexed_lines))
            current_added_lines = []
            current_indexed_lines = []
            parts = line.split()
            if len(parts) >= 4:
                b_path = parts[3]
                current_file = b_path[2:] if b_path.startswith("b/") else b_path
        elif line.startswith("+++ b/"):
            current_file = line[6:].strip()
        elif line.startswith("+") and not line.startswith("+++"):
            code_line = line[1:]
            current_added_lines.append(code_line)
            current_indexed_lines.append((idx, code_line))
        elif not line.startswith("-") and not line.startswith("---") and not line.startswith("@@"):
            # Plain code or context line
            current_added_lines.append(line)
            current_indexed_lines.append((idx, line))

    if current_added_lines or current_file != "diff.patch":
        files.append((current_file, current_added_lines, current_indexed_lines))

    # If diff wasn't in unified git diff format, treat whole text as single file
    if not files:
        indexed = [(idx, line) for idx, line in enumerate(lines, 1)]
        files.append(("diff.patch", lines, indexed))

    return files

def is_doc_file(filename: str) -> bool:
    """Checks if file is documentation where prompt injection keywords are educational."""
    lower = filename.lower().replace("\\", "/")
    doc_extensions = (".md", ".txt", ".rst", ".adoc")
    if lower.endswith(doc_extensions) or lower.startswith("docs/") or "/docs/" in lower:
        return True
    return False

def is_test_file(filename: str) -> bool:
    """Checks if file is a test file where eval/exec assertions are standard practice."""
    lower = filename.lower().replace("\\", "/")
    if lower.startswith("tests/") or "/tests/" in lower or "/test/" in lower:
        return True
    if any(lower.endswith(s) for s in ("_test.py", "test_.py", ".test.js", ".test.ts", ".spec.js", ".spec.ts")):
        return True
    return False

def is_safe_test_eval(code_str: str) -> bool:
    """Allows benign, simple test assertions like assert eval('2 + 2') == 4 in test files."""
    if re.search(r"(?<![\w.])exec\s*\(", code_str):
        return False
    m = re.search(r"eval\s*\(\s*(['\"])(.*?)\1\s*\)", code_str)
    if m:
        inner = m.group(2).lower()
        dangerous = (
            "os", "sys", "subprocess", "socket", "pty", "builtins", "__",
            "system", "popen", "open", "read", "curl", "wget", "sh", "bash",
            "fetch", "env", "token", "key", "password", "secret", "passwd",
            "shadow", "credentials"
        )
        if any(d in inner for d in dangerous):
            return False
        return True
    return False

def scan_content(content: str, filename: str = "diff.patch") -> Dict[str, Any]:
    """
    Main Security Scanner Engine:
    - Scans diffs and raw files
    - Unrolls obfuscations
    - Enforces injection and runtime policies
    - Suppresses false alarms for docs and tests
    """
    issues = []
    
    # Check for Zero-Width Unicode Characters across entire content
    for line_idx, raw_line in enumerate(content.splitlines(), 1):
        if ZERO_WIDTH_REGEX.search(raw_line):
            issues.append({
                "category": "PROMPT_INJECTION",
                "rule_id": "ZERO_WIDTH_CHARACTER_INJECTION",
                "line": line_idx,
                "risk_score": 95,
                "severity": "CRITICAL",
                "evidence": f"Zero-width hidden unicode character detected: {repr(raw_line.strip()[:100])}"
            })

    # Normalize zero-width characters for subsequent analysis
    clean_content = ZERO_WIDTH_REGEX.sub("", content)

    # Parse diff into file chunks
    file_chunks = split_diff_by_files(clean_content)

    for chunk_filename, added_lines, indexed_lines in file_chunks:
        effective_file = chunk_filename if chunk_filename != "diff.patch" else filename
        is_doc = is_doc_file(effective_file)
        is_test = is_test_file(effective_file)

        # 1. Check for workflow tampering
        wf_issues = check_workflow_tampering(effective_file, added_lines)
        issues.extend(wf_issues)

        # 2. Check for npm package.json issues
        if effective_file.endswith("package.json"):
            npm_issues = check_npm_package_json(added_lines)
            issues.extend(npm_issues)

        # 3. Check for typosquats in Python requirement files
        if any(effective_file.endswith(req) for req in ("requirements.txt", "Pipfile", "pyproject.toml", "setup.py")):
            for line_no, raw_line in indexed_lines:
                clean_req = raw_line.lower().split("==")[0].split(">=")[0].split("<=")[0].strip()
                if clean_req in TYPOSQUAT_MAP:
                    issues.append({
                        "category": "DANGEROUS_CODE",
                        "rule_id": "TYPOSQUATTED_DEPENDENCY",
                        "line": line_no,
                        "risk_score": 90,
                        "severity": "CRITICAL",
                        "evidence": f"Typosquatted Python package '{clean_req}' detected (Legitimate: {TYPOSQUAT_MAP[clean_req]})"
                    })

        # 4. Check each line for prompt injections & dangerous runtime patterns
        for line_no, raw_line in indexed_lines:
            # Check prompt injection patterns
            for pattern, rule_id, risk in SOCIAL_ENGINEERING_PATTERNS:
                match = re.search(pattern, raw_line)
                if match:
                    if is_doc:
                        # In documentation files, suppress if quoted or an educational example
                        m_start, m_end = match.span()
                        prefix = raw_line[:m_start].strip().lower()
                        is_quoted = False
                        if (m_start > 0 and raw_line[m_start-1] in ('"', "'", '`')) or (m_end < len(raw_line) and raw_line[m_end] in ('"', "'", '`')):
                            is_quoted = True
                        if '"' in raw_line and raw_line.count('"') >= 2:
                            first_q = raw_line.find('"')
                            last_q = raw_line.rfind('"')
                            if first_q < m_start and m_end <= last_q + 1:
                                is_quoted = True
                        if "'" in raw_line and raw_line.count("'") >= 2:
                            first_q = raw_line.find("'")
                            last_q = raw_line.rfind("'")
                            if first_q < m_start and m_end <= last_q + 1:
                                is_quoted = True
                        if '`' in raw_line and raw_line.count('`') >= 2:
                            first_q = raw_line.find('`')
                            last_q = raw_line.rfind('`')
                            if first_q < m_start and m_end <= last_q + 1:
                                is_quoted = True

                        educational_markers = ("cautious of", "often write", "example", "e.g.", "such as", "defending against", "attacks like", "mitigate")
                        is_educational = any(marker in prefix or marker in raw_line.lower() for marker in educational_markers)

                        if is_quoted or is_educational:
                            continue  # Harmless documentation reference

                        issues.append({
                            "category": "PROMPT_INJECTION",
                            "rule_id": rule_id,
                            "line": line_no,
                            "risk_score": risk,
                            "severity": "CRITICAL" if risk >= 85 else "HIGH",
                            "evidence": f"[Doc Injection] {raw_line.strip()[:140]}"
                        })
                    else:
                        issues.append({
                            "category": "PROMPT_INJECTION",
                            "rule_id": rule_id,
                            "line": line_no,
                            "risk_score": risk,
                            "severity": "CRITICAL" if risk >= 85 else "HIGH",
                            "evidence": raw_line.strip()[:140]
                        })

            # Check Cyrillic/Greek homoglyphs
            homoglyph_line, had_homoglyphs = normalize_homoglyphs(raw_line)
            if had_homoglyphs:
                for pattern, rule_id, risk in SOCIAL_ENGINEERING_PATTERNS:
                    if re.search(pattern, homoglyph_line):
                        issues.append({
                            "category": "PROMPT_INJECTION",
                            "rule_id": "HOMOGLYPH_OBFUSCATION_INJECTION",
                            "line": line_no,
                            "risk_score": 98,
                            "severity": "CRITICAL",
                            "evidence": f"Homoglyph-obfuscated prompt injection: {raw_line.strip()[:100]} (Normalized: {homoglyph_line.strip()[:100]})"
                        })
                        break

            # Run de-obfuscation pipeline
            line_str, had_env_concat = deobfuscate_string_concatenation(raw_line)
            line_str = deobfuscate_array_joins(line_str)
            line_str, charcode_payload = deobfuscate_from_char_code(line_str)
            line_str, hex_tokens = deobfuscate_escapes(line_str)

            if had_env_concat:
                issues.append({
                    "category": "DANGEROUS_CODE",
                    "rule_id": "OBFUSCATED_ENV_ACCESS",
                    "line": line_no,
                    "risk_score": 90,
                    "severity": "CRITICAL",
                    "evidence": f"Obfuscated process.env access resolved: {raw_line.strip()[:120]}"
                })
            elif re.search(r"process\s*\[\s*['\"]env['\"]\s*\]", raw_line, re.I):
                issues.append({
                    "category": "DANGEROUS_CODE",
                    "rule_id": "BRACKET_PROCESS_ENV_ACCESS",
                    "line": line_no,
                    "risk_score": 85,
                    "severity": "HIGH",
                    "evidence": f"Bracket notation process['env'] access: {raw_line.strip()[:120]}"
                })

            if hex_tokens:
                issues.append({
                    "category": "DANGEROUS_CODE",
                    "rule_id": "HEX_ESCAPED_OBFUSCATION",
                    "line": line_no,
                    "risk_score": 92,
                    "severity": "CRITICAL",
                    "evidence": f"Hex/Unicode escape resolved to sensitive primitive: {', '.join(hex_tokens)}"
                })

            if charcode_payload:
                issues.append({
                    "category": "DANGEROUS_CODE",
                    "rule_id": "STRING_FROMCHARCODE_OBFUSCATION",
                    "line": line_no,
                    "risk_score": 92,
                    "severity": "CRITICAL",
                    "evidence": f"String.fromCharCode obfuscation resolved: '{charcode_payload[:80]}'"
                })

            # Check base64 payloads
            b64_findings = inspect_base64_payloads(line_str)
            for bf in b64_findings:
                bf["line"] = line_no
                issues.append(bf)

            # Check dangerous runtime patterns
            for pattern, rule_id, risk in DANGEROUS_RUNTIME_PATTERNS:
                if re.search(pattern, line_str):
                    # In test files, only harmless test assertions like eval('2 + 2') are allowed
                    if is_test and rule_id == "DYNAMIC_EVAL_EXECUTION":
                        if is_safe_test_eval(line_str):
                            continue

                    issues.append({
                        "category": "DANGEROUS_CODE",
                        "rule_id": rule_id,
                        "line": line_no,
                        "risk_score": risk,
                        "severity": "CRITICAL" if risk >= 85 else "HIGH",
                        "evidence": raw_line.strip()[:140] + (f" (De-obfuscated: {line_str.strip()[:100]})" if line_str != raw_line else "")
                    })

        # 5. Check Python AST for python files or added python code
        if effective_file.endswith(".py") or any("import " in l or "def " in l for l in added_lines):
            py_code = "\n".join(added_lines)
            ast_issues = check_python_ast(py_code)
            for ai in ast_issues:
                if is_test and ai["rule_id"] == "AST_PYTHON_EVAL":
                    if is_safe_test_eval(py_code):
                        continue
                issues.append(ai)

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
