---
name: create-scraping-plan-using-firecrawl
description: Research and create comprehensive Firecrawl web scraping implementation plan
argument-hint: [optional: target-website-url]
---

You are an expert web scraping specialist creating a comprehensive, research-driven implementation plan for web scraping using **Firecrawl v2**.

## Core Methodology

**DO NOT rely only on your pre-existing knowledge about Firecrawl.** Actively research current documentation to ensure accuracy with the latest API version.

**CRITICAL**: Firecrawl v2 has significant changes from v1. Always verify the current API capabilities, parameters, and best practices through documentation research.

## Agent Usage

This command uses specialized agents for thorough research:
- **web-researcher**: For Firecrawl documentation, features, and best practices
- **code-researcher**: For analyzing target website structure and existing codebase patterns

Launch agents in parallel when possible for efficiency.

## Phase 1: Gather User Requirements

Ask the user for the following information ONE AT A TIME (conversational approach):

### 1. Target Website Details
- Homepage URL
- Login page URL (if authentication required)
- Username/email and password (if authentication required)
- Any additional authentication requirements (2FA, tokens, session cookies, etc.)

### 2. Scraping Scope
What type of scraping do you need?
1. **Single page scraping** - Extract data from one specific URL
2. **Multi-page crawling** - Crawl entire website or specific sections
3. **URL discovery** - Map all URLs on a website
4. **Structured extraction** - Extract specific data across multiple pages
5. **Web search + scrape** - Search the web and scrape results

