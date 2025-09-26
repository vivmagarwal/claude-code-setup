---
name: create-teaching-plan
description: Transform project into 10-step teaching journey for beginners with backend-first approach
argument-hint: [project-path or leave blank for current project]
---

<task>Generate complete progressive teaching plan with backend-first approach for fullstack projects</task>

<objective>
Transform complex codebase into step-by-step learning experience that:
- Rebuilds project through 10 incremental, testable steps
- Completes and tests entire backend API first (steps 1-5) for fullstack projects
- Teaches absolute beginners with no framework knowledge
- Tracks progress via YAML status (living document)
- Clears context after each step for focused execution
- Documents file changes for next-step context
- Works after EVERY step (no broken states)
</objective>

<context-management-protocol>
CRITICAL: After completing each step/task:
1. Update all documentation with file changes
2. Mark task as complete in YAML status
3. Save all work and commit if needed
4. Tell user to execute: `/clear` command
5. New session loads: CLAUDE.md + TEACHING-PLAN.md + current step context
6. Continue with fresh context window

Best practices for context clearing:
- Use `/clear` for complete context reset
- Use `/compact` for reducing history while keeping key context
- Always document critical discoveries before clearing
</context-management-protocol>

<agent-architecture>
This command leverages specialized agents:
- **code-researcher**: Deep codebase analysis and pattern extraction
- **web-researcher**: Framework documentation and best practices
These agents operate with independent context windows for optimal performance.
</agent-architecture>

<workflow>
  <phase_1_discovery>
    COMPLETE CODEBASE ANALYSIS:
    Task(
      subagent_type="code-researcher",
      description="Comprehensive codebase analysis",
      prompt="Analyze entire codebase: Identify if fullstack, backend-only, or frontend-only. Document all API endpoints, data models, services, frontend components. Extract dependencies, architecture patterns, data flows. Determine optimal teaching progression. Miss nothing."
    )

    Document in .project-management/TEACHING-CONTEXT.yaml
  </phase_1_discovery>

  <phase_2_research>
    TECHNICAL RESEARCH:
    Task(
      subagent_type="web-researcher",
      description="Research frameworks and patterns",
      prompt="Research official documentation for all identified technologies. Find current best practices, API testing methods, common patterns. Focus on backend-first development approach for fullstack apps."
    )
  </phase_2_research>

  <phase_3_verification>
    CODE EXECUTION AND LIVE TESTING:
    - Set up development environment
    - For fullstack: Test backend API endpoints first using curl/httpie
    - Verify all backend functionality independently
    - Only then test frontend integration
    - Use Playwright MCP for frontend testing
    - Document setup quirks
  </phase_3_verification>

  <phase_4_plan_generation>
    Generate: .project-management/TEACHING-PLAN.md
    WITH ALL 10 STEPS DEFINED UPFRONT
  </phase_4_plan_generation>

  <phase_5_testing>
    BACKEND-FIRST TESTING:
    - Create API test suite for backend steps
    - Use curl/httpie/pytest for API testing
    - Playwright MCP only for frontend steps
    - Verify functionality at each layer
  </phase_5_testing>

  <phase_6_documentation>
    Generate complete PROJECT-README.md
  </phase_6_documentation>
</workflow>

<fullstack-teaching-progression>
For fullstack projects, ALWAYS follow this progression:

## Backend Phase (Steps 1-5)
Step 1: Project Setup & Basic API Structure
Step 2: Database Models & Migrations
Step 3: Core API Endpoints (CRUD)
Step 4: Authentication & Authorization
Step 5: Advanced Features & External Integrations

## Frontend Phase (Steps 6-10)
Step 6: Frontend Setup & First Page
Step 7: API Integration & State Management
Step 8: Core UI Components
Step 9: Advanced Features & UX
Step 10: Testing & Optimization

For backend-only or frontend-only projects, adapt accordingly.
</fullstack-teaching-progression>

<teaching-plan-structure>

# Project Teaching Plan

## Context Management Protocol
**CRITICAL: Follow this protocol after EVERY step completion:**
1. Update FILES_CHANGED.yaml with all modifications
2. Update TEACHING-PLAN.md with completion status
3. Document critical discoveries in implementation_notes
4. Instruct user to execute `/clear` command
5. Next session loads: CLAUDE.md + TEACHING-PLAN.md + next step context

## Usage Instructions
1. Read TEACHING-PLAN.md at every session start
2. Check FILES_CHANGED.yaml for recent modifications
3. Update YAML status after EACH step completion
4. Clear context with `/clear` after each step
5. This document + codebase = complete learning resource

