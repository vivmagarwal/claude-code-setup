# Planning Teaching Topics - Guide for Claude

## Purpose
This guide defines how to create comprehensive teaching plans for topics before creating notebooks. The plan ensures structured, progressive learning using the back-and-forth teach-practice pattern.

## Core Philosophy: Adaptive Planning

**This is NOT a rigid template.** The number of instructor/learner activity pairs you create should be **determined by the topic's natural complexity**, not by following a fixed pattern.

- Simple topics (2 concepts) → 2 pairs
- Moderate topics (3-4 concepts) → 3-4 pairs
- Complex topics (5-7+ concepts) → 5-7+ pairs

**Your job**: Analyze the topic, count the discrete concepts, and create exactly that many pairs - no more, no less.

## When to Use This Guide
- User provides a topic or list of topics to teach
- Before creating any teaching notebooks
- When planning a curriculum or course structure
- When breaking down complex topics into teachable units

## Core Process

### 1. **Receive Topic(s)**
- Single topic: "List Comprehensions"
- Multiple topics: "Python Basics: Variables, Data Types, Control Flow, Functions"
- Complex topic: "Building RAG Systems with LangChain"

### 2. **Ultrathink & Assess Complexity**
**CRITICAL**: Before creating the plan, think deeply about:

**Conceptual Analysis:**
- What are the foundational concepts learners need?
- How do concepts build on each other?
- What's the natural progression from simple to complex?
- Where are common misconceptions or difficult concepts?
- What prerequisite knowledge is required?

**Complexity Assessment - Decide Activity Pairs Needed:**

Ask yourself: **How many distinct, teachable concepts does this topic contain?**

Each concept = 1 instructor/learner pair. Think in terms of conceptual units, not arbitrary numbers.

**Simple Topics** (2 instructor/learner pairs):
- Topic has 2 clear concepts
- Example: "Python String Methods" → (1) Basic methods like upper/lower/strip, (2) Advanced methods like split/join/replace
- Example: "Boolean Logic" → (1) Basic operators (and/or/not), (2) Complex conditions

**Moderate Topics** (3-4 pairs):
- Topic has 3-4 related concepts that build on each other
- Example: "List Comprehensions" → (1) Basic syntax, (2) Conditionals, (3) Complex data structures, (4) Nested comprehensions
- Example: "Functions" → (1) Definition & calling, (2) Parameters & return, (3) Scope, (4) Lambda functions

**Complex Topics** (5-7 pairs):
- Topic requires breaking into many smaller conceptual units
- Example: "Object-Oriented Programming" → (1) Classes & objects, (2) Attributes & methods, (3) Inheritance, (4) Polymorphism, (5) Encapsulation, (6) Class methods & static methods, (7) Magic methods
- Example: "Async Programming" → Multiple pairs covering fundamentals, async/await, concurrent operations, error handling, real-world patterns

**Rule of Thumb:**
- Count the discrete concepts, not lines of code
- Each pair should teach ONE core idea
- Don't artificially inflate or deflate the number
- **Be flexible** - if topic naturally needs 2 pairs, use 2; if it needs 6, use 6

### 3. **Create Plan Structure**

The plan MUST be saved in: `.project-management/teaching-plan-[TOPIC_NAME].md`

**Plan Template:**

