# Teaching with Google Colab - Guide for Claude

## Purpose
This guide defines the structure and workflow for creating educational Colab notebooks that help learners understand programming concepts through hands-on practice.

## Core Principles

### 1. Notebook Structure
Each topic follows this exact sequence:
1. **Text Cell**: Lesson explanation (collapsible with `#` or `##`)
2. **Code Cell(s)**: Instructor demonstration with solution collapsed below
3. **Code Cell(s)**: Learner in-class activity with solution collapsed below
4. **Code Cell(s)**: Optional extra practice with solution collapsed below

### 2. Text Cell Format
- Start each section/topic with `#` for main topics or `##` for subtopics (makes them collapsible)
- Write beginner-friendly explanations that are accurate and clear
- Keep explanations concise but complete

### 3. Code Cell Guidelines

#### Instructor Activity
- Clearly define the problem/task
- State expected outcomes explicitly
- Include comprehensive inline comments
- Place solution in collapsed markdown cell immediately below using:
  ```markdown
  <details>
  <summary>Solution</summary>

  \`\`\`python
  # Solution code here
  \`\`\`

  </details>
  ```

#### Learner In-Class Activity
- Same structure as instructor activity
- Appropriate difficulty for classroom setting
- Clear problem statement and expected output
- Solution collapsed below

#### Optional Extra Practice
- More challenging than in-class activities
- Same collapsed solution format
- Marked clearly as "optional"

### 4. Dependencies
- **ALWAYS** install dependencies in the very first cell using `!pip install`
- Example: `!pip install numpy pandas matplotlib`

### 5. Execution Workflow

**CRITICAL**: When creating notebooks, you MUST:
1. Execute each cell immediately after creating it using the IDE tools
2. Verify the output is correct before proceeding
3. If issues arise, fix them immediately - no dirty patches
4. Research using context7 and other tools if needed for robust solutions
5. Only move to the next cell after current cell is verified working

### 6. Code Quality Standards
- All code must be reliable and robust
- Include proper error handling where appropriate
- Use meaningful variable names
- Add inline comments explaining logic
- Test edge cases

## Example Structure

```markdown
# Topic Name

[Beginner-friendly explanation of the concept]

## Instructor Demonstration

**Problem**: [Clear problem statement]
**Expected Output**: [What should happen]

\`\`\`python
# Empty cell for live demonstration
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
# Complete solution with inline comments
# explaining each step
\`\`\`

</details>

## In-Class Activity

**Task**: [Clear task description]
**Expected Output**: [Specific expected result]

\`\`\`python
# Empty cell for learners to code
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
# Complete solution with inline comments
\`\`\`

</details>

## Optional Extra Practice

**Challenge**: [More complex task]
**Expected Output**: [Specific expected result]

\`\`\`python
# Empty cell for extra practice
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
# Complete solution with inline comments
\`\`\`

</details>
```

## Checklist for Creating Teaching Notebooks

- [ ] First cell installs all dependencies with `!pip install`
- [ ] Each section starts with `#` or `##` text cell
- [ ] Lesson explanations are beginner-friendly and accurate
- [ ] Each activity has clear problem statement
- [ ] Expected outputs are explicitly stated
- [ ] All code has inline comments
- [ ] Solutions are collapsed using `<details>` and `<summary>`
- [ ] Each cell is executed and verified before moving to next
- [ ] Code is robust with no dirty patches
- [ ] All outputs are verified correct

## When Referenced

When a user references this guide, you should:
1. Ask for the topic/concept to teach
2. Create structured notebook following the exact format above
3. Execute each cell using IDE tools before proceeding
4. Verify outputs and fix issues immediately
5. Ensure all solutions are collapsed by default
6. Make explanations beginner-friendly yet accurate
