# Claude Prompting Guide

## Core Principles

### Be Clear and Direct
- Use precise, straightforward language
- Avoid ambiguous instructions
- State exactly what you want

### Structure Matters
- XML tags for clarity: `<instructions>`, `<example>`, `<data>`
- Separate context from task
- Use consistent formatting

### Less is More
- Remove unnecessary words
- Focus on essential information
- Keep prompts actionable

## Fundamental Techniques

### 1. Role Prompting (System Prompts)
Give Claude a specific professional role for enhanced accuracy.

```python
system="You are a seasoned data scientist at a Fortune 500 company."
```

**Example:**
```
System: You are a senior security engineer specializing in web application security.

User: Review this authentication code for vulnerabilities.
```

**Impact:** Transforms generic responses into expert-level analysis.

### 2. Multishot Prompting (3-5 Examples)
Show Claude the exact pattern you want.

```xml
<examples>
<example>
Input: "The product exceeded expectations"
Output: POSITIVE - Product Quality
</example>

<example>
Input: "Shipping took forever"
Output: NEGATIVE - Delivery
</example>

<example>
Input: "Great value for money"
Output: POSITIVE - Pricing
</example>
</examples>

Now categorize: "Customer service was unhelpful"
```

### 3. Chain of Thought (CoT)
Let Claude work through problems step-by-step.

**Basic:**
```
Solve this problem. Think step-by-step.
```

**Structured:**
```xml
<thinking>
1. Break down the requirements
2. Analyze each component
3. Consider edge cases
</thinking>

<answer>
[Final solution here]
</answer>
```

### 4. XML Tags for Structure
Organize complex prompts clearly.

```xml
<task>Build a REST API endpoint</task>

<requirements>
- Accept JSON payload
- Validate email format
- Return 201 on success
</requirements>

<constraints>
- Use Express.js
- Include error handling
</constraints>
```

### 5. Prefilling Responses
Control output format from the start.

**Force JSON output:**
```
Assistant: {
```

**Skip preambles:**
```
Assistant: The solution is:
```

## Advanced Patterns

### Complex Task Decomposition
```xml
<objective>Refactor legacy authentication system</objective>

<current_state>
- Basic password storage
- No rate limiting
- Session tokens in cookies
</current_state>

<target_state>
- Bcrypt password hashing
- Rate limiting with Redis
- JWT tokens
</target_state>

<steps>
1. Audit current implementation
2. Design migration strategy
3. Implement incrementally
4. Test thoroughly
</steps>
```

### Conditional Logic
```
If the code uses TypeScript:
  - Add proper type annotations
  - Use interfaces for objects
  - Enable strict mode

Otherwise:
  - Add JSDoc comments
  - Use PropTypes for validation
```

## Claude Code Specific

### Custom Slash Commands
Create in `.claude/commands/commit.md`:

```markdown
---
allowed-tools: Bash(git add:*), Bash(git status:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---

Stage all changes and commit with message: $ARGUMENTS
```

Usage: `/commit Fix authentication bug`

### Subagents
Create specialized assistants in `.claude/agents/code-reviewer.md`:

```markdown
---
name: code-reviewer
description: Reviews code for quality, security, and maintainability
tools: Read, Grep, Glob, Bash
---

You are a senior code reviewer ensuring high standards.

Review checklist:
- Code simplicity
- Proper error handling
- No exposed secrets
- Input validation
- Performance considerations

Provide feedback by priority:
1. Critical issues (must fix)
2. Warnings (should fix)
3. Suggestions (consider)
```

### Effective Task Instructions
```
Build a user authentication feature:
1. Create registration endpoint
2. Add password validation (min 8 chars, 1 number, 1 special)
3. Implement JWT token generation
4. Add rate limiting (5 attempts per minute)
5. Write unit tests
6. Update API documentation
```

## Common Patterns

### Bug Fixing
```
Error: "TypeError: Cannot read property 'id' of undefined" in UserService.js:45

1. Locate the error source
2. Identify the root cause
3. Fix with proper null checking
4. Add defensive programming
5. Test the fix
```

### Code Generation
```
Create a React component:
- Name: UserProfile
- Props: userId (string), showEmail (boolean)
- Fetch user data on mount
- Handle loading and error states
- Use existing design system components
```

### Refactoring
```
Refactor calculatePrice() function:
- Current issues: 200 lines, nested conditionals, magic numbers
- Goals: Extract methods, add constants, improve readability
- Maintain all existing functionality
- Add unit tests for each extracted method
```

## Quick Reference

### Do's
- Use bullet points for lists
- Number sequential steps
- Include specific constraints
- Provide success criteria
- Give concrete examples

### Don'ts
- Write verbose explanations
- Use flowery language
- Leave requirements ambiguous
- Mix instructions with context
- Forget edge cases
- Use emojis

### Power Tips
1. **Test your prompts:** Start simple, add complexity
2. **Iterate quickly:** Refine based on outputs
3. **Be specific:** "Fix bugs" vs "Fix null pointer exception in login handler"
4. **Use examples:** Show don't just tell
5. **Structure complex tasks:** Break into clear phases

## Example: Complete Feature Request

```xml
<task>Add dark mode to settings page</task>

<requirements>
- Toggle switch in preferences
- Save preference to localStorage
- Apply theme on page load
- Smooth transition animation
</requirements>

<technical_specs>
- CSS variables for colors
- React Context for state
- No external libraries
</technical_specs>

<success_criteria>
- Toggle works instantly
- Preference persists on refresh
- All components respect theme
- Accessibility maintained
</success_criteria>

Think through the implementation step-by-step, then build it.
```

## Troubleshooting

### Vague Outputs
**Problem:** Claude gives generic responses
**Solution:** Add role + specific examples

### Wrong Format
**Problem:** Output doesn't match expectations
**Solution:** Use prefilling or structured examples

### Missing Steps
**Problem:** Claude skips important parts
**Solution:** Use numbered lists or XML sections

### Too Verbose
**Problem:** Unnecessarily long responses
**Solution:** Add "Be concise" or "No explanation needed"

## Quick Templates

### Code Review
```
Review [file] for:
- Security vulnerabilities
- Performance issues
- Code smells
Priority: security > performance > style
```

### Debugging
```
Bug: [description]
Error: [exact message]
File: [location]
Expected: [behavior]
Actual: [behavior]
Find and fix the root cause.
```

### Documentation
```
Document this function:
- Purpose (one line)
- Parameters with types
- Return value
- Example usage
- Edge cases
```

## Prompting Principles Summary

### The Essentials
1. **Clarity over cleverness** - Direct instructions beat elaborate descriptions
2. **Structure over prose** - Bullets, numbers, and sections beat paragraphs  
3. **Examples over explanations** - Show the pattern you want
4. **Constraints guide creativity** - Specific boundaries produce better results
5. **Iteration beats perfection** - Start simple, refine based on outputs

### Writing Style
- **Minimal markdown** - Use only when it adds clarity
- **No fluff** - Every word should serve a purpose
- **Action-oriented** - Use imperative mood ("Create", "Fix", "Analyze")
- **Complete yet concise** - Include all necessary details, nothing more

### Structure Hierarchy
1. Simple tasks → Direct instruction
2. Multi-step tasks → Numbered list
3. Complex tasks → XML sections
4. Domain expertise needed → Role + examples
5. Specific format required → Prefill or template

### The Anti-Pattern List
- Verbose introductions
- Redundant instructions  
- Mixing context with commands
- Vague success criteria
- Unnecessary complications
- Decorative language

Remember: Clear & concise prompts = Better outputs. Test, iterate, refine.