"""
CopilotShield - Persistent Agent Reputation & Key Registry
Uses SQLite to store real agent registrations, public keys, and verifiable audit history.
No hardcoded stats - all metrics are dynamically computed from recorded audits.
"""

import sqlite3
import os
import time
from typing import Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "copilot_shield.db")

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
        is_revoked INTEGER DEFAULT 0
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
    conn.commit()
    conn.close()

def register_agent(agent_id: str, name: str, pub_key_base64: str, authorized_email: str, org: str) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO agents (agent_id, name, public_key_base64, authorized_email_pattern, organization, registered_at)
        VALUES (?, ?, ?, ?, ?, ?)
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
    """Computes dynamic reputation metrics from real audit logs in the database."""
    conn = get_db()
    cursor = conn.cursor()
    try:
        agent = get_agent(agent_id)
        if not agent:
            return {
                "registered": False,
                "agent_id": agent_id,
                "error": "AGENT_NOT_REGISTERED",
                "details": f"No agent with ID '{agent_id}' exists in the cryptographic registry."
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
            "is_revoked": bool(agent["is_revoked"])
        }
    finally:
        conn.close()

# Initialize database schema on load
init_db()
