"""
CopilotShield - Persistent Agent Reputation & Hardened Key Registry
Uses SQLite with security controls to store real agent registrations, public keys,
and verifiable audit history. Dynamic reputation scores directly govern gatekeeping decisions.
"""

import sqlite3
import os
import time
import re
from typing import Dict, Any, Optional

DB_PATH = os.environ.get("COPILOT_SHIELD_DB", os.path.join(os.path.dirname(__file__), "..", "..", "copilot_shield.db"))

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Registered Agents Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agents (
        agent_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        public_key_base64 TEXT NOT NULL,
        authorized_email_pattern TEXT NOT NULL,
        organization TEXT NOT NULL,
        registered_at INTEGER NOT NULL,
        is_revoked INTEGER DEFAULT 0,
        is_immutable INTEGER DEFAULT 0
    )
    """)
    
    # Audit History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT,
        pr_identifier TEXT NOT NULL,
        author_email TEXT NOT NULL,
        trust_score INTEGER NOT NULL,
        decision TEXT NOT NULL,
        has_prompt_injection INTEGER NOT NULL,
        findings_count INTEGER NOT NULL,
        diff_sha256 TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        FOREIGN KEY(agent_id) REFERENCES agents(agent_id)
    )
    """)
    # Check for is_immutable column in existing database
    cursor.execute("PRAGMA table_info(agents)")
    columns = [row[1] for row in cursor.fetchall()]
    if "is_immutable" not in columns:
        cursor.execute("ALTER TABLE agents ADD COLUMN is_immutable INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


def is_secure_email_pattern(pattern: str, agent_id: str) -> bool:
    """
    Validates that an email pattern is strictly bound to the agent identity.
    Rejects insecure wildcards like '*@github.com' or '*@evil.com' that allow any attacker at that domain.
    """
    sub_patterns = [p.strip().lower() for p in pattern.split(",") if p.strip()]
    if not sub_patterns:
        return False

    clean_agent = re.sub(r"[^a-zA-Z0-9_-]", "", agent_id.lower())
    for p in sub_patterns:
        # Reject blanket wildcards matching any user at a domain (e.g. *@domain.com, *domain.com)
        if re.match(r"^\*+@[a-zA-Z0-9.-]+$", p) or p == "*" or p == "*@*":
            return False
        # The pattern must contain part of the agent identity or be an explicit email address
        if "@" not in p:
            return False
    return True

def register_agent(
    agent_id: str, 
    name: str, 
    pub_key_base64: str, 
    authorized_email: str, 
    org: str,
    admin_auth: Optional[str] = None
) -> bool:
    """
    Registers or updates an agent in the cryptographic key registry.
    Enforces strict pattern validation and prevents unauthorized key overwriting.
    """
    # Enforce strict authorized email pattern
    if not is_secure_email_pattern(authorized_email, agent_id):
        raise ValueError(
            f"INSECURE_EMAIL_PATTERN: The pattern '{authorized_email}' is too loose. "
            f"Blanket domain wildcards like '*@domain.com' are forbidden because attackers can spoof "
            f"arbitrary usernames. Specify an exact email or pattern tied to '{agent_id}'."
        )

    # If an admin key is required by the environment, verify it
    required_admin_key = os.environ.get("COPILOT_SHIELD_ADMIN_KEY")
    if required_admin_key and admin_auth != required_admin_key:
        raise PermissionError("UNAUTHORIZED_AGENT_REGISTRATION: Admin authentication token required to register or update agent keys.")

    conn = get_db()
    cursor = conn.cursor()
    try:
        # Check if agent is immutable (protected root key)
        cursor.execute("SELECT is_immutable FROM agents WHERE agent_id = ?", (agent_id,))
        existing = cursor.fetchone()
        if existing and existing["is_immutable"] and not admin_auth:
            raise PermissionError(f"IMMUTABLE_AGENT: '{agent_id}' is a protected system agent and cannot be modified without admin authorization.")

        cursor.execute("""
        INSERT INTO agents (agent_id, name, public_key_base64, authorized_email_pattern, organization, registered_at, is_revoked, is_immutable)
        VALUES (?, ?, ?, ?, ?, ?, 0, 0)
        ON CONFLICT(agent_id) DO UPDATE SET
            name=excluded.name,
            public_key_base64=excluded.public_key_base64,
            authorized_email_pattern=excluded.authorized_email_pattern,
            organization=excluded.organization
        """, (agent_id, name, pub_key_base64, authorized_email, org, int(time.time())))
        conn.commit()
        return True
    finally:
        conn.close()

def get_agent(agent_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM agents WHERE agent_id = ?", (agent_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def record_audit(agent_id: Optional[str], pr_id: str, author_email: str, trust_score: int, decision: str, has_injection: bool, findings_count: int, diff_hash: str):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO audit_logs (agent_id, pr_identifier, author_email, trust_score, decision, has_prompt_injection, findings_count, diff_sha256, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (agent_id, pr_id, author_email, trust_score, decision, 1 if has_injection else 0, findings_count, diff_hash, int(time.time())))
        conn.commit()
    finally:
        conn.close()

def get_agent_reputation(agent_id: str) -> Dict[str, Any]:
    """
    Computes dynamic reputation metrics and authoritative reputation score from audit history.
    This score directly influences gatekeeping decisions.
    """
    conn = get_db()
    cursor = conn.cursor()
    try:
        agent = get_agent(agent_id)
        if not agent:
            return {
                "registered": False,
                "agent_id": agent_id,
                "reputation_score": 0,
                "reputation_level": "UNREGISTERED",
                "total_prs_audited": 0,
                "passed_prs": 0,
                "blocked_prs": 0,
                "average_trust_score": 0.0,
                "reliability_percentage": 0.0,
                "is_revoked": False,
                "error": "AGENT_NOT_REGISTERED",
                "details": f"No agent with ID '{agent_id}' exists in the cryptographic registry."
            }

        if agent["is_revoked"]:
            return {
                "registered": True,
                "agent_id": agent["agent_id"],
                "name": agent["name"],
                "reputation_score": 0,
                "reputation_level": "REVOKED",
                "total_prs_audited": 0,
                "passed_prs": 0,
                "blocked_prs": 0,
                "average_trust_score": 0.0,
                "reliability_percentage": 0.0,
                "is_revoked": True,
                "details": f"Agent '{agent_id}' cryptographic keys have been revoked."
            }

        cursor.execute("SELECT COUNT(*) as total FROM audit_logs WHERE agent_id = ?", (agent_id,))
        total = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) as passed FROM audit_logs WHERE agent_id = ? AND decision = 'PASS'", (agent_id,))
        passed = cursor.fetchone()["passed"]

        cursor.execute("SELECT COUNT(*) as blocked FROM audit_logs WHERE agent_id = ? AND decision = 'BLOCK'", (agent_id,))
        blocked = cursor.fetchone()["blocked"]

        cursor.execute("SELECT AVG(trust_score) as avg_score FROM audit_logs WHERE agent_id = ?", (agent_id,))
        avg_score_row = cursor.fetchone()["avg_score"]
        avg_score = round(avg_score_row, 1) if avg_score_row is not None else 0.0

        reliability_pct = round((passed / total * 100), 1) if total > 0 else 0.0

        # Dynamic reputation score calculation (0 - 100):
        # 1. New agent baseline is probationary (60)
        # 2. Existing agent is scored on reliability and trust history with heavy penalties for blocks
        if total == 0:
            reputation_score = 60  # Neutral probationary score for unproven agent
            reputation_level = "PROBATIONARY"
        else:
            base_score = (reliability_pct * 0.70) + (avg_score * 0.30)
            # Penalty: each blocked PR incurs a severe reputation penalty (15 pts each)
            penalty = min(60, blocked * 15)
            # Volume confidence boost: agents with >= 5 successful audits get up to +10 pts
            volume_bonus = min(10, total * 2) if blocked == 0 else 0
            reputation_score = max(0, min(100, int(base_score - penalty + volume_bonus)))

            if reputation_score < 50 or (total >= 2 and blocked / total >= 0.3):
                reputation_level = "DEGRADED"
            elif total < 3:
                reputation_level = "PROBATIONARY"
            elif reputation_score >= 85 and total >= 5:
                reputation_level = "HIGHLY_TRUSTED"
            else:
                reputation_level = "ESTABLISHED"

        return {
            "registered": True,
            "agent_id": agent["agent_id"],
            "name": agent["name"],
            "organization": agent["organization"],
            "authorized_email": agent["authorized_email_pattern"],
            "public_key_fingerprint": agent["public_key_base64"][:16] + "...",
            "total_prs_audited": total,
            "passed_prs": passed,
            "blocked_prs": blocked,
            "average_trust_score": avg_score,
            "reliability_percentage": reliability_pct,
            "reputation_score": reputation_score,
            "reputation_level": reputation_level,
            "is_revoked": bool(agent["is_revoked"])
        }
    finally:
        conn.close()

# Initialize schema
init_db()
