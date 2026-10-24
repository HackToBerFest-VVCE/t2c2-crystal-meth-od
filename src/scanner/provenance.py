"""
CopilotShield - Cryptographic Agent Provenance Engine
Performs REAL Ed25519 signature verification against public keys registered in the SQLite registry.
Prevents identity forgery, signature spoofing, and author email impersonation.
"""

import base64
import hashlib
import fnmatch
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

from .reputation_db import get_agent, register_agent

def generate_keypair():
    """Generates a genuine Ed25519 keypair for an agent."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    return {
        "private_key_base64": base64.b64encode(priv_bytes).decode("utf-8"),
        "public_key_base64": base64.b64encode(pub_bytes).decode("utf-8")
    }

def sign_diff(private_key_base64: str, diff_content: str) -> str:
    """Signs the SHA256 digest of a diff using the agent's private Ed25519 key."""
    priv_bytes = base64.b64decode(private_key_base64)
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
    diff_hash = hashlib.sha256(diff_content.encode("utf-8")).digest()
    signature = private_key.sign(diff_hash)
    return base64.b64encode(signature).decode("utf-8")

def extract_commit_trailers(commit_message: str) -> Dict[str, str]:
    """Extracts git trailers like X-Copilot-Agent-ID, X-Signature from commit messages."""
    metadata = {}
    for line in commit_message.strip().splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            k = key.strip()
            v = val.strip()
            if k.startswith("X-") or k in ["Signed-off-by", "Co-authored-by", "Agent-ID"]:
                metadata[k] = v
    return metadata

def verify_provenance(author_email: str, commit_message: str, diff_content: str) -> Dict[str, Any]:
    """
    Real Cryptographic Provenance Verification:
    1. Extracts Agent-ID and Signature from commit trailers.
    2. Queries local SQLite registry for registered Ed25519 public key.
    3. Validates author email against authorized pattern (blocks impersonation like attacker@evil.com).
    4. Computes SHA256 of the diff.
    5. Mathematically verifies Ed25519 signature using public key.
    """
    metadata = extract_commit_trailers(commit_message)
    agent_id = metadata.get("X-Copilot-Agent-ID") or metadata.get("Agent-ID")
    raw_sig = metadata.get("X-Signature")
    
    diff_sha = hashlib.sha256(diff_content.encode("utf-8")).digest()
    diff_hex = hashlib.sha256(diff_content.encode("utf-8")).hexdigest()

    # 1. No agent headers at all
    if not agent_id:
        if "bot" in author_email.lower() or "agent" in author_email.lower():
            return {
                "verified": False,
                "status": "UNATTESTED_BOT",
                "agent_id": "unknown-bot",
                "agent_name": "Unregistered Bot Account",
                "confidence_score": 10,
                "diff_digest": diff_hex[:16],
                "details": "Author claims bot identity in email but provided no X-Copilot-Agent-ID or cryptographic attestation."
            }
        return {
            "verified": False,
            "status": "HUMAN_CONTRIBUTOR",
            "agent_id": "human",
            "agent_name": "Standard Contributor (No Agent Attestation)",
            "confidence_score": 50,
            "diff_digest": diff_hex[:16],
            "details": "No agent attestation headers present. Standard manual review required."
        }

    # 2. Check if agent is enrolled in the cryptographic registry
    agent = get_agent(agent_id)
    if not agent:
        return {
            "verified": False,
            "status": "UNREGISTERED_AGENT_ID",
            "agent_id": agent_id,
            "agent_name": "Unknown / Unregistered Agent",
            "confidence_score": 0,
            "diff_digest": diff_hex[:16],
            "details": f"Agent ID '{agent_id}' is not enrolled in the trusted agent public key registry."
        }

    if agent["is_revoked"]:
        return {
            "verified": False,
            "status": "AGENT_KEY_REVOKED",
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "confidence_score": 0,
            "diff_digest": diff_hex[:16],
            "details": f"Cryptographic keys for agent '{agent_id}' have been revoked due to security policy."
        }

    # 3. Check author email authorization (Preventing attacker@evil.com spoofing copilot-workspace)
    authorized_pattern = agent["authorized_email_pattern"]
    if not fnmatch.fnmatch(author_email.lower(), authorized_pattern.lower()):
        return {
            "verified": False,
            "status": "AUTHOR_IMPERSONATION_DETECTED",
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "confidence_score": 0,
            "diff_digest": diff_hex[:16],
            "details": f"CRITICAL: Author '{author_email}' is not authorized to sign as '{agent_id}'. Expected pattern: '{authorized_pattern}'."
        }

    # 4. Check signature existence
    if not raw_sig:
        return {
            "verified": False,
            "status": "MISSING_SIGNATURE",
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "confidence_score": 0,
            "diff_digest": diff_hex[:16],
            "details": "Agent ID specified but X-Signature header is missing from commit message."
        }

    # 5. Perform Real Ed25519 Signature Verification
    try:
        sig_clean = raw_sig.split(":")[-1].strip()
        sig_bytes = base64.b64decode(sig_clean)
        
        pub_bytes = base64.b64decode(agent["public_key_base64"])
        public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_bytes)
        
        # Verify signature over SHA256(diff)
        public_key.verify(sig_bytes, diff_sha)

        return {
            "verified": True,
            "status": "CRYPTOGRAPHICALLY_VERIFIED",
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "organization": agent["organization"],
            "confidence_score": 100,
            "diff_digest": diff_hex[:16],
            "details": "Ed25519 cryptographic signature verified successfully against enrolled public key."
        }
    except (InvalidSignature, ValueError, Exception) as e:
        return {
            "verified": False,
            "status": "INVALID_CRYPTOGRAPHIC_SIGNATURE",
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "confidence_score": 0,
            "diff_digest": diff_hex[:16],
            "details": f"SIGNATURE VERIFICATION FAILED: The provided X-Signature does not match the diff hash. Possible payload tampering or forged signature ({type(e).__name__})."
        }