```markdown
# Teaching Plan: [Topic Name]

## Overview
Brief description of what will be taught.

## Learning Objectives
By the end of this teaching series, learners will be able to:
- [Objective 1]
- [Objective 2]
- [Objective 3]
- [Objective 4]
- [Objective 5]

## Prerequisites
- [Prerequisite 1]
- [Prerequisite 2]

## Teaching Strategy

### Back-and-Forth Pattern
This plan uses the **teach-practice-teach-practice** pattern:
- Instructor demonstrates a concept with scaffolded examples
- Learner immediately practices that SAME concept
- Instructor introduces next concept building on previous
- Learner practices the new concept
- Pattern repeats until all concepts covered
- Final optional practice integrates all concepts

### Progressive Scaffolding
- **Within Activities**: Each activity contains multiple examples (simple → complex)
- **Across Activities**: Each activity builds on previous ones
- **Beginner-Friendly**: Start with basics, gradually increase complexity
- **Real-World Focus**: Connect every concept to real world software engineering

## Activity Breakdown

**IMPORTANT**: The number of activity pairs below should match your complexity assessment.
- Simple topic (2 concepts) = 2 instructor/learner pairs
- Moderate topic (3-4 concepts) = 3-4 pairs
- Complex topic (5-7 concepts) = 5-7 pairs

Create as many pairs as needed - no more, no less.

---

### Instructor Activity 1: [First Core Concept]
**Concept**: [What fundamental idea does this teach?]

**Examples to demonstrate** (2-5 examples, scaffolded simple→complex):
1. [Simplest example - isolated concept]
2. [Slightly more complex - adds one element]
3. [Realistic application]
[Add more examples if concept requires them]

**Key Points to Emphasize**:
- [Critical understanding 1]
- [Critical understanding 2]

**Real-World Connection**:
- [How this is used in actual software/AI systems]

---

### Learner Activity 1: [Practice First Core Concept]
**Practice Focus**: [SAME concept as Instructor Activity 1]

**Exercises** (2-4 exercises, scaffolded):
1. [Exercise directly practicing what was just demonstrated]
2. [Slightly harder exercise on same concept]
3. [Real-world context exercise]
[Add more if needed for thorough practice]

**Expected Difficulty**: [Easy/Medium]

---

### Instructor Activity 2: [Second Core Concept - builds on first]
**Concept**: [What new idea does this introduce?]

**Examples to demonstrate** (2-5 examples):
1. [New concept introduction]
2. [Combining with previous concept]
3. [Realistic application]

**Key Points to Emphasize**:
- [Critical understanding]

**Real-World Connection**:
- [How this builds on previous learning]

---

### Learner Activity 2: [Practice Second Core Concept]
**Practice Focus**: [SAME concept as Instructor Activity 2]

**Exercises** (2-4 exercises):
1. [Practice new concept]
2. [Combine with previous learning]

---

[CONTINUE THIS PATTERN FOR EACH CONCEPT IN YOUR TOPIC]

**For each additional concept, add:**
- Instructor Activity N: [Concept N]
- Learner Activity N: [Practice Concept N]

**Stop when you've covered all core concepts. Don't add filler activities.**

---

### Optional Extra Practice: [Integration of All Concepts]
**Purpose**: Challenge learners to integrate everything they've learned

**Challenge Problems** (3-5 problems):
1. [Multi-concept problem]
2. [Real-world AI scenario]
3. [RAG pipeline problem]
4. [Agentic AI application]

**Expected Difficulty**: [Medium/Hard]

## Implementation Notes

### Notebook Organization
- **Repository**: `[class_name]/notebooks/`
- **Notebook Name**: `[NN_topic_name].ipynb`
- **README**: Include Open in Colab badge

### Dependencies
```
pip install [list all required packages]
```

### Estimated Teaching Time
- Instructor Activities: [X minutes each]
- Learner Activities: [Y minutes each]
- Optional Practice: [Z minutes]
- **Total**: ~[Total minutes]

### Key Success Metrics
- [ ] Learners can independently solve basic problems after Activity 1
- [ ] Learners can combine concepts after Activity 2
- [ ] Learners can apply to AI/RAG scenarios after Activity 3
- [ ] Learners successfully complete optional challenges

## Notes for Notebook Creation
- Follow `teaching-with-colab.md` guide for notebook structure
- Each activity must have `##` header (collapsible)
- All solutions must be collapsed using `<details>` and `<summary>`
- Include "Why this works" explanations in every solution
- Execute and verify each cell before proceeding
- Connect to AI/RAG/Agentic AI applications throughout

