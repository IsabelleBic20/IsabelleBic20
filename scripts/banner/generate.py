#!/usr/bin/env python3
"""
generate.py - Generate animated terminal profile banners for dark and light modes.
Pure Python / stdlib only. No external dependencies required.
"""

from __future__ import annotations

import html
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets"

W, H = 1180, 590

ROWS = [
    ("Subject", "Isabelle Bicudo"),
    ("Role", "Software Engineer · AI/ML Researcher"),
    ("Origin", "Campo Grande, MS · Brazil"),
    ("Education", "M.Sc. Computer Science @ UFMS"),
    ("Status", "Building + Researching + Shipping"),
    ("ToolChain", "VS Code · Rider · Docker · Git"),
    ("Core.Lang", "C# · Python · TypeScript · SQL"),
    ("Core.Frontend", "Angular · Next.js · React · Tailwind"),
    ("Core.Backend", "ASP.NET Core · Clean Architecture · EF Core"),
    ("Core.Data", "Ralph Kimball DW · MySQL · SQL Server · DuckDB"),
    ("Core.AI/ML", "PyTorch · TensorFlow · U-Net · OpenCV · Scikit-Learn"),
    ("Core.QA/CI", "Pytest · Jest · Cypress · GitHub Actions"),
    ("Grid.LinkedIn", "/in/isabellebicudo"),
    ("Grid.GitHub", "IsabelleBic20"),
    ("Grid.Mail", "isabellebicudo70@gmail.com"),
]

THEMES = {
    "dark": {
        "bg": "#0a0f1d",
        "panel_bg": "#0f172a",
        "panel_border": "#1e293b",
        "header_bg": "#131f37",
        "header_text": "#94a3b8",
        "title": "#00d9ff",
        "chrome": "#00d9ff",
        "accent": "#10b981",
        "purple": "#aa9bef",
        "text": "#f1f5f9",
        "muted": "#94a3b8",
        "line": "#1e293b",
        "dots": "#334155",
        "grid_line": "#1e293b",
        "node": "#00d9ff",
        "node_glow": "#38bdf8",
        "synapse": "#00d9ff",
        "radar": "#00d9ff",
    },
    "light": {
        "bg": "#f8fafc",
        "panel_bg": "#ffffff",
        "panel_border": "#e2e8f0",
        "header_bg": "#f1f5f9",
        "header_text": "#64748b",
        "title": "#0284c7",
        "chrome": "#0284c7",
        "accent": "#059669",
        "purple": "#7c3aed",
        "text": "#0f172a",
        "muted": "#64748b",
        "line": "#e2e8f0",
        "dots": "#cbd5e1",
        "grid_line": "#e2e8f0",
        "node": "#0284c7",
        "node_glow": "#0ea5e9",
        "synapse": "#0284c7",
        "radar": "#0284c7",
    },
}

FONT_MONO = "ui-monospace, 'Fira Code', 'JetBrains Mono', 'SFMono-Regular', Menlo, Monaco, Consolas, monospace"


def text_width(s: str, size: float) -> float:
    return len(s) * size * 0.60


def dotted_leader(start: float, end: float, y: float) -> str:
    if end <= start:
        return ""
    dots = []
    step = 7.0
    x = start
    while x < end:
        dots.append(f"M{x:.1f} {y:.1f}h1")
        x += step
    return " ".join(dots)


