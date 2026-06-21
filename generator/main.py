import os
import json
import requests
from datetime import datetime
from collections import Counter

def fetch_github_telemetry(username):
    # GitHub API üzerinden ham kullanıcı verilerini ve dilleri çeker
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    user_url = f"https://api.github.com/users/{username}"
    user_data = requests.get(user_url, headers=headers).json()
    
    # Tüm repoları çek
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    repos_response = requests.get(repos_url, headers=headers)
    repos_data = repos_response.json() if repos_response.status_code == 200 else []
    
    total_stars = 0
    languages = Counter()
    
    for repo in repos_data:
        if isinstance(repo, dict):
            total_stars += repo.get("stargazers_count", 0)
            lang = repo.get("language")
            if lang:
                # Dilleri topla
                languages[lang] += 1
                
    # En çok kullanılan 5 dili al
    top_langs = languages.most_common(5)
    total_lang_count = sum(languages.values())
    
    lang_stats = []
    # Bilinen diller için renk paleti (Cyberpunk / HUD uyumlu neon renkler eklendi)
    colors = {
        "Python": "#3b82f6", "JavaScript": "#facc15", "TypeScript": "#60a5fa", 
        "HTML": "#f97316", "CSS": "#a855f7", "Java": "#ea580c", "C++": "#ec4899", 
        "C": "#9ca3af", "C#": "#22c55e", "Go": "#06b6d4", "Rust": "#fdba74", 
        "Shell": "#84cc16", "Vue": "#10b981", "PHP": "#8b5cf6", "Ruby": "#ef4444"
    }
              
    for lang, count in top_langs:
        pct = (count / total_lang_count) * 100 if total_lang_count > 0 else 0
        color = colors.get(lang, "#0ea5e9") # Varsayılan neon mavi
        lang_stats.append({"name": lang, "percent": pct, "color": color})
        
    return {
        "stars": total_stars,
        "repos": user_data.get("public_repos", 0),
        "followers": user_data.get("followers", 0),
        "top_languages": lang_stats,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def generate_stats_card(metrics, output_path):
    # HUD (Heads Up Display) Cyberpunk ve Kompleks Tasarım
    lang_bars = ""
    y_offset = 135
    for i, lang in enumerate(metrics.get("top_languages", [])):
        bar_width = int((lang['percent'] / 100) * 300)
        lang_bars += f"""
        <g transform="translate(0, {i * 40})">
            <text x="0" y="10" class="hud-text" fill="{lang['color']}">{lang['name']}</text>
            <text x="300" y="10" class="hud-value-small" text-anchor="end" fill="#fff">{lang['percent']:.1f}%</text>
            <!-- Background bar -->
            <rect x="0" y="18" width="300" height="4" fill="#1f2937" rx="2"/>
            <!-- Foreground bar with animation -->
            <rect x="0" y="18" width="0" height="4" fill="{lang['color']}" rx="2" filter="url(#glow-light)">
                <animate attributeName="width" from="0" to="{bar_width}" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.2 1" keyTimes="0;1"/>
            </rect>
            <!-- Decorative dots -->
            <circle cx="0" cy="20" r="3" fill="#fff" filter="url(#glow-light)">
                <animate attributeName="cx" from="0" to="{bar_width}" dur="1.5s" fill="freeze" calcMode="spline" keySplines="0.1 0.8 0.2 1" keyTimes="0;1"/>
            </circle>
        </g>
        """

    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="850" height="420" viewBox="0 0 850 420">
    <defs>
        <linearGradient id="hud-bg" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#050505"/>
            <stop offset="50%" stop-color="#0e1118"/>
            <stop offset="100%" stop-color="#050505"/>
        </linearGradient>
        <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
            <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#3b82f6" stroke-opacity="0.08" stroke-width="1"/>
            <circle cx="30" cy="30" r="1" fill="#3b82f6" opacity="0.3"/>
        </pattern>
        <pattern id="dots" width="8" height="8" patternUnits="userSpaceOnUse">
            <rect x="0" y="0" width="1" height="1" fill="#10b981" opacity="0.15"/>
        </pattern>
        <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="4" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="heavy-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="8" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="glow-light" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    </defs>

    <style>
        .hud-title {{ font: bold 28px 'Courier New', monospace; fill: #3b82f6; letter-spacing: 5px; }}
        .hud-subtitle {{ font: 12px 'Courier New', monospace; fill: #10b981; letter-spacing: 2.5px; text-transform: uppercase; }}
        .hud-text {{ font: bold 12px 'Consolas', monospace; letter-spacing: 1px; text-transform: uppercase; }}
        .hud-value {{ font: bold 26px 'Consolas', monospace; fill: #f8fafc; }}
        .hud-value-small {{ font: bold 14px 'Consolas', monospace; }}
        .hud-label {{ font: bold 11px 'Courier New', monospace; fill: #6b7280; letter-spacing: 2px; }}
        .hud-border {{ stroke: #3b82f6; fill: none; }}
        
        @keyframes scanline {{
            0% {{ transform: translateY(-100%); }}
            100% {{ transform: translateY(420px); }}
        }}
        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}
        @keyframes rotate {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @keyframes reverse-rotate {{
            0% {{ transform: rotate(360deg); }}
            100% {{ transform: rotate(0deg); }}
        }}
        .scan-line {{ animation: scanline 5s linear infinite; opacity: 0.15; }}
        .blinking {{ animation: blink 2s infinite; }}
        .spinning {{ transform-origin: center; animation: rotate 15s linear infinite; }}
        .spinning-fast {{ transform-origin: center; animation: reverse-rotate 8s linear infinite; }}
    </style>

    <!-- Base Backgrounds -->
    <rect width="850" height="420" fill="url(#hud-bg)" rx="10"/>
    <rect width="850" height="420" fill="url(#grid)" rx="10"/>
    <rect width="850" height="420" fill="url(#dots)" rx="10" opacity="0.6"/>
    
    <!-- Scanline Effect -->
    <rect class="scan-line" width="850" height="30" fill="url(#hud-bg)" stroke="#3b82f6" stroke-width="1" />

    <!-- Outer HUD Frame (Angled Tech Borders) -->
    <path d="M 20 45 L 45 20 L 805 20 L 830 45 L 830 375 L 805 400 L 45 400 L 20 375 Z" class="hud-border" stroke-width="1.5" opacity="0.7"/>
    <path d="M 15 50 L 40 25 L 200 25" class="hud-border" stroke-width="3" filter="url(#glow)"/>
    <path d="M 835 370 L 810 395 L 650 395" class="hud-border" stroke-width="3" filter="url(#glow)"/>
    
    <!-- Corner Decorative Accents -->
    <g stroke="#3b82f6" stroke-width="2" filter="url(#glow-light)">
        <!-- Top Left -->
        <line x1="25" y1="60" x2="25" y2="80"/>
        <line x1="25" y1="60" x2="45" y2="60"/>
        <!-- Bottom Right -->
        <line x1="825" y1="360" x2="825" y2="340"/>
        <line x1="825" y1="360" x2="805" y2="360"/>
    </g>

    <!-- Header Section -->
    <g transform="translate(60, 70)">
        <text x="0" y="0" class="hud-title" filter="url(#heavy-glow)">YAVUZ_SB // CORE_SYSTEM</text>
        <text x="0" y="28" class="hud-subtitle blinking">STATUS: ONLINE_ | OVERRIDE: GRANTED_ | SECURITY: MAX</text>
        <rect x="0" y="45" width="730" height="1" fill="#3b82f6" opacity="0.5"/>
        <rect x="0" y="45" width="200" height="2" fill="#10b981" filter="url(#glow)"/>
        <rect x="220" y="43" width="50" height="4" fill="#facc15" filter="url(#glow-light)"/>
    </g>

    <text x="790" y="90" class="hud-text" text-anchor="end" fill="#9ca3af">SYS_TIME: {metrics['timestamp']}</text>

    <!-- Left Column: Hexagon Core Metrics -->
    <g transform="translate(60, 150)">
        <!-- Hexagon 1: Stars -->
        <g transform="translate(0, 0)">
            <polygon points="45,0 90,22 90,72 45,95 0,72 0,22" stroke="#10b981" stroke-width="1.5" fill="#0f172a" opacity="0.9" filter="url(#glow-light)"/>
            <polygon points="45,8 80,28 80,66 45,86 10,66 10,28" fill="none" stroke="#10b981" stroke-width="1" stroke-dasharray="4 2" opacity="0.5"/>
            <text x="45" y="40" class="hud-label" text-anchor="middle">STARS</text>
            <text x="45" y="65" class="hud-value" text-anchor="middle" fill="#10b981" filter="url(#glow)">{metrics['stars']}</text>
        </g>
        
        <!-- Hexagon 2: Repos -->
        <g transform="translate(110, 60)">
            <polygon points="45,0 90,22 90,72 45,95 0,72 0,22" stroke="#3b82f6" stroke-width="1.5" fill="#0f172a" opacity="0.9" filter="url(#glow-light)"/>
            <polygon points="45,8 80,28 80,66 45,86 10,66 10,28" fill="none" stroke="#3b82f6" stroke-width="1" stroke-dasharray="4 2" opacity="0.5"/>
            <text x="45" y="40" class="hud-label" text-anchor="middle">REPOS</text>
            <text x="45" y="65" class="hud-value" text-anchor="middle" fill="#3b82f6" filter="url(#glow)">{metrics['repos']}</text>
        </g>
        
        <!-- Hexagon 3: Followers -->
        <g transform="translate(220, 0)">
            <polygon points="45,0 90,22 90,72 45,95 0,72 0,22" stroke="#8b5cf6" stroke-width="1.5" fill="#0f172a" opacity="0.9" filter="url(#glow-light)"/>
            <polygon points="45,8 80,28 80,66 45,86 10,66 10,28" fill="none" stroke="#8b5cf6" stroke-width="1" stroke-dasharray="4 2" opacity="0.5"/>
            <text x="45" y="40" class="hud-label" text-anchor="middle">NODES</text>
            <text x="45" y="65" class="hud-value" text-anchor="middle" fill="#8b5cf6" filter="url(#glow)">{metrics['followers']}</text>
        </g>
    </g>

    <!-- Center Tech Radar Decoration -->
    <g transform="translate(215, 305)">
        <circle cx="0" cy="0" r="50" fill="none" stroke="#3b82f6" stroke-width="1" opacity="0.3" stroke-dasharray="2 4"/>
        <circle cx="0" cy="0" r="40" fill="none" stroke="#10b981" stroke-width="2" opacity="0.6" class="spinning"/>
        <circle cx="0" cy="0" r="28" fill="none" stroke="#8b5cf6" stroke-width="1.5" opacity="0.5" stroke-dasharray="15 5" class="spinning-fast"/>
        <circle cx="0" cy="0" r="5" fill="#3b82f6" filter="url(#glow)"/>
        <!-- Radar Sweep -->
        <path d="M 0 0 L 0 -50 A 50 50 0 0 1 50 0 Z" fill="#3b82f6" opacity="0.15" class="spinning"/>
        <line x1="0" y1="0" x2="50" y2="0" stroke="#3b82f6" stroke-width="2" opacity="0.9" filter="url(#glow)" class="spinning"/>
    </g>

    <!-- Connection Lines connecting Hexagons to Tech Stack -->
    <path d="M 330 200 L 380 200 L 430 150 L 480 150" fill="none" stroke="#3b82f6" stroke-width="1.5" opacity="0.5" stroke-dasharray="6 4"/>
    <path d="M 280 305 L 430 305 L 430 150" fill="none" stroke="#10b981" stroke-width="1.5" opacity="0.3"/>
    <circle cx="480" cy="150" r="4" fill="#ffffff" filter="url(#glow)"/>

    <!-- Right Column: Technology Stack (Languages) -->
    <g transform="translate(480, 140)">
        <text x="0" y="0" class="hud-subtitle" fill="#3b82f6" filter="url(#glow-light)">// TECH_STACK_MATRIX</text>
        <rect x="0" y="10" width="300" height="1" fill="#3b82f6" opacity="0.4"/>
        
        <!-- Rendered Language Bars -->
        <g transform="translate(0, 30)">
            {lang_bars}
        </g>
    </g>

    <!-- Bottom Readout Console -->
    <g transform="translate(480, 345)">
        <rect x="0" y="0" width="310" height="40" fill="#0f172a" stroke="#3b82f6" stroke-width="1" rx="4" opacity="0.8"/>
        <rect x="0" y="0" width="4" height="40" fill="#10b981" rx="2"/>
        <text x="15" y="18" class="hud-label" fill="#10b981">> SYSTEM_DIAGNOSTICS_RUNNING...</text>
        <text x="15" y="32" class="hud-label">> MEMORY_LEAKS: 0 | OPTIMIZATION: 100%</text>
    </g>

</svg>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    telemetry_data = fetch_github_telemetry("YavuzSB")
    generate_stats_card(telemetry_data, "assets/generated/stats-card.svg")
    print("Telemetry card compiler optimization code: 0. Success.")
