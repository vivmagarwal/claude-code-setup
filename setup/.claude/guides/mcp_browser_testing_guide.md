# MCP Browser Testing Guide

**Purpose:** Prevent chat-killing errors when using browser MCP tools.

---

## Quick Reference

```
WORKFLOW:
  take_screenshot filePath="/tmp/screenshot.png"
  Read /tmp/screenshot.png
  → Hook auto-resizes to ≤1900px

SAFE TOOLS:
  ✅ navigate_page, take_screenshot, click, resize_page, list_console_messages

BANNED TOOLS (will KILL the chat):
  ❌ ALL playwright__* tools
  ❌ take_snapshot
```

---

## Safe Tools

| Tool | Notes |
|------|-------|
| `navigate_page` | No content returned |
| `take_screenshot` (with filePath) | Hook auto-resizes |
| `click` | Action only |
| `resize_page` | Action only |
| `list_console_messages` | Browser JSON |

---

## Banned Tools

| Tool | Why |
|------|-----|
| `take_snapshot` | Returns DOM text with invalid Unicode from LaTeX |
| `playwright__*` (ALL) | Returns accessibility tree with invalid Unicode |

**If you use these:** Chat dies. No recovery. Must terminate and start fresh.

---

## The Two Errors

### Error 1: Image >2000px (Recoverable)

```
API Error: 400 "At least one of the image dimensions exceed max allowed size..."
```

**Why:** Retina displays (2x) double screenshot size. 1440×900 viewport → 2880×1800 actual.

**Fix:** Use file-based workflow. Hook auto-resizes.

### Error 2: Invalid Unicode (FATAL)

```
API Error: 400 "The request body is not valid JSON: no low surrogate..."
```

**Why:** Playwright/take_snapshot returns page text containing invalid Unicode from LaTeX/math.

**Fix:** NEVER use banned tools. Chat is dead if this happens.

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| "2000 pixels" | Use `filePath` parameter, hook resizes automatically |
| "browser already running" | `pkill -f "chrome-devtools-mcp"`, retry |
| "no low surrogate" | Chat DEAD. Terminate. Start fresh. |

---

## How Hooks Work

All hooks are inline in `.claude/settings.json` (no external scripts):

- **PreToolUse (Read):** Auto-resizes images >1900px before Claude reads them
- **PostToolUse (take_screenshot):** Auto-resizes saved screenshots to ≤1900px

Uses `sips` (macOS built-in). No dependencies needed.