def generate_neural_mesh(theme: str) -> str:
    """Generate animated neural network / constellation graphic in left panel."""
    t = THEMES[theme]
    cx, cy = 225, 290
    
    parts = []
    
    # Background subtle coordinate grid
    for gx in range(50, 410, 40):
        parts.append(f'<line x1="{gx}" y1="80" x2="{gx}" y2="520" stroke="{t["grid_line"]}" stroke-width="0.75" opacity="0.4"/>')
    for gy in range(100, 510, 40):
        parts.append(f'<line x1="50" y1="{gy}" x2="410" y2="{gy}" stroke="{t["grid_line"]}" stroke-width="0.75" opacity="0.4"/>')

    # Radar scan circles
    for r, op in [(55, 0.45), (105, 0.35), (150, 0.25)]:
        parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t["radar"]}" stroke-width="1" opacity="{op}"/>')

    # Radar scanning line
    parts.append(
        f'<g transform="translate({cx},{cy})">'
        f'<line x1="0" y1="0" x2="150" y2="0" stroke="{t["chrome"]}" stroke-width="1.5" opacity="0.7">'
        f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/>'
        f'</line>'
        f'</g>'
    )

    # Fixed seed for consistent beautiful constellation
    rng = random.Random(42)
    nodes = [
        # (x, y, label, priority)
        (225, 290, "AI.CORE", True),
        (160, 210, "U-NET", False),
        (290, 205, "KIMBALL.DW", False),
        (140, 360, "ASPNET", False),
        (300, 370, "VISION", False),
        (225, 170, "ML.UPLIFT", False),
        (225, 410, "CLEAN.ARCH", False),
        (100, 275, "PYTORCH", False),
        (350, 295, "C#", False),
        (130, 150, "ETL", False),
        (320, 145, "NEXTJS", False),
        (110, 430, "PYTEST", False),
        (340, 435, "SQL", False),
    ]

    # Draw synapse lines between close nodes
    for i, (x1, y1, _, _) in enumerate(nodes):
        for j, (x2, y2, _, _) in enumerate(nodes):
            if i < j:
                dist = math.hypot(x1 - x2, y1 - y2)
                if dist < 125:
                    op = max(0.15, 0.7 - (dist / 140))
                    parts.append(
                        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                        f'stroke="{t["synapse"]}" stroke-width="1.2" opacity="{op:.2f}">'
                        f'<animate attributeName="opacity" values="{op:.2f};{min(1.0, op*2):.2f};{op:.2f}" '
                        f'dur="{3 + (i*j)%4}s" repeatCount="indefinite"/>'
                        f'</line>'
                    )

    # Draw nodes and labels
    for i, (nx, ny, nlabel, is_center) in enumerate(nodes):
        r = 5.0 if is_center else 3.2
        glow_r = 9.0 if is_center else 6.0
        color = t["title"] if is_center else t["node"]
        pulse_dur = "2.4s" if is_center else f"{2.0 + (i % 3) * 0.8}s"
        
        # Outer glow
        parts.append(
            f'<circle cx="{nx}" cy="{ny}" r="{glow_r}" fill="{color}" opacity="0.25">'
            f'<animate attributeName="r" values="{glow_r};{glow_r + 4};{glow_r}" dur="{pulse_dur}" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.35;0.1;0.35" dur="{pulse_dur}" repeatCount="indefinite"/>'
            f'</circle>'
        )
        # Inner core
        parts.append(
            f'<circle cx="{nx}" cy="{ny}" r="{r}" fill="{color}">'
            f'<animate attributeName="opacity" values="1;0.6;1" dur="{pulse_dur}" repeatCount="indefinite"/>'
            f'</circle>'
        )
        # Label
        label_y = ny - 8 if ny < 290 else ny + 13
        parts.append(
            f'<text x="{nx}" y="{label_y}" text-anchor="middle" fill="{t["muted"]}" '
            f'font-family="{FONT_MONO}" font-size="8.5" font-weight="600" letter-spacing="0.5">{nlabel}</text>'
        )

    # Live telemetry data in left panel
    parts.extend([
        f'<rect x="50" y="472" width="330" height="46" rx="5" fill="{t["panel_bg"]}" stroke="{t["panel_border"]}" stroke-width="1" opacity="0.95"/>',
        f'<text x="62" y="490" fill="{t["accent"]}" font-family="{FONT_MONO}" font-size="9.5" font-weight="700">● FLAGSHIP: U-NET CV RESEARCH</text>',
        f'<text x="62" y="506" fill="{t["muted"]}" font-family="{FONT_MONO}" font-size="8.5">F1: 89% · IoU: 85% · 1,000+ AERIAL IMAGES · UFMS</text>',
    ])

    return "".join(parts)


