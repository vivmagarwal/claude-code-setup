---
name: create-engineering-plan
description: Convert product requirements into actionable engineering plan
argument-hint: <requirements-file-path> [optional: specific-features]
---

<task>Create engineering plan from product requirements</task>

<objective>
Transform requirements into actionable plan that:
- Breaks down into ordered user stories and tasks (logical development sequence)
- Guides junior developers with complete context (codebase + this doc only)
- Updates after each task completion (active document)
- Tracks progress via YAML status (project management & tracking tool)
</objective>

<agent-usage>
This command leverages specialized agents for efficiency:
- **code-researcher**: Deep codebase analysis and understanding
- **web-researcher**: Technical documentation and best practices research
These agents work autonomously with their own context windows for better performance.
</agent-usage>

<process>
  <step_1_analyze>
    • Read requirements: $ARGUMENTS
    • Extract ALL stories/features (miss nothing)
    • Ask clarifying questions immediately
    • Identify all files needing changes
    • Think hardest - be thorough
  </step_1_analyze>

  <step_2_context>
    • Use Task tool with code-researcher agent for deep codebase analysis:
      Task(
        subagent_type="code-researcher",
        description="Analyze codebase structure",
        prompt="Provide comprehensive codebase analysis: structure, architecture patterns, dependencies, key components"
      )
    • Extract architecture patterns from analysis
    • Map component relationships
  </step_2_context>

  <step_3_research>
    • Use Task tool with web-researcher agent for technical research:
      Task(
        subagent_type="web-researcher",
        description="Research technologies and best practices",
        prompt="Research framework documentation, best practices, and patterns for technologies identified in the project. Focus on official docs and current industry standards."
      )
    • Note: The web-researcher agent will automatically:
      - Use Context7 MCP for framework documentation
      - Use WebFetch for specific URLs and GitHub
      - Use chrome-devtools MCP for dynamic sites
      - Prioritize official sources and recent information
  </step_3_research>

  <step_4_design>
    • Choose simple, robust solutions
    • Document architectural decisions
    • Order tasks by dependencies
  </step_4_design>

  <step_5_output>
    • Generate plan using structure below
    • Save as: {feature}-engineering-plan.md
  </step_5_output>
</process>

<structure>

# {Feature} Engineering Plan

## Usage
1. Read at session start
2. Update status after EACH task
3. Document discoveries inline
4. Keep sections current

## Workflow
1. Verify previous story = `completed`
2. Check ALL pre_implementation flags = `true` (never skip)
3. Execute task by task systematically
4. Update `task_notes` with context (critical - only source of truth)
5. Ensure working app after EVERY step

## Recommended MCP Servers
- **chrome-devtools**: Verify UI changes
- **Context7**: Get library docs

## Rules
- NO legacy fallback (unless explicit)
- NO backwards compatibility (unless explicit)
- Simple, robust, reiable, maintainable code
- After EACH feature: compile → test → verify
- Test external behavior (API calls, tools executed, results returned)
- Remove ALL mocks/simulations before completion
- Ask clarifying questions upfront
- Identify files to change per task

## Project Overview
[One paragraph summary]

## Story Breakdown and Status

```yaml
stories:
  - story_id: "STORY-001"
    story_title: "[Feature name]"
    story_description: "[User value]"
    story_pre_implementation:
      requirements_understood: false
      context_gathered: false
      plan_read: false
      architecture_documented: false
      environment_ready: false
      tests_defined: false
    story_post_implementation:
      all_tasks_completed: false
      feature_working: false
      plan_updated: false
    story_implementation_status: "not_started"  # not_started | in_progress | completed
    tasks:
      - task_id: "TASK-001.1"
        task_title: "[Specific action]"
        task_description: "[What and why]"
        task_acceptance_criteria:
          - "[Measurable outcome]"
        task_pre_implementation:
          previous_task_done: true
        task_ready_to_complete:
          criteria_met: false
          code_working: false
          tests_passing: false
          integration_tested: false
          plan_updated: false
        task_implementation_status: "not_started"  # not_started | in_progress | testing | completed
        task_implementation_notes: "[Critical context for next developer - codebase + this doc are only sources]"
```

## Architecture Decisions

**Decision 1**: [Choice]
- Reasoning: [Why]
- Impact: [What]

**Decision 2:** [Choice]
- Reasoning: [Why]
- Impact: [What]

## Commands

```bash
# Setup
[install command]

# Development
[run command]
[test command]
[lint command]

# Build
[build command]
```

## Standards
- [Code style rules]
- [Naming conventions]
- [File organization]

## Git Flow
- Branch: feature/{story-id}
- Commit: "TASK-{id}: {description}"
- PR after story complete

## Documentation
- [API docs URL]
- [Framework guide]
- [Internal wiki]

## Config Files
- package.json: [purpose]
- .env.example: [variables]
- tsconfig.json: [settings]

## Directory Structure
```
src/
├── components/
├── services/
└── utils/
```

</structure>

<output_checklist>
☐ All stories extracted from requirements
☐ Tasks ordered by dependencies
☐ Every task has clear acceptance criteria
☐ Commands are complete and tested
☐ File changes identified per task
☐ Junior developer can execute independently 
</output_checklist>