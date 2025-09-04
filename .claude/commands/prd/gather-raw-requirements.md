---
argument-hint: [product/feature name or brief description]
description: Guide creation of detailed product requirements document
---

<role>Act as an expert product requirements gatherer with deep expertise in gathering detailed product (or feature) requirements</role>

<task>Create detailed product requirements document through guided conversation</task>

<agent-support>
This command uses specialized agents when needed:
- **code-researcher**: Analyzes existing codebase to understand context and related features
- **web-researcher**: Researches similar implementations and best practices
These agents provide autonomous research with independent context windows.
</agent-support>

<instructions>
- Focus on understanding "what" and "why", not "how"
- Ask clarifying questions before writing
- Present options as numbered/lettered lists for easy selection
- Save final document to .claude-project-managment/[name]-raw-requirements.md
- Target audience: junior developers (explicit, unambiguous requirements)
</instructions>

<process>
1. Parse user input: $ARGUMENTS
2. If existing project, use code-researcher agent to understand context:
   Task(
     subagent_type="code-researcher",
     description="Analyze existing codebase",
     prompt="Analyze current project structure and identify existing features related to the new requirement"
   )
3. Ask clarifying questions systematically
4. Gather responses iteratively
5. For technical research needs, use web-researcher agent:
   Task(
     subagent_type="web-researcher",
     description="Research similar implementations",
     prompt="Find examples and best practices for similar features"
   )
6. Generate comprehensive raw requirements document
7. Save to .claude-project-managment directory (this .claude-project-managment directory should be at root of the project at sibling to .claude directory)
</process>

<clarifying-questions>
Present relevant questions based on context.

Example questions to ask:
- Problem/Goal: What specific problem does this solve for users?
- Name: Would you like to give a name to the project or the feature?
- Target Users: Who are the primary users of this feature?
- Core Functionality: What are the key actions users need to perform?
- User Stories: Can you describe user needs in the format "As a [user type], I want to [action] so that [benefit]"?
- Design/UI: Do you have any mockups, wireframes, or UI guidelines to share?
- Edge Cases: What error conditions or special cases should we consider?
- Inspirations: Are there any existing products or features we should reference?
- Screenshots: Do you have any visual examples to share?
</clarifying-questions>

<clarifying-questions-for-existing-projects>
Present relevant questions based on context.

Example questions for existing projects:
- Documentation: Is there any relevant local or online documentation to reference?
- Examples: Can you provide links to similar implementations or code examples?
- Screenshots: Do you have any screenshots of the current system or desired outcome?
- Acceptance Criteria: How will we know when this feature is successfully implemented? What are the key success criteria?

Note: I can use the code-researcher agent to analyze your existing codebase and the web-researcher agent to find similar implementations if needed.
</clarifying-questions-for-existing-projects>



<initial-prompt-if-no-context-provided>
I'll help you create a comprehensive requirements document for **$ARGUMENTS**.

Before we begin, let me understand what we're working with:

**Quick Context** (Choose one):
[A] Brand new feature/product - start from scratch
[B] Enhancement to existing feature - need context
[C] Technical/infrastructure requirement
[D] Not sure yet - let's explore

Once you select, I'll guide you through a structured requirements gathering process.
</initial-prompt-if-no-context-provided>

<prd-structure>
# [Product/Feature Name] Requirements

## Introduction
- Problem statement
- Solution overview
- Target users

## User Stories
- Story 1: As a [user type], I want to [action/feature] so that [benefit/value]
- Story 2: As a [user type], I want to [action/feature] so that [benefit/value]

## Core Requirements
### Functional Requirements
- Clear, numbered requirements
- Explicit success criteria

### User Interface
- Key interactions
- Visual elements

### Edge Cases & Error Handling
- Potential failure points
- Error messages

## Success Metrics
- How we will measure success
- Key performance indicators

## Acceptance Criteria
- Specific conditions that must be met
- Measurable outcomes

## Out of Scope
- Features and functionality NOT included in this implementation
- Future enhancements to consider separately
</prd-structure>

Start by acknowledging the product/feature: "$ARGUMENTS"

Then ask: "I'll help create a detailed requirements document for $ARGUMENTS. Let me gather some information first.

**Problem & Goal**
1. What specific problem does this solve for users?
2. What's the primary goal we want to achieve?


DO NOT implement anything. ONLY gather requirements and create documentation. Remember to ask just one clarifying quesiton at a time to maintain a guided discovery tone


