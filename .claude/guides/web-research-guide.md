# Web Research Guide

## Tool Hierarchy: Choose the Right Tool

```
1. Context7 MCP      � Official framework/library documentation
2. WebSearch         � Current events, general queries, finding resources
3. WebFetch          � Specific URLs, articles, GitHub pages
4. GitHub CLI        � Repository data, issues, PRs, releases
5. Playwright MCP    � JavaScript-heavy sites, interactive content
```

## 1. Context7 MCP Server (Priority for Documentation)

### When to Use
- **ALWAYS FIRST** for framework/library documentation
- React, Next.js, Vue, Angular, TypeScript, Node.js, etc.
- API references and code examples
- Best practices from official sources

### Usage Pattern
```xml
<research>
1. First: mcp__context7__resolve-library-id
   Input: "react" or "nextjs" or "tailwind"
   
2. Then: mcp__context7__get-library-docs
   Input: Resolved library ID from step 1
   Options: 
   - tokens: 10000 (default, increase for more context)
   - topic: "hooks" or "routing" (optional focus)
</research>
```

### Example Workflow
```python
# User asks: "How do I use React hooks?"

# Step 1: Resolve library
mcp__context7__resolve-library-id(libraryName="react")
# Returns: /facebook/react

# Step 2: Get documentation
mcp__context7__get-library-docs(
    context7CompatibleLibraryID="/facebook/react",
    topic="hooks",
    tokens=15000
)
```

## 2. WebSearch (General Research)

### When to Use
- Current events, news, issues etc
- Finding relevant resources
- Comparing solutions
- Discovering tools/libraries
- Market research

### Best Practices
```python
WebSearch(
    query="React performance optimization 2025",  # Include year for current info
    allowed_domains=["react.dev", "web.dev"],     # Optional: trusted sources
    blocked_domains=["badsite.com"]             # Optional: avoid outdated
)
```

### Search Query Optimization
- **Specific terms**: "React Server Components" vs "React components"
- **Include year**: "Next.js 14 features 2025"
- **Use operators**: "site:github.com TypeScript generics"
- **Technical queries**: Include error messages in quotes

## 3. WebFetch (Specific URLs)

### When to Use
- Blog posts and articles
- Documentation not in Context7
- GitHub README files
- Release notes
- Stack Overflow answers

### Usage Patterns
```python
# Standard fetch
WebFetch(
    url="https://github.com/vercel/next.js",
    prompt="List the main features and recent updates"
)

# GitHub raw content
WebFetch(
    url="https://raw.githubusercontent.com/vercel/next.js/main/README.md",
    prompt="Extract setup instructions"
)

# Technical articles
WebFetch(
    url="https://web.dev/articles/optimize-lcp",
    prompt="Summarize optimization techniques"
)
```

### URL Patterns to Remember
- **GitHub Raw**: `https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file}`
- **NPM Package**: `https://www.npmjs.com/package/{package-name}`
- **MDN Docs**: `https://developer.mozilla.org/en-US/docs/{path}`

## 4. GitHub Research Methods

### Method 1: GitHub CLI (via Bash)
```bash
# Repository information
gh api repos/facebook/react

# Latest releases
gh api repos/vercel/next.js/releases/latest

# Pull requests
gh api repos/microsoft/TypeScript/pulls?state=open&per_page=5

# Issues
gh api repos/vuejs/vue/issues?labels=bug&state=open

# Repository topics
gh api repos/tailwindlabs/tailwindcss/topics
```

### Method 2: WebFetch for GitHub
```python
# Repository main page
WebFetch(
    url="https://github.com/facebook/react",
    prompt="What are the key features and installation instructions?"
)

# Specific file
WebFetch(
    url="https://github.com/vercel/next.js/blob/main/docs/architecture.md",
    prompt="Explain the architecture"
)
```

### Method 3: Direct Raw Access
```python
# Package.json analysis
WebFetch(
    url="https://raw.githubusercontent.com/facebook/react/main/package.json",
    prompt="List all dependencies and their purposes"
)
```

## 5. Playwright MCP (Dynamic Content)

### When to Use
- JavaScript-rendered content
- Interactive documentation
- Sites requiring navigation
- Form submissions
- Content behind authentication

### Basic Workflow
```python
# 1. Navigate to page
mcp__playwright__browser_navigate(
    url="https://example.com/docs"
)

# 2. Take snapshot (better than screenshot)
mcp__playwright__browser_snapshot()

# 3. Interact if needed
mcp__playwright__browser_click(
    element="API Reference button",
    ref="button[aria-label='API']"
)

# 4. Extract content
mcp__playwright__browser_snapshot()
```

### Advanced Patterns
```python
# Search within dynamic site
mcp__playwright__browser_type(
    element="Search input",
    ref="input#search",
    text="authentication",
    submit=True
)

# Wait for content
mcp__playwright__browser_wait_for(
    text="Results loaded"
)
```

