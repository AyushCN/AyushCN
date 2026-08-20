import requests
import os
from datetime import datetime

TOKEN = os.getenv("GITHUB_TOKEN")
USERNAME = "AyushCN"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Repos you want to track (order = priority)
TRACKED = [
    "api-sandbox",
    "fusiontech",
    "berth",
    "dungeons-and-dragons",
    "pharmacy_dbms",
    "smart-waste",
    "car-management-system",
]

def get_repo(name):
    url = f"https://api.github.com/repos/{USERNAME}/{name}"
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    return r.json()

def format_date(iso):
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y")
    except:
        return "Unknown"

def build_section():
    lines = []
    lines.append("## // ACTIVE PROTOCOLS (LIVE)\n")

    for i, name in enumerate(TRACKED):
        data = get_repo(name)
        if not data:
            continue

        status = "● **LIVE**" if i < 2 else "○ **RUN**"
        desc = data.get("description") or "No description"
        lang = data.get("language") or "N/A"
        stars = data.get("stargazers_count", 0)
        forks = data.get("forks_count", 0)
        updated = format_date(data.get("updated_at", ""))
        url = data.get("html_url")

        # Special display names
        display = {
            "fusiontech": "YamlAnchor (fusiontech)",
            "dungeons-and-dragons": "Elyndor (dungeons-and-dragons)",
        }.get(name, name)

        lines.append(f"### {status} [{display}]({url})")
        lines.append(f"[![Last Commit](https://img.shields.io/github/last-commit/{USERNAME}/{name}?style=flat-square&color=00ff9d&label=LAST%20COMMIT)]({url})")
        lines.append(f"[![Stars](https://img.shields.io/github/stars/{USERNAME}/{name}?style=flat-square&color=00f0ff)]({url})")
        lines.append(f"[![Language](https://img.shields.io/github/languages/top/{USERNAME}/{name}?style=flat-square)]({url})")
        lines.append("")
        lines.append(f"{desc}")
        lines.append(f"**Last pulse:** {updated}  |  **Stars:** {stars}  |  **Forks:** {forks}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)

def main():
    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    # Markers so we only replace the live section
    start = "<!-- LIVE-SECTION-START -->"
    end = "<!-- LIVE-SECTION-END -->"

    if start not in content or end not in content:
        print("Markers not found. Please add them to README.md")
        return

    new_section = build_section()
    before = content.split(start)[0]
    after = content.split(end)[1]

    updated = before + start + "\n\n" + new_section + "\n" + end + after

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(updated)

    print("README updated successfully")

if __name__ == "__main__":
    main()
