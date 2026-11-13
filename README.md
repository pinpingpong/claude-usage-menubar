# Claude Usage Menu Bar

A tiny macOS menu bar widget that shows your Claude plan usage at a glance, so you don't have to keep running `/usage` or opening the settings page.

```
◔ 17% · 14%          ← session (5h) · weekly
```

Click it for details:

- Session (5h) and weekly usage, with local reset times
- Model-specific weekly limits, when your plan has them
- How this week's usage splits across Claude Code, chat and Cowork
- Link to claude.ai usage settings, manual refresh

The icon turns orange at 70% and red at 90%.

## How it works

A single Python script (standard library only) run by [SwiftBar](https://github.com/swiftbar/SwiftBar) every 5 minutes. It reads the login Claude Code already stores in macOS Keychain and asks Anthropic for the same usage data `/usage` shows.

No API key, no extra login, no dependencies. Your token is only sent to `api.anthropic.com`.

## Requirements

- macOS
- [Claude Code](https://claude.com/claude-code), logged in with a Claude subscription (Pro/Max)
- Python 3 (ships with macOS developer tools)
- [Homebrew](https://brew.sh)

## Install

```bash
brew install --cask swiftbar
mkdir -p ~/.config/swiftbar
curl -o ~/.config/swiftbar/claude-usage.5m.py \
  https://raw.githubusercontent.com/pinpingpong/claude-usage-menubar/main/claude-usage.5m.py
chmod +x ~/.config/swiftbar/claude-usage.5m.py
defaults write com.ameba.SwiftBar PluginDirectory "$HOME/.config/swiftbar"
open -a SwiftBar
```

On first run, macOS asks whether SwiftBar can access the `Claude Code-credentials` keychain item. Click **Always Allow**.

To change the refresh interval, rename the file: `claude-usage.1m.py` refreshes every minute, `claude-usage.15m.py` every 15.

## Troubleshooting

| Shows | Meaning |
|---|---|
| `Login expired` | The stored token expired. Open Claude Code once and it refreshes. |
| `HTTP 4xx/5xx` or `Error` | The endpoint changed or is down. See caveat below. |
| Nothing in the menu bar | Check SwiftBar's plugin folder is `~/.config/swiftbar`, or the icon may be hidden behind the notch. |

## Caveat

This uses an **undocumented** Anthropic endpoint (`/api/oauth/usage`), the same one Claude Code appears to use for `/usage`. It is not an official API, can change without notice, and this project is not affiliated with Anthropic.

## License

MIT
