# High-Stakes Browser Testing Guide

**Purpose:** Thorough, step-by-step browser testing for applications where reliability matters - education, healthcare, finance, or any user-critical system.

---

## When to Use This Guide

Use this guide when testing:
- Educational content (students depend on accuracy)
- Financial applications (users depend on correctness)
- Healthcare tools (patients depend on reliability)
- Any application where bugs harm real people

---

## The Golden Rule

```
TEST EVERY SINGLE ITEM. ONE AT A TIME. NO SHORTCUTS.
```

---

## Session Startup (Do First)

```bash
# Kill zombie browser processes
pkill -f "chrome-devtools-mcp" 2>/dev/null; sleep 2
```

---

## Screenshot Workflow

```
# Take screenshot → Hook auto-resizes → Read the file
mcp__chrome-devtools__take_screenshot filePath="/tmp/screenshot.png"
Read /tmp/screenshot.png
```

---

## Safe vs Banned Tools

| Safe | Use For |
|------|---------|
| `navigate_page` | Open pages |
| `take_screenshot filePath="..."` | Visual verification |
| `click`, `hover`, `drag`, `type`, `fill_form`, etc. | All interaction tools allowed |
| `list_console_messages` | Check errors |
| All other tools | Allowed unless they extract page text |

| Banned (on pages with LaTeX/math) | Why |
|-----------------------------------|-----|
| `take_snapshot` | Returns DOM text - invalid Unicode |
| `browser_snapshot` | Returns accessibility tree - invalid Unicode |

**Rule:** All tools are allowed EXCEPT those that extract TEXT from pages (snapshot tools). Action tools and screenshots are always safe.

---

## The Testing Checklist

For **EVERY** item being tested:

### 1. Load & Visual Check

```
navigate_page url="..."
take_screenshot filePath="/tmp/screenshot.png"
Read /tmp/screenshot.png
```

Verify:
- [ ] Page loads (no blank screen)
- [ ] Layout is clean and professional
- [ ] No overlapping elements
- [ ] Text is readable (good contrast)
- [ ] Images/icons load correctly

### 2. Console Check

```
list_console_messages
```

Verify:
- [ ] Zero JavaScript errors
- [ ] No 404 or network errors
- [ ] No critical warnings

### 3. Interactive Testing (Act Like a User)

**Test EVERY interaction:**

| Element | How to Test |
|---------|-------------|
| Buttons | Click each one, verify response |
| Forms | Submit valid AND invalid data |
| Sliders | Move to min, max, middle |
| Drag & Drop | Drag all items to all targets |
| Modals | Open and close all |
| Navigation | Test all links and back/forward |
| Error states | Trigger and verify error handling |

After each interaction:
```
take_screenshot filePath="/tmp/screenshot.png"
Read /tmp/screenshot.png
```

### 4. Content Accuracy

- [ ] All text is factually correct
- [ ] No typos or grammatical errors
- [ ] Numbers and calculations are accurate
- [ ] Dates and times are correct
- [ ] Names and references are accurate

### 5. Edge Cases

- [ ] Empty states handled
- [ ] Long text doesn't break layout
- [ ] Special characters display correctly
- [ ] Loading states work
- [ ] Error states are helpful

### 6. Record Result

After passing all checks:
- Mark item as verified
- Note any issues found and fixed
- Move to next item

---

## What is FORBIDDEN

- **NO batch verification** - Never mark multiple items without testing each
- **NO sampling** - "Tested 5, assuming rest are fine" is NOT acceptable
- **NO assumptions** - "This probably works" is NOT verification
- **NO shortcuts** - If you didn't click it, you didn't test it

---

## The Correct Workflow

```
Load → Screenshot → Console → Click Everything → Verify Content → Record → Next

Load → Screenshot → Console → Click Everything → Verify Content → Record → Next

... repeat for every item ...
```

---

## Accountability Questions

Before marking ANY item as verified, ask yourself:

1. Did I physically LOAD this in a browser?
2. Did I physically CLICK every interactive element?
3. Did I physically TEST every user flow?
4. Did I physically READ the content for accuracy?
5. Would I stake my reputation on this being perfect?

**If ANY answer is NO, do NOT mark it as verified.**

---

## Error Recovery

| Error | Action |
|-------|--------|
| "2000 pixels" | Use `filePath` parameter (hook auto-resizes) |
| "browser already running" | `pkill -f "chrome-devtools-mcp"`, retry |
| "no low surrogate" | Chat DEAD. Terminate. Start fresh. Avoid snapshot tools on pages with math/LaTeX. |

---

## Tracking Schema (Template)

For tracking verification status, use these fields per item:

```json
{
  "item_id": "unique-id",
  "item_name": "Item Name",
  "tested": "",
  "ui_quality": "",
  "content_accurate": "",
  "test_notes": ""
}
```

**Status values:**
- `""` - Not yet verified
- `"PASS"` - Verified and passed
- `"FIX"` - Issue found, fix in progress

**Item is ready only when ALL fields are `"PASS"`**

---

## Why This Matters

When testing high-stakes applications:
- A student might have ONE chance at their exam
- A patient might rely on ONE medical calculation
- A user might make ONE financial decision

**Broken functionality or inaccurate content causes real harm.**

Your testing is the last line of defense between bugs and real users.

---

## Quick Start Checklist

```
[ ] Kill zombie processes: pkill -f "chrome-devtools-mcp"
[ ] Use file-based screenshots: filePath="/tmp/screenshot.png"
[ ] Check console after every page load
[ ] Click EVERY button
[ ] Test EVERY interaction
[ ] Read EVERY piece of content
[ ] Record result before moving on
[ ] Never skip, never batch, never assume
```
