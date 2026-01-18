# Documentation Guide

How to maintain project documentation for senior engineers.

---

## Philosophy

**Audience**: Senior engineers who are experts in their craft but new to this project.

- **Concise, not verbose** - Skip obvious steps. No hand-holding.
- **Complete, not sparse** - Don't omit critical context. A new engineer should understand any feature from docs alone.
- **The `docs/` folder is the onboarding source** - Everything needed to understand the project lives here.

---

## Typical Documentation Structure

```
docs/
├── ARCHITECTURE.md       # System overview, database, auth, key components
├── DEVELOPER_GUIDE.md    # Setup, patterns, code standards
├── API_REFERENCE.md      # REST/GraphQL endpoints
├── DEPLOYMENT.md         # Hosting, env vars, CI/CD
├── DESIGN_SYSTEM.md      # Colors, typography, spacing (if UI project)
├── CONTRIBUTING.md       # Contribution process
└── [FEATURE]_GUIDE.md    # Feature-specific docs as needed

CLAUDE.md                 # AI assistant context (root level)
```

Adapt based on project needs. Not every project needs every file.

---

## When to Update

| Change Type | Update |
|-------------|--------|
| New API endpoint | API_REFERENCE.md |
| Database schema change | ARCHITECTURE.md |
| New service/module | ARCHITECTURE.md |
| New directory structure | DEVELOPER_GUIDE.md |
| Auth changes | ARCHITECTURE.md |
| Deployment config | DEPLOYMENT.md |
| Design tokens | DESIGN_SYSTEM.md |
| New feature | Create or update relevant guide |
| Removed feature | Remove from docs, update cross-references |

**Rule**: Update docs in the same PR as the code change.

---

## Update Principles

1. **Source code is truth** - Document what code does, not what it should do
2. **Same PR** - Code and docs ship together
3. **Cross-reference** - Link to related docs; don't duplicate
4. **File paths** - Always relative to repo root: `src/lib/auth/...`
5. **No future features** - Don't document planned work as if it exists

---

## What Lives Where

### ARCHITECTURE.md
- System diagram / high-level overview
- Service/module table with paths and responsibilities
- Database schema (tables, key relationships)
- Auth flow and methods
- Core architectural decisions and why

### DEVELOPER_GUIDE.md
- Local setup instructions
- Project structure (directories)
- Key patterns (components, data fetching, error handling)
- Code standards and conventions
- How to add common things (new route, new component, etc.)

### API_REFERENCE.md
- All endpoints: method, path, auth requirements
- Request/response examples
- Error codes and meanings
- Rate limits if applicable

### DEPLOYMENT.md
- Hosting platform details
- Environment variables (names, purposes - not values)
- Build and deploy process
- Rollback procedures

### Feature-Specific Guides
- Create `[FEATURE]_GUIDE.md` for complex features
- Include: purpose, architecture, key files, common tasks
- Example: `PAYMENTS_GUIDE.md`, `SEARCH_GUIDE.md`

---

## Writing Style

**Do:**
- Use tables for structured information
- Use code blocks for examples
- Reference file paths: "See `src/lib/auth/session.ts`"
- Explain the "why" behind non-obvious decisions
- Keep prose minimal

**Don't:**
- Copy-paste large code blocks (reference files instead)
- Explain basic programming concepts
- Document obvious things ("Run `npm install` to install dependencies")
- Write step-by-step tutorials for simple tasks

---

## Adding Documentation

### New Feature
1. Decide: standalone guide or section in existing doc?
2. Add to ARCHITECTURE.md service table
3. Add directory to DEVELOPER_GUIDE.md structure
4. Document API endpoints if applicable

### New API Route
Add to API_REFERENCE.md:
```markdown
### POST /api/resource

Creates a new resource.

**Auth**: Required
**Body**: `{ name: string, type: "a" | "b" }`
**Response**: `{ id: string, ...resource }`
**Errors**: 400 (validation), 401 (unauthorized)
```

### Database Change
Update ARCHITECTURE.md schema section. Only document tables/fields actually in use.

---

## Verification Checklist

Before merging:
- [ ] Docs match actual code behavior
- [ ] No references to removed/renamed files
- [ ] Cross-links work
- [ ] Examples are accurate and runnable
- [ ] No planned features documented as existing

---

## Remember

> A senior engineer joining the project tomorrow should be able to understand the entire system by reading `docs/` - nothing more, nothing less.
