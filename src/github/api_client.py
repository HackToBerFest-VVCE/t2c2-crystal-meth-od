"""
CopilotShield - Real GitHub REST API Integration
Interacts with GitHub API to:
- Fetch live PR diff and commit details
- Post real audit markdown comments on PRs
- Create real GitHub Commit Status Checks (state: success / failure)
"""

import urllib.request
import urllib.error
import json
import os
from typing import Dict, Any, Optional

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.environ.get("GITHUB_TOKEN")

    def _headers(self, accept="application/vnd.github.v3+json") -> Dict[str, str]:
        headers = {
            "Accept": accept,
            "User-Agent": "CopilotShield-Security-Gatekeeper"
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def get_pr_diff(self, repo: str, pr_number: int) -> str:
        """Fetches the raw diff of a pull request from GitHub API."""
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
        headers = self._headers(accept="application/vnd.github.v3.diff")
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"GitHub API error {e.code} while fetching PR #{pr_number} from {repo}: {error_body}")

    def get_pr_details(self, repo: str, pr_number: int) -> Dict[str, Any]:
        """Fetches PR metadata (head sha, author, commit message)."""
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
        req = urllib.request.Request(url, headers=self._headers())
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "head_sha": data["head"]["sha"],
                "author_email": data["user"]["login"] + "@users.noreply.github.com",
                "title": data["title"],
                "body": data.get("body") or ""
            }

    def post_pr_comment(self, repo: str, pr_number: int, comment_body: str) -> bool:
        """Posts an audit comment to a GitHub PR issue thread."""
        if not self.token:
            print("[!] GITHUB_TOKEN not set. Skipping live comment post.")
            return False

        url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
        payload = json.dumps({"body": comment_body}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=self._headers(), method="POST")

        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status in (200, 201)
        except urllib.error.HTTPError as e:
            print(f"[!] Failed to post PR comment: {e.code} - {e.read().decode('utf-8', errors='ignore')}")
            return False

    def create_commit_status(self, repo: str, sha: str, state: str, description: str, target_url: str = "") -> bool:
        """
        Creates a GitHub Commit Status Check:
        state: 'success' | 'failure' | 'error' | 'pending'
        """
        if not self.token:
            print("[!] GITHUB_TOKEN not set. Skipping live status check update.")
            return False

        url = f"https://api.github.com/repos/{repo}/statuses/{sha}"
        payload = json.dumps({
            "state": state,
            "context": "CopilotShield / Provenance & Injection Gate",
            "description": description[:140],
            "target_url": target_url
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers=self._headers(), method="POST")

        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status in (200, 201)
        except urllib.error.HTTPError as e:
            print(f"[!] Failed to update commit status: {e.code} - {e.read().decode('utf-8', errors='ignore')}")
            return False
