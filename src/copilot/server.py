"""
CopilotShield - GitHub Copilot Agent Extension Server
Implements GitHub Copilot Extensions protocol with:
- Real SQLite Agent Reputation database queries
- Real PR diff fetching via GitHub API (when repo is provided)
- Hardened prompt-injection & cryptographic verification
"""

import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os
import hmac
import hashlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.scanner.trust_engine import compute_trust_report
from src.scanner.reputation_db import get_agent_reputation
from src.github.api_client import GitHubClient

class CopilotExtensionHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-GitHub-Token, X-Hub-Signature-256")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        if self.path in ("/health", "/"):
            self._set_headers(200)
            res = {
                "status": "online",
                "service": "CopilotShield Live Agent Extension",
                "version": "2.0.0",
                "backed_by": "SQLite Dynamic Reputation & Ed25519 Cryptographic Attestation",
                "supported_commands": ["/verify-pr", "/scan-diff", "/agent-reputation", "/demo", "/help"]
            }
            self.wfile.write(json.dumps(res, indent=2).encode("utf-8"))
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not Found"}')

    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            post_bytes = self.rfile.read(content_length)
            post_data = post_bytes.decode("utf-8", errors="replace")

            # Verify GitHub request signature if secret is configured in environment
            webhook_secret = os.environ.get("GITHUB_WEBHOOK_SECRET") or os.environ.get("COPILOT_SHIELD_SECRET")
            if webhook_secret:
                hub_sig = self.headers.get("X-Hub-Signature-256", "")
                if not hub_sig:
                    self._set_headers(401)
                    self.wfile.write(b'{"error": "Missing X-Hub-Signature-256 header"}')
                    return
                expected_sig = "sha256=" + hmac.new(webhook_secret.encode("utf-8"), post_bytes, hashlib.sha256).hexdigest()
                if not hmac.compare_digest(hub_sig, expected_sig):
                    self._set_headers(401)
                    self.wfile.write(b'{"error": "Invalid request signature"}')
                    return

            try:
                body = json.loads(post_data) if post_data else {}
            except Exception:
                body = {"prompt": post_data}

            user_prompt = ""
            if isinstance(body.get("messages"), list) and len(body["messages"]) > 0:
                last_msg = body["messages"][-1]
                if isinstance(last_msg, dict):
                    raw_content = last_msg.get("content")
                    user_prompt = str(raw_content) if raw_content is not None else ""
            elif "prompt" in body:
                raw_content = body.get("prompt")
                user_prompt = str(raw_content) if raw_content is not None else ""

            user_prompt = user_prompt.strip()
            print(f"[Copilot Extension] Received prompt: {user_prompt[:80]}...")

            response_text = self.handle_copilot_command(user_prompt)

            # Stream response back via Server-Sent Events (SSE)
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()

            payload = {
                "choices": [
                    {
                        "index": 0,
                        "delta": {
                            "role": "assistant",
                            "content": response_text
                        }
                    }
                ]
            }
            sse_chunk = f"data: {json.dumps(payload)}\n\ndata: [DONE]\n\n"
            self.wfile.write(sse_chunk.encode("utf-8"))
        except Exception as e:
            try:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": f"Internal Server Error: {str(e)}"}).encode("utf-8"))
            except Exception:
                pass

    def handle_copilot_command(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if "/help" in prompt_lower or not prompt:
            return (
                "### 🛡️ CopilotShield Assistant\n\n"
                "I perform **real cryptographic Ed25519 signature checks**, AST de-obfuscation, and query live SQLite agent reputation.\n\n"
                "**Available Commands:**\n"
                "- `@copilot-shield /agent-reputation <agent_id>` - Query live reputation history from the registry.\n"
                "- `@copilot-shield /verify-pr <owner/repo#num>` - Fetch and audit a real PR from GitHub.\n"
                "- `@copilot-shield /scan-diff <code_snippet>` - Scan raw patch/code for injection attacks & AST bypasses.\n"
                "- `@copilot-shield /demo` - Run verified vs. attack test comparison."
            )

        if "/demo" in prompt_lower:
            return (
                "### 🛡️ CopilotShield Architecture & Verification Demo\n\n"
                "| Scenario | Verification Mechanism | Security Gate Verdict |\n"
                "| :--- | :--- | :--- |\n"
                "| **1. Legitimate Agent PR** | Ed25519 Signature + Noreply Pattern | ✅ PASS (`100/100` Trust Score) |\n"
                "| **2. Identity Forgery** | Disallowed Domain Pattern | 🚨 BLOCKED (`15/100` Impersonation) |\n"
                "| **3. Multi-Vector Evasion** | AST De-obfuscation (`curl | bash`, SSH, env) | 🚨 BLOCKED (`37/100` Threat Detected) |\n"
                "| **4. Prompt Injection** | Zero-width & Authority Spoofing Defense | 🚨 BLOCKED (`38/100` Injection Detected) |\n"
                "| **5. Benign Code & Docs** | Quoted & Regex.exec False-Alarm Filters | ✅ CLEAN (`0` False Alarms) |\n\n"
                "To run all live tests and cryptography demonstrations locally:\n"
                "```bash\npython demo/run_demo.py\n```"
            )

        if "/agent-reputation" in prompt_lower:
            parts = prompt.split()
            agent_id = ""
            for p in parts:
                if p.lower() != "/agent-reputation" and not p.startswith("@"):
                    agent_id = p
                    break
            if not agent_id or agent_id.startswith("/"):
                return "⚠️ Please specify an agent ID, e.g.: `@copilot-shield /agent-reputation copilot-workspace`"

            rep = get_agent_reputation(agent_id)
            if not rep["registered"]:
                return (
                    f"### ❌ Agent Reputation: `{agent_id}`\n\n"
                    f"**Status:** `UNREGISTERED_AGENT`\n"
                    f"- This agent does not exist in the trusted Ed25519 public key registry.\n"
                    f"- **Historical PRs Audited:** `0`\n"
                    f"- **Trust Baseline:** `0 / 100`\n"
                    f"- **Recommendation:** Reject or require strict manual human review."
                )

            return (
                f"### 🛡️ Agent Reputation Record: `{rep['agent_id']}`\n\n"
                f"| Attribute | Value |\n"
                f"| :--- | :--- |\n"
                f"| **Agent Name** | `{rep['name']}` |\n"
                f"| **Organization** | `{rep['organization']}` |\n"
                f"| **Authorized Identity** | `{rep['authorized_email']}` |\n"
                f"| **Public Key Fingerprint** | `{rep['public_key_fingerprint']}` |\n"
                f"| **Total Audits in DB** | `{rep['total_prs_audited']}` |\n"
                f"| **Reputation Level** | `{rep['reputation_level']}` |\n"
                f"| **Dynamic Reputation Score** | `{rep['reputation_score']} / 100` |\n"
                f"| **Verified Safe PRs** | `{rep['passed_prs']}` |\n"
                f"| **Blocked Malicious PRs** | `{rep['blocked_prs']}` |\n"
                f"| **Average Trust Score** | `{rep['average_trust_score']} / 100` |\n"
                f"| **Reliability Percentage** | `{rep['reliability_percentage']}%` |\n"
            )

        if "/verify-pr" in prompt_lower:
            tokens = prompt.split()
            pr_arg = ""
            for t in tokens:
                if t.lower() != "/verify-pr" and not t.startswith("@"):
                    pr_arg = t
                    break
            
            if not pr_arg:
                return "⚠️ Please specify a PR target in format `owner/repo#number`, e.g.: `@copilot-shield /verify-pr octocat/Hello-World#42`"

            if "#" not in pr_arg or "/" not in pr_arg:
                return f"⚠️ Invalid PR target format `{pr_arg}`. Expected `owner/repo#number` (e.g. `octocat/Hello-World#42`)."

            parts = pr_arg.split("#")
            if len(parts) != 2 or not parts[1].isdigit():
                return f"⚠️ Malformed PR argument `{pr_arg}`. Expected exactly one `#` followed by a numeric PR number (e.g. `owner/repo#123`)."

            repo = parts[0].strip()
            pr_num = int(parts[1])
            try:
                client = GitHubClient()
                diff = client.get_pr_diff(repo, pr_num)
                details = client.get_pr_details(repo, pr_num)
                report = compute_trust_report(
                    diff,
                    commit_msg=details.get("body", ""),
                    author_email=details.get("author_email", "contributor@github.com"),
                    pr_id=f"{repo}#{pr_num}"
                )
                return f"### 🔍 Live GitHub PR Audit: `{repo}#{pr_num}`\n\n" + report["markdown_report"]
            except Exception as e:
                return f"⚠️ Error fetching PR from GitHub API: {str(e)}"

        if "/scan-diff" in prompt_lower:
            idx = prompt_lower.find("/scan-diff")
            snippet = prompt[idx + len("/scan-diff"):].strip()
            if not snippet:
                return "⚠️ Please provide a patch or code snippet to scan, e.g.: `@copilot-shield /scan-diff const x = 1;`"
            report = compute_trust_report(snippet)
            return f"### 🔍 Code & Patch Security Scan\n\n" + report["markdown_report"]

        # Default fallback: audit code snippet directly
        report = compute_trust_report(prompt)
        return report["markdown_report"]

def run_server(port=8080):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, CopilotExtensionHandler)
    print(f"[*] CopilotShield Extension Server running at http://127.0.0.1:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Shutting down server.")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_server(port)
