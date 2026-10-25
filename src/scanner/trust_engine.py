"""
CopilotShield - Authoritative Trust Engine
Calculates true multi-factor Trust Score (0-100) combining:
1. Security & AST analysis (40%)
2. Cryptographic Provenance (30%)
3. Dynamic SQLite Agent Reputation (15%)
4. Automated Test Verification (15%)

Agent reputation actively governs merge decisions: degraded agents or probationary agents
cannot bypass gates. Records real audit telemetry to SQLite.
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
    
    # 3. Dynamic SQLite Reputation Query
    agent_id = prov_report.get("agent_id")
    if agent_id and prov_report.get("verified"):
        rep_report = get_agent_reputation(agent_id)
        rep_score = rep_report.get("reputation_score", 60)
        rep_level = rep_report.get("reputation_level", "PROBATIONARY")
    else:
        rep_report = {
            "registered": False,
            "reputation_score": 50,
            "reputation_level": "UNATTESTED",
            "reliability_percentage": 0.0,
            "total_prs_audited": 0,
            "blocked_prs": 0
        }
        rep_score = 50
        rep_level = "UNATTESTED"

    # 4. Sandbox Test Execution
    if run_sandbox_tests:
        sandbox_res = run_tests_in_sandbox(test_command)
        test_passed = sandbox_res["passed"]
        test_details = sandbox_res["details"]
    else:
        test_passed = True
        test_details = "Static audit (no sandbox command specified)."

    # Multi-Factor Score Calculation
    sec_penalty = sec_report["max_risk_score"]
    sec_score = max(0, 100 - sec_penalty)
    prov_score = prov_report["confidence_score"]
    test_score = 100 if test_passed else 0

    # Composite Trust Score: 40% Security, 30% Provenance, 15% Dynamic Reputation, 15% Tests
    trust_score = int(
        (sec_score * 0.40) + 
        (prov_score * 0.30) + 
        (rep_score * 0.15) + 
        (test_score * 0.15)
    )
    
    # DECISION GATEKEEPING LOGIC ENFORCING REPUTATION & CRYPTO:
    if prov_report["status"] in ("AUTHOR_IMPERSONATION_DETECTED", "INVALID_CRYPTOGRAPHIC_SIGNATURE", "REGISTRY_TAMPERING_DETECTED"):
        decision = "BLOCK"
        decision_label = "🚨 CRITICAL FORGERY / TAMPERING - MERGE BLOCKED"
        badge_color = "red"
        trust_score = min(trust_score, 15)  # Cap score immediately on forgery
    elif sec_report["has_prompt_injection"] or sec_penalty >= 85:
        decision = "BLOCK"
        decision_label = "🚨 INJECTION ATTACK / THREAT - MERGE BLOCKED"
        badge_color = "red"
    elif not test_passed:
        decision = "BLOCK"
        decision_label = "❌ TEST FAILURE - MERGE BLOCKED"
        badge_color = "red"
    elif rep_level == "REVOKED":
        decision = "BLOCK"
        decision_label = "🚨 REVOKED AGENT - MERGE BLOCKED"
        badge_color = "red"
        trust_score = min(trust_score, 10)
    elif rep_level == "DEGRADED":
        decision = "BLOCK"
        decision_label = "🚨 DEGRADED AGENT REPUTATION - MERGE BLOCKED"
        badge_color = "red"
        trust_score = min(trust_score, 45)
    elif rep_level == "PROBATIONARY" and rep_report["total_prs_audited"] < 3:
        # Unproven agent: must undergo manual human signoff even with valid crypto
        decision = "WARN"
        decision_label = "⚠️ PROBATIONARY AGENT - MANUAL REVIEW REQUIRED"
        badge_color = "yellow"
    elif prov_report["verified"] and sec_report["is_safe"] and trust_score >= 80:
        decision = "PASS"
        decision_label = "✅ CRYPTOGRAPHICALLY VERIFIED - AUTO-MERGE ELIGIBLE"
        badge_color = "brightgreen"
    else:
        decision = "WARN"
        decision_label = "⚠️ UNATTESTED CONTRIBUTOR - MANUAL REVIEW REQUIRED"
        badge_color = "yellow"

    # Record audit telemetry into SQLite database
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
| **Dynamic Reputation** | `{rep_level}` | `{rep_score}/100` |
| **Automated Tests** | `{"PASS" if test_passed else "FAIL"}` | `{test_score}/100` |

* **Agent Identity:** `{prov_report['agent_name']}` (`{prov_report['agent_id']}`)
* **Attestation Verification:** {prov_report['details']}
* **Reputation Status:** Level `{rep_level}`, Reliability `{rep_report.get('reliability_percentage', 0)}%` ({rep_report.get('total_prs_audited', 0)} historical audits)
* **Test Verification:** {test_details}
"""

    if sec_report["findings"]:
        markdown += "\n#### ⚠️ Detected Security Risks:\n"
        for idx, f in enumerate(sec_report["findings"], 1):
            markdown += f"- **[{f['severity']}] {f['rule_id']}** (Line {f.get('line', '?')})\n  - Evidence: `{f['evidence']}`\n"
    else:
        markdown += "\n> ✨ **Zero prompt injections, obfuscations, or dangerous code patterns detected.**\n"

    return {
        "trust_score": trust_score,
        "decision": decision,
        "decision_label": decision_label,
        "badge_color": badge_color,
        "security": sec_report,
        "provenance": prov_report,
        "reputation": rep_report,
        "markdown_report": markdown
    }
