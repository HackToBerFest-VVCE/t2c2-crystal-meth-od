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
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-GitHub-Token")
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
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        try:
            body = json.loads(post_data) if post_data else {}
        except Exception:
            body = {"prompt": post_data}

        user_prompt = ""
        if "messages" in body and isinstance(body["messages"], list):
            last_msg = body["messages"][-1]
            user_prompt = last_msg.get("content", "")
        else:
            user_prompt = body.get("prompt", "")

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

        if "/agent-reputation" in prompt_lower:
            parts = prompt.split()
            agent_id = parts[-1] if len(parts) > 1 else ""
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
                f"| **Verified Safe PRs** | `{rep['passed_prs']}` |\n"
                f"| **Blocked Malicious PRs** | `{rep['blocked_prs']}` |\n"
                f"| **Average Trust Score** | `{rep['average_trust_score']} / 100` |\n"
                f"| **Reliability Percentage** | `{rep['reliability_percentage']}%` |\n"
            )

        if "/verify-pr" in prompt_lower:
            # Check if an actual GitHub repo/PR is provided, e.g. /verify-pr owner/repo#1
            tokens = prompt.split()
            pr_arg = tokens[-1] if len(tokens) > 1 else ""
            
            if "/" in pr_arg and "#" in pr_arg:
                repo, pr_num_str = pr_arg.split("#")
                try:
                    pr_num = int(pr_num_str)
                    client = GitHubClient()
                    diff = client.get_pr_diff(repo, pr_num)
                    details = client.get_pr_details(repo, pr_num)
                    report = compute_trust_report(diff, commit_msg=details["body"], author_email=details["author_email"], pr_id=f"{repo}#{pr_num}")
                    return f"### 🔍 Live GitHub PR Audit: `{repo}#{pr_num}`\n\n" + report["markdown_report"]
                except Exception as e:
                    return f"⚠️ Error fetching PR from GitHub API: {str(e)}"

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