For crawling:
- Full site or specific sections?
- URL patterns to include/exclude (e.g., only /docs/* or /blog/*)
- Maximum number of pages to crawl
- Maximum discovery depth
- Should it crawl entire domain (including parent/sibling pages)?
- Should it follow external links?
- Should it include subdomains?

### 3. Content Requirements
- What content to extract? (articles, products, documentation, tables, etc.)
- Output format preferences:
  - **Markdown** - Clean, LLM-ready markdown
  - **HTML** - Cleaned HTML
  - **Raw HTML** - Original HTML
  - **JSON** - Structured data with schema
  - **Links** - Extract all links
  - **Screenshot** - Page screenshots
  - **Summary** - AI-generated summary
- Specific data fields needed? (titles, dates, authors, prices, etc.)
- Should extract only main content or full page?
- Any HTML tags/classes/IDs to include or exclude?

### 4. Authentication & Actions Requirements
- Does the site require login?
- Any cookie consent dialogs to handle?
- Any popups or overlays to dismiss?
- Need to interact with page elements? (click buttons, fill forms, scroll, etc.)
- Need to wait for dynamic content to load?

### 5. Technical Constraints
- Performance requirements (speed vs. freshness)
- Rate limiting concerns (delay between requests)
- Cache preferences (use cached data or always fetch fresh?)
- Request timeout requirements
- Proxy requirements (auto proxy, residential, etc.)
- Storage location for output files
- Webhook URL for real-time notifications (optional)
- Any existing code/patterns to follow?

## Phase 2: Research Current Firecrawl Documentation

Use the **web-researcher** agent to research these official sources:

Task(
  subagent_type="web-researcher",
  description="Research Firecrawl v2 documentation",
  prompt="""
Research comprehensive Firecrawl v2 documentation from these sources:

1. **Official Documentation**: https://docs.firecrawl.dev/
   - Quickstart guide
   - Current version and features overview
   - Migration guide (v1 to v2 changes)

2. **Core Features**:
   - Scrape endpoint: https://docs.firecrawl.dev/features/scrape
   - Crawl endpoint: https://docs.firecrawl.dev/features/crawl
   - Map endpoint: https://docs.firecrawl.dev/features/map
   - Search endpoint: https://docs.firecrawl.dev/features/search
   - Extract endpoint: https://docs.firecrawl.dev/features/extract

3. **Advanced Scraping Guide**: https://docs.firecrawl.dev/advanced-scraping-guide
   - All scrape options (formats, includeTags, excludeTags, etc.)
   - Actions for browser automation
   - Authentication approaches
   - Crawler options
   - PDF parsing

4. **API Reference**: https://docs.firecrawl.dev/api-reference/v2-introduction
   - Complete parameter documentation
   - Request/response formats
   - Rate limits and pricing

5. **SDKs**:
   - Python SDK: https://docs.firecrawl.dev/sdks/python
   - Node.js SDK: https://docs.firecrawl.dev/sdks/node

6. **Webhooks** (if needed): https://docs.firecrawl.dev/webhooks/overview
   - Webhook configuration
   - Event types
   - Security best practices

Provide:
- Current version capabilities
- Best authentication methods using Actions
- All available formats and their use cases
- Crawler options and strategies
- Complete code examples from official docs
- Links to all referenced documentation pages
- Breaking changes from v1 to v2
"""
)

## Phase 3: Inspect Target Website Using Playwright MCP

**YOU (Claude Code) must use Playwright MCP directly to inspect the target website.**

DO NOT delegate this to an agent. Use the Playwright MCP tools yourself to:

### Step 1: Navigate and Screenshot

```
Use mcp__playwright__browser_navigate to visit the target URL
Use mcp__playwright__browser_take_screenshot to capture the page
Use mcp__playwright__browser_snapshot to get the page structure
```

### Step 2: Identify Key Elements

For **Authentication** (if required):
1. Navigate to login page: `mcp__playwright__browser_navigate`
2. Take screenshot: `mcp__playwright__browser_take_screenshot`
3. Get page snapshot: `mcp__playwright__browser_snapshot`
4. Identify and test selectors:
   - Username/email field selector
   - Password field selector
   - Submit button selector
   - Cookie consent/popup selectors (if present)
   - Success indicator after login
   - Any CSRF tokens or hidden fields

For **Content Extraction**:
1. Navigate to target content page
2. Take screenshot of the page
3. Get page snapshot to analyze structure
4. Identify:
   - Main content container selector
   - Elements to exclude (nav, header, footer, aside, ads)
   - Dynamic content patterns
   - Embedded iframes (if any)
   - Pagination selectors (if applicable)

### Step 3: Verify Selectors

Use `mcp__playwright__browser_click` or `mcp__playwright__browser_snapshot` to verify:
- Selectors are unique and work correctly
- Forms can be filled
- Buttons are clickable
- Success indicators are detectable

### Step 4: Document Findings

After testing with Playwright MCP, document:
- **Exact CSS selectors** (tested and verified)
- **Page structure** (main content, elements to exclude)
- **Authentication flow** (step-by-step with verified selectors)
- **Screenshots** (save URLs from Playwright)
- **Any anti-bot measures** (CAPTCHA, Cloudflare, rate limiting)

**CRITICAL**: All selectors in the final plan MUST be real selectors you verified using Playwright MCP, not placeholders.

## Phase 4: Create Implementation Plan

Based on research results, generate a comprehensive markdown file named `{target_site}_firecrawl_plan.md` with:

### Required Sections

#### 1. Project Overview
- Target website: [URL]
- Firecrawl v2 capabilities used: [scrape/crawl/map/search/extract]
- Authentication method: [actions-based/none]
- Scraping strategy: [single page/multi-page crawl/extraction]
- Expected pages: [user estimate]
- Output formats: [markdown/json/html/etc.]
- **Special features**: Automatic iframe/embedded content extraction included

#### 2. Installation & Setup

```bash
# Python SDK installation
pip install firecrawl-py

# Node.js SDK installation
npm install @mendable/firecrawl-js

# API Key setup
# Get your API key from: https://firecrawl.dev/
```

```python
# Python initialization
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")
```

```javascript
// Node.js initialization
import Firecrawl from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });
```

#### 3. Authentication Implementation (If Required)

**Using Firecrawl Actions for Authentication:**

Firecrawl's Actions feature allows you to automate browser interactions before scraping. This is the recommended approach for authentication.

```python
# Python: Authentication with Actions
from firecrawl import Firecrawl
import os

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

# Scrape authenticated page using Actions
result = firecrawl.scrape(
    url="[LOGIN_URL]",
    formats=["markdown"],
    actions=[
        # Wait for page to load
        {"type": "wait", "milliseconds": 1000},

        # Handle cookie consent (if present)
        # {"type": "click", "selector": "#accept-cookies"},

        # Fill in username
        {"type": "click", "selector": "[USERNAME_SELECTOR]"},
        {"type": "write", "text": os.getenv("USERNAME")},

        # Fill in password
        {"type": "click", "selector": "[PASSWORD_SELECTOR]"},
        {"type": "write", "text": os.getenv("PASSWORD")},

        # Submit login form
        {"type": "click", "selector": "[SUBMIT_SELECTOR]"},

        # Wait for successful login
        {"type": "wait", "milliseconds": 2000},

        # Navigate to target page or continue scraping
        # The session is now authenticated
    ]
)

print(result["markdown"])
```

```javascript
// Node.js: Authentication with Actions
import Firecrawl from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });

const result = await firecrawl.scrape({
  url: '[LOGIN_URL]',
  formats: ['markdown'],
  actions: [
    { type: 'wait', milliseconds: 1000 },
    // { type: 'click', selector: '#accept-cookies' }, // If needed
    { type: 'click', selector: '[USERNAME_SELECTOR]' },
    { type: 'write', text: process.env.USERNAME },
    { type: 'click', selector: '[PASSWORD_SELECTOR]' },
    { type: 'write', text: process.env.PASSWORD },
    { type: 'click', selector: '[SUBMIT_SELECTOR]' },
    { type: 'wait', milliseconds: 2000 },
  ],
});

console.log(result.markdown);
```

**Available Actions:**
- `wait` - Wait for specified milliseconds
- `click` - Click an element
- `write` - Type text into an element
- `press` - Press a keyboard key
- `scroll` - Scroll up or down
- `scrape` - Scrape a specific element
- `screenshot` - Take a screenshot
- `executeJavascript` - Run custom JavaScript

**Action Sequence Example (Complex Flow):**
```python
actions=[
    # Initial page load
    {"type": "wait", "milliseconds": 1000},

    # Dismiss cookie banner
    {"type": "click", "selector": "#cookie-accept"},
    {"type": "wait", "milliseconds": 500},

    # Login
    {"type": "write", "selector": "#email", "text": os.getenv("EMAIL")},
    {"type": "press", "key": "Tab"},
    {"type": "write", "text": os.getenv("PASSWORD")},
    {"type": "click", "selector": "button[type='submit']"},
    {"type": "wait", "milliseconds": 3000},

    # Navigate to protected page
    {"type": "click", "selector": "a[href='/dashboard']"},
    {"type": "wait", "milliseconds": 2000},

    # Scroll to load dynamic content
    {"type": "scroll", "direction": "down"},
    {"type": "wait", "milliseconds": 1000},

    # Take screenshot
    {"type": "screenshot", "fullPage": True},
]
```

#### 4. Main Scraping Implementation

Choose the appropriate implementation based on requirements:

**Option A: Single Page Scraping**

```python
# Python: Scrape single page with multiple formats
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

result = firecrawl.scrape(
    url="[TARGET_URL]",
    formats=[
        "markdown",
        "links",
        "html",
        {
            "type": "json",
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "date": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["title", "content"]
            }
        },
        {"type": "screenshot", "fullPage": True}
    ],
    onlyMainContent=True,
    includeTags=["article", "main", ".content"],
    excludeTags=["nav", "footer", "#ads", ".sidebar"],
    waitFor=2000,  # Wait for dynamic content
    timeout=30000,
    maxAge=0  # Always fetch fresh (disable cache)
)

# Access different formats
print(result["markdown"])
print(result["json"])
print(result["links"])
print(result["screenshot"])  # URL to screenshot
```

**Option B: Multi-Page Crawling**

```python
# Python: Crawl multiple pages
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

# Start crawl and wait for completion
crawl_result = firecrawl.crawl(
    url="[BASE_URL]",
    limit=100,
    maxDiscoveryDepth=3,
    includePaths=["^/blog/.*", "^/docs/.*"],
    excludePaths=["^/admin/.*", "^/api/.*"],
    allowSubdomains=False,
    allowExternalLinks=False,
    delay=1,  # 1 second delay between requests
    scrape_options={
        "formats": ["markdown", "links"],
        "onlyMainContent": True,
        "excludeTags": ["nav", "footer"],
        "timeout": 30000
    }
)

# Process results
for page in crawl_result["data"]:
    print(f"URL: {page['metadata']['sourceURL']}")
    print(f"Title: {page['metadata']['title']}")
    print(f"Markdown length: {len(page['markdown'])}")
    print("---")
```

```javascript
// Node.js: Crawl with async/await
import Firecrawl from '@mendable/firecrawl-js';

const firecrawl = new Firecrawl({ apiKey: 'fc-YOUR-API-KEY' });

const crawlResult = await firecrawl.crawl({
  url: '[BASE_URL]',
  limit: 100,
  maxDiscoveryDepth: 3,
  includePaths: ['^/blog/.*', '^/docs/.*'],
  excludePaths: ['^/admin/.*'],
  scrapeOptions: {
    formats: ['markdown', 'links'],
    onlyMainContent: true,
    excludeTags: ['nav', 'footer'],
  },
});

for (const page of crawlResult.data) {
  console.log(`URL: ${page.metadata.sourceURL}`);
  console.log(`Title: ${page.metadata.title}`);
  console.log('---');
}
```

**Option C: URL Discovery (Map)**

```python
# Python: Map all URLs on a website
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

# Discover all URLs
map_result = firecrawl.map(
    url="[BASE_URL]",
    search="blog",  # Filter URLs containing "blog"
    limit=500,
    includeSubdomains=True
)

print(f"Found {len(map_result['links'])} URLs")
for url in map_result['links']:
    print(url)
```

**Option D: Structured Data Extraction**

```python
# Python: Extract structured data from multiple pages
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

# Extract with schema
extract_result = firecrawl.extract(
    urls=["[URL1]", "[URL2]", "[BASE_URL]/*"],  # Supports wildcards
    prompt="Extract product information including name, price, description, and features",
    schema={
        "type": "object",
        "properties": {
            "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "price": {"type": "number"},
                        "description": {"type": "string"},
                        "features": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["name", "price"]
                }
            }
        },
        "required": ["products"]
    },
    enableWebSearch=True  # Enable for broader context
)

print(extract_result["data"])
```

**Option E: Web Search + Scrape**

```python
# Python: Search the web and scrape results
from firecrawl import Firecrawl

firecrawl = Firecrawl(api_key="fc-YOUR-API-KEY")

search_result = firecrawl.search(
    query="best practices for [TOPIC]",
    limit=5,
    sources=[{"type": "web"}, {"type": "news"}],
    scrape_options={
        "formats": ["markdown"],
        "onlyMainContent": True
    }
)

# Access web results with scraped content
for result in search_result["data"]["web"]:
    print(f"Title: {result['title']}")
    print(f"URL: {result['url']}")
    print(f"Content: {result['markdown'][:200]}...")
    print("---")
```

#### 5. Advanced Features

**Automatic iframe & Embedded Content Handling:**

Firecrawl automatically extracts content from iframes and embedded elements without any configuration. This includes:
- Social media embeds (Twitter, Facebook, Instagram)
- Video players (YouTube, Vimeo)
- Maps (Google Maps)
- Payment forms and secure inputs
- Chat widgets
- Advertisement frames
- Nested and cross-origin iframes
- Dynamically loaded iframes

```python
# Python: iframe content is automatically extracted
result = firecrawl.scrape(
    url="https://example.com/page-with-embeds",
    formats=["markdown"]
)
# Markdown output will seamlessly include all iframe content
print(result["markdown"])
```

**Technical capabilities:**
- Recursive iframe traversal at any depth
- Cross-origin iframe handling
- Automatic waiting for iframe content to load
- Support for dynamically injected iframes
- Proper handling of sandboxed iframes

**No additional configuration needed** - this works automatically with all scraping and crawling endpoints.

**Webhook Integration (Real-time Notifications):**

```python
# Python: Crawl with webhook notifications
result = firecrawl.crawl(
    url="[BASE_URL]",
    limit=1000,
    webhook={
        "url": "https://your-domain.com/webhook",
        "metadata": {"job_id": "12345", "user": "john"},
        "events": ["started", "page", "completed"]
    }
)

# Your webhook endpoint will receive:
# - crawl.started: When crawl begins
# - crawl.page: For each page scraped
# - crawl.completed: When crawl finishes
# - crawl.failed: If crawl encounters error
```

**Caching Strategy:**

```python
# Fresh data (no cache)
result = firecrawl.scrape(url="[URL]", maxAge=0)

# Use cache if less than 1 hour old
result = firecrawl.scrape(url="[URL]", maxAge=3600000)  # 1 hour in ms

# Default: Use cache if less than 2 days old
result = firecrawl.scrape(url="[URL]")  # maxAge defaults to 172800000 (2 days)
```

**PDF Parsing:**

```python
# Explicitly enable PDF parsing
result = firecrawl.scrape(
    url="[PDF_URL]",
    formats=["markdown"],
    parsers=["pdf"]
)
```

**Change Tracking:**

```python
# Track changes on a page
result = firecrawl.scrape(
    url="[URL]",
    formats=[
        "markdown",
        {
            "type": "changeTracking",
            "tag": "version-1",
            "modes": ["full", "diff"]
        }
    ]
)
```

#### 6. Complete Production Script

```python
"""
Firecrawl Production Scraper
[Description based on requirements]
"""
import os
import json
from datetime import datetime
from pathlib import Path
from firecrawl import Firecrawl

# Configuration
CONFIG = {
    "api_key": os.getenv("FIRECRAWL_API_KEY"),
    "base_url": "[BASE_URL]",
    "output_dir": "output",
    "max_pages": 100,
    "formats": ["markdown", "links"],
    # Add more based on requirements
}

def ensure_output_dir():
    """Create output directory structure"""
    Path(CONFIG["output_dir"]).mkdir(parents=True, exist_ok=True)
    Path(f"{CONFIG['output_dir']}/content").mkdir(exist_ok=True)
    Path(f"{CONFIG['output_dir']}/metadata").mkdir(exist_ok=True)
    Path(f"{CONFIG['output_dir']}/logs").mkdir(exist_ok=True)

def save_page(page_data, index):
    """Save scraped page to disk"""
    timestamp = datetime.now().isoformat()

    # Save markdown content
    if "markdown" in page_data:
        with open(f"{CONFIG['output_dir']}/content/page_{index:04d}.md", 'w') as f:
            f.write(page_data["markdown"])

    # Save metadata
    metadata = {
        "index": index,
        "timestamp": timestamp,
        "url": page_data.get("metadata", {}).get("sourceURL"),
        **page_data.get("metadata", {})
    }
    with open(f"{CONFIG['output_dir']}/metadata/page_{index:04d}.json", 'w') as f:
        json.dump(metadata, f, indent=2)

def main():
    """Main scraping orchestration"""
    ensure_output_dir()

    # Initialize Firecrawl
    firecrawl = Firecrawl(api_key=CONFIG["api_key"])

    print(f"Starting scrape of {CONFIG['base_url']}")
    print(f"Output directory: {CONFIG['output_dir']}")

    try:
        # [Choose appropriate method based on requirements]

        # Example: Crawl
        result = firecrawl.crawl(
            url=CONFIG["base_url"],
            limit=CONFIG["max_pages"],
            scrape_options={
                "formats": CONFIG["formats"],
                "onlyMainContent": True,
                "timeout": 30000
            }
        )

        # Process and save results
        for idx, page in enumerate(result["data"], 1):
            save_page(page, idx)
            print(f"Saved page {idx}/{len(result['data'])}: {page['metadata']['sourceURL']}")

        # Save summary
        summary = {
            "timestamp": datetime.now().isoformat(),
            "base_url": CONFIG["base_url"],
            "total_pages": len(result["data"]),
            "status": result.get("status"),
            "credits_used": result.get("creditsUsed")
        }
        with open(f"{CONFIG['output_dir']}/metadata/summary.json", 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"\n✓ Completed! Scraped {len(result['data'])} pages")
        print(f"  Total credits used: {result.get('creditsUsed')}")

    except Exception as e:
        print(f"✗ Error: {e}")
        # Log error
        with open(f"{CONFIG['output_dir']}/logs/error.log", 'a') as f:
            f.write(f"{datetime.now().isoformat()} - {str(e)}\n")
        raise

if __name__ == "__main__":
    main()
```

#### 7. Output Structure

```
output/
├── content/
│   ├── page_0001.md
│   ├── page_0002.md
│   └── ...
├── metadata/
│   ├── page_0001.json
│   ├── page_0002.json
│   ├── summary.json
│   └── ...
└── logs/
    └── error.log
```

#### 8. Troubleshooting Guide

**Common Issues and Solutions:**

- **Authentication fails**:
  - Verify selectors are correct using Playwright inspector
  - Check for CAPTCHA or rate limiting on login page
  - Ensure wait times are sufficient for page loads
  - Try increasing `waitFor` in actions
  - Check if site uses JavaScript-rendered login forms

- **Content not extracted correctly**:
  - Use `onlyMainContent: false` to get full page
  - Adjust `includeTags` and `excludeTags` to target specific elements
  - Increase `waitFor` for dynamic content
  - Check if content is in iframes
  - Try different output formats

- **Rate limiting / 429 errors**:
  - Increase `delay` parameter in crawl
  - Reduce concurrent requests
  - Use caching (`maxAge`) to avoid re-fetching
  - Consider using proxy option

- **Timeout errors**:
  - Increase `timeout` parameter (default: 30000ms)
  - Check if page has slow-loading resources
  - Use actions to wait for specific elements

- **Incomplete crawl results**:
  - Check `maxDiscoveryDepth` - may need to increase
  - Verify `includePaths` and `excludePaths` patterns
  - Check if `limit` is too low
  - Enable `crawlEntireDomain` for parent/sibling pages
  - Enable `allowSubdomains` if needed

- **API key issues**:
  - Verify API key is correct: https://firecrawl.dev/
  - Check if key has required permissions
  - Ensure key is properly set in environment

- **Webhook not receiving events**:
  - Verify webhook URL is publicly accessible
  - Check webhook security signature
  - Review event types configuration
  - Test with webhook testing tools

**Debug Mode:**

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test single page first
result = firecrawl.scrape(url="[TEST_URL]", formats=["markdown"])
print(result)
```

#### 9. API Reference & Documentation

- **Main Documentation**: https://docs.firecrawl.dev/
- **Scrape API**: https://docs.firecrawl.dev/api-reference/endpoint/scrape
- **Crawl API**: https://docs.firecrawl.dev/api-reference/endpoint/crawl
- **Map API**: https://docs.firecrawl.dev/api-reference/endpoint/map
- **Extract API**: https://docs.firecrawl.dev/api-reference/endpoint/extract
- **Search API**: https://docs.firecrawl.dev/api-reference/endpoint/search
- **Advanced Guide**: https://docs.firecrawl.dev/advanced-scraping-guide
- **Rate Limits**: https://docs.firecrawl.dev/rate-limits
- **Python SDK**: https://docs.firecrawl.dev/sdks/python
- **Node SDK**: https://docs.firecrawl.dev/sdks/node
- **Webhooks**: https://docs.firecrawl.dev/webhooks/overview

**Version**: Firecrawl v2
**Documentation researched**: [date]

#### 10. Environment Variables

```bash
# .env file
FIRECRAWL_API_KEY=fc-your-api-key-here
USERNAME=your-username  # If authentication required
PASSWORD=your-password  # If authentication required
EMAIL=your-email       # If authentication required
```

```python
# Load environment variables
from dotenv import load_dotenv
load_dotenv()
```

#### 11. Quick Start Commands

```bash
# Install dependencies
pip install firecrawl-py python-dotenv

# Set API key
export FIRECRAWL_API_KEY="fc-YOUR-API-KEY"

# Run scraper
python scraper.py
```

#### 12. Cost Estimation

Based on Firecrawl pricing:
- Scrape: [X] credits per page
- Crawl: [X] credits per page
- Extract: See https://firecrawl.dev/extract#pricing

Estimated total: [calculation based on requirements]

Monitor usage at: https://firecrawl.dev/app

#### 13. Next Steps

1. **Get API Key**: https://firecrawl.dev/
2. **Install SDK**: `pip install firecrawl-py` or `npm install @mendable/firecrawl-js`
3. **Test authentication** (if required): Run single page scrape with actions
4. **Test single page**: Verify selectors and formats work correctly
5. **Run small crawl**: Test with `limit: 5` first
6. **Scale up**: Increase to full requirements
7. **Monitor usage**: Check dashboard for credits and errors

## Phase 5: Validation Checklist

Before finalizing the plan, verify:

**Research Quality:**
- [ ] Latest Firecrawl v2 documentation reviewed
- [ ] All endpoints (scrape/crawl/map/extract/search) understood
- [ ] Actions feature capabilities documented
- [ ] Authentication approach validated
- [ ] All documentation links valid and current

**Code Quality:**
- [ ] All code uses current Firecrawl v2 API
- [ ] No v1 deprecated methods used
- [ ] Code is complete and runnable (no placeholders)
- [ ] Error handling included
- [ ] Security notes included (env vars for credentials)
- [ ] Both Python and Node.js examples provided (where relevant)

**Specificity:**
- [ ] Selectors are specific to target website
- [ ] Configuration matches user requirements
- [ ] Appropriate endpoint chosen (scrape/crawl/map/extract)
- [ ] Output formats match requirements
- [ ] Authentication flow documented (if required)

**Completeness:**
- [ ] All user requirements addressed
- [ ] Output structure defined
- [ ] Error handling and troubleshooting included
- [ ] Cost estimation provided
- [ ] Next steps are clear and actionable

## Output Format

The implementation plan must:
- Be immediately executable by developer with no Firecrawl experience
- Include complete, copy-paste-ready code for both Python and Node.js
- Reference official docs for every major feature
- Include actual selectors and configuration (not placeholders)
- Have clear section headers and code blocks
- Explain WHY each approach was chosen based on requirements

## Important Notes

- **Stay Current**: Prioritize official Firecrawl v2 docs
- **Version Awareness**: This is for Firecrawl v2 (not v1)
- **No Assumptions**: If feature not clear, note this and suggest alternatives
- **Code Quality**: All code must be production-ready with error handling
- **Security**: Use environment variables for credentials and API keys
- **Multiple SDKs**: Provide examples in both Python and Node.js where relevant

## Success Criteria

The implementation plan succeeds if:
1. Developer can follow it without additional research
2. All code based on current Firecrawl v2 documentation
3. Scraping/crawling works on first attempt (or clear debugging provided)
4. Plan includes all advanced features user requested
5. Cost estimation helps user plan budget

## Execution Flow

1. **Ask user questions** (Phase 1) - one question at a time, conversational
2. **Research documentation** (Phase 2) - use web-researcher agent for Firecrawl v2 docs
3. **INSPECT TARGET WEBSITE** (Phase 3) - **YOU MUST use Playwright MCP directly**:
   - Navigate to target URL and login page
   - Take screenshots
   - Get page snapshots
   - Identify and verify all selectors
   - Test authentication flow
   - Document exact selectors (no placeholders!)
4. **Synthesize findings** - combine research + verified selectors
5. **Generate plan** (Phase 4) - create comprehensive markdown with REAL selectors
6. **Validate** (Phase 5) - check all requirements met
7. **Present** - show plan location and next steps

**CRITICAL**: Phase 3 must be done by YOU using Playwright MCP, not delegated to an agent. All selectors in the plan must be verified and real.

## Critical Success Factors

**The plan MUST:**
1. Be based on Firecrawl v2 API (not v1)
2. Include authentication via Actions if required
3. Choose the right endpoint (scrape vs crawl vs extract vs map)
4. **Use REAL selectors verified via Playwright MCP** (not placeholders!)
5. Provide complete working code examples with actual selectors
6. Include troubleshooting for common issues
7. Reference official documentation throughout

**The plan FAILS if:**
1. Code uses v1 API or deprecated methods
2. Authentication approach is unclear or incomplete
3. Wrong endpoint chosen for the use case
4. **Selectors are generic placeholders like "[USERNAME_SELECTOR]"** - MUST be real!
5. Selectors were not verified using Playwright MCP in Phase 3
6. No cost estimation provided

Remember: Firecrawl v2 is powerful and handles many edge cases automatically. Focus on choosing the right endpoint and configuring it correctly for the user's specific needs.
