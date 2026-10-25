"""
Rich Visual System Architecture Renderer for Team Crystal Meth-od.
Adds full visual illustrations:
- 3D SQLite multi-tier cylinder databases
- Git branch nodes, diffs & commit trailers
- Ed25519 cryptographic keys, locks & shields
- AST syntax trees & de-obfuscation flows
- Test sandbox beakers & trust score meters
- Visual badges & icons across all 5 workflow cards, middle integration engine, tech stack & bottom key features.
"""

from PIL import Image, ImageDraw, ImageFont
import math
import os

def create_rich_visual_architecture():
    template_path = r"C:/Users/hp/.gemini/antigravity/brain/5d832c7a-5310-48c8-be7e-694eab1a0476/.user_uploaded/media_1792914214399_c066a8ea.jpg"
    im = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(im)

    # 1. Clean old template areas
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
    f_card_body = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 8)
    f_card_body_bold = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 8)
    f_sec_hdr = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 11)
    f_tech_k = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 9)
    f_tech_v = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 9)
    f_feat_title = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 9)
    f_feat_desc = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 8)
    f_badge = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 8)
    f_mini = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 7)

    # 2. Render Plaque: TEAM CRYSTAL METH-OD
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

    # Visual Helper Functions
    def draw_cylinder_db(x, y, w, h, fill_top=(230, 245, 255), fill_body=(210, 235, 250), outline=(20, 70, 130), num_layers=3):
        layer_h = h / num_layers
        ell_h = layer_h * 0.45
        for i in range(num_layers - 1, -1, -1):
            ly = y + i * (layer_h * 0.85)
            draw.rectangle([(x, ly + ell_h / 2), (x + w, ly + layer_h)], fill=fill_body)
            draw.ellipse([(x, ly + layer_h - ell_h / 2), (x + w, ly + layer_h + ell_h / 2)], fill=fill_body, outline=outline, width=1)
            draw.line([(x, ly + ell_h / 2), (x, ly + layer_h)], fill=outline, width=1)
            draw.line([(x + w, ly + ell_h / 2), (x + w, ly + layer_h)], fill=outline, width=1)
            draw.ellipse([(x, ly), (x + w, ly + ell_h)], fill=fill_top, outline=outline, width=1)
            # Status light
            draw.ellipse([(x + w - 8, ly + layer_h * 0.55), (x + w - 4, ly + layer_h * 0.55 + 4)], fill=(30, 190, 80))

    def draw_git_branch(x, y, color=(40, 40, 40)):
        # Main line
        draw.line([(x + 5, y + 2), (x + 5, y + 26)], fill=color, width=2)
        # Commit node 1
        draw.ellipse([(x + 2, y + 2), (x + 8, y + 8)], fill=(255, 255, 255), outline=color, width=2)
        # Commit node 2
        draw.ellipse([(x + 2, y + 20), (x + 8, y + 26)], fill=(255, 255, 255), outline=color, width=2)
        # Branch curve
        draw.line([(x + 5, y + 14), (x + 16, y + 6)], fill=color, width=2)
        draw.ellipse([(x + 13, y + 3), (x + 19, y + 9)], fill=(40, 120, 220), outline=color, width=1)

    def draw_key_icon(x, y, color=(200, 140, 20)):
        # Circle head
        draw.ellipse([(x, y + 4), (x + 10, y + 14)], fill=(255, 255, 255), outline=color, width=2)
        draw.ellipse([(x + 3, y + 7), (x + 7, y + 11)], fill=color)
        # Shaft
        draw.line([(x + 10, y + 9), (x + 22, y + 9)], fill=color, width=2)
        # Teeth
        draw.line([(x + 18, y + 9), (x + 18, y + 14)], fill=color, width=2)
        draw.line([(x + 21, y + 9), (x + 21, y + 13)], fill=color, width=2)

    def draw_shield_icon(x, y, w, h, fill_col=(235, 248, 240), stroke_col=(30, 140, 60), check=True):
        pts = [
            (x + w / 2, y),
            (x + w, y + h * 0.25),
            (x + w, y + h * 0.65),
            (x + w / 2, y + h),
            (x, y + h * 0.65),
            (x, y + h * 0.25)
        ]
        draw.polygon(pts, fill=fill_col, outline=stroke_col)
        if check:
            # Checkmark
            draw.line([(x + w * 0.28, y + h * 0.52), (x + w * 0.45, y + h * 0.70)], fill=stroke_col, width=2)
            draw.line([(x + w * 0.45, y + h * 0.70), (x + w * 0.75, y + h * 0.35)], fill=stroke_col, width=2)

    def draw_ast_icon(x, y, color=(40, 100, 180)):
        # Root
        draw.ellipse([(x + 8, y), (x + 16, y + 8)], fill=(40, 100, 180))
        # Left child
        draw.ellipse([(x, y + 14), (x + 8, y + 22)], fill=(20, 140, 70))
        # Right child
        draw.ellipse([(x + 16, y + 14), (x + 24, y + 22)], fill=(200, 90, 20))
        # Connectors
        draw.line([(x + 12, y + 8), (x + 4, y + 14)], fill=color, width=1)
        draw.line([(x + 12, y + 8), (x + 20, y + 14)], fill=color, width=1)

    def draw_test_tubes(x, y, color=(160, 50, 180)):
        # Tube 1
        draw.rectangle([(x + 2, y + 4), (x + 10, y + 22)], outline=color, width=1, fill=(245, 235, 255))
        draw.ellipse([(x + 2, y + 18), (x + 10, y + 26)], fill=(180, 80, 220), outline=color, width=1)
        # Liquid line
        draw.line([(x + 2, y + 12), (x + 10, y + 12)], fill=color, width=1)
        # Tube 2
        draw.rectangle([(x + 14, y + 2), (x + 22, y + 20)], outline=(40, 120, 200), width=1, fill=(235, 245, 255))
        draw.ellipse([(x + 14, y + 16), (x + 22, y + 24)], fill=(40, 150, 220), outline=(40, 120, 200), width=1)

    def draw_gauge_icon(x, y, color=(30, 150, 70)):
        # Dial arc
        draw.arc([(x, y), (x + 24, y + 24)], start=160, end=380, fill=color, width=3)
        # Center pin
        draw.ellipse([(x + 10, y + 10), (x + 14, y + 14)], fill=(20, 20, 20))
        # Needle pointing high/100
        draw.line([(x + 12, y + 12), (x + 20, y + 6)], fill=(200, 40, 30), width=2)

    def draw_terminal_icon(x, y, w=24, h=18):
        draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=2, fill=(25, 30, 40), outline=(80, 80, 80), width=1)
        draw.rectangle([(x, y), (x + w, y + 5)], fill=(45, 50, 65))
        draw.ellipse([(x + 2, y + 1.5), (x + 4, y + 3.5)], fill=(220, 60, 50))
        draw.ellipse([(x + 5.5, y + 1.5), (x + 7.5, y + 3.5)], fill=(220, 180, 40))
        draw.ellipse([(x + 9, y + 1.5), (x + 11, y + 3.5)], fill=(40, 180, 60))
        # Prompt
        draw.line([(x + 3, y + 8), (x + 7, y + 11)], fill=(40, 220, 120), width=1)
        draw.line([(x + 7, y + 11), (x + 3, y + 14)], fill=(40, 220, 120), width=1)
        draw.line([(x + 9, y + 13), (x + 14, y + 13)], fill=(255, 255, 255), width=1)

    # 4. Render 5 Top Workflow Step Cards WITH VISUALS
    cards_data = [
        {
            "num": "1",
            "title": "Agent Attestation\n& Key Signing",
            "visual_type": "git_key",
            "badge": "Ed25519",
            "bullets": [
                "• AI Agent generates code change & diff",
                "• Computes SHA-256 digest of Git patch",
                "• Signs commit with Ed25519 private key",
                "• Appends X-Copilot-Agent-ID trailer",
                "• Attaches cryptographic X-Signature"
            ]
        },
        {
            "num": "2",
            "title": "Cryptographic\nProvenance Gate",
            "visual_type": "shield",
            "badge": "Verified",
            "bullets": [
                "• Verifies Ed25519 signature over diff SHA",
                "• Enforces strict authorized email pattern",
                "• Blocks domain & identity spoofing",
                "• Detects PR diff registry tampering",
                "• Enforces immutable root-of-trust"
            ]
        },
        {
            "num": "3",
            "title": "Multi-Vector\nInjection Scanner",
            "visual_type": "ast_firewall",
            "badge": "Firewall",
            "bullets": [
                "• De-obfuscates string concat ('en'+'v')",
                "• Resolves hex/unicode escape sequences",
                "• Normalizes Cyrillic & visual homoglyphs",
                "• Intercepts curl|bash shell execution",
                "• Blocks reverse shells & .env exfiltration"
            ]
        },
        {
            "num": "4",
            "title": "Dynamic SQLite\nReputation & Tests",
            "visual_type": "db_tests",
            "badge": "SQLite3",
            "bullets": [
                "• Queries dynamic SQLite agent history",
                "• Evaluates rolling pass/block audit trail",
                "• Runs tests in sandbox with shell=False",
                "• Eliminates false alarms on quoted docs",
                "• Permits safe test assertion evaluations"
            ]
        },
        {
            "num": "5",
            "title": "Trust Scoring\n& Gatekeeping",
            "visual_type": "gauge",
            "badge": "Gatekeeper",
            "bullets": [
                "• Multi-factor score computed (0-100)",
                "• Autonomous gate: PASS, WARN, BLOCK",
                "• Posts rich PR Markdown audit comment",
                "• Dispatches GitHub Commit Status Check",
                "• Interacts with Copilot Chat extensions"
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
        draw.rounded_rectangle([(x1, y_top), (x2, y_top + 36)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)

        # Number circle badge
        draw.ellipse([(x1 + 6, y_top + 6), (x1 + 28, y_top + 28)], fill=(30, 30, 30))
        draw.text((x1 + 13, y_top + 10), c["num"], fill=(255, 255, 255), font=f_card_num)

        # Title
        t_lines = c["title"].split("\n")
        draw.text((x1 + 34, y_top + 5), t_lines[0], fill=(15, 15, 15), font=f_card_title)
        draw.text((x1 + 34, y_top + 18), t_lines[1], fill=(15, 15, 15), font=f_card_title)

        # VISUAL STRIP (Card Illustrated Graphics)
        vis_y = y_top + 42
        draw.rounded_rectangle([(x1 + 6, vis_y), (x2 - 6, vis_y + 30)], radius=4, fill=(248, 250, 252), outline=(210, 215, 225), width=1)

        if c["visual_type"] == "git_key":
            draw_git_branch(x1 + 12, vis_y + 2)
            draw_key_icon(x1 + 42, vis_y + 6)
            # Hash badge
            draw.rounded_rectangle([(x1 + 75, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(235, 242, 250), outline=(100, 150, 210), width=1)
            draw.text((x1 + 80, vis_y + 9), "#SHA256+Ed25519", fill=(20, 60, 140), font=f_mini)

        elif c["visual_type"] == "shield":
            draw_shield_icon(x1 + 14, vis_y + 4, 18, 22, fill_col=(235, 250, 240), stroke_col=(30, 140, 60), check=True)
            # Identity card badge
            draw.rounded_rectangle([(x1 + 40, vis_y + 6), (x1 + 88, vis_y + 24)], radius=3, fill=(255, 255, 255), outline=(140, 140, 140), width=1)
            draw.text((x1 + 45, vis_y + 9), "ID Attested", fill=(40, 40, 40), font=f_mini)
            # Verified check badge
            draw.rounded_rectangle([(x1 + 94, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(235, 248, 240), outline=(30, 140, 60), width=1)
            draw.text((x1 + 100, vis_y + 9), "100/100 Trust", fill=(20, 120, 50), font=f_mini)

        elif c["visual_type"] == "ast_firewall":
            draw_ast_icon(x1 + 12, vis_y + 4)
            # Terminal scan window
            draw_terminal_icon(x1 + 44, vis_y + 6, w=32, h=18)
            # Block badge
            draw.rounded_rectangle([(x1 + 84, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(255, 240, 240), outline=(200, 50, 50), width=1)
            draw.text((x1 + 89, vis_y + 9), "BLOCKED (0 FP)", fill=(180, 30, 30), font=f_mini)

        elif c["visual_type"] == "db_tests":
            # 3D Cylinder Database Visual
            draw_cylinder_db(x1 + 12, vis_y + 3, 24, 24, fill_top=(230, 245, 255), fill_body=(210, 235, 250), outline=(30, 80, 140), num_layers=3)
            # Test tubes
            draw_test_tubes(x1 + 46, vis_y + 2)
            # Rep score badge
            draw.rounded_rectangle([(x1 + 78, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(240, 250, 245), outline=(40, 140, 80), width=1)
            draw.text((x1 + 83, vis_y + 9), "SQLite Telemetry", fill=(20, 100, 50), font=f_mini)

        elif c["visual_type"] == "gauge":
            draw_gauge_icon(x1 + 12, vis_y + 4)
            # Decision Badge
            draw.rounded_rectangle([(x1 + 46, vis_y + 6), (x1 + 102, vis_y + 24)], radius=3, fill=(235, 248, 240), outline=(30, 140, 60), width=1)
            draw.text((x1 + 51, vis_y + 9), "AUTO-MERGE", fill=(20, 110, 40), font=f_mini)
            # Status badge
            draw.rounded_rectangle([(x1 + 108, vis_y + 6), (x2 - 10, vis_y + 24)], radius=3, fill=(255, 245, 235), outline=(220, 120, 30), width=1)
            draw.text((x1 + 114, vis_y + 9), "PR Check", fill=(160, 70, 10), font=f_mini)

        # Bullets
        by = vis_y + 36
        for b in c["bullets"]:
            draw.text((x1 + 8, by), b, fill=(35, 35, 35), font=f_card_body)
            by += 15

        # Directional Arrow to next card
        if idx < 4:
            ax = x2 + 2
            ay = (y_top + y_bot) // 2
            draw.line([(ax, ay), (ax + 7, ay)], fill=(60, 60, 60), width=2)
            draw.polygon([(ax + 6, ay - 4), (ax + 10, ay), (ax + 6, ay + 4)], fill=(60, 60, 60))

    # 5. Middle Left: Pipeline Components & Integration
    ml_x1, ml_y1, ml_x2, ml_y2 = 56, 358, 628, 516
    draw.rounded_rectangle([(ml_x1, ml_y1), (ml_x2, ml_y2)], radius=7, fill=(255, 255, 255), outline=(130, 130, 130), width=1)
    draw.rounded_rectangle([(ml_x1, ml_y1), (ml_x2, ml_y1 + 22)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)
    draw.text((ml_x1 + 10, ml_y1 + 4), "Pipeline Components & Integration (GitHub-Native & Copilot Extension)", fill=(20, 20, 20), font=f_sec_hdr)

    # Input Box: Untrusted Agent PR
    draw.rounded_rectangle([(ml_x1 + 8, ml_y1 + 30), (ml_x1 + 98, ml_y1 + 148)], radius=6, fill=(248, 250, 252), outline=(100, 100, 100), width=1)
    draw_git_branch(ml_x1 + 14, ml_y1 + 36)
    draw.text((ml_x1 + 38, ml_y1 + 36), "Untrusted", fill=(10, 10, 10), font=f_card_body_bold)
    draw.text((ml_x1 + 38, ml_y1 + 48), "Agent PR", fill=(10, 10, 10), font=f_card_body_bold)
    draw.line([(ml_x1 + 12, ml_y1 + 64), (ml_x1 + 94, ml_y1 + 64)], fill=(210, 215, 220), width=1)
    draw.text((ml_x1 + 12, ml_y1 + 70), "• Git Patch Diff", fill=(50, 50, 50), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 86), "• X-Signature", fill=(50, 50, 50), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 102), "• Agent-ID", fill=(50, 50, 50), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 118), "• Author Email", fill=(50, 50, 50), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 132), "• Commit SHA", fill=(50, 50, 50), font=f_card_body)

    # Arrow to Engine
    draw.line([(ml_x1 + 101, ml_y1 + 89), (ml_x1 + 113, ml_y1 + 89)], fill=(60, 60, 60), width=2)
    draw.polygon([(ml_x1 + 112, ml_y1 + 85), (ml_x1 + 117, ml_y1 + 89), (ml_x1 + 112, ml_y1 + 93)], fill=(60, 60, 60))

    # Engine Container
    eng_x1 = ml_x1 + 119
    eng_x2 = ml_x1 + 366
    draw.rounded_rectangle([(eng_x1, ml_y1 + 28), (eng_x2, ml_y1 + 150)], radius=6, fill=(246, 248, 252), outline=(70, 70, 70), width=1)
    draw.rectangle([(eng_x1, ml_y1 + 28), (eng_x2, ml_y1 + 46)], fill=(225, 232, 244))
    draw.text((eng_x1 + 22, ml_y1 + 32), "CopilotShield Engine (GitHub Actions / Server)", fill=(15, 30, 60), font=f_card_body_bold)

    # 4 Modules with Icons inside Engine
    m_w = 116
    m_h = 44

    # Mod 1: Ed25519
    draw.rounded_rectangle([(eng_x1 + 6, ml_y1 + 52), (eng_x1 + 6 + m_w, ml_y1 + 52 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw_key_icon(eng_x1 + 10, ml_y1 + 56, color=(180, 130, 20))
    draw.text((eng_x1 + 36, ml_y1 + 56), "Ed25519 Crypto", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 10, ml_y1 + 71), "Signature Verifier", fill=(70, 70, 70), font=f_card_body)
    draw.text((eng_x1 + 10, ml_y1 + 82), "& Registry Tamper Lock", fill=(100, 100, 100), font=f_card_body)

    # Mod 2: AST De-obfuscator
    draw.rounded_rectangle([(eng_x1 + 126, ml_y1 + 52), (eng_x1 + 126 + m_w, ml_y1 + 52 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw_ast_icon(eng_x1 + 130, ml_y1 + 54, color=(40, 100, 180))
    draw.text((eng_x1 + 158, ml_y1 + 56), "AST De-obfuscator", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 130, ml_y1 + 71), "String Concat & Joins", fill=(70, 70, 70), font=f_card_body)
    draw.text((eng_x1 + 130, ml_y1 + 82), "Hex/Unicode Escapes", fill=(100, 100, 100), font=f_card_body)

    # Mod 3: Injection Scanner
    draw.rounded_rectangle([(eng_x1 + 6, ml_y1 + 100), (eng_x1 + 6 + m_w, ml_y1 + 100 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw_shield_icon(eng_x1 + 10, ml_y1 + 104, 14, 18, fill_col=(255, 235, 235), stroke_col=(180, 40, 40), check=False)
    draw.text((eng_x1 + 28, ml_y1 + 104), "Injection Firewall", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 10, ml_y1 + 119), "Authority & Homoglyphs", fill=(70, 70, 70), font=f_card_body)
    draw.text((eng_x1 + 10, ml_y1 + 130), "curl|bash & Rev Shells", fill=(100, 100, 100), font=f_card_body)

    # Mod 4: Test Sandbox
    draw.rounded_rectangle([(eng_x1 + 126, ml_y1 + 100), (eng_x1 + 126 + m_w, ml_y1 + 100 + m_h)], radius=4, fill=(255, 255, 255), outline=(160, 160, 160), width=1)
    draw_terminal_icon(eng_x1 + 130, ml_y1 + 104, w=20, h=15)
    draw.text((eng_x1 + 154, ml_y1 + 104), "Test Suite Sandbox", fill=(20, 20, 20), font=f_card_body_bold)
    draw.text((eng_x1 + 130, ml_y1 + 119), "Isolated Execution", fill=(70, 70, 70), font=f_card_body)
    draw.text((eng_x1 + 130, ml_y1 + 130), "shell=False Enforced", fill=(100, 100, 100), font=f_card_body)

    # Connected Visual SQLite 3D Database Container
    db_x1 = eng_x2 + 8
    db_x2 = ml_x2 - 8

    # Top Database Box with 3D Cylinders
    draw.rounded_rectangle([(db_x1, ml_y1 + 28), (db_x2, ml_y1 + 82)], radius=6, fill=(245, 250, 255), outline=(40, 100, 180), width=1)
    # Draw prominent 3D cylinder database
    draw_cylinder_db(db_x1 + 10, ml_y1 + 34, 44, 42, fill_top=(220, 245, 255), fill_body=(180, 225, 250), outline=(20, 80, 160), num_layers=3)
    draw.text((db_x1 + 60, ml_y1 + 34), "SQLite Dynamic DB", fill=(10, 60, 130), font=f_card_body_bold)
    draw.text((db_x1 + 60, ml_y1 + 47), "copilot_shield.db", fill=(80, 100, 120), font=f_card_body)
    draw.text((db_x1 + 60, ml_y1 + 59), "• Agent Public Keys", fill=(40, 80, 120), font=f_mini)
    draw.text((db_x1 + 60, ml_y1 + 70), "• Audit Telemetry Logs", fill=(40, 80, 120), font=f_mini)

    # Bidirectional arrows between engine and DB
    draw.line([(eng_x2 + 1, ml_y1 + 50), (db_x1 - 1, ml_y1 + 50)], fill=(30, 100, 180), width=2)
    draw.polygon([(eng_x2 + 3, ml_y1 + 47), (eng_x2 - 2, ml_y1 + 50), (eng_x2 + 3, ml_y1 + 53)], fill=(30, 100, 180))
    draw.polygon([(db_x1 - 3, ml_y1 + 47), (db_x1 + 2, ml_y1 + 50), (db_x1 - 3, ml_y1 + 53)], fill=(30, 100, 180))

    # Output Enforcements Container
    draw.rounded_rectangle([(db_x1, ml_y1 + 88), (db_x2, ml_y1 + 150)], radius=6, fill=(250, 252, 255), outline=(50, 120, 70), width=1)
    draw.text((db_x1 + 8, ml_y1 + 92), "Outputs & Enforcements:", fill=(20, 40, 80), font=f_card_body_bold)

    # Output 1: Verified Code
    draw.ellipse([(db_x1 + 10, ml_y1 + 107), (db_x1 + 18, ml_y1 + 115)], fill=(30, 170, 70))
    draw.text((db_x1 + 22, ml_y1 + 106), "Verified Codebase (Auto-Merge)", fill=(10, 120, 40), font=f_card_body_bold)

    # Output 2: Markdown audit
    draw.ellipse([(db_x1 + 10, ml_y1 + 121), (db_x1 + 18, ml_y1 + 129)], fill=(40, 90, 200))
    draw.text((db_x1 + 22, ml_y1 + 120), "Authoritative PR Markdown Audit", fill=(20, 60, 140), font=f_card_body_bold)

    # Output 3: Status check
    draw.ellipse([(db_x1 + 10, ml_y1 + 135), (db_x1 + 18, ml_y1 + 143)], fill=(220, 110, 20))
    draw.text((db_x1 + 22, ml_y1 + 134), "GitHub Commit Status (PASS/BLOCK)", fill=(140, 60, 10), font=f_card_body_bold)

    # 6. Middle Right: Tech Stack Specification WITH VISUAL ICONS
    mr_x1, mr_y1, mr_x2, mr_y2 = 638, 358, 968, 516
    draw.rounded_rectangle([(mr_x1, mr_y1), (mr_x2, mr_y2)], radius=7, fill=(255, 255, 255), outline=(130, 130, 130), width=1)
    draw.rounded_rectangle([(mr_x1, mr_y1), (mr_x2, mr_y1 + 22)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)
    draw.text((mr_x1 + 10, mr_y1 + 4), "Tech Stack & Implementation Specification", fill=(20, 20, 20), font=f_sec_hdr)

    tech_items = [
        ("🔐 Cryptography:", "Ed25519 (RFC 8032), SHA-256, HMAC-SHA256"),
        ("⚡ CI/CD Platform:", "GitHub Actions Composite Action, REST API"),
        ("🤖 Agent Protocol:", "Copilot Agent Extensions Protocol (HTTP/SSE)"),
        ("🌲 Analysis & AST:", "Python ast module, Unicode Homoglyph Engine"),
        ("🗄️ Database Engine:", "SQLite3 (Dynamic Reputation & Audit Trail)"),
        ("🧪 Test Isolation:", "Pytest (39 Unit Tests), Subprocess Sandbox"),
        ("🐍 Core Runtime:", "Python 3.11+ / Strict Cryptographic Policies")
    ]

    ty = mr_y1 + 30
    for k, v in tech_items:
        draw.text((mr_x1 + 10, ty), k, fill=(15, 15, 15), font=f_tech_k)
        draw.text((mr_x1 + 125, ty), v, fill=(45, 45, 45), font=f_tech_v)
        ty += 16
        draw.line([(mr_x1 + 8, ty - 2), (mr_x2 - 8, ty - 2)], fill=(238, 240, 242), width=1)

    # 7. Bottom Section: Key Features WITH ILLUSTRATED BADGES
    kf_x1, kf_y1, kf_x2, kf_y2 = 56, 524, 968, 626
    draw.rounded_rectangle([(kf_x1, kf_y1), (kf_x2, kf_y2)], radius=7, fill=(255, 255, 255), outline=(130, 130, 130), width=1)
    draw.rounded_rectangle([(kf_x1, kf_y1), (kf_x2, kf_y2 + 20)], radius=7, fill=(244, 246, 249), outline=(150, 150, 150), width=1)
    draw.text((kf_x1 + 10, kf_y1 + 3), "Key Features & Architectural Security Guarantees", fill=(20, 20, 20), font=f_sec_hdr)

    features = [
        {
            "title": "Cryptographic Provenance",
            "icon": "key",
            "desc1": "Ed25519 digital signatures prove",
            "desc2": "agent authenticity & prevent spoofing."
        },
        {
            "title": "Anti-Evasion AST Engine",
            "icon": "ast",
            "desc1": "Unrolls string concatenations, joins,",
            "desc2": "and hex/unicode escapes dynamically."
        },
        {
            "title": "Prompt Injection Firewall",
            "icon": "shield",
            "desc1": "Neutralizes authority spoofing, hidden",
            "desc2": "system tags, reverse shells & homoglyphs."
        },
        {
            "title": "Dynamic SQLite Reputation",
            "icon": "db",
            "desc1": "Historical PR audit logs & pass rates",
            "desc2": "actively govern autonomous merge gating."
        },
        {
            "title": "Automated CI/CD Gate",
            "icon": "terminal",
            "desc1": "Posts rich PR markdown audits, sets",
            "desc2": "status checks & serves Copilot Chat."
        }
    ]

    col_w = (kf_x2 - kf_x1) // 5
    for idx, f in enumerate(features):
        fx = kf_x1 + idx * col_w + 6

        # Draw Illustrated Circular Badge for each feature
        badge_cx = fx + 16
        badge_cy = kf_y1 + 38
        draw.ellipse([(badge_cx - 12, badge_cy - 12), (badge_cx + 12, badge_cy + 12)], fill=(240, 245, 252), outline=(100, 140, 200), width=1)

        if f["icon"] == "key":
            draw_key_icon(badge_cx - 10, badge_cy - 8, color=(190, 130, 20))
        elif f["icon"] == "ast":
            draw_ast_icon(badge_cx - 10, badge_cy - 10, color=(30, 100, 180))
        elif f["icon"] == "shield":
            draw_shield_icon(badge_cx - 7, badge_cy - 9, 14, 18, fill_col=(235, 250, 240), stroke_col=(30, 140, 60), check=True)
        elif f["icon"] == "db":
            draw_cylinder_db(badge_cx - 8, badge_cy - 9, 16, 18, fill_top=(225, 245, 255), fill_body=(190, 225, 250), outline=(20, 80, 160), num_layers=2)
        elif f["icon"] == "terminal":
            draw_terminal_icon(badge_cx - 9, badge_cy - 7, w=18, h=14)

        # Title and description next to/under icon
        draw.text((fx + 34, kf_y1 + 26), f["title"], fill=(15, 15, 15), font=f_feat_title)
        draw.text((fx + 34, kf_y1 + 42), f["desc1"], fill=(70, 70, 70), font=f_feat_desc)
        draw.text((fx + 34, kf_y1 + 54), f["desc2"], fill=(70, 70, 70), font=f_feat_desc)

        if idx < 4:
            draw.line([(fx + col_w - 4, kf_y1 + 26), (fx + col_w - 4, kf_y2 - 6)], fill=(225, 225, 225), width=1)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "copilot_shield_architecture_template.png")
    im.save(out_path)
    print(f"Successfully generated rich visual architecture diagram: {out_path}")

if __name__ == "__main__":
    create_rich_visual_architecture()
