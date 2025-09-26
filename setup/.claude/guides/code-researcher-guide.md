# Code Researcher Agent - Quick Reference Guide

## When to Use Code Researcher

The `code-researcher` agent is your go-to specialist for deep codebase analysis. Use it when you need to:

- 🗺️ **Map an entire codebase** - Understand structure and architecture
- 🔍 **Find specific implementations** - Locate features and understand how they work
- 🐛 **Debug issues** - Root cause analysis and call chain tracing
- ❓ **Answer questions** - Get detailed answers about code behavior
- 📦 **Extract context** - Generate focused context for specific tasks

## Usage Examples

### Example 1: Understand Entire Codebase
```python
Task(
    subagent_type="code-researcher",
    description="Analyze codebase structure",
    prompt="""
    Provide comprehensive analysis of this codebase:
    - Overall architecture and structure
    - Technology stack and dependencies
    - Key components and their relationships
    - Entry points and main flows
    - Testing setup
    """
)
```

### Example 2: Find Feature Implementation
```python
Task(
    subagent_type="code-researcher",
    description="Find authentication implementation",
    prompt="""
    Research the authentication feature:
    - Where is login/logout implemented?
    - How are tokens handled?
    - What middleware/guards are used?
    - How is user state managed?
    Include file:line references
    """
)
```

### Example 3: Debug an Issue
```python
Task(
    subagent_type="code-researcher",
    description="Debug TypeError",
    prompt="""
    Investigate error: "TypeError: Cannot read property 'map' of undefined"
    - Find where error occurs
    - Trace the call chain
    - Identify root cause
    - Suggest fix with code
    """
)
```

### Example 4: Answer Specific Question
```python
Task(
    subagent_type="code-researcher",
    description="How does caching work",
    prompt="""
    How is caching implemented in this codebase?
    - What caching strategy is used?
    - Where is cache configured?
    - What gets cached and for how long?
    - How is cache invalidation handled?
    """
)
```

### Example 5: Extract Context for Task
```python
Task(
    subagent_type="code-researcher",
    description="Context for adding dark mode",
    prompt="""
    Extract all relevant context for implementing dark mode:
    - Current theme/styling setup
    - Component structure
    - State management for preferences
    - CSS/styling approach
    - Similar features already implemented
    Focus only on what's needed for this task
    """
)
```

## Key Capabilities

### 1. Multi-Level Analysis
- **File Level**: Structure, organization, dependencies
- **Code Level**: Functions, classes, implementations
- **Logic Level**: Data flow, call chains, algorithms
- **System Level**: Architecture, patterns, integrations

### 2. Smart Search Strategies
- Import/dependency tracing
- Pattern-based searching
- AST-aware analysis
- Cross-reference validation

### 3. Context Management
- Starts narrow, expands as needed
- Follows code structure naturally
- Preserves only relevant information
- Summarizes aggressively

### 4. Output Formats
- Comprehensive overviews
- Feature deep-dives
- Issue investigations
- Targeted context extraction

## What Makes It Different

Unlike simple search tools, code-researcher:
- **Understands code relationships** - Not just text matching
- **Follows execution flow** - Traces through call chains
- **Builds dependency graphs** - Maps interconnections
- **Provides actionable insights** - Not just raw results

## Integration with Main Workflow

```python
# Typical workflow
1. Use code-researcher to understand existing code
2. Get targeted context for your task
3. Implement changes with full understanding
4. Use code-researcher to verify impact

# Example
research = Task(
    subagent_type="code-researcher",
    description="Understand payment system",
    prompt="Full analysis of payment processing..."
)
# Then implement new payment method with complete context
```

## Tips for Best Results

### Be Specific About Needs
```python
# Good
"Find all API endpoints related to user management with their middleware"

# Too vague  
"Tell me about the API"
```

### Request Appropriate Detail Level
```python
# For overview
"High-level architecture and main components"

# For implementation
"Detailed code flow with line numbers for checkout process"
```

### Use for Complex Tasks
```python
# Perfect use cases:
- Refactoring large features
- Understanding legacy code
- Debugging complex issues
- Onboarding to new codebase

# Not needed for:
- Reading single file (use Read)
- Simple searches (use Grep)
- File listing (use LS)
```

## Expected Outputs

The agent provides structured reports with:
- 📁 **File references** - Exact locations (file:line)
- 🔗 **Relationships** - How components connect
- 💻 **Code snippets** - Relevant implementations
- 📊 **Visualizations** - Structure diagrams when helpful
- 💡 **Insights** - Patterns and recommendations
- ⚡ **Action items** - Next steps or fixes

## Performance Notes

- Works efficiently on codebases up to 100k+ files
- Intelligently filters irrelevant files (node_modules, builds)
- Uses parallel search for speed
- Caches findings within session

## Common Patterns

### Onboarding Pattern
```
1. Overall structure analysis
2. Identify key components
3. Understand main flows
4. Deep dive into specific areas
```

### Debugging Pattern
```
1. Find error location
2. Trace execution path
3. Identify data flow
4. Pinpoint root cause
```

### Feature Pattern
```
1. Search for feature keywords
2. Map all related files
3. Understand implementation
4. Document dependencies
```

Remember: code-researcher handles the complexity of codebase analysis so you can focus on understanding and building.