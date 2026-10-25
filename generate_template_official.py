"""
Official Hacktober Halloween Template System Architecture Renderer for Team Crystal Meth-od.
Generates pixel-perfect architecture diagram matching the organizer's exact B&W illustrated template.
"""

from PIL import Image, ImageDraw, ImageFont
import os

def render_official_template():
    template_path = r"C:/Users/hp/.gemini/antigravity/brain/5d832c7a-5310-48c8-be7e-694eab1a0476/.user_uploaded/media_1792914214399_c066a8ea.jpg"
    im = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(im)

    # 1. Clean old content
    bg_canvas = (245, 245, 245)
    # Clean plaque text & ribbon ornaments in middle
    draw.rectangle([(295, 60), (730, 106)], fill=bg_canvas)
    # Clean subtitle text
    draw.rectangle([(60, 107), (965, 133)], fill=bg_canvas)
    # Clean inner canvas completely
    draw.rectangle([(54, 134), (970, 628)], fill=(255, 255, 255))

    # Fonts
    f_team = ImageFont.truetype("C:/Windows/Fonts/timesbd.ttf", 23)
    f_sub = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
    f_card_num = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 12)
    f_card_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 10)
    f_card_body = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 9)
    f_card_body_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 9)
    f_sec_hdr = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 11)
    f_tech_k = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 9)
    f_tech_v = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 9)
    f_feat_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 10)
    f_feat_desc = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 8)

    # 2. Render Plaque: TEAM CRYSTAL METH-OD
    # Gothic framed plaque
    draw.line([(310, 62), (715, 62)], fill=(20, 20, 20), width=2)
    draw.line([(310, 104), (715, 104)], fill=(20, 20, 20), width=2)
    draw.polygon([(300, 83), (312, 62), (312, 104)], fill=(20, 20, 20))
    draw.polygon([(725, 83), (713, 62), (713, 104)], fill=(20, 20, 20))

    team_text = "TEAM CRYSTAL METH-OD"
    bbox_t = draw.textbbox((0, 0), team_text, font=f_team)
    wt = bbox_t[2] - bbox_t[0]
    draw.text((512 - wt / 2, 70), team_text, fill=(10, 10, 10), font=f_team)

    # 3. Render Subtitle
    sub_text = "SYSTEM ARCHITECTURE: CopilotShield - Cryptographic Agent Provenance & Prompt-Injection Firewall"
    bbox_s = draw.textbbox((0, 0), sub_text, font=f_sub)
    ws = bbox_s[2] - bbox_s[0]
    draw.text((512 - ws / 2, 112), sub_text, fill=(15, 15, 15), font=f_sub)

    # 4. Render 5 Top Workflow Step Cards
    cards_data = [
        {
            "num": "1",
            "title": "Agent Attestation\n& Key Signing",
            "badge": "Ed25519",
            "bullets": [
                "• AI Agent generates PR diff",
                "• Computes SHA-256 diff hash",
                "• Signs commit with Ed25519 key",
                "• Appends X-Copilot-Agent-ID",
                "• Attaches X-Signature trailer"
            ]
        },
        {
            "num": "2",
            "title": "Cryptographic\nProvenance Gate",
            "badge": "Verified",
            "bullets": [
                "• Verifies Ed25519 signature",
                "• Enforces strict email noreply",
                "• Blocks domain/ID impersonation",
                "• Blocks key registry tampering",
                "• Enforces immutable root-of-trust"
            ]
        },
        {
            "num": "3",
            "title": "Multi-Vector\nInjection Scanner",
            "badge": "Firewall",
            "bullets": [
                "• Unrolls string concat ('en'+'v')",
                "• Resolves hex/unicode escapes",
                "• Normalizes Cyrillic homoglyphs",
                "• Intercepts curl|bash pipelines",
                "• Blocks reverse shells & .env theft"
            ]
        },
        {
            "num": "4",
            "title": "Dynamic SQLite\nReputation & Tests",
            "badge": "SQLite3",
            "bullets": [
                "• Queries dynamic reputation DB",
                "• Tracks rolling pass/block audits",
                "• Runs tests in sandbox (shell=False)",
                "• Quoted doc injection filter",
                "• Eliminates false alarms on tests"
            ]
        },
        {
            "num": "5",
            "title": "Trust Scoring\n& Gatekeeping",
            "badge": "Gatekeeper",
            "bullets": [
                "• 4-Factor Trust Score (0-100)",
                "• Multi-gate: PASS, WARN, BLOCK",
                "• Posts rich PR Markdown audit",
                "• Sets commit status check",
                "• Governs Copilot Chat extensions"
            ]
        }
    ]

    x_starts = [56, 241, 426, 611, 796]
    card_w = 172
    y_top = 140
    y_bot = 350

    for idx, c in enumerate(cards_data):
        x1 = x_starts[idx]
        x2 = x1 + card_w

        # Card body
        draw.rounded_rectangle([(x1, y_top), (x2, y_bot)], radius=7, fill=(255, 255, 255), outline=(130, 130, 130), width=1)
        # Header banner
        draw.rounded_rectangle([(x1, y_top), (x2, y_top + 38)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)

        # Number circle badge
        draw.ellipse([(x1 + 6, y_top + 7), (x1 + 30, y_top + 31)], fill=(30, 30, 30))
        draw.text((x1 + 14, y_top + 11), c["num"], fill=(255, 255, 255), font=f_card_num)

        # Title
        t_lines = c["title"].split("\n")
        draw.text((x1 + 36, y_top + 6), t_lines[0], fill=(15, 15, 15), font=f_card_title)
        draw.text((x1 + 36, y_top + 19), t_lines[1], fill=(15, 15, 15), font=f_card_title)

        # Mini badge
        draw.rounded_rectangle([(x2 - 48, y_top + 44), (x2 - 8, y_top + 58)], radius=3, fill=(235, 240, 248), outline=(180, 190, 210), width=1)
        draw.text((x2 - 44, y_top + 46), c["badge"], fill=(30, 60, 120), font=f_card_body_bold)

        # Bullets
        by = y_top + 64
        for b in c["bullets"]:
            draw.text((x1 + 8, by), b, fill=(35, 35, 35), font=f_card_body)
            by += 16

        # Directional Arrow to next card
        if idx < 4:
            ax = x2 + 2
            ay = (y_top + y_bot) // 2
            # Draw crisp arrow line and head
            draw.line([(ax, ay), (ax + 7, ay)], fill=(70, 70, 70), width=2)
            draw.polygon([(ax + 6, ay - 4), (ax + 10, ay), (ax + 6, ay + 4)], fill=(70, 70, 70))

    # 5. Middle Left: Pipeline Components & Integration
    ml_x1, ml_y1, ml_x2, ml_y2 = 56, 358, 628, 516
    draw.rounded_rectangle([(ml_x1, ml_y1), (ml_x2, ml_y2)], radius=7, fill=(255, 255, 255), outline=(130, 130, 130), width=1)
    draw.rounded_rectangle([(ml_x1, ml_y1), (ml_x2, ml_y1 + 22)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)
    draw.text((ml_x1 + 10, ml_y1 + 4), "Pipeline Components & Integration (GitHub-Native & Extension)", fill=(20, 20, 20), font=f_sec_hdr)

    # Input Box: Untrusted Agent PR
    draw.rounded_rectangle([(ml_x1 + 10, ml_y1 + 34), (ml_x1 + 102, ml_y1 + 144)], radius=6, fill=(248, 250, 252), outline=(100, 100, 100), width=1)
    draw.text((ml_x1 + 16, ml_y1 + 44), "Untrusted", fill=(10, 10, 10), font=f_card_body_bold)
    draw.text((ml_x1 + 16, ml_y1 + 58), "Agent PR", fill=(10, 10, 10), font=f_card_body_bold)
    draw.line([(ml_x1 + 16, ml_y1 + 74), (ml_x1 + 96, ml_y1 + 74)], fill=(200, 200, 200), width=1)
    draw.text((ml_x1 + 16, ml_y1 + 82), "• Git Patch Diff", fill=(60, 60, 60), font=f_card_body)
    draw.text((ml_x1 + 16, ml_y1 + 98), "• X-Signature", fill=(60, 60, 60), font=f_card_body)
    draw.text((ml_x1 + 16, ml_y1 + 114), "• Agent-ID", fill=(60, 60, 60), font=f_card_body)
    draw.text((ml_x1 + 16, ml_y1 + 128), "• Author Email", fill=(60, 60, 60), font=f_card_body)

    # Arrow to Engine
    draw.line([(ml_x1 + 105, ml_y1 + 89), (ml_x1 + 118, ml_y1 + 89)], fill=(60, 60, 60), width=2)
    draw.polygon([(ml_x1 + 117, ml_y1 + 85), (ml_x1 + 122, ml_y1 + 89), (ml_x1 + 117, ml_y1 + 93)], fill=(60, 60, 60))

    # Engine Container
    eng_x1 = ml_x1 + 124
    eng_x2 = ml_x1 + 382
    draw.rounded_rectangle([(eng_x1, ml_y1 + 30), (eng_x2, ml_y1 + 148)], radius=6, fill=(246, 248, 252), outline=(70, 70, 70), width=1)
    draw.rectangle([(eng_x1, ml_y1 + 30), (eng_x2, ml_y1 + 48)], fill=(225, 232, 244))
    draw.text((eng_x1 + 28, ml_y1 + 34), "CopilotShield Engine (GitHub Actions / Server)", fill=(15, 30, 60), font=f_card_body_bold)

    # 4 Modules
    m_w = 120
    m_h = 42
    # Mod 1: Ed25519
    draw.rounded_rectangle([(eng_x1 + 6, ml_y1 + 54), (eng_x1 + 6 + m_w, ml_y1 + 54 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw.text((eng_x1 + 12, ml_y1 + 60), "Ed25519 Crypto", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 12, ml_y1 + 72), "Signature Verifier", fill=(80, 80, 80), font=f_card_body)
    draw.text((eng_x1 + 12, ml_y1 + 84), "& Registry Lock", fill=(100, 100, 100), font=f_card_body)

    # Mod 2: AST De-obfuscator
    draw.rounded_rectangle([(eng_x1 + 132, ml_y1 + 54), (eng_x1 + 132 + m_w, ml_y1 + 54 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw.text((eng_x1 + 138, ml_y1 + 60), "AST De-obfuscator", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 138, ml_y1 + 72), "String Concat & Joins", fill=(80, 80, 80), font=f_card_body)
    draw.text((eng_x1 + 138, ml_y1 + 84), "Hex/Unicode Escapes", fill=(100, 100, 100), font=f_card_body)

    # Mod 3: Injection Scanner
    draw.rounded_rectangle([(eng_x1 + 6, ml_y1 + 100), (eng_x1 + 6 + m_w, ml_y1 + 100 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw.text((eng_x1 + 12, ml_y1 + 106), "Injection Firewall", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 12, ml_y1 + 118), "Authority & Homoglyphs", fill=(80, 80, 80), font=f_card_body)
    draw.text((eng_x1 + 12, ml_y1 + 130), "curl|bash & Rev Shells", fill=(100, 100, 100), font=f_card_body)

    # Mod 4: Test Sandbox
    draw.rounded_rectangle([(eng_x1 + 132, ml_y1 + 100), (eng_x1 + 132 + m_w, ml_y1 + 100 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw.text((eng_x1 + 138, ml_y1 + 106), "Test Suite Sandbox", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 138, ml_y1 + 118), "Isolated Execution", fill=(80, 80, 80), font=f_card_body)
    draw.text((eng_x1 + 138, ml_y1 + 130), "shell=False Enforced", fill=(100, 100, 100), font=f_card_body)

    # Connected SQLite DB Box
    db_x1 = eng_x2 + 10
    db_x2 = ml_x2 - 10
    draw.rounded_rectangle([(db_x1, ml_y1 + 30), (db_x2, ml_y1 + 68)], radius=5, fill=(245, 250, 245), outline=(50, 110, 50), width=1)
    draw.text((db_x1 + 10, ml_y1 + 36), "SQLite Dynamic DB", fill=(20, 80, 30), font=f_card_body_bold)
    draw.text((db_x1 + 10, ml_y1 + 49), "Audit History & Reputation Logs", fill=(50, 100, 50), font=f_card_body)

    # Output Items Box
    draw.rounded_rectangle([(db_x1, ml_y1 + 74), (db_x2, ml_y1 + 148)], radius=5, fill=(250, 252, 255), outline=(70, 90, 130), width=1)
    draw.text((db_x1 + 8, ml_y1 + 80), "Outputs & Enforcements:", fill=(20, 30, 70), font=f_card_body_bold)
    draw.text((db_x1 + 8, ml_y1 + 96), "✔ Verified PR (Auto-Merge)", fill=(10, 120, 40), font=f_card_body_bold)
    draw.text((db_x1 + 8, ml_y1 + 112), "💬 Authoritative Markdown Audit", fill=(20, 60, 140), font=f_card_body_bold)
    draw.text((db_x1 + 8, ml_y1 + 128), "🚦 GitHub Commit Status Check", fill=(140, 60, 20), font=f_card_body_bold)

    # 6. Middle Right: Tech Stack Specification
    mr_x1, mr_y1, mr_x2, mr_y2 = 638, 358, 968, 516
    draw.rounded_rectangle([(mr_x1, mr_y1), (mr_x2, mr_y2)], radius=7, fill=(255, 255, 255), outline=(130, 130, 130), width=1)
    draw.rounded_rectangle([(mr_x1, mr_y1), (mr_x2, mr_y1 + 22)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)
    draw.text((mr_x1 + 10, mr_y1 + 4), "Tech Stack Specification", fill=(20, 20, 20), font=f_sec_hdr)

    tech_items = [
        ("Cryptography:", "Ed25519 (RFC 8032), SHA-256, HMAC-SHA256"),
        ("CI/CD Platform:", "GitHub Actions Composite Action, REST API"),
        ("Agent Protocol:", "Copilot Agent Extensions Protocol (HTTP/SSE)"),
        ("Analysis & AST:", "Python ast module, Unicode Homoglyph Engine"),
        ("Database Engine:", "SQLite3 (Dynamic Reputation & Audit Trail)"),
        ("Test Isolation:", "Pytest (39 Unit Tests), Subprocess Sandbox"),
        ("Runtime & Core:", "Python 3.11+ / Strict Cryptographic Policies")
    ]

    ty = mr_y1 + 30
    for k, v in tech_items:
        draw.text((mr_x1 + 10, ty), k, fill=(15, 15, 15), font=f_tech_k)
        draw.text((mr_x1 + 115, ty), v, fill=(45, 45, 45), font=f_tech_v)
        ty += 16
        # separator line
        draw.line([(mr_x1 + 8, ty - 2), (mr_x2 - 8, ty - 2)], fill=(238, 240, 242), width=1)

    # 7. Bottom Section: Key Features
    kf_x1, kf_y1, kf_x2, kf_y2 = 56, 524, 968, 626
    draw.rounded_rectangle([(kf_x1, kf_y1), (kf_x2, kf_y2)], radius=7, fill=(255, 255, 255), outline=(130, 130, 130), width=1)
    draw.rounded_rectangle([(kf_x1, kf_y1), (kf_x2, kf_y1 + 20)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)
    draw.text((kf_x1 + 10, kf_y1 + 3), "Key Features & Architectural Security Guarantees", fill=(20, 20, 20), font=f_sec_hdr)

    features = [
        ("Cryptographic Provenance", "Ed25519 digital signatures prove", "agent authenticity & prevent spoofing."),
        ("Anti-Evasion AST Engine", "Unrolls string concatenations, joins,", "and hex/unicode escapes dynamically."),
        ("Prompt Injection Firewall", "Neutralizes authority spoofing, hidden", "system tags, reverse shells & homoglyphs."),
        ("Dynamic SQLite Reputation", "Historical PR audit logs & pass rates", "actively govern autonomous merge gating."),
        ("Automated CI/CD Gate", "Posts rich PR markdown audits, sets", "status checks & serves Copilot Chat.")
    ]

    col_w = (kf_x2 - kf_x1) // 5
    for idx, (f_title, f_l1, f_l2) in enumerate(features):
        fx = kf_x1 + idx * col_w + 6
        # Bullet badge
        draw.rectangle([(fx, kf_y1 + 27), (fx + 5, kf_y1 + 37)], fill=(40, 40, 40))
        draw.text((fx + 10, kf_y1 + 26), f_title, fill=(15, 15, 15), font=f_feat_title)
        draw.text((fx + 10, kf_y1 + 42), f_l1, fill=(70, 70, 70), font=f_feat_desc)
        draw.text((fx + 10, kf_y1 + 54), f_l2, fill=(70, 70, 70), font=f_feat_desc)
        if idx < 4:
            draw.line([(fx + col_w - 4, kf_y1 + 26), (fx + col_w - 4, kf_y2 - 6)], fill=(225, 225, 225), width=1)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "copilot_shield_architecture_template.png")
    im.save(out_path)
    print(f"Successfully generated official template architecture diagram: {out_path}")

if __name__ == "__main__":
    render_official_template()