def render_svg(theme: str) -> str:
    t = THEMES[theme]
    
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="Isabelle Bicudo profile terminal" font-family="{FONT_MONO}">',
        '<defs>',
        '  <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">',
        '    <feGaussianBlur stdDeviation="3" result="blur" />',
        '    <feMerge>',
        '      <feMergeNode in="blur" />',
        '      <feMergeNode in="SourceGraphic" />',
        '    </feMerge>',
        '  </filter>',
        '</defs>',
        # Main Background & border
        f'<rect width="{W}" height="{H}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="1.5"/>',
        
        # Terminal Window Header
        f'<path d="M0 12C0 5.373 5.373 0 12 0h{W-24}c6.627 0 12 5.373 12 12v32H0V12z" fill="{t["header_bg"]}"/>',
        f'<line x1="0" y1="44" x2="{W}" y2="44" stroke="{t["line"]}" stroke-width="1"/>',
        
        # Window buttons (macOS style)
        '<circle cx="24" cy="22" r="6" fill="#ff5f56"/>',
        '<circle cx="44" cy="22" r="6" fill="#ffbd2e"/>',
        '<circle cx="64" cy="22" r="6" fill="#27c93f"/>',
        
        # Terminal Header Title
        f'<text x="{W/2}" y="27" text-anchor="middle" fill="{t["header_text"]}" '
        f'font-size="12" font-weight="600" letter-spacing="0.8">isabelle@workstation:~$ ./profile.sh --live</text>',

        # Left Panel (Neural Matrix Visualizer)
        f'<rect x="24" y="60" width="382" height="505" rx="8" fill="{t["panel_bg"]}" stroke="{t["panel_border"]}" stroke-width="1"/>',
        f'<path d="M24 96H406" stroke="{t["panel_border"]}"/>',
        f'<text x="40" y="84" fill="{t["title"]}" font-size="12" font-weight="700" letter-spacing="1.2">NEURAL.TELEMETRY</text>',
        f'<text x="390" y="84" text-anchor="end" fill="{t["muted"]}" font-size="10">27-DIM VEC</text>',
    ]

    # Add Neural Mesh & telemetry
    parts.append(generate_neural_mesh(theme))

    # Right Information Panel (SYSTEM.INFO)
    rx, ry, rw, rh = 422, 60, 734, 505
    parts.extend([
        f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" fill="{t["panel_bg"]}" stroke="{t["panel_border"]}" stroke-width="1"/>',
        f'<path d="M{rx} {ry+36}H{rx+rw}" stroke="{t["panel_border"]}"/>',
        
        # Header in right panel
        f'<text x="{rx+20}" y="{ry+24}" fill="{t["title"]}" font-size="13" font-weight="700" letter-spacing="1.2">SYSTEM.INFO</text>',
        
        # LIVE indicator
        f'<circle cx="{rx+rw-195}" cy="{ry+20}" r="4.5" fill="#ef4444">'
        f'<animate attributeName="opacity" values="1;0.25;1" dur="1.5s" repeatCount="indefinite"/>'
        f'</circle>',
        f'<text x="{rx+rw-184}" y="{ry+24}" fill="#ef4444" font-size="11.5" font-weight="700">LIVE</text>',
        
        # Profile Pill
        f'<rect x="{rx+rw-140}" y="{ry+9}" width="124" height="23" rx="11.5" fill="{t["title"]}" fill-opacity="0.15" stroke="{t["title"]}" stroke-width="1"/>',
        f'<text x="{rx+rw-78}" y="{ry+24}" text-anchor="middle" fill="{t["title"]}" font-size="12" font-weight="700">@IsabelleBic20</text>',
    ])

    # Dotted leaders and rows
    value_right = rx + rw - 20
    row_y = ry + 68
    row_gap = 26.5
    
    for label, value in ROWS:
        val_w = text_width(value, 12.5)
        lbl_w = text_width(label, 12.5)
        leader_start = rx + 20 + lbl_w + 10
        leader_end = value_right - val_w - 10
        
        parts.extend([
            f'<text x="{rx+20}" y="{row_y}" fill="{t["muted"]}" font-size="12.5" font-weight="500">{html.escape(label)}</text>',
            f'<path d="{dotted_leader(leader_start, leader_end, row_y - 4)}" fill="none" stroke="{t["dots"]}" stroke-width="1" shape-rendering="crispEdges"/>',
            f'<text x="{value_right}" y="{row_y}" text-anchor="end" fill="{t["text"]}" font-size="12.5" font-weight="600">{html.escape(value)}</text>',
        ])
        row_y += row_gap

    # Footer inside right panel
    foot_y = ry + rh - 18
    parts.extend([
        f'<line x1="{rx+15}" y1="{foot_y-16}" x2="{rx+rw-15}" y2="{foot_y-16}" stroke="{t["panel_border"]}"/>',
        f'<text x="{rx+20}" y="{foot_y}" fill="{t["accent"]}" font-size="11" font-weight="700">● ALL SYSTEMS NOMINAL</text>',
        f'<text x="{value_right}" y="{foot_y}" text-anchor="end" fill="{t["muted"]}" font-size="11">UTC-4 · BRAZIL NODE</text>',
        '</svg>',
    ])

    return "".join(parts)


def main() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        svg = render_svg(theme)
        out = ASSETS / f"banner-{theme}.svg"
        out.write_text(svg, encoding="utf-8")
        size_kb = len(svg.encode("utf-8")) / 1024
        print(f"wrote {out.relative_to(ROOT)} ({size_kb:.1f} KiB)")


if __name__ == "__main__":
    main()