## Research Workflows

### Workflow 1: Framework Feature Research
```
1. Context7 � Get official docs
2. WebSearch � Find tutorials/articles (current year)
3. GitHub � Check examples in popular repos
4. WebFetch � Read specific implementation guides
```

### Workflow 2: Debugging Error Research
```
1. WebSearch � Search exact error message
2. GitHub � Check library issues
3. Stack Overflow � Via WebFetch
4. Official docs � Via Context7
```

### Workflow 3: Best Practices Research
```
1. Context7 � Official recommendations
2. WebSearch � "best practices {topic} 2024"
3. GitHub � Study popular implementations
4. WebFetch � Read expert articles
```

### Workflow 4: Library Comparison
```
1. npm trends � Via WebFetch
2. GitHub � Star count, activity, issues
3. Context7 � Documentation quality
4. WebSearch � Community opinions
```

## Common Research Patterns

### Pattern: Get Latest Framework Version
```python
# Option 1: NPM
WebFetch(
    url="https://www.npmjs.com/package/next",
    prompt="What is the latest version?"
)

# Option 2: GitHub
gh api repos/vercel/next.js/releases/latest
```

### Pattern: Find Code Examples
```python
# Option 1: Official docs
mcp__context7__get-library-docs(
    context7CompatibleLibraryID="/vercel/next.js",
    topic="app router examples"
)

# Option 2: GitHub search
WebSearch(
    query="site:github.com 'next.js app router' example"
)
```

### Pattern: Architecture Decisions
```python
# Research approach
1. Context7 � Official architecture guide
2. WebSearch � "{framework} architecture patterns 2024"
3. GitHub � Popular boilerplates/starters
4. WebFetch � Technical blog posts
```

## Best Practices

### 1. Tool Selection Priority
```
Documentation � Context7 > WebFetch > WebSearch
Code Examples � GitHub > Context7 > WebSearch
Current Events � WebSearch > WebFetch
Dynamic Sites � Playwright > WebFetch
```

### 2. Efficient Research
- **Batch requests**: Research multiple aspects simultaneously
- **Cache awareness**: WebFetch has 15-minute cache
- **Specific prompts**: Tell tools exactly what to extract
- **Verify currency**: Always check dates on articles

### 3. Quality Signals
```
High Quality:
- Official docs (Context7)
- GitHub repos with recent commits
- Articles from current year
- High star/download count

Low Quality:
- Outdated tutorials (>2 years)
- Sites with many ads
- Incomplete documentation
- Abandoned projects
```

### 4. Research Documentation
Always document your research in code comments or engineering plans:
```javascript
// Based on React 18 docs: https://react.dev/reference/react/hooks
// Implementation pattern from: https://github.com/vercel/next.js/tree/main/examples
// Performance optimization: https://web.dev/articles/optimize-lcp
```

## Troubleshooting

### Issue: Context7 library not found
```python
# Solution: Try variations
resolve-library-id("nextjs")  # Try: "next.js", "next", "vercel next"
```

### Issue: WebFetch timeout
```python
# Solution: Use Playwright for heavy sites
mcp__playwright__browser_navigate(url="...")
mcp__playwright__browser_snapshot()
```

### Issue: GitHub rate limits
```python
# Solution: Use WebFetch instead of gh api
WebFetch(url="https://github.com/...", prompt="...")
```

### Issue: Outdated information
```python
# Solution: Add year to searches
WebSearch(query="React best practices 2024")
```

## Quick Reference

### Documentation Research
```python
# Priority order:
1. mcp__context7__*          # Official docs
2. WebFetch(github_url)       # README/docs
3. WebSearch("docs...")       # Find resources
```

### Code Examples
```python
# Priority order:
1. gh api repos/{owner}/{repo}  # Real implementations
2. Context7(topic="examples")    # Official examples
3. WebSearch("site:github.com")  # Community code
```

### Problem Solving
```python
# Priority order:
1. WebSearch("error message")    # Find solutions
2. gh api .../issues?q=          # Check known issues
3. WebFetch(stackoverflow_url)   # Community answers
```

### Current Information
```python
# Priority order:
1. WebSearch("topic 2024")       # Latest info
2. gh api .../releases/latest    # Latest versions
3. WebFetch(blog_url)           # Recent articles
```

## Research Checklist

Before implementing based on research:
- [ ] Checked official documentation (Context7)
- [ ] Verified information is current (< 1 year old)
- [ ] Found working examples (GitHub)
- [ ] Confirmed best practices (multiple sources)
- [ ] Noted version compatibility
- [ ] Documented sources in code

## Remember

1. **Context7 first** for framework documentation
2. **Be specific** in search queries and prompts
3. **Verify dates** on articles and documentation
4. **Cross-reference** multiple sources
5. **Document sources** for future reference
6. **Use the right tool** for each research task

The goal: Get accurate, current information efficiently using the optimal tool for each situation.