## Revision History
- [Date]: Initial plan created
- [Date]: [Any revisions made]
```

## Workflow When Referenced

When a user asks to plan teaching for topics, follow these steps:

1. **Understand Scope**
   - Clarify the topic(s)
   - Identify target audience level
   - Understand time constraints (if any)

2. **Ultrathink the Structure** (Use Complexity Assessment Framework)
   - Break topic into discrete, teachable concepts
   - **Count the concepts** - this determines number of pairs
   - Determine logical progression between concepts
   - Identify dependencies between concepts
   - Plan real-world connections
   - **Be honest**: Does this topic need 2 pairs or 6? Don't force it into a template.

3. **Create the Plan File**
   - Save in `.project-management/teaching-plan-[topic-name].md`
   - Use the template above
   - Be specific about examples and exercises
   - Include timing estimates
   - Note prerequisites clearly

4. **Validate the Plan**
   - Does it follow back-and-forth pattern?
   - Is scaffolding clear within and across activities?
   - Are AI/RAG/Agentic connections meaningful?
   - Will learners be able to apply concepts after each pair?
   - Is optional practice truly integrative?

5. **Present to User**
   - Show the plan location
   - Highlight key learning progression
   - Ask for feedback before notebook creation
   - Confirm teaching approach aligns with goals

## Key Principles

- **Think Before You Build**: Planning prevents poorly structured notebooks
- **Progressive Complexity**: Each activity builds on previous, never jumps ahead
- **Immediate Practice**: Learners practice what was just taught, not later
- **Real-World Focus**: Every concept connects to AI/RAG/Agentic applications
- **Beginner-Friendly**: Assume minimal prior knowledge, build gradually
- **Scaffolding Everywhere**: Within examples, across activities, in complexity
- **Integration at End**: Optional practice combines all learned concepts

## Example Planning Sessions

### Example 1: Simple Topic (2 Pairs)

**User**: "Plan teaching for Python string formatting"

**Claude Ultrathink**:
String formatting has 2 main concepts:
1. Basic formatting (f-strings, .format(), %)
2. Advanced formatting (alignment, padding, number formatting)

This is a SIMPLE topic - just 2 pairs needed.

**Creates Plan**: `.project-management/teaching-plan-string-formatting.md`
- Activity 1: Basic string formatting methods
- Activity 2: Advanced formatting techniques
- Optional: Complex real-world formatting scenarios

### Example 2: Moderate Topic (3 Pairs)

**User**: "Plan teaching for Python list comprehensions"

**Claude Ultrathink**:
List comprehensions have 3 distinct concepts:
1. Basic syntax and transformations
2. Conditional filtering
3. Working with nested/complex structures

This is a MODERATE topic - 3 pairs needed.

**Creates Plan**: `.project-management/teaching-plan-list-comprehensions.md`
- Activity 1: Basic syntax and simple transformations
- Activity 2: Conditional filtering
- Activity 3: Complex data structures and nesting
- Optional: Multi-condition, nested, integrated problems

### Example 3: Complex Topic (6 Pairs)

**User**: "Plan teaching for Python decorators"

**Claude Ultrathink**:
Decorators are complex with 6 teachable concepts:
1. Function basics review (functions as first-class objects)
2. Simple decorators (basic wrapper pattern)
3. Decorators with arguments
4. Preserving metadata (@wraps)
5. Class decorators
6. Practical decorator patterns (caching, timing, logging)

This is a COMPLEX topic - 6 pairs needed.

**Creates Plan**: `.project-management/teaching-plan-decorators.md`
- Activity 1: Functions as first-class objects
- Activity 2: Simple decorator pattern
- Activity 3: Decorators with arguments
- Activity 4: Preserving function metadata
- Activity 5: Class decorators
- Activity 6: Practical decorator patterns
- Optional: Build custom decorators for real-world scenarios

**Key Takeaway**: Number of pairs = Number of discrete concepts, not a fixed template!

## Critical Reminders

- **Always ultrathink first** - don't rush to create plan
- **Assess complexity honestly** - count actual concepts, not arbitrary numbers
- **Be flexible with activity count** - 2 pairs for simple topics, 6+ for complex ones
- **Back-and-forth is mandatory** - every instructor activity needs corresponding learner activity
- **Scaffolding is non-negotiable** - must progress gradually
- **No filler activities** - only create pairs for genuine concepts
- **Plan before implementation** - the plan guides notebook creation
- **Optional practice at END only** - one section covering all concepts

## Flexibility Decision Framework

When planning, ask these questions:

**"How many distinct concepts?"**
- ✅ Each distinct concept = 1 pair
- ❌ Don't split one concept into multiple pairs just to hit a number
- ❌ Don't combine multiple concepts into one pair to keep it short

**"Can this concept stand alone?"**
- ✅ Yes = Deserves its own pair
- ❌ No = Combine with related concept

**"Will learners need practice on this specific concept?"**
- ✅ Yes = Create the instructor/learner pair
- ❌ No = It's a detail, not a core concept

**"Am I following a template or thinking about the topic?"**
- ✅ Thinking about the topic = Good
- ❌ Following a template = Bad

## Common Mistakes to Avoid

❌ **"List comprehensions always needs 3 pairs because the example shows 3"**
- ✅ Assess the actual topic - it might need 2 or 7

❌ **"I'll create 5 pairs because this seems complex"**
- ✅ Count the actual concepts first, then create that many pairs

❌ **"Simple topics should have at least 3 pairs to look substantial"**
- ✅ Simple topics with 2 clear concepts only need 2 pairs

❌ **"I'll split this concept into 2 activities to make more content"**
- ✅ One concept = one pair. Don't artificially inflate.

**Remember**: Quality over quantity. A well-structured 2-pair plan is better than a bloated 5-pair plan with artificial divisions.

## When Plan is Complete

After creating the plan and getting user approval:
1. Reference the `teaching-with-colab.md` guide
2. Create notebooks following the plan structure
3. Update plan with any changes made during implementation
4. Mark plan as "Implemented" with notebook location
