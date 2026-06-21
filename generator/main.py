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
    # Tokyo Night renk paleti ile ham SVG kod matrisini oluşturur
    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="850" height="200" viewBox="0 0 850 200">
    <style>
        .bg {{ fill: #1a1b26; rx: 8px; }}
        .border {{ stroke: #414868; stroke-width: 2; fill: none; rx: 8px; }}
        .title {{ font: bold 18px 'Fira Code', monospace; fill: #7aa2f7; }}
        .label {{ font: 14px 'Fira Code', monospace; fill: #565f89; }}
        .value {{ font: bold 14px 'Fira Code', monospace; fill: #bb9af3; }}
        .metric-line {{ stroke: #414868; stroke-dasharray: 4 4; stroke-width: 1; }}
        .timestamp {{ font: 11px 'Fira Code', monospace; fill: #414868; }}
    </style>
    <rect class="bg" width="850" height="200"/>
    <rect class="border" width="848" height="198" x="1" y="1"/>
    
    <text x="30" y="40" class="title">📡 CORE SYSTEM TELEMETRY DIAGNOSTICS</text>
    <line x1="30" y1="55" x2="820" y2="55" stroke="#414868" stroke-width="2"/>
    
    <text x="50" y="90" class="label">[METRIC_01] Total System Stars ........ :</text>
    <text x="400" y="90" class="value">{{metrics['stars']}}</text>
    <line x1="50" y1="105" x2="800" y2="105" class="metric-line"/>
    
    <text x="50" y="130" class="label">[METRIC_02] Public Repos Loaded ....... :</text>
    <text x="400" y="130" class="value">{{metrics['repos']}}</text>
    <line x1="50" y1="145" x2="800" y2="145" class="metric-line"/>
    
    <text x="50" y="160" class="label">[METRIC_03] Connected Network Nodes ... :</text>
    <text x="400" y="160" class="value">{{metrics['followers']}} followers</text>
    
    <text x="580" y="40" class="timestamp">RUNTIME: {{metrics['timestamp']}} UTC</text>
</svg>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_template)

if __name__ == "__main__":
    # YavuzSB için telemetriyi çalıştır ve deponun içine yaz
    telemetry_data = fetch_github_telemetry("YavuzSB")
    generate_stats_card(telemetry_data, "assets/generated/stats-card.svg")
    print("Telemetry card compiler optimization code: 0. Success.")
