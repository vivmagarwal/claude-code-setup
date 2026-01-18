# Engineering Plan Prompt

---

## PART 1: EXECUTION INSTRUCTIONS

*How you (LLM/developer) should work when implementing features using this system.*

---

### 1.1 Research Phase (Before Planning)

Use **sub-agents** (`Task` tool with `subagent_type=Explore` or `code-researcher`) to:
- Read user-provided source files → summarize key points
- Scan for project standards (CLAUDE.md, README, docs/)
- Identify ALL documentation files that may need updating
- Explore relevant codebase areas for patterns and conventions

**Output**: Distilled findings flow into the plan. Main context stays clean.

### 1.2 Context Management (Throughout Implementation)

| Situation | Action |
|-----------|--------|
| Reading files >200 lines | Use sub-agent → summarize back |
| Exploring unfamiliar code | Use sub-agent with `subagent_type=Explore` |
| Checking reference implementations | Use sub-agent → extract relevant patterns |
| Understanding dependencies | Use sub-agent → return only what's needed |

**Main thread contains ONLY**: the plan, active task context, code being modified.

### 1.3 Update Triggers

Update the plan immediately when:
- Starting or completing any task
- Encountering issues or finding solutions
- Making architectural decisions
- TodoWrite progress changes

### 1.4 Code Quality Standards

- Solid, robust, maintainable code only
- Root cause analysis over surface-level patches
- Simple yet stable—no over-engineering
- No dirty fixes or ugly patches

### 1.5 Completion Criteria

The work is NOT complete until:
- All implementation tasks are ✅
- All documentation tasks are ✅
- Plan reflects final state

---

## PART 2: PLAN SPECIFICATION

*What the engineering plan document should contain and how it should be structured.*

---

### 2.1 Location

```
.project-management/{feature}-plan.md
```

### 2.2 Template

```markdown
# {Feature} Plan

## Current Status
- **Active Task:** [task ID or description]
- **Blocked:** [yes/no - reason if blocked]
- **Last Updated:** [date via terminal command]

## Execution Reminder
<!-- Keep this section at the top for quick reference during implementation -->
When working on this plan:
- Use sub-agents (`Task` tool with `subagent_type=Explore` or `code-researcher`) for reading large files, exploring code, or researching dependencies
- Return only summaries and relevant snippets to the main thread—not entire file contents
- Update this plan immediately after completing each task
- This plan must be self-sufficient: a developer should be able to start working with just this document and have all the context and progress needed
- Audience: senior developers who may be new to the project — provide full context, but don't over-explain. Document decisions and context, not obvious steps.

## Context
[4-5 sentences: what we're building and why]

## Source Materials
<!-- Summarized by sub-agents during research phase -->
| Source | Path | Summary |
|--------|------|---------|
| [name] | [absolute path] | [key points] |

## Project Standards
<!-- Discovered by sub-agents during research phase -->
- Developer guide: [path if exists]
- Documentation guide: [path if exists]
- Key conventions: [summarize]

## Tasks
| # | Task | Status | Files | Notes |
|---|------|--------|-------|-------|
| 1 | [description] | ⬜/🔄/✅ | [absolute paths] | [decisions, issues, solutions] |

## Documentation Tasks (REQUIRED)
<!-- Identified during research. Plan is NOT complete until all are ✅ -->
| # | Doc Task | Status | File | What to Document |
|---|----------|--------|------|------------------|
| D1 | [doc name] | ⬜ | [path] | [scope] |
| Dn | Inline code docs | ⬜ | [modified files] | JSDoc, comments |

## Key Decisions
- [Decision]: [Rationale] → [Impact]

## Reference
- Key files: [absolute paths]
- External docs: [links]

## Progress Log
| Date | Completed | Notes |
|------|-----------|-------|
```

### 2.3 Content Standards

- **Conciseness**: Senior engineers will use this. Document decisions and context, not obvious steps.
- **Absolute paths**: Always use full file paths, never descriptions like "the main config file"
- **New developer test**: Codebase + this plan = everything needed to continue from any point

---

## EXECUTION FLOW

```
1. Research      → Sub-agents gather context, findings go into plan
2. Create Plan   → Document all findings, tasks, and documentation needs
3. Implement     → Work tasks sequentially; use sub-agents for file reads
4. Update        → Update plan after EACH task completion
5. Test          → Validate implementation
6. Document      → Complete all documentation tasks (REQUIRED)
7. Done          → All tasks including docs are ✅
```

---

## WHY THIS WORKS

- **Two-thread model**: Sub-agents handle research/reading; main thread stays focused on active work
- **Living document**: Plan is both roadmap and progress tracker
- **Context-efficient**: Only essential information in main context window
- **Continuation-ready**: Any developer can pick up mid-project

---

Ask clarifying questions before creating the plan if requirements are unclear.
