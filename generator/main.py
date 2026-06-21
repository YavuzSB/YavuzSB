import os
import json
import requests
from datetime import datetime

def fetch_github_telemetry(username):
    # GitHub API üzerinden ham kullanıcı verilerini çeker
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    
    user_url = f"https://api.github.com/users/{username}"
    user_data = requests.get(user_url, headers=headers).json()
    
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_data = requests.get(repos_url, headers=headers).json()
    
    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data if isinstance(repo, dict))
    total_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    
    return {
        "stars": total_stars,
        "repos": total_repos,
        "followers": followers,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def generate_stats_card(metrics, output_path):
    # Modern, glowing, and aesthetic telemetry design
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="850" height="260" viewBox="0 0 850 260">
    <defs>
        <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#16161e" />
            <stop offset="100%" stop-color="#24283b" />
        </linearGradient>
        <linearGradient id="neon-blue" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#7aa2f7" />
            <stop offset="100%" stop-color="#7dcfff" />
        </linearGradient>
        <linearGradient id="neon-purple" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#bb9af3" />
            <stop offset="100%" stop-color="#9d7cd8" />
        </linearGradient>
        <linearGradient id="neon-green" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#9ece6a" />
            <stop offset="100%" stop-color="#73daca" />
        </linearGradient>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="5" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="glow-light" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="2" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    </defs>
    
    <style>
        .title {{ font: bold 22px 'Fira Code', monospace; fill: #7aa2f7; letter-spacing: 1.5px; }}
        .label {{ font: 14px 'Fira Code', monospace; fill: #a9b1d6; font-weight: 500; }}
        .value {{ font: bold 28px 'Fira Code', monospace; fill: #ffffff; }}
        .timestamp {{ font: 11px 'Fira Code', monospace; fill: #565f89; }}
        .box {{ fill: #1a1b26; stroke: #414868; stroke-width: 1.5; rx: 12px; }}
        .icon-bg {{ fill: #24283b; rx: 8px; }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(15px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes pulse {{
            0% {{ opacity: 0.7; }}
            50% {{ opacity: 1; }}
            100% {{ opacity: 0.7; }}
        }}
        .anim-delay-1 {{ animation: fadeIn 0.8s ease-out forwards; opacity: 0; }}
        .anim-delay-2 {{ animation: fadeIn 0.8s ease-out 0.2s forwards; opacity: 0; }}
        .anim-delay-3 {{ animation: fadeIn 0.8s ease-out 0.4s forwards; opacity: 0; }}
        .pulsing-dot {{ animation: pulse 2s infinite; fill: #f7768e; }}
    </style>

    <!-- Outer Background -->
    <rect width="850" height="260" fill="url(#bg-grad)" rx="16"/>
    <rect width="848" height="258" x="1" y="1" fill="none" stroke="#414868" stroke-width="2" rx="16"/>
    <rect width="850" height="260" fill="none" stroke="url(#neon-blue)" stroke-width="1" rx="16" opacity="0.3"/>
    
    <!-- Header -->
    <g transform="translate(45, 50)">
        <circle cx="10" cy="-6" r="6" class="pulsing-dot" filter="url(#glow-light)"/>
        <text x="35" y="0" class="title" filter="url(#glow-light)">SYSTEM TELEMETRY DIAGNOSTICS</text>
        <line x1="35" y1="20" x2="760" y2="20" stroke="#414868" stroke-width="2" stroke-dasharray="4 4" opacity="0.6"/>
        <text x="545" y="-3" class="timestamp">LAST SYNC: {metrics['timestamp']} UTC</text>
    </g>

    <!-- Metric Cards Container -->
    <g transform="translate(45, 110)">
        
        <!-- Stars Card -->
        <g class="anim-delay-1" transform="translate(0, 0)">
            <rect width="235" height="110" class="box" />
            <rect width="235" height="4" fill="url(#neon-blue)" rx="2" opacity="0.9" filter="url(#glow)"/>
            
            <g transform="translate(20, 25)">
                <rect width="40" height="40" class="icon-bg" />
                <path d="M 20 8 l 4 11 l 12 0 l -9 7 l 4 11 l -11 -8 l -11 8 l 4 -11 l -9 -7 l 12 0 Z" fill="#7dcfff" opacity="0.9" filter="url(#glow-light)"/>
            </g>
            
            <text x="75" y="45" class="label">Total Stars</text>
            <text x="75" y="80" class="value" fill="#7dcfff">{metrics['stars']}</text>
        </g>
        
        <!-- Repos Card -->
        <g class="anim-delay-2" transform="translate(260, 0)">
            <rect width="235" height="110" class="box" />
            <rect width="235" height="4" fill="url(#neon-green)" rx="2" opacity="0.9" filter="url(#glow)"/>
            
            <g transform="translate(20, 25)">
                <rect width="40" height="40" class="icon-bg" />
                <path d="M 12 12 h 16 v 18 h -16 z M 12 16 h 16 M 16 12 v -4 h 8 v 4" stroke="#9ece6a" stroke-width="2.5" fill="none" opacity="0.9" filter="url(#glow-light)"/>
            </g>
            
            <text x="75" y="45" class="label">Public Repos</text>
            <text x="75" y="80" class="value" fill="#9ece6a">{metrics['repos']}</text>
        </g>
        
        <!-- Followers Card -->
        <g class="anim-delay-3" transform="translate(520, 0)">
            <rect width="235" height="110" class="box" />
            <rect width="235" height="4" fill="url(#neon-purple)" rx="2" opacity="0.9" filter="url(#glow)"/>
            
            <g transform="translate(20, 25)">
                <rect width="40" height="40" class="icon-bg" />
                <circle cx="20" cy="16" r="6" stroke="#bb9af3" stroke-width="2.5" fill="none" opacity="0.9" filter="url(#glow-light)"/>
                <path d="M 10 32 c 0 -8 20 -8 20 0" stroke="#bb9af3" stroke-width="2.5" fill="none" opacity="0.9" filter="url(#glow-light)"/>
            </g>
            
            <text x="75" y="45" class="label">Network Nodes</text>
            <text x="75" y="80" class="value" fill="#bb9af3">{metrics['followers']}</text>
        </g>
    </g>
</svg>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    # YavuzSB için telemetriyi çalıştır ve deponun içine yaz
    telemetry_data = fetch_github_telemetry("YavuzSB")
    generate_stats_card(telemetry_data, "assets/generated/stats-card.svg")
    print("Telemetry card compiler optimization code: 0. Success.")
