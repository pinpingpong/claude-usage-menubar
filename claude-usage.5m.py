#!/usr/bin/env python3
# <xbar.title>Claude Usage</xbar.title>
# <xbar.desc>Shows Claude plan usage (session + weekly) in the menu bar.</xbar.desc>
# Uses the Claude Code login saved in macOS Keychain. Unofficial endpoint: may break if Anthropic changes it.
import json, subprocess, urllib.request
from datetime import datetime

URL = "https://api.anthropic.com/api/oauth/usage"
LABELS = {"session": "Session (5h)", "weekly_all": "Weekly (all models)"}


def token():
    raw = subprocess.run(
        ["security", "find-generic-password", "-s", "Claude Code-credentials", "-w"],
        capture_output=True, text=True, check=True,
    ).stdout
    return json.loads(raw)["claudeAiOauth"]["accessToken"]


def fmt_reset(iso):
    if not iso:
        return ""
    t = datetime.fromisoformat(iso).astimezone()
    if t.date() == datetime.now().astimezone().date():
        return t.strftime("today %-I:%M %p")
    return t.strftime("%a %-d %b %-I:%M %p")


def color(pct):
    return "red" if pct >= 90 else "orange" if pct >= 70 else None


def main():
    try:
        req = urllib.request.Request(URL, headers={
            "Authorization": f"Bearer {token()}",
            "anthropic-beta": "oauth-2025-04-20",
        })
        data = json.load(urllib.request.urlopen(req, timeout=10))
    except urllib.error.HTTPError as e:
        hint = "Login expired: open Claude Code once to refresh" if e.code == 401 else f"HTTP {e.code}"
        print("Claude ⚠ | sfimage=gauge.with.dots.needle.33percent")
        print("---")
        print(hint)
        print("Refresh | refresh=true")
        return
    except Exception as e:
        print("Claude ⚠ | sfimage=gauge.with.dots.needle.33percent")
        print("---")
        print(f"Error: {type(e).__name__}")
        print("Refresh | refresh=true")
        return

    limits = data.get("limits") or []
    by_kind = {l["kind"]: l for l in limits}
    s = by_kind.get("session", {}).get("percent", 0)
    w = by_kind.get("weekly_all", {}).get("percent", 0)
    top = max(s, w)
    c = color(top)
    print(f"{s:.0f}% · {w:.0f}% | sfimage=gauge.with.dots.needle.50percent" + (f" color={c}" if c else ""))
    print("---")

    for l in limits:
        name = LABELS.get(l["kind"])
        if not name:
            model = ((l.get("scope") or {}).get("model") or {}).get("display_name")
            name = f"Weekly ({model})" if model else l["kind"]
        line = f"{name}: {l['percent']:.0f}%  ·  resets {fmt_reset(l.get('resets_at'))}"
        c = color(l["percent"])
        print(line + (f" | color={c}" if c else ""))

    rows = (data.get("seven_day_breakdown") or {}).get("rows") or []
    rows = [r for r in rows if r.get("percent")]
    if rows:
        print("---")
        print("Share of this week's usage")
        for r in rows:
            print(f"--{r['display_name']}: {r['percent']}%")

    print("---")
    print("Open usage page | href=https://claude.ai/settings/usage")
    print("Refresh now | refresh=true")


main()
