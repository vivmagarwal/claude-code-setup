---
name: create-scraping-plan-using-crawl4ai
description: Research and create comprehensive Crawl4AI web scraping implementation plan
argument-hint: [optional: target-website-url]
---

You are an expert web scraping specialist creating a comprehensive, research-driven implementation plan for authenticated web scraping using **Crawl4AI**.

## Core Methodology

**DO NOT rely only on your pre-existing knowledge about Crawl4AI.** Actively research current documentation AND verify the actual API through code inspection to ensure accuracy with the latest library version.

**CRITICAL**: Crawl4AI has frequent breaking changes between versions. Documentation may lag behind actual API. Always verify imports, method signatures, and parameters through live code inspection before generating the implementation plan.

## Agent Usage

This command uses specialized agents for thorough research:
- **web-researcher**: For Crawl4AI documentation, authentication methods, and best practices
- **code-researcher**: For analyzing target website structure and existing codebase patterns

Launch agents in parallel when possible for efficiency.

## Phase 1: Gather User Requirements

Ask the user for the following information ONE AT A TIME (conversational approach):

### 1. Target Website Details
- Homepage URL
- Login page URL (if different from homepage)
- Username/email and password
- Any additional authentication requirements (2FA, tokens, session cookies, etc.)

### 2. Crawling Scope
- Full site or specific sections?
- URL patterns to include/exclude (e.g., only /docs/* or /blog/*)
- Maximum number of pages to crawl
- Estimated total pages on site (if known)

### 3. Content Requirements
- What content to extract? (articles, products, documentation, tables, etc.)
- Output format preferences (Markdown, JSON, HTML, or combination)
- Specific data fields needed? (titles, dates, authors, prices, etc.)
- Should media be extracted? (images, videos, downloads)

### 4. Technical Constraints
- Performance requirements (speed vs. politeness)
- Concurrent crawling preferences (number of parallel requests)
- Rate limiting concerns (requests per second/minute)
- Storage location for output files
- Any existing code/patterns to follow?

## Phase 2: Research Current Crawl4AI Documentation

Use the **web-researcher** agent to research these official sources:

Task(
  subagent_type="web-researcher",
  description="Research Crawl4AI documentation",
  prompt="""
Research comprehensive Crawl4AI documentation from these sources:

1. **Official Documentation**: https://docs.crawl4ai.com/
   - Current version and overview
   - Setup & Installation section
   - Quick Start guide
   - Advanced features

2. **Authentication Documentation**: https://docs.crawl4ai.com/advanced/hooks-auth/
   - Current authentication methods
   - Hook types for login automation
   - Session management approaches
   - Cookie handling

3. **Browser Configuration**: https://docs.crawl4ai.com/core/browser-crawler-config/
   - BrowserConfig parameters
   - CrawlerRunConfig parameters
   - Session and persistent context options

4. **URL Discovery & Crawling**:
   - URL seeding methods
   - Sitemap crawling capabilities
   - Recursive link discovery
   - URL filtering options

5. **Content Extraction**: https://docs.crawl4ai.com/core/markdown-generation/
   - Markdown generation strategies
   - Content filtering options
   - Data extraction methods
   - File saving approaches

6. **GitHub Repository**: https://github.com/unclecode/crawl4ai
   - Latest version number
   - Recent examples in examples/ directory
   - Latest release notes
   - Breaking changes in recent versions

Provide:
- Current version number
- Best authentication method for login-protected sites
- URL discovery strategies
- Content extraction capabilities
- Complete code examples from official docs
- Links to all referenced documentation pages
"""
)

## Phase 3: Inspect Target Login Page

Use the **web-researcher** agent with Playwright MCP to inspect the login page:

Task(
  subagent_type="web-researcher",
  description="Analyze target login page structure",
  prompt="""
Navigate to the login page at: [LOGIN_URL]

Identify and document:
1. Username/email field selector (CSS selector or XPath)
2. Password field selector
3. Submit button selector
4. Any CSRF tokens or hidden fields
5. Success indicator after login (e.g., user menu, dashboard element)
6. Any anti-bot measures (reCAPTCHA, Cloudflare, etc.)

Use Playwright MCP to:
- Take screenshot of login page
- Inspect HTML structure
- Test form field selectors
- Document exact selectors needed

Provide exact, working selectors for implementation.
"""
)

## Phase 3.5: Verify Crawl4AI API (CRITICAL - DO NOT SKIP)

**This phase prevents breaking changes from derailing implementation.**

Use the **code-researcher** agent to verify the actual API:

Task(
  subagent_type="code-researcher",
  description="Verify Crawl4AI actual API",
  prompt="""
Install Crawl4AI in the current environment and verify the actual working API.

Run these verification commands:

```python
import crawl4ai
import inspect

# 1. Get exact version
print(f"Crawl4AI Version: {crawl4ai.__version__}")

# 2. List all available exports
available = [x for x in dir(crawl4ai) if not x.startswith('_')]
print(f"Available exports: {available}")

# 3. Verify BrowserConfig parameters
from crawl4ai import BrowserConfig
print("\nBrowserConfig signature:")
print(inspect.signature(BrowserConfig.__init__))

# 4. Verify CrawlerRunConfig parameters
from crawl4ai import CrawlerRunConfig
print("\nCrawlerRunConfig signature:")
print(inspect.signature(CrawlerRunConfig.__init__))

# 5. Verify AsyncWebCrawler.arun signature
from crawl4ai import AsyncWebCrawler
print("\nAsyncWebCrawler.arun signature:")
print(inspect.signature(AsyncWebCrawler.arun))

# 6. Check for common authentication patterns
# Test if hooks exist in CrawlerRunConfig
try:
    config = CrawlerRunConfig(hooks={})
    print("✓ Hooks parameter exists in CrawlerRunConfig")
except TypeError as e:
    print(f"✗ Hooks parameter error: {e}")
    print("→ Use storage_state in BrowserConfig instead")

# 7. Verify markdown/content extraction imports
try:
    from crawl4ai import DefaultMarkdownGenerator, PruningContentFilter
    print("✓ DefaultMarkdownGenerator and PruningContentFilter available")
except ImportError as e:
    print(f"✗ Import error: {e}")

# 8. Verify URL seeding
try:
    from crawl4ai import AsyncUrlSeeder, SeedingConfig, BFSDeepCrawlStrategy
    print("✓ URL seeding classes available")
    print(f"AsyncUrlSeeder methods: {[m for m in dir(AsyncUrlSeeder) if not m.startswith('_')]}")
except ImportError as e:
    print(f"✗ Import error: {e}")
```

Document:
- Actual working imports
- Correct parameter names
- Method signatures that differ from documentation
- Alternative approaches if expected features don't exist
- Version-specific warnings

Provide a "VERIFIED API" section with copy-paste ready imports and configurations.
"""
)

## Phase 4: Create Implementation Plan

Based on research results, generate a comprehensive markdown file named `{target_site}_crawl4ai_plan.md` with:

### Required Sections

#### 1. Project Overview
- Target website: [URL]
- Crawl4AI version: [from research]
- Authentication method: [based on docs]
- URL discovery strategy: [sitemap/recursive/manual]
- Expected pages: [user estimate]

#### 2. Installation & Setup
```bash
# Installation commands from official docs
[commands here]

# Verification
[verification steps]
```

#### 3. Authentication Implementation

**VERIFIED API (from Phase 3.5):**
```python
# Imports verified to work with Crawl4AI v[X.X.X]
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from playwright.async_api import async_playwright
import json
import os
```

**Primary Approach (storage_state method):**
```python
# Complete authentication code
# Based on verified API from Phase 3.5
# Include actual selectors discovered in Phase 3

STORAGE_STATE_FILE = "auth_state.json"

async def perform_login():
    """
    Authenticate with target website using Playwright.
    Saves authentication state for reuse by Crawl4AI.

    Based on: [link to docs section]
    Verified with: Crawl4AI v[X.X.X]
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to login page
            await page.goto("[LOGIN_URL]", wait_until="networkidle")

            # Fill credentials (actual selectors from Phase 3)
            await page.locator("[USERNAME_SELECTOR]").fill(os.getenv("USERNAME"))
            await page.locator("[PASSWORD_SELECTOR]").fill(os.getenv("PASSWORD"))

            # Submit form
            await page.locator("[SUBMIT_SELECTOR]").click()

            # Wait for success indicator
            await page.wait_for_selector("[SUCCESS_SELECTOR]", timeout=10000)

            # Save authentication state
            storage_state = await context.storage_state()
            with open(STORAGE_STATE_FILE, 'w') as f:
                json.dump(storage_state, f)

        finally:
            await browser.close()

async def ensure_authenticated():
    """
    Ensure valid authentication state exists.
    """
    if not os.path.exists(STORAGE_STATE_FILE):
        await perform_login()
```

**Alternative Approach (if hooks are supported):**
```python
# Only use if Phase 3.5 verification confirms hooks parameter exists
async def on_page_context_created(page, context, **kwargs):
    """
    Hook-based authentication (use only if verified in Phase 3.5)
    """
    # [Hook implementation]
    pass
```


#### 4. URL Discovery Strategy
```python
# Complete URL discovery implementation
# Based on user requirements and docs

async def discover_urls():
    """
    Discover all URLs to crawl.
    Strategy: [chosen method]
    Based on: [link to docs section]
    """
    # [Complete implementation]
    # [URL filtering logic]
    # [Expected output]
    pass
```

#### 5. Main Crawling Script
```python
# Full, production-ready script
# Current API methods from docs
# Content extraction configuration
# File saving logic
# Error handling and retry mechanisms

async def main():
    """
    Main crawling orchestration.
    """
    # [Complete, runnable code]
    pass

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

#### 6. Configuration Parameters
```python
# All customizable settings
CRAWL_CONFIG = {
    "max_pages": [value],
    "concurrent_requests": [value],
    "rate_limit": [value],
    "output_format": [value],
    # [More settings based on user requirements]
}
```

#### 7. Output File Structure
```
output/
├── content/
│   ├── page_001.md
│   ├── page_002.md
│   └── ...
├── metadata/
│   └── crawl_metadata.json
└── logs/
    └── crawl_log.txt
```

#### 8. Troubleshooting Guide

**Common Issues and Solutions:**

- **Authentication fails**:
  - Verify selectors with Playwright inspector
  - Check for CAPTCHA or rate limiting
  - Confirm success indicator selector is correct
  - Try running with `headless=False` to see what's happening

- **API parameter errors** (e.g., "unexpected keyword argument"):
  - Run Phase 3.5 verification script again
  - Check if Crawl4AI version changed
  - Use `help(ClassName)` to see current parameters
  - Review this plan's "Version-Specific Notes" section

- **Content not extracted**:
  - Verify markdown generator is configured
  - Check if `process_iframes=True` for embedded content
  - Increase `delay_before_return_html` for dynamic content
  - Test single URL first to isolate issue

- **Rate limiting errors**:
  - Reduce `CONCURRENT_REQUESTS`
  - Increase `RATE_LIMIT_DELAY`
  - Add exponential backoff retry logic

- **Memory issues**:
  - Process URLs in smaller batches
  - Set `cache_mode=CacheMode.BYPASS`
  - Monitor memory with `psutil`

- **Import errors**:
  - Verify imports match Phase 3.5 verification results
  - Check class name capitalization (e.g., `AsyncUrlSeeder` not `AsyncURLSeeder`)
  - Use `dir(crawl4ai)` to see what's actually available

Links to relevant documentation sections.

#### 9. Version-Specific Notes

**Tested with Crawl4AI version:** [actual installed version from Phase 3.5]
**Installation date:** [date]
**API Verification Date:** [when Phase 3.5 was run]

**⚠️ API Stability Warning:**
Crawl4AI has frequent breaking changes between versions. This plan was generated using the actual API verified in Phase 3.5. If you encounter errors:
1. Run the Phase 3.5 verification script again
2. Compare output with "VERIFIED API" sections in this plan
3. Update code to match current API

**Known Working Imports (verified in Phase 3.5):**
```python
# These imports were tested and work with v[X.X.X]
from crawl4ai import (
    AsyncWebCrawler,           # ✓ Verified
    BrowserConfig,             # ✓ Verified
    CrawlerRunConfig,          # ✓ Verified
    AsyncUrlSeeder,            # ✓ Verified (note: AsyncUrlSeeder not AsyncURLSeeder)
    SeedingConfig,             # ✓ Verified
    DefaultMarkdownGenerator,  # ✓ Verified
    PruningContentFilter,      # ✓ Verified
    CacheMode,                 # ✓ Verified
)
```

**Parameter Compatibility Notes:**
- `storage_state`: ✓ Works in BrowserConfig
- `hooks`: [✓/✗ based on Phase 3.5 test] - Use storage_state if unavailable
- `enable_rate_limiting`: [✓/✗ based on verification]
- `enable_stealth`: [✓/✗ based on verification]

**Alternative Approaches (if primary method fails):**
- Authentication: storage_state (primary), hooks (if available)
- URL Discovery: sitemap seeding (primary), manual list (fallback)
- Content Extraction: DefaultMarkdownGenerator (primary), custom extraction (fallback)

#### 10. Documentation References
- **Crawl4AI version:** [version number from Phase 3.5]
- **GitHub Release:** https://github.com/unclecode/crawl4ai/releases/tag/v[X.X.X]
- **Authentication docs:** [URL]
- **Browser config docs:** [URL]
- **Examples:** [GitHub URLs]
- **Documentation researched:** [date]
- **API verified:** [date from Phase 3.5]

#### 11. Quick API Verification Script

**Run this if you encounter import or parameter errors:**

```python
# verify_api.py - Quick API check
import crawl4ai
import inspect

print(f"Crawl4AI Version: {crawl4ai.__version__}")

# Test imports from this plan
try:
    from crawl4ai import (
        AsyncWebCrawler,
        BrowserConfig,
        CrawlerRunConfig,
        AsyncUrlSeeder,
        DefaultMarkdownGenerator,
    )
    print("✓ All imports successful")
except ImportError as e:
    print(f"✗ Import failed: {e}")
    print("→ Run Phase 3.5 verification to get current imports")

# Test BrowserConfig with storage_state
try:
    config = BrowserConfig(storage_state="test.json")
    print("✓ storage_state parameter works")
except TypeError:
    print("✗ storage_state not supported - check Phase 3.5 verification")

# Test CrawlerRunConfig parameters
try:
    config = CrawlerRunConfig(process_iframes=True)
    print("✓ process_iframes parameter works")
except TypeError as e:
    print(f"✗ Parameter error: {e}")
```

**Usage:** `python verify_api.py`

#### 12. Next Steps
1. Install Crawl4AI: `[command]`
2. Configure credentials: `[where to put them]`
3. Test authentication: `[test command]`
4. Run small test crawl: `[command]`
5. Run full crawl: `[command]`
6. Verify results: `[how to check]`

## Phase 5: Validation Checklist

Before finalizing the plan, verify:

**API Verification (Critical):**
- [ ] Phase 3.5 verification completed successfully
- [ ] All imports tested with actual `import` statements
- [ ] Method signatures verified with `inspect.signature()`
- [ ] Parameters tested with actual instantiation
- [ ] Version number documented from `crawl4ai.__version__`

**Code Quality:**
- [ ] All code uses VERIFIED API methods from Phase 3.5
- [ ] No deprecated methods or parameters used
- [ ] Code is complete and runnable (no placeholders like `[value]`)
- [ ] Alternative approaches documented for unstable features
- [ ] Error handling included
- [ ] Security notes included (env vars for credentials)

**Documentation:**
- [ ] Authentication approach matches verified working method
- [ ] All documentation links valid and current
- [ ] "Version-Specific Notes" section complete
- [ ] "Quick API Verification Script" included
- [ ] Troubleshooting includes API compatibility issues

**Specificity:**
- [ ] Selectors are specific to target website (from Phase 3)
- [ ] Configuration matches user requirements
- [ ] Verified imports match actual availability
- [ ] Parameter names match Phase 3.5 verification

**Resilience:**
- [ ] Multiple approaches documented (primary + fallback)
- [ ] Clear guidance if API changes
- [ ] Verification script user can run
- [ ] Version-specific warnings included

## Output Format

The implementation plan must:
- Be immediately executable by developer with no Crawl4AI experience
- Include complete, copy-paste-ready code
- Reference official docs for every major feature
- Include actual selectors and configuration (not placeholders)
- Have clear section headers and code blocks
- Explain WHY each approach was chosen based on docs

## Important Notes

- **Stay Current**: Prioritize official docs over other sources
- **Version Awareness**: Note which Crawl4AI version the plan targets
- **No Assumptions**: If feature documentation not found, note this and suggest alternatives
- **Code Quality**: All code must be production-ready with error handling
- **Security**: Remind user to use environment variables for credentials in production

## Success Criteria

The implementation plan succeeds if:
1. Developer can follow it without additional research
2. All code based on current, verified documentation
3. Authentication and crawling work on first attempt (or clear debugging provided)
4. Plan remains valid until next major Crawl4AI version

## Execution Flow

1. **Ask user questions** (Phase 1) - one question at a time, conversational
2. **Launch parallel research** (Phase 2 & 3) - use both agents simultaneously
3. **VERIFY ACTUAL API** (Phase 3.5) - **DO NOT SKIP** - install and test the library
4. **Synthesize findings** - combine research + verification results
5. **Generate plan** (Phase 4) - create comprehensive markdown file with verified API
6. **Validate** (Phase 5) - check all requirements met, especially API verification
7. **Present** - show plan location and next steps

## Critical Success Factors

**The plan MUST:**
1. Be based on VERIFIED working API (Phase 3.5), not just documentation
2. Include version-specific notes and warnings
3. Provide fallback approaches for unstable features
4. Include a quick verification script user can run
5. Document exact version tested against

**The plan FAILS if:**
1. Code uses deprecated or non-existent methods
2. Parameter names don't match actual API
3. Imports fail in fresh environment
4. No guidance provided for API changes

Remember: Documentation-driven + API-verified approach ensures plan works on first attempt with current Crawl4AI version.
