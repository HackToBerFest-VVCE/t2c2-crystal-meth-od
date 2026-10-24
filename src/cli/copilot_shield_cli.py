#!/usr/bin/env python3
"""
CopilotShield CLI - Hardened Developer, CI & Cryptographic Tool
Commands:
  scan            Audit a diff/file for prompt injections, backdoors & crypto provenance
  keygen          Generate genuine Ed25519 keypair for an AI agent
  sign            Sign a diff file using an agent private key
  register-agent  Enroll an agent's public key into the local SQLite registry
  reputation      Query dynamic reputation metrics from the database
"""

import sys
import argparse
import os

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from src.scanner.trust_engine import compute_trust_report
from src.scanner.provenance import generate_keypair, sign_diff
from src.scanner.reputation_db import register_agent, get_agent_reputation
from src.github.api_client import GitHubClient

ASCII_BANNER = """
   ______            _ __      __  ____  __    _      __    __
  / ____/___  ____  (_) /___  / /_/ __/ / /_  (_)__  / /___/ /
 / /   / __ \/ __ \/ / / __ \/ __/\ \  / __ \/ / _ \/ / __  / 
/ /___/ /_/ / /_/ / / / /_/ / /____\ \/ / / / /  __/ / /_/ /  
\____/\____/ .___/_/_/\____/\__/_____/_/ /_/_/\___/_/\__,_/   
          /_/     Autonomous Agent Trust & Security Gateway    
"""

def print_banner():
    print(ASCII_BANNER)

def cmd_scan(args):
    if not os.path.exists(args.file):
        print(f"[!] File not found: {args.file}")
        sys.exit(1)

    with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    print(f"\n[*] Auditing file: {args.file} ({len(content)} bytes)...")
    report = compute_trust_report(
        diff_text=content,
        commit_msg=args.commit_msg,
        author_email=args.author,
        pr_id=args.file,
        run_sandbox_tests=args.run_tests,
        test_command=args.test_cmd
    )

    print("\n" + "="*60)
    print(f"  DECISION: {report['decision_label']}")
    print(f"  OVERALL TRUST SCORE: {report['trust_score']} / 100")
    print("="*60)
    print(f"  Provenance: {report['provenance']['status']} (Score: {report['provenance']['confidence_score']})")
    print(f"  Security Status: {'CLEAN' if report['security']['is_safe'] else 'THREATS DETECTED'}")
    print(f"  Prompt Injections: {report['security']['has_prompt_injection']}")
    print(f"  Total Findings: {report['security']['total_issues']}")
    print("="*60)

    if report['security']['findings']:
        print("\n[!] DETECTED ISSUES:")
        for idx, item in enumerate(report['security']['findings'], 1):
            print(f"  [{idx}] Severity: {item['severity']} | Rule: {item['rule_id']} (Line {item['line']})")
            print(f"      Evidence: {item['evidence']}")
    else:
        print("\n[+] Verification Complete: Safe to merge!")

    print("\n[i] Markdown PR summary output:\n")
    print(report["markdown_report"])

    # Optional GitHub Comment & Status posting
    if args.repo and args.pr:
        client = GitHubClient()
        print(f"[*] Posting audit comment to GitHub repo {args.repo} PR #{args.pr}...")
        client.post_pr_comment(args.repo, int(args.pr), report["markdown_report"])
        if args.commit_sha:
            status = "success" if report["decision"] == "PASS" else "failure"
            client.create_commit_status(args.repo, args.commit_sha, status, report["decision_label"])

    if report["decision"] == "BLOCK":
        sys.exit(1)

def cmd_keygen(args):
    keys = generate_keypair()
    print("\n[+] Generated Genuine Ed25519 Keypair for AI Agent:")
    print("-" * 65)
    print(f"Public Key (Enroll in Registry):\n{keys['public_key_base64']}")
    print("-" * 65)
    print(f"Private Key (Keep Secret on Agent):\n{keys['private_key_base64']}")
    print("-" * 65)

def cmd_sign(args):
    if not os.path.exists(args.file):
        print(f"[!] File not found: {args.file}")
        sys.exit(1)
    with open(args.file, "r", encoding="utf-8") as f:
        diff_text = f.read()

    sig = sign_diff(args.key, diff_text)
    print("\n[+] Genuine Ed25519 Signature Generated over Diff SHA256:")
    print(f"X-Signature: {sig}\n")

def cmd_register(args):
    ok = register_agent(
        agent_id=args.id,
        name=args.name,
        pub_key_base64=args.pubkey,
        authorized_email=args.email,
        org=args.org
    )
    if ok:
        print(f"[+] Successfully registered agent '{args.id}' in SQLite key registry.")

def cmd_reputation(args):
    rep = get_agent_reputation(args.id)
    print("\n" + "="*50)
    print(f" AGENT REPUTATION QUERY: {args.id}")
    print("="*50)
    for k, v in rep.items():
        print(f"  {k}: {v}")
    print("="*50)

def main():
    print_banner()
    parser = argparse.ArgumentParser(description="CopilotShield CLI - Verifiable Agent Gatekeeper")
    subparsers = parser.add_subparsers(dest="command")

    # scan
    p_scan = subparsers.add_parser("scan", help="Scan a diff or file")
    p_scan.add_argument("--file", "-f", required=True, help="Path to diff/file")
    p_scan.add_argument("--author", "-a", default="contributor@github.com", help="Author email")
    p_scan.add_argument("--commit-msg", "-m", default="", help="Commit message containing git trailers")
    p_scan.add_argument("--run-tests", action="store_true", help="Execute real test suite in sandbox")
    p_scan.add_argument("--test-cmd", default=None, help="Custom test command, e.g. 'pytest' or 'npm test'")
    p_scan.add_argument("--repo", help="GitHub repo owner/repo for API integration")
    p_scan.add_argument("--pr", help="Pull request number")
    p_scan.add_argument("--commit-sha", help="Commit SHA to set status check")

    # keygen
    subparsers.add_parser("keygen", help="Generate real Ed25519 keypair for an agent")

    # sign
    p_sign = subparsers.add_parser("sign", help="Sign a diff file with private key")
    p_sign.add_argument("--file", "-f", required=True, help="Path to diff file")
    p_sign.add_argument("--key", "-k", required=True, help="Agent private key (base64)")

    # register-agent
    p_reg = subparsers.add_parser("register-agent", help="Register an agent in local DB")
    p_reg.add_argument("--id", required=True, help="Unique agent ID")
    p_reg.add_argument("--name", required=True, help="Human-readable agent name")
    p_reg.add_argument("--pubkey", required=True, help="Agent Ed25519 public key (base64)")
    p_reg.add_argument("--email", required=True, help="Authorized email pattern (e.g. *workspace@github.com)")
    p_reg.add_argument("--org", default="OpenSource", help="Organization name")

    # reputation
    p_rep = subparsers.add_parser("reputation", help="Query agent reputation from DB")
    p_rep.add_argument("--id", required=True, help="Agent ID")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "keygen":
        cmd_keygen(args)
    elif args.command == "sign":
        cmd_sign(args)
    elif args.command == "register-agent":
        cmd_register(args)
    elif args.command == "reputation":
        cmd_reputation(args)

if __name__ == "__main__":
    main()
