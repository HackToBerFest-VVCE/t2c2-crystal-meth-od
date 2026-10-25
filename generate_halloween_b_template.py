"""
Halloween Illustrated Architecture Generator for Team Crystal Meth-od (Option B).
Renders directly on the official Hacktoberfest Halloween template:
- Keeps the deep black gothic dead tree, black tombstones/crosses, black haunted house, and black carved pumpkins
- Festive Halloween title plaque & colorful glowing card borders
- Full architectural iconography suite and 3D SQLite database
"""

from PIL import Image, ImageDraw, ImageFont
import os

def generate_halloween_template_b():
    template_path = r"C:/Users/hp/.gemini/antigravity/brain/5d832c7a-5310-48c8-be7e-694eab1a0476/.user_uploaded/media_1792914214399_c066a8ea.jpg"
    im = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(im)

    # 1. Clean old template text areas while strictly preserving all black gothic border artwork
    # (dead trees, tombstones, haunted house, jack-o-lanterns, moon, bats)
    bg_canvas = (245, 245, 245)
    # Clean plaque text in banner
    draw.rectangle([(295, 60), (730, 106)], fill=bg_canvas)
    # Clean subtitle text
    draw.rectangle([(60, 107), (965, 133)], fill=bg_canvas)
    # Clean inner white canvas
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

    # 2. Render Halloween Plaque: TEAM CRYSTAL METH-OD with festive pumpkin orange and black outline
    draw.line([(310, 62), (715, 62)], fill=(20, 20, 20), width=2)
    draw.line([(310, 104), (715, 104)], fill=(20, 20, 20), width=2)
    draw.polygon([(300, 83), (312, 62), (312, 104)], fill=(20, 20, 20))
    draw.polygon([(725, 83), (713, 62), (713, 104)], fill=(20, 20, 20))

    team_text = "TEAM CRYSTAL METH-OD"
    bbox_t = draw.textbbox((0, 0), team_text, font=f_team)
    wt = bbox_t[2] - bbox_t[0]
    # Subtle shadow then bold text
    draw.text((512 - wt / 2 + 1, 71), team_text, fill=(20, 15, 10), font=f_team)
    draw.text((512 - wt / 2, 70), team_text, fill=(225, 85, 12), font=f_team)

    # 3. Render Subtitle
    sub_text = "SYSTEM ARCHITECTURE: CopilotShield - Cryptographic Agent Provenance & Prompt-Injection Firewall"
    bbox_s = draw.textbbox((0, 0), sub_text, font=f_sub)
    ws = bbox_s[2] - bbox_s[0]
    draw.text((512 - ws / 2, 112), sub_text, fill=(15, 15, 15), font=f_sub)

    # Visual Helper Functions
    def draw_cylinder_db(x, y, w, h, fill_top=(230, 245, 255), fill_body=(210, 235, 250), outline=(2, 132, 199), num_layers=3):
        layer_h = h / num_layers
        ell_h = layer_h * 0.45
        for i in range(num_layers - 1, -1, -1):
            ly = y + i * (layer_h * 0.85)
            draw.rectangle([(x, ly + ell_h / 2), (x + w, ly + layer_h)], fill=fill_body)
            draw.ellipse([(x, ly + layer_h - ell_h / 2), (x + w, ly + layer_h + ell_h / 2)], fill=fill_body, outline=outline, width=1)
            draw.line([(x, ly + ell_h / 2), (x, ly + layer_h)], fill=outline, width=1)
            draw.line([(x + w, ly + ell_h / 2), (x + w, ly + layer_h)], fill=outline, width=1)
            draw.ellipse([(x, ly), (x + w, ly + ell_h)], fill=fill_top, outline=outline, width=1)
            # LED status light
            draw.ellipse([(x + w - 8, ly + layer_h * 0.55), (x + w - 4, ly + layer_h * 0.55 + 4)], fill=(34, 197, 94))

    def draw_git_branch(x, y, color=(40, 40, 40)):
        draw.line([(x + 5, y + 2), (x + 5, y + 26)], fill=color, width=2)
        draw.ellipse([(x + 2, y + 2), (x + 8, y + 8)], fill=(255, 255, 255), outline=color, width=2)
        draw.ellipse([(x + 2, y + 20), (x + 8, y + 26)], fill=(255, 255, 255), outline=color, width=2)
        draw.line([(x + 5, y + 14), (x + 16, y + 6)], fill=color, width=2)
        draw.ellipse([(x + 13, y + 3), (x + 19, y + 9)], fill=(234, 88, 12), outline=color, width=1)

    def draw_key_icon(x, y, color=(217, 119, 6)):
        draw.ellipse([(x, y + 4), (x + 10, y + 14)], fill=(255, 255, 255), outline=color, width=2)
        draw.ellipse([(x + 3, y + 7), (x + 7, y + 11)], fill=color)
        draw.line([(x + 10, y + 9), (x + 22, y + 9)], fill=color, width=2)
        draw.line([(x + 18, y + 9), (x + 18, y + 14)], fill=color, width=2)
        draw.line([(x + 21, y + 9), (x + 21, y + 13)], fill=color, width=2)

    def draw_shield_icon(x, y, w, h, fill_col=(235, 250, 240), stroke_col=(22, 163, 74), check=True):
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
            draw.line([(x + w * 0.28, y + h * 0.52), (x + w * 0.45, y + h * 0.70)], fill=stroke_col, width=2)
            draw.line([(x + w * 0.45, y + h * 0.70), (x + w * 0.75, y + h * 0.35)], fill=stroke_col, width=2)

    def draw_ast_icon(x, y, color=(37, 99, 235)):
        draw.ellipse([(x + 8, y), (x + 16, y + 8)], fill=(37, 99, 235))
        draw.ellipse([(x, y + 14), (x + 8, y + 22)], fill=(22, 163, 74))
        draw.ellipse([(x + 16, y + 14), (x + 24, y + 22)], fill=(234, 88, 12))
        draw.line([(x + 12, y + 8), (x + 4, y + 14)], fill=color, width=1)
        draw.line([(x + 12, y + 8), (x + 20, y + 14)], fill=color, width=1)

    def draw_test_tubes(x, y, color=(168, 85, 247)):
        draw.rectangle([(x + 2, y + 4), (x + 10, y + 22)], outline=color, width=1, fill=(250, 245, 255))
        draw.ellipse([(x + 2, y + 18), (x + 10, y + 26)], fill=(192, 132, 252), outline=color, width=1)
        draw.line([(x + 2, y + 12), (x + 10, y + 12)], fill=color, width=1)
        draw.rectangle([(x + 14, y + 2), (x + 22, y + 20)], outline=(2, 132, 199), width=1, fill=(240, 249, 255))
        draw.ellipse([(x + 14, y + 16), (x + 22, y + 24)], fill=(56, 189, 248), outline=(2, 132, 199), width=1)

    def draw_gauge_icon(x, y, color=(22, 163, 74)):
        draw.arc([(x, y), (x + 24, y + 24)], start=160, end=380, fill=color, width=3)
        draw.ellipse([(x + 10, y + 10), (x + 14, y + 14)], fill=(20, 20, 20))
        draw.line([(x + 12, y + 12), (x + 20, y + 6)], fill=(220, 38, 38), width=2)

    def draw_terminal_icon(x, y, w=24, h=18):
        draw.rounded_rectangle([(x, y), (x + w, y + h)], radius=2, fill=(15, 23, 42), outline=(71, 85, 105), width=1)
        draw.rectangle([(x, y), (x + w, y + 5)], fill=(30, 41, 59))
        draw.ellipse([(x + 2, y + 1.5), (x + 4, y + 3.5)], fill=(239, 68, 68))
        draw.ellipse([(x + 5.5, y + 1.5), (x + 7.5, y + 3.5)], fill=(245, 158, 11))
        draw.ellipse([(x + 9, y + 1.5), (x + 11, y + 3.5)], fill=(34, 197, 94))
        draw.line([(x + 3, y + 8), (x + 7, y + 11)], fill=(74, 222, 128), width=1)
        draw.line([(x + 7, y + 11), (x + 3, y + 14)], fill=(74, 222, 128), width=1)
        draw.line([(x + 9, y + 13), (x + 14, y + 13)], fill=(255, 255, 255), width=1)

    # 4. Render 5 Top Workflow Step Cards WITH HALLOWEEN THEMED BORDERS
    cards_data = [
        {
            "num": "1",
            "title": "Agent Attestation\n& Key Signing",
            "visual_type": "git_key",
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
            "bullets": [
                "• Multi-factor score computed (0-100)",
                "• Autonomous gate: PASS, WARN, BLOCK",
                "• Posts rich PR Markdown audit comment",
                "• Dispatches GitHub Commit Status Check",
                "• Interacts with Copilot Chat extensions"
            ]
        }
    ]

    card_theme_colors = [
        ((234, 88, 12), (255, 247, 237)),   # 1. Halloween Orange
        ((217, 119, 6), (254, 252, 232)),   # 2. Pumpkin Amber
        ((22, 163, 74), (240, 253, 244)),   # 3. Emerald Green
        ((2, 132, 199), (240, 249, 255)),   # 4. Cyber Cyan
        ((194, 65, 12), (255, 241, 242)),   # 5. Dark Orange
    ]

    x_starts = [56, 241, 426, 611, 796]
    card_w = 172
    y_top = 140
    y_bot = 350

    for idx, c in enumerate(cards_data):
        x1 = x_starts[idx]
        x2 = x1 + card_w
        outline_c, header_bg = card_theme_colors[idx]

        # Card body with themed colored border
        draw.rounded_rectangle([(x1, y_top), (x2, y_bot)], radius=7, fill=(255, 255, 255), outline=outline_c, width=2)
        # Header banner with themed subtle tint
        draw.rounded_rectangle([(x1, y_top), (x2, y_top + 36)], radius=7, fill=header_bg, outline=outline_c, width=1)

        # Number circle badge with themed color
        draw.ellipse([(x1 + 6, y_top + 6), (x1 + 28, y_top + 28)], fill=outline_c)
        draw.text((x1 + 13, y_top + 10), c["num"], fill=(255, 255, 255), font=f_card_num)

        # Title
        t_lines = c["title"].split("\n")
        draw.text((x1 + 34, y_top + 5), t_lines[0], fill=(15, 23, 42), font=f_card_title)
        draw.text((x1 + 34, y_top + 18), t_lines[1], fill=(15, 23, 42), font=f_card_title)

        # VISUAL STRIP (Card Illustrated Graphics)
        vis_y = y_top + 42
        draw.rounded_rectangle([(x1 + 6, vis_y), (x2 - 6, vis_y + 30)], radius=4, fill=(248, 250, 252), outline=(226, 232, 240), width=1)

        if c["visual_type"] == "git_key":
            draw_git_branch(x1 + 12, vis_y + 2)
            draw_key_icon(x1 + 42, vis_y + 6)
            draw.rounded_rectangle([(x1 + 75, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(255, 247, 237), outline=(234, 88, 12), width=1)
            draw.text((x1 + 80, vis_y + 9), "#SHA256+Ed25519", fill=(194, 65, 12), font=f_mini)

        elif c["visual_type"] == "shield":
            draw_shield_icon(x1 + 14, vis_y + 4, 18, 22, fill_col=(235, 250, 240), stroke_col=(22, 163, 74), check=True)
            draw.rounded_rectangle([(x1 + 40, vis_y + 6), (x1 + 88, vis_y + 24)], radius=3, fill=(255, 255, 255), outline=(148, 163, 184), width=1)
            draw.text((x1 + 45, vis_y + 9), "ID Attested", fill=(51, 65, 85), font=f_mini)
            draw.rounded_rectangle([(x1 + 94, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(240, 253, 244), outline=(22, 163, 74), width=1)
            draw.text((x1 + 100, vis_y + 9), "100/100 Trust", fill=(21, 128, 61), font=f_mini)

        elif c["visual_type"] == "ast_firewall":
            draw_ast_icon(x1 + 12, vis_y + 4)
            draw_terminal_icon(x1 + 44, vis_y + 6, w=32, h=18)
            draw.rounded_rectangle([(x1 + 84, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(254, 242, 242), outline=(239, 68, 68), width=1)
            draw.text((x1 + 89, vis_y + 9), "BLOCKED (0 FP)", fill=(185, 28, 28), font=f_mini)

        elif c["visual_type"] == "db_tests":
            draw_cylinder_db(x1 + 12, vis_y + 3, 24, 24, fill_top=(240, 249, 255), fill_body=(224, 242, 254), outline=(2, 132, 199), num_layers=3)
            draw_test_tubes(x1 + 46, vis_y + 2)
            draw.rounded_rectangle([(x1 + 78, vis_y + 6), (x2 - 12, vis_y + 24)], radius=3, fill=(240, 253, 244), outline=(34, 197, 94), width=1)
            draw.text((x1 + 83, vis_y + 9), "SQLite Telemetry", fill=(21, 128, 61), font=f_mini)

        elif c["visual_type"] == "gauge":
            draw_gauge_icon(x1 + 12, vis_y + 4)
            draw.rounded_rectangle([(x1 + 46, vis_y + 6), (x1 + 102, vis_y + 24)], radius=3, fill=(240, 253, 244), outline=(22, 163, 74), width=1)
            draw.text((x1 + 51, vis_y + 9), "AUTO-MERGE", fill=(21, 128, 61), font=f_mini)
            draw.rounded_rectangle([(x1 + 108, vis_y + 6), (x2 - 10, vis_y + 24)], radius=3, fill=(255, 247, 237), outline=(234, 88, 12), width=1)
            draw.text((x1 + 114, vis_y + 9), "PR Check", fill=(194, 65, 12), font=f_mini)

        # Bullets
        by = vis_y + 36
        for b in c["bullets"]:
            draw.text((x1 + 8, by), b, fill=(30, 41, 59), font=f_card_body)
            by += 15

        # Directional Arrow to next card
        if idx < 4:
            ax = x2 + 2
            ay = (y_top + y_bot) // 2
            draw.line([(ax, ay), (ax + 7, ay)], fill=(100, 116, 139), width=2)
            draw.polygon([(ax + 6, ay - 4), (ax + 10, ay), (ax + 6, ay + 4)], fill=(100, 116, 139))

    # 5. Middle Left: Pipeline Components & Integration
    ml_x1, ml_y1, ml_x2, ml_y2 = 56, 358, 628, 516
    draw.rounded_rectangle([(ml_x1, ml_y1), (ml_x2, ml_y2)], radius=7, fill=(255, 255, 255), outline=(148, 163, 184), width=1)
    draw.rounded_rectangle([(ml_x1, ml_y1), (ml_x2, ml_y1 + 22)], radius=7, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((ml_x1 + 10, ml_y1 + 4), "Pipeline Components & Integration (GitHub-Native & Copilot Extension)", fill=(15, 23, 42), font=f_sec_hdr)

    # Input Box: Untrusted Agent PR
    draw.rounded_rectangle([(ml_x1 + 8, ml_y1 + 30), (ml_x1 + 98, ml_y1 + 148)], radius=6, fill=(255, 247, 237), outline=(234, 88, 12), width=1)
    draw_git_branch(ml_x1 + 14, ml_y1 + 36)
    draw.text((ml_x1 + 38, ml_y1 + 36), "Untrusted", fill=(15, 23, 42), font=f_card_body_bold)
    draw.text((ml_x1 + 38, ml_y1 + 48), "Agent PR", fill=(15, 23, 42), font=f_card_body_bold)
    draw.line([(ml_x1 + 12, ml_y1 + 64), (ml_x1 + 94, ml_y1 + 64)], fill=(254, 215, 170), width=1)
    draw.text((ml_x1 + 12, ml_y1 + 70), "• Git Patch Diff", fill=(51, 65, 85), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 86), "• X-Signature", fill=(51, 65, 85), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 102), "• Agent-ID", fill=(51, 65, 85), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 118), "• Author Email", fill=(51, 65, 85), font=f_card_body)
    draw.text((ml_x1 + 12, ml_y1 + 132), "• Commit SHA", fill=(51, 65, 85), font=f_card_body)

    # Arrow to Engine
    draw.line([(ml_x1 + 101, ml_y1 + 89), (ml_x1 + 113, ml_y1 + 89)], fill=(100, 116, 139), width=2)
    draw.polygon([(ml_x1 + 112, ml_y1 + 85), (ml_x1 + 117, ml_y1 + 89), (ml_x1 + 112, ml_y1 + 93)], fill=(100, 116, 139))

    # Engine Container
    eng_x1 = ml_x1 + 119
    eng_x2 = ml_x1 + 366
    draw.rounded_rectangle([(eng_x1, ml_y1 + 28), (eng_x2, ml_y1 + 150)], radius=6, fill=(248, 250, 252), outline=(100, 116, 139), width=1)
    draw.rectangle([(eng_x1, ml_y1 + 28), (eng_x2, ml_y1 + 46)], fill=(224, 231, 255))
    draw.text((eng_x1 + 22, ml_y1 + 32), "CopilotShield Engine (GitHub Actions / Server)", fill=(30, 58, 138), font=f_card_body_bold)

    # 4 Modules with Icons inside Engine
    m_w = 116
    m_h = 44

    # Mod 1: Ed25519
    draw.rounded_rectangle([(eng_x1 + 6, ml_y1 + 52), (eng_x1 + 6 + m_w, ml_y1 + 52 + m_h)], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_key_icon(eng_x1 + 10, ml_y1 + 56, color=(217, 119, 6))
    draw.text((eng_x1 + 36, ml_y1 + 56), "Ed25519 Crypto", fill=(15, 23, 42), font=f_card_body_bold)
    draw.text((eng_x1 + 10, ml_y1 + 71), "Signature Verifier", fill=(71, 85, 105), font=f_card_body)
    draw.text((eng_x1 + 10, ml_y1 + 82), "& Registry Tamper Lock", fill=(100, 116, 139), font=f_card_body)

    # Mod 2: AST De-obfuscator
    draw.rounded_rectangle([(eng_x1 + 126, ml_y1 + 52), (eng_x1 + 126 + m_w, ml_y1 + 52 + m_h)], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_ast_icon(eng_x1 + 130, ml_y1 + 54, color=(37, 99, 235))
    draw.text((eng_x1 + 158, ml_y1 + 56), "AST De-obfuscator", fill=(15, 23, 42), font=f_card_body_bold)
    draw.text((eng_x1 + 130, ml_y1 + 71), "String Concat & Joins", fill=(71, 85, 105), font=f_card_body)
    draw.text((eng_x1 + 130, ml_y1 + 82), "Hex/Unicode Escapes", fill=(100, 116, 139), font=f_card_body)

    # Mod 3: Injection Scanner
    draw.rounded_rectangle([(eng_x1 + 6, ml_y1 + 100), (eng_x1 + 6 + m_w, ml_y1 + 100 + m_h)], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_shield_icon(eng_x1 + 10, ml_y1 + 104, 14, 18, fill_col=(254, 242, 242), stroke_col=(220, 38, 38), check=False)
    draw.text((eng_x1 + 28, ml_y1 + 104), "Injection Firewall", fill=(15, 23, 42), font=f_card_body_bold)
    draw.text((eng_x1 + 10, ml_y1 + 119), "Authority & Homoglyphs", fill=(71, 85, 105), font=f_card_body)
    draw.text((eng_x1 + 10, ml_y1 + 130), "curl|bash & Rev Shells", fill=(100, 116, 139), font=f_card_body)

    # Mod 4: Test Sandbox
    draw.rounded_rectangle([(eng_x1 + 126, ml_y1 + 100), (eng_x1 + 126 + m_w, ml_y1 + 100 + m_h)], radius=4, fill=(255, 255, 255), outline=(203, 213, 225), width=1)
    draw_terminal_icon(eng_x1 + 130, ml_y1 + 104, w=20, h=15)
    draw.text((eng_x1 + 154, ml_y1 + 104), "Test Suite Sandbox", fill=(15, 23, 42), font=f_card_body_bold)
    draw.text((eng_x1 + 130, ml_y1 + 119), "Isolated Execution", fill=(71, 85, 105), font=f_card_body)
    draw.text((eng_x1 + 130, ml_y1 + 130), "shell=False Enforced", fill=(100, 116, 139), font=f_card_body)

    # Connected Visual SQLite 3D Database Container
    db_x1 = eng_x2 + 8
    db_x2 = ml_x2 - 8

    draw.rounded_rectangle([(db_x1, ml_y1 + 28), (db_x2, ml_y1 + 82)], radius=6, fill=(240, 249, 255), outline=(2, 132, 199), width=1)
    draw_cylinder_db(db_x1 + 10, ml_y1 + 34, 44, 42, fill_top=(224, 242, 254), fill_body=(186, 230, 253), outline=(2, 132, 199), num_layers=3)
    draw.text((db_x1 + 60, ml_y1 + 34), "SQLite Dynamic DB", fill=(3, 105, 161), font=f_card_body_bold)
    draw.text((db_x1 + 60, ml_y1 + 47), "copilot_shield.db", fill=(100, 116, 139), font=f_card_body)
    draw.text((db_x1 + 60, ml_y1 + 59), "• Agent Public Keys", fill=(30, 64, 175), font=f_mini)
    draw.text((db_x1 + 60, ml_y1 + 70), "• Audit Telemetry Logs", fill=(30, 64, 175), font=f_mini)

    # Bidirectional bus lines between engine and DB
    draw.line([(eng_x2 + 1, ml_y1 + 50), (db_x1 - 1, ml_y1 + 50)], fill=(2, 132, 199), width=2)
    draw.polygon([(eng_x2 + 3, ml_y1 + 47), (eng_x2 - 2, ml_y1 + 50), (eng_x2 + 3, ml_y1 + 53)], fill=(2, 132, 199))
    draw.polygon([(db_x1 - 3, ml_y1 + 47), (db_x1 + 2, ml_y1 + 50), (db_x1 - 3, ml_y1 + 53)], fill=(2, 132, 199))

    # Output Enforcements Container
    draw.rounded_rectangle([(db_x1, ml_y1 + 88), (db_x2, ml_y1 + 150)], radius=6, fill=(255, 255, 255), outline=(34, 197, 94), width=1)
    draw.text((db_x1 + 8, ml_y1 + 92), "Outputs & Enforcements:", fill=(15, 23, 42), font=f_card_body_bold)

    draw.ellipse([(db_x1 + 10, ml_y1 + 107), (db_x1 + 18, ml_y1 + 115)], fill=(34, 197, 94))
    draw.text((db_x1 + 22, ml_y1 + 106), "Verified Codebase (Auto-Merge)", fill=(21, 128, 61), font=f_card_body_bold)

    draw.ellipse([(db_x1 + 10, ml_y1 + 121), (db_x1 + 18, ml_y1 + 129)], fill=(37, 99, 235))
    draw.text((db_x1 + 22, ml_y1 + 120), "Authoritative PR Markdown Audit", fill=(29, 78, 216), font=f_card_body_bold)

    draw.ellipse([(db_x1 + 10, ml_y1 + 135), (db_x1 + 18, ml_y1 + 143)], fill=(234, 88, 12))
    draw.text((db_x1 + 22, ml_y1 + 134), "GitHub Commit Status (PASS/BLOCK)", fill=(194, 65, 12), font=f_card_body_bold)

    # 6. Middle Right: Tech Stack Specification
    mr_x1, mr_y1, mr_x2, mr_y2 = 638, 358, 968, 516
    draw.rounded_rectangle([(mr_x1, mr_y1), (mr_x2, mr_y2)], radius=7, fill=(255, 255, 255), outline=(148, 163, 184), width=1)
    draw.rounded_rectangle([(mr_x1, mr_y1), (mr_x2, mr_y1 + 22)], radius=7, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((mr_x1 + 10, mr_y1 + 4), "Tech Stack & Implementation Specification", fill=(15, 23, 42), font=f_sec_hdr)

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
        draw.text((mr_x1 + 10, ty), k, fill=(15, 23, 42), font=f_tech_k)
        draw.text((mr_x1 + 125, ty), v, fill=(51, 65, 85), font=f_tech_v)
        ty += 16
        draw.line([(mr_x1 + 8, ty - 2), (mr_x2 - 8, ty - 2)], fill=(241, 245, 249), width=1)

    # 7. Bottom Section: Key Features WITH ILLUSTRATED BADGES
    kf_x1, kf_y1, kf_x2, kf_y2 = 56, 524, 968, 626
    draw.rounded_rectangle([(kf_x1, kf_y1), (kf_x2, kf_y2)], radius=7, fill=(255, 255, 255), outline=(148, 163, 184), width=1)
    draw.rounded_rectangle([(kf_x1, kf_y1), (kf_x2, kf_y2 + 20)], radius=7, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((kf_x1 + 10, kf_y1 + 3), "Key Features & Architectural Security Guarantees", fill=(15, 23, 42), font=f_sec_hdr)

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

        badge_cx = fx + 16
        badge_cy = kf_y1 + 38
        draw.ellipse([(badge_cx - 12, badge_cy - 12), (badge_cx + 12, badge_cy + 12)], fill=(240, 249, 255), outline=(186, 230, 253), width=1)

        if f["icon"] == "key":
            draw_key_icon(badge_cx - 10, badge_cy - 8, color=(217, 119, 6))
        elif f["icon"] == "ast":
            draw_ast_icon(badge_cx - 10, badge_cy - 10, color=(37, 99, 235))
        elif f["icon"] == "shield":
            draw_shield_icon(badge_cx - 7, badge_cy - 9, 14, 18, fill_col=(240, 253, 244), stroke_col=(22, 163, 74), check=True)
        elif f["icon"] == "db":
            draw_cylinder_db(badge_cx - 8, badge_cy - 9, 16, 18, fill_top=(240, 249, 255), fill_body=(224, 242, 254), outline=(2, 132, 199), num_layers=2)
        elif f["icon"] == "terminal":
            draw_terminal_icon(badge_cx - 9, badge_cy - 7, w=18, h=14)

        draw.text((fx + 34, kf_y1 + 26), f["title"], fill=(15, 23, 42), font=f_feat_title)
        draw.text((fx + 34, kf_y1 + 42), f["desc1"], fill=(71, 85, 105), font=f_feat_desc)
        draw.text((fx + 34, kf_y1 + 54), f["desc2"], fill=(71, 85, 105), font=f_feat_desc)

        if idx < 4:
            draw.line([(fx + col_w - 4, kf_y1 + 26), (fx + col_w - 4, kf_y2 - 6)], fill=(226, 232, 240), width=1)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "copilot_shield_architecture_halloween.png")
    im.save(out_path)
    print(f"Successfully generated Halloween template edition: {out_path}")

if __name__ == "__main__":
    generate_halloween_template_b()