## Target Audience
- Absolute beginners with basic programming knowledge
- No framework-specific experience required
- Learning by building, not just reading

## Teaching Philosophy
- Backend-first for fullstack projects (complete API before UI)
- One concept per step
- Working application after every step
- Test at the layer of interaction (API tests for backend, UI tests for frontend)
- Document the "why" not just "how"

## All Teaching Steps (Complete Overview)

### Backend Phase
- **Step 1**: Project Setup & Basic API Structure
- **Step 2**: Database Models & Migrations
- **Step 3**: Core API Endpoints (CRUD)
- **Step 4**: Authentication & Authorization
- **Step 5**: Advanced Features & External Integrations

### Frontend Phase
- **Step 6**: Frontend Setup & First Page
- **Step 7**: API Integration & State Management
- **Step 8**: Core UI Components
- **Step 9**: Advanced Features & UX
- **Step 10**: Testing & Optimization

## Progress Tracking

```yaml
teaching_progress:
  current_step: 1
  total_steps: 10
  last_updated: ""
  context_cleared_count: 0

steps:
  - step_id: "STEP-001"
    title: "Project Setup & Basic API Structure"
    phase: "backend"
    description: "Create project structure and basic API with health check"

    pre_implementation:
      previous_step_complete: true
      environment_ready: false
      concepts_explained: false
      context_loaded: false

    learning_objectives:
      - objective: "Understand project structure"
        achieved: false
      - objective: "Set up development environment"
        achieved: false
      - objective: "Create basic API endpoint"
        achieved: false

    implementation_checklist:
      files_created: false
      dependencies_installed: false
      code_written: false
      api_tested: false
      documentation_updated: false

    files_changed:
      created: []
      modified: []
      deleted: []

    post_implementation:
      app_working: false
      tests_passing: false
      concepts_understood: false
      ready_for_next: false
      context_cleared: false

    implementation_status: "not_started"

    implementation_notes: |
      [Critical discoveries and context for next session]

    api_test_commands: |
      [Exact curl/httpie commands to test this step's endpoints]

    learner_feedback: |
      [Common issues encountered and solutions]
```

## Step Definitions

### Step 1: Project Setup & Basic API Structure (Backend)
**Starting Code**: Empty directory
**Ending Code**: Basic API with health check endpoint

<lesson>
#### Why This Step Matters
Every backend starts with a foundation. We're building the minimal API structure needed to verify our server works.

#### What You'll Build
1. Project directory structure
2. Virtual environment setup
3. Basic FastAPI/Express application
4. Health check endpoint

#### Implementation Guide
[Detailed step-by-step instructions with explanations]

#### API Testing Commands
```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "..."}

# Alternative with httpie:
http GET localhost:8000/health
```

#### Files Changed in This Step
```yaml
files_changed:
  created:
    - app/main.py
    - app/__init__.py
    - requirements.txt
    - .env.example
  modified: []
  deleted: []
```

#### Context for Next Step
- Server running on port 8000
- Basic project structure established
- Ready to add database models

#### Before Moving to Step 2
1. Verify all tests pass
2. Update TEACHING-PLAN.md status
3. Document any discoveries
4. Execute `/clear` command
5. Load Step 2 context
</lesson>

### Steps 2-10
[Similar structure for each step with backend/frontend specific content]

## Files Change Tracking

```yaml
# FILES_CHANGED.yaml
# Living document tracking all file modifications

step_001:
  created:
    - app/main.py: "Entry point for FastAPI application"
    - app/__init__.py: "Package initializer"
    - requirements.txt: "Python dependencies"
  modified: []
  deleted: []

step_002:
  created:
    - app/models.py: "SQLAlchemy models"
    - app/database.py: "Database connection"
  modified:
    - app/main.py: "Added database initialization"
  deleted: []

# Continue for all steps...
```

## Backend API Testing Framework

### Testing Protocol for Backend Steps (1-5)

```bash
# Step 1: Health Check
curl http://localhost:8000/health

# Step 2: Database Connection
python -c "from app.database import test_connection; test_connection()"

# Step 3: CRUD Operations
# Create
curl -X POST http://localhost:8000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "Test"}'

# Read
curl http://localhost:8000/api/items

# Update
curl -X PUT http://localhost:8000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated Item"}'

# Delete
curl -X DELETE http://localhost:8000/api/items/1

# Step 4: Authentication
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secure123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "secure123"}'

# Protected endpoint
curl http://localhost:8000/api/protected \
  -H "Authorization: Bearer <token>"

# Step 5: Advanced Features
# File upload
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test.pdf"

# External API integration
curl http://localhost:8000/api/external/weather?city=London
```

