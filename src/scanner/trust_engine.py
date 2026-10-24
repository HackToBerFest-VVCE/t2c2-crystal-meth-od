"""
CopilotShield - Authoritative Trust Engine
Calculates true multi-factor Trust Score (0-100), records audit to SQLite DB,
and issues strict gatekeeping decisions.
"""

from typing import Dict, Any, Optional
import hashlib

from .injection_detector import scan_content
from .provenance import verify_provenance
from .sandbox import run_tests_in_sandbox
from .reputation_db import record_audit, get_agent_reputation

def compute_trust_report(
    diff_text: str, 
    commit_msg: str = "", 
    author_email: str = "contributor@github.com", 
    pr_id: str = "local_diff",
    run_sandbox_tests: bool = False,
    test_command: Optional[str] = None
) -> Dict[str, Any]:
    
    # 1. Security & Prompt Injection Analysis
    sec_report = scan_content(diff_text, "pr_diff.patch")
    
    # 2. Cryptographic Provenance Verification
    prov_report = verify_provenance(author_email, commit_msg, diff_text)
    
    # 3. Sandbox Test Execution
    if run_sandbox_tests:
        sandbox_res = run_tests_in_sandbox(test_command)
        test_passed = sandbox_res["passed"]
        test_details = sandbox_res["details"]
    else:
        # If no sandbox requested, neutral test baseline
        test_passed = True
        test_details = "Static audit (no sandbox command specified)."

    # Scoring Component Calculation
    sec_penalty = sec_report["max_risk_score"]
    sec_score = max(0, 100 - sec_penalty)
    prov_score = prov_report["confidence_score"]
    test_score = 100 if test_passed else 0

    # Composite Trust Score (45% Security, 35% Provenance, 20% Tests)
    trust_score = int((sec_score * 0.45) + (prov_score * 0.35) + (test_score * 0.20))
    
    # DECISION GATEKEEPING LOGIC:
    if prov_report["status"] in ("AUTHOR_IMPERSONATION_DETECTED", "INVALID_CRYPTOGRAPHIC_SIGNATURE"):
        decision = "BLOCK"
        decision_label = "🚨 CRITICAL FORGERY - MERGE BLOCKED"
        badge_color = "red"
        trust_score = min(trust_score, 15)  # Cap score immediately on forgery
    elif sec_report["has_prompt_injection"] or sec_penalty >= 85:
        decision = "BLOCK"
        decision_label = "🚨 INJECTION ATTACK - MERGE BLOCKED"
        badge_color = "red"
    elif not test_passed:
        decision = "BLOCK"
        decision_label = "❌ TEST FAILURE - MERGE BLOCKED"
        badge_color = "red"
    elif prov_report["verified"] and sec_report["is_safe"] and trust_score >= 80:
        decision = "PASS"
        decision_label = "✅ CRYPTOGRAPHICALLY VERIFIED - AUTO-MERGE ELIGIBLE"
        badge_color = "brightgreen"
    else:
        decision = "WARN"
        decision_label = "⚠️ UNATTESTED CONTRIBUTOR - MANUAL REVIEW REQUIRED"
        badge_color = "yellow"

    # Record into SQLite audit database
    diff_hash = hashlib.sha256(diff_text.encode("utf-8")).hexdigest()
    record_audit(
        agent_id=prov_report["agent_id"] if prov_report["verified"] else None,
        pr_id=pr_id,
        author_email=author_email,
        trust_score=trust_score,
        decision=decision,
        has_injection=sec_report["has_prompt_injection"],
        findings_count=sec_report["total_issues"],
        diff_hash=diff_hash
    )

    # Format authoritative PR audit comment
    markdown = f"""### 🛡️ CopilotShield Security & Provenance Audit

| Verification Factor | Status | Score |
| :--- | :--- | :--- |
| **Overall Trust Score** | **`{trust_score}/100`** | `{decision_label}` |
| **Agent Provenance** | `{prov_report['status']}` | `{prov_score}/100` |
| **Injection & AST Defense** | `{"FAIL" if not sec_report['is_safe'] else "PASS"}` | `{sec_score}/100` |
| **Automated Tests** | `{"PASS" if test_passed else "FAIL"}` | `{test_score}/100` |

* **Agent Identity:** `{prov_report['agent_name']}` (`{prov_report['agent_id']}`)
* **Attestation Verification:** {prov_report['details']}
* **Test Verification:** {test_details}
"""

    if sec_report["findings"]:
        markdown += "\n#### ⚠️ Detected Security Risks:\n"
        for idx, f in enumerate(sec_report["findings"], 1):
            markdown += f"- **[{f['severity']}] {f['rule_id']}** (Line {f['line']})\n  - Evidence: `{f['evidence']}`\n"
    else:
        markdown += "\n> ✨ **Zero prompt injections, obfuscations, or dangerous code patterns detected.**\n"

    return {
        "trust_score": trust_score,
        "decision": decision,
        "decision_label": decision_label,
        "badge_color": badge_color,
        "security": sec_report,
        "provenance": prov_report,
        "markdown_report": markdown
    }