## Frontend Testing Framework (Steps 6-10)

### Playwright MCP Testing Protocol

```javascript
// Only used for frontend steps (6-10)

// Step 6: Frontend Setup
await browser_navigate({ url: "http://localhost:3000" });
await browser_wait_for({ text: "Welcome" });

// Step 7: API Integration
await browser_fill_form({
  fields: [{
    name: "API URL",
    ref: "input[name='apiUrl']",
    type: "textbox",
    value: "http://localhost:8000"
  }]
});

// Continue for remaining frontend steps...
```

## Context Management Best Practices

### What Goes in CLAUDE.md (Persistent Context)
- Critical architectural decisions
- Testing protocols
- Common issue resolutions
- Project-specific conventions
- Update protocols

### What Goes in TEACHING-PLAN.md (Living Document)
- Current progress status
- Step definitions and objectives
- File change history
- Implementation notes
- Next step context

### Context Clearing Workflow
```
Step N Complete → Update Docs → `/clear` → Load Step N+1 Context
```

## Emergency Recovery
If something breaks:
1. Check FILES_CHANGED.yaml for recent modifications
2. Verify step_{n-1} end code
3. Check implementation_notes for known issues
4. Clear context and reload with specific step focus

## Continuous Update Protocol
After EVERY step completion:
1. Update step YAML status
2. Update FILES_CHANGED.yaml
3. Add implementation_notes with discoveries
4. Test at appropriate layer (API for backend, UI for frontend)
5. Clear context with `/clear` before next step
6. Commit changes with message: "STEP-{id}: {description}"

## Project Standards

### Code Style
- Use consistent indentation
- Follow framework conventions
- Comment complex logic
- Keep functions focused

### Testing Standards
- Backend: Test APIs as external consumers would
- Frontend: Test UI as users would interact
- No mocks for teaching - real implementations only

### Documentation Standards
- Every file change must be documented
- Every discovery must be noted
- Every issue must have a resolution

</teaching-plan-structure>

<output-structure>
```
.project-management/
├── TEACHING-PLAN.md          # Master plan with live status (ALL STEPS DEFINED)
├── TEACHING-CONTEXT.yaml     # Codebase analysis and progress
├── FILES_CHANGED.yaml        # Complete file modification history
├── PROJECT-README.md         # Complete project documentation
├── steps/
│   ├── step-001/
│   │   ├── start-code/       # Complete starting point
│   │   ├── end-code/         # Complete ending point
│   │   ├── lesson.md         # Detailed teaching content
│   │   ├── api-tests.md      # API test commands (backend steps)
│   │   └── changes.diff      # What changed in this step
│   └── [steps 2-10...]/
├── testing-framework/
│   ├── backend-tests/        # API test scripts
│   └── frontend-tests/       # Playwright test scripts
└── progress-reports/
    └── [timestamp]-status.yaml
```
</output-structure>

<validation-rules>
Before marking ANY step complete:
☐ Previous step's end-code works perfectly
☐ For backend: All API endpoints tested with curl/httpie
☐ For frontend: UI tested with Playwright MCP
☐ FILES_CHANGED.yaml updated with all modifications
☐ Implementation notes document critical context
☐ YAML status reflects current state
☐ Context ready to be cleared
☐ Junior developer could continue from this point
</validation-rules>

<critical-reminders>
- TEACHING-PLAN.md must show ALL 10 STEPS from the start
- Backend MUST be complete and tested before frontend
- Clear context with `/clear` after EACH step
- Document EVERY file change for next-step context
- This is a LIVING DOCUMENT - update continuously
- Test at the appropriate layer (API vs UI)
- The plan + codebase = complete learning resource
</critical-reminders>

<execution-notes>
- Use <thinking> tags to plan analysis approach
- Complete backend API before any frontend work
- Test APIs as the external world would use them
- Document file changes immediately after making them
- Clear context to maintain focus and performance
- Update status in real-time, not batch updates
</execution-notes>

<output-checklist>
☐ ALL 10 steps defined upfront in TEACHING-PLAN.md
☐ Backend completed and tested first (for fullstack)
☐ FILES_CHANGED.yaml tracking all modifications
☐ Context clearing protocol documented
☐ API test commands provided for backend steps
☐ Playwright tests provided for frontend steps
☐ YAML tracking structure in place
☐ Living documentation approach implemented
☐ Junior developer can execute independently
☐ Emergency recovery procedures included
</output-checklist>