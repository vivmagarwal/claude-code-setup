# Teaching with Google Colab - Guide for Claude

## Purpose
This guide defines the structure and workflow for creating educational python notebooks that help learners understand programming concepts through hands-on practice with scaffolded, progressive, hands-on learning.

## Core Principles

### 1. Notebook Structure
Each topic starts with `#` (collapsible) and follows a **back-and-forth teach-practice pattern**:

```
# Topic Name
- Learning objectives
- Why this matters 
- Prerequisite concepts

## Instructor Activity 1
[Demonstrates foundational Concept A]
- Multiple scaffolded code examples (simple → complex)
- Each with solution collapsed below

## Learner Activity 1
[Practice the SAME Concept A]
- Exercises directly mirroring instructor examples
- Each with solution collapsed below

## Instructor Activity 2
[Demonstrates Concept B, builds on A]
- Multiple scaffolded code examples
- Each with solution collapsed below

## Learner Activity 2
[Practice the SAME Concept B]
- Exercises directly mirroring instructor examples
- Each with solution collapsed below

## Instructor Activity 3
[Demonstrates Concept C, integrates A + B]
- Multiple scaffolded code examples
- Each with solution collapsed below

## Learner Activity 3
[Practice the SAME Concept C]
- Exercises directly mirroring instructor examples
- Each with solution collapsed below

...continue back-and-forth pattern as needed...

## Optional Extra Practice
[Challenge problems at the END covering ALL concepts]
- Multiple challenging exercises integrating everything learned
- Each with solution collapsed below
```

**Key Points:**
- **Back-and-forth pattern**: Instructor teaches → Learner practices immediately → Instructor teaches next → Learner practices that
- Activities use `##` headers (collapsible for clean organization)
- Each learner activity practices the **SAME concept** just demonstrated by instructor
- Number of instructor/learner pairs depends on topic complexity (LLM decides)
- Within each activity, examples scaffold from simple → complex
- Progression happens **across the sequence** of paired activities
- Optional practice is **ONE section at the END** covering all concepts learned

### 2. Text Cell Format

#### Topic Introduction (using `#`)
Must include:
1. **Learning Objectives**: "By the end of this section, you will be able to..."
   - List 3-5 specific, measurable outcomes
   - Use action verbs: create, implement, debug, explain, analyze

2. **Why This Matters**: Real-world AI/RAG/Agentic AI context
   - How this concept applies to AI systems
   - Use in RAG pipelines (retrieval, processing, generation)
   - Application in agentic AI workflows
   - Keep examples concrete and practical

3. **Prerequisites**: What learners should know before starting

#### Activity Headers (using `##`)
- Each activity uses `##` for collapsibility
- Format: "Instructor Activity 1", "Learner Activity 1", "Instructor Activity 2", etc.
- No difficulty level labels needed - progression is implicit in the sequence
- Write beginner-friendly explanations that are accurate and clear
- Keep explanations concise but complete
- Each learner activity should mirror the concept from its corresponding instructor activity

### 3. Code Cell Guidelines

#### Progressive Scaffolding Within Activities
Each activity (Instructor/Learner/Optional) contains multiple code examples that increase in complexity:

**Example 1**: Simplest concept application
- Single focused task
- Minimal variables/logic
- Clear, isolated concept

**Example 2**: Builds on Example 1
- Adds one new element or complexity
- References/extends previous example
- Shows progression naturally

**Example 3**: More advanced combination
- Integrates multiple concepts
- Realistic use case
- Prepares for next difficulty level

Continue adding examples as needed for the topic.

#### Thought-Process/Dry Run Cells (When Needed)
For complex logic, add a "trace through" cell before the code:
```markdown
**Let's trace through this step-by-step:**
1. Variable x starts as...
2. The loop iterates...
3. Each iteration does...
4. Final result will be...
```

#### Visual Aids Guidelines
Include diagrams/flowcharts when explaining:
- **Control flow**: loops, conditionals, branching logic
- **Data structures**: relationships, hierarchies, transformations
- **System architecture**: how components interact
- **Process flow**: multi-step operations, pipelines

Use simple ASCII art, markdown tables, or suggest drawing tools when needed.

#### Code Cell Structure
For each code example:
- Clearly define the problem/task
- State expected outcomes explicitly
- Include comprehensive inline comments explaining the "why"
- Place solution in collapsed markdown cell immediately below using:
  ```markdown
  <details>
  <summary>Solution</summary>

  \`\`\`python
  # Solution code here with detailed comments
  \`\`\`

  **Why this works:**
  [Brief explanation of key concepts]

  </details>
  ```

### 4. Repository Structure

When creating teaching notebooks in a repository, organize them properly:

**Folder Structure:**
```
repository_root/
├── class_name_or_subject/
│   ├── notebooks/
│   │   ├── 01_topic_name.ipynb
│   │   ├── 02_another_topic.ipynb
│   │   └── 03_advanced_topic.ipynb
│   └── README.md
```

**README.md Format:**
The README should contain "Open in Colab" badges for each notebook:

```markdown
# Class Name / Subject

## Notebooks

### Topic 1: Topic Name
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USERNAME/REPO_NAME/blob/main/CLASS_NAME/notebooks/01_topic_name.ipynb)

### Topic 2: Another Topic
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USERNAME/REPO_NAME/blob/main/CLASS_NAME/notebooks/02_another_topic.ipynb)
```

**Badge Link Pattern:**
```markdown
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USERNAME/REPO_NAME/blob/main/PATH/TO/NOTEBOOK.ipynb)
```

**When Creating Notebooks:**
1. Create the class/subject folder if it doesn't exist
2. Create a `notebooks/` subfolder inside it
3. Save `.ipynb` files in the `notebooks/` folder
4. Create/update README.md with Open in Colab badges for each notebook
5. Use consistent naming: `01_topic_name.ipynb`, `02_next_topic.ipynb`, etc.

### 5. Dependencies
- **ALWAYS** install dependencies in the very first cell using `!pip install`
- Example: `!pip install numpy pandas matplotlib`

### 6. Execution Workflow

**CRITICAL**: When creating notebooks, you MUST:
1. Execute each cell immediately after creating it using the IDE tools
2. Verify the output is correct before proceeding
3. If issues arise, fix them immediately - no dirty patches
4. Research using context7 and other tools if needed for robust solutions
5. Only move to the next cell after current cell is verified working

### 7. Code Quality Standards
- All code must be reliable and robust
- Include proper error handling where appropriate
- Use meaningful variable names
- Add inline comments explaining logic
- Test edge cases

## Example Structure

```markdown
# List Comprehensions in Python

## Learning Objectives
By the end of this section, you will be able to:
- Create basic list comprehensions to transform data
- Apply conditional logic within list comprehensions
- Combine list comprehensions with real-world data processing
- Use list comprehensions in AI/RAG/Agentic AI workflows

## Why This Matters: Real-World AI/RAG/Agentic Applications
**In AI Systems:**
- Efficiently process large datasets for model training
- Transform raw data into features for ML pipelines

**In RAG Pipelines:**
- Filter and rank retrieved documents based on relevance scores
- Extract specific fields from multiple retrieved chunks
- Batch process embeddings and metadata

**In Agentic AI:**
- Parse and structure tool outputs from multiple agents
- Filter action sequences based on confidence scores
- Transform agent responses into standardized formats

## Prerequisites
- Basic Python lists and loops
- Understanding of for loops and if statements

---

## Instructor Activity 1
**Concept**: Basic list comprehension syntax and simple transformations

### Example 1: Simple Transformation

**Problem**: Square each number in a list
**Expected Output**: `[1, 4, 9, 16, 25]`

\`\`\`python
# Empty cell for live demonstration
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
# Traditional approach with for loop
numbers = [1, 2, 3, 4, 5]
squared_traditional = []
for num in numbers:
    squared_traditional.append(num ** 2)

# List comprehension approach - more concise and Pythonic
squared_comprehension = [num ** 2 for num in numbers]

print("Traditional:", squared_traditional)
print("Comprehension:", squared_comprehension)
# Output: [1, 4, 9, 16, 25]
\`\`\`

**Why this works:**
List comprehensions combine the loop and append in one line: `[expression for item in iterable]`. This approach is more readable, faster, and Pythonic.

</details>

### Example 2: String Transformations

**Problem**: Convert a list of names to uppercase
**Expected Output**: `['ALICE', 'BOB', 'CHARLIE']`

\`\`\`python
# Empty cell for demonstration
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
names = ['alice', 'bob', 'charlie']

# Use list comprehension with string method
uppercase_names = [name.upper() for name in names]

print("Uppercase:", uppercase_names)
# Output: ['ALICE', 'BOB', 'CHARLIE']
\`\`\`

**Why this works:**
You can call methods on items within the comprehension expression.

</details>

---

## Learner Activity 1
**Practice**: Basic list comprehension syntax and simple transformations

### Exercise 1: Temperature Conversion

**Task**: Convert a list of Celsius temperatures to Fahrenheit using list comprehension (F = C * 9/5 + 32)
**Given**: `celsius = [0, 10, 20, 30, 40]`
**Expected Output**: `[32.0, 50.0, 68.0, 86.0, 104.0]`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
celsius = [0, 10, 20, 30, 40]

# Convert each Celsius value to Fahrenheit
fahrenheit = [c * 9/5 + 32 for c in celsius]

print("Fahrenheit:", fahrenheit)
# Output: [32.0, 50.0, 68.0, 86.0, 104.0]
\`\`\`

**Why this works:**
The expression `c * 9/5 + 32` is applied to each item in the celsius list.

</details>

### Exercise 2: String Length

**Task**: Create a list of lengths for each word in a sentence
**Given**: `words = ['hello', 'world', 'python', 'ai']`
**Expected Output**: `[5, 5, 6, 2]`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
words = ['hello', 'world', 'python', 'ai']

# Get length of each word
lengths = [len(word) for word in words]

print("Lengths:", lengths)
# Output: [5, 5, 6, 2]
\`\`\`

**Why this works:**
The `len()` function is applied to each word in the comprehension.

</details>

---

## Instructor Activity 2
**Concept**: Adding conditional logic (filtering) to list comprehensions

### Example 1: Filtering with Conditions

**Problem**: Square only the even numbers
**Expected Output**: `[4, 16]`

\`\`\`python
# Empty cell for demonstration
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
numbers = [1, 2, 3, 4, 5]

# List comprehension with if condition
even_squared = [num ** 2 for num in numbers if num % 2 == 0]

print("Even squared:", even_squared)
# Output: [4, 16]
\`\`\`

**Why this works:**
Pattern: `[expression for item in iterable if condition]` - the if filters which items to process.

</details>

### Example 2: Filtering Strings

**Problem**: Extract words longer than 4 characters
**Expected Output**: `['python', 'programming']`

\`\`\`python
# Empty cell for demonstration
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
words = ['ai', 'python', 'is', 'for', 'programming']

# Filter words by length
long_words = [word for word in words if len(word) > 4]

print("Long words:", long_words)
# Output: ['python', 'programming']
\`\`\`

**Why this works:**
The condition `if len(word) > 4` filters out short words before including them in the result.

</details>

---

## Learner Activity 2
**Practice**: Adding conditional logic (filtering) to list comprehensions

### Exercise 1: Filter Positive Numbers

**Task**: Extract only positive numbers from a list
**Given**: `numbers = [-5, 3, -2, 8, -1, 0, 7]`
**Expected Output**: `[3, 8, 7]`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
numbers = [-5, 3, -2, 8, -1, 0, 7]

# Filter for positive numbers only
positive = [num for num in numbers if num > 0]

print("Positive:", positive)
# Output: [3, 8, 7]
\`\`\`

**Why this works:**
The condition `if num > 0` filters to include only positive numbers.

</details>

### Exercise 2: Filter Names Starting with 'A'

**Task**: Extract names that start with the letter 'A'
**Given**: `names = ['Alice', 'Bob', 'Anna', 'Charlie', 'Alex']`
**Expected Output**: `['Alice', 'Anna', 'Alex']`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
names = ['Alice', 'Bob', 'Anna', 'Charlie', 'Alex']

# Filter names starting with 'A'
a_names = [name for name in names if name.startswith('A')]

print("A names:", a_names)
# Output: ['Alice', 'Anna', 'Alex']
\`\`\`

**Why this works:**
The `startswith('A')` method checks if the name begins with 'A', filtering the results.

</details>

---

## Instructor Activity 3
**Concept**: Real-world AI/RAG/Agentic applications with complex data structures

### Example 1: RAG Document Filtering

**Problem**: Filter documents by relevance score (common in RAG systems)
**Expected Output**: List of document titles with score > 0.7

\`\`\`python
# Empty cell for demonstration
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
# Simulating retrieved documents with relevance scores from a RAG system
documents = [
    {"title": "Python Basics", "score": 0.85},
    {"title": "JavaScript Guide", "score": 0.45},
    {"title": "Python Advanced", "score": 0.92},
    {"title": "Java Tutorial", "score": 0.60},
]

# Extract titles of highly relevant documents (score > 0.7)
relevant_titles = [doc["title"] for doc in documents if doc["score"] > 0.7]

print("Relevant documents:", relevant_titles)
# Output: ['Python Basics', 'Python Advanced']
\`\`\`

**Why this works:**
This is a common RAG pattern - filtering retrieved chunks by relevance threshold before passing to LLM.

</details>

### Example 2: Agent Action Filtering

**Problem**: Filter AI agent actions by confidence score
**Expected Output**: Actions with confidence >= 0.8

\`\`\`python
# Empty cell for demonstration
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
# Agent returns multiple possible actions with confidence scores
actions = [
    {"action": "send_email", "confidence": 0.95},
    {"action": "schedule_meeting", "confidence": 0.65},
    {"action": "create_document", "confidence": 0.88},
    {"action": "delete_file", "confidence": 0.45},
]

# Extract high-confidence actions only
high_conf = [a["action"] for a in actions if a["confidence"] >= 0.8]

print("High confidence actions:", high_conf)
# Output: ['send_email', 'create_document']
\`\`\`

**Why this works:**
In agentic AI, filtering by confidence prevents low-quality actions from being executed.

</details>

---

## Learner Activity 3
**Practice**: Real-world AI/RAG/Agentic applications with complex data structures

### Exercise 1: Filter Users by Age

**Task**: Extract usernames of users aged 18 or older
**Given**:
\`\`\`python
users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30},
    {"name": "Diana", "age": 16}
]
\`\`\`
**Expected Output**: `['Alice', 'Charlie']`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
users = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 17},
    {"name": "Charlie", "age": 30},
    {"name": "Diana", "age": 16}
]

# Extract names of adult users
adults = [user["name"] for user in users if user["age"] >= 18]

print("Adults:", adults)
# Output: ['Alice', 'Charlie']
\`\`\`

**Why this works:**
We access the dictionary values using keys and filter based on the age condition.

</details>

### Exercise 2: Clean Text Chunks for RAG

**Scenario:** You have text chunks and need to prepare them for embedding generation (common in RAG).

**Task**: Extract and clean text from chunks, removing empty strings
**Given**:
\`\`\`python
chunks = [
    {"id": 1, "text": "Introduction to AI"},
    {"id": 2, "text": ""},
    {"id": 3, "text": "Machine Learning Basics"},
    {"id": 4, "text": "   "},
]
\`\`\`
**Expected Output**: `['Introduction to AI', 'Machine Learning Basics']`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
chunks = [
    {"id": 1, "text": "Introduction to AI"},
    {"id": 2, "text": ""},
    {"id": 3, "text": "Machine Learning Basics"},
    {"id": 4, "text": "   "},
]

# Extract text, strip whitespace, and filter out empty strings
clean_texts = [chunk["text"].strip() for chunk in chunks if chunk["text"].strip()]

print("Clean texts:", clean_texts)
# Output: ['Introduction to AI', 'Machine Learning Basics']
\`\`\`

**Why this works:**
- `.strip()` removes leading/trailing whitespace
- `if chunk["text"].strip()` filters out empty strings (empty strings are "falsy")
- This prevents sending empty texts to embedding APIs (saves cost and errors)
- Note: `.strip()` is called twice - once for cleaning in the expression, once for filtering in the condition

</details>

---

## Optional Extra Practice
**Challenge yourself with these problems that integrate all the concepts**

### Challenge 1: Multi-Condition Filtering

**Task**: Extract even numbers that are also greater than 5
**Given**: `numbers = [2, 4, 6, 8, 10, 12, 3, 5, 7]`
**Expected Output**: `[6, 8, 10, 12]`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
numbers = [2, 4, 6, 8, 10, 12, 3, 5, 7]

# Multiple conditions with 'and'
result = [num for num in numbers if num % 2 == 0 and num > 5]

print("Result:", result)
# Output: [6, 8, 10, 12]
\`\`\`

**Why this works:**
Multiple conditions can be combined with `and` / `or` operators in the if clause.

</details>

### Challenge 2: RAG Pipeline - Extract and Transform

**Scenario**: Process RAG results to get clean, relevant document snippets

**Task**: Extract text from high-scoring documents and convert to lowercase
**Given**:
\`\`\`python
rag_results = [
    {"text": "PYTHON is Great", "score": 0.9},
    {"text": "Java Tutorial", "score": 0.5},
    {"text": "ADVANCED Python", "score": 0.85},
    {"text": "C++ Guide", "score": 0.3}
]
\`\`\`
**Expected Output**: `['python is great', 'advanced python']`

\`\`\`python
# Your code here
\`\`\`

<details>
<summary>Solution</summary>

\`\`\`python
rag_results = [
    {"text": "PYTHON is Great", "score": 0.9},
    {"text": "Java Tutorial", "score": 0.5},
    {"text": "ADVANCED Python", "score": 0.85},
    {"text": "C++ Guide", "score": 0.3}
]

# Filter by score AND transform to lowercase
relevant_text = [doc["text"].lower() for doc in rag_results if doc["score"] >= 0.8]

print("Relevant text:", relevant_text)
# Output: ['python is great', 'advanced python']
\`\`\`

**Why this works:**
Combines filtering (score check) with transformation (lowercase) in a single comprehension.
This is a realistic RAG preprocessing step.

</details>

```

## Checklist for Creating Teaching Notebooks

### Topic Setup
- [ ] First cell installs all dependencies with `!pip install`
- [ ] Topic starts with `#` header (collapsible)
- [ ] Learning objectives clearly stated (3-5 specific outcomes)
- [ ] "Why This Matters" section with AI/RAG/Agentic AI applications
- [ ] Prerequisites listed

### Activity Structure
- [ ] Back-and-forth pattern: Instructor Activity 1 → Learner Activity 1 → Instructor Activity 2 → Learner Activity 2...
- [ ] Each activity uses `##` header (numbered sequentially)
- [ ] Each learner activity practices the SAME concept from its corresponding instructor activity
- [ ] Multiple code examples within each activity (scaffolded progression)
- [ ] Examples increase in complexity within each activity
- [ ] Clear problem statement for each example
- [ ] Expected outputs explicitly stated
- [ ] Optional Extra Practice is ONE section at the END

### Pedagogical Elements
- [ ] Thought-process/dry run cells for complex logic (when needed)
- [ ] Visual aids (diagrams/flowcharts) when explaining flow or architecture
- [ ] All code has inline comments explaining "why", not just "what"

### Solutions
- [ ] Solutions collapsed using `<details>` and `<summary>`
- [ ] Solutions include "Why this works" explanations
- [ ] Solutions reference real-world AI/RAG/Agentic applications where relevant

### Execution Quality
- [ ] Each cell executed and verified before moving to next
- [ ] Code is robust with no dirty patches
- [ ] All outputs verified correct
- [ ] Edge cases considered

### Progressive Learning
- [ ] Within-activity scaffolding (Example 1 → Example 2 → Example 3 within each activity)
- [ ] Across-activity progression (Activity 1 teaches basics → Activity 2 builds on it → Activity 3 integrates)
- [ ] Number of instructor/learner pairs appropriate for topic complexity
- [ ] Back-and-forth pattern maintained throughout
- [ ] Each learner activity reinforces concepts from corresponding instructor activity

## When Referenced

When a user references this guide, you should:

1. **Understand the Topic**: Ask for the topic/concept to teach and clarify scope

2. **Set Up Repository Structure**:
   - Create `class_name/notebooks/` folder structure
   - Prepare to create README.md with Open in Colab badges
   - Use numbered naming: `01_topic.ipynb`, `02_topic.ipynb`, etc.

3. **Create Learning Foundation**:
   - Write learning objectives (3-5 specific outcomes)
   - Explain "Why This Matters" with AI/RAG/Agentic AI applications
   - List prerequisites

4. **Plan Activity Sequence**: Determine how many instructor/learner pairs needed
   - Break topic into discrete concepts (Concept A, B, C, etc.)
   - Simple topics: 2-3 instructor/learner pairs
   - Complex topics: 4-6 instructor/learner pairs
   - Each pair: Instructor Activity N → Learner Activity N (practicing same concept)

5. **Create Notebook(s)**: Save in `class_name/notebooks/` folder
   - Use numbered naming convention
   - Each notebook covers one major topic

6. **Build Activities in Back-and-Forth Pattern**:
   - Instructor Activity 1: Teach Concept A with multiple scaffolded examples
   - Learner Activity 1: Practice Concept A with exercises mirroring instructor examples
   - Instructor Activity 2: Teach Concept B (building on A) with scaffolded examples
   - Learner Activity 2: Practice Concept B with corresponding exercises
   - Continue pattern for all concepts
   - Optional Extra Practice: ONE final section with integrated challenges

7. **Within Each Activity**: Create multiple scaffolded examples
   - Start simple (single concept, minimal complexity)
   - Build up (add elements progressively)
   - Realistic application (integrates concepts)

8. **Add Pedagogical Elements**:
   - Thought-process cells for complex logic (when needed)
   - Visual aids when explaining flow/architecture
   - Inline comments explaining "why"
   - "Why this works" in solutions

9. **Execute and Verify**:
   - Use IDE tools to execute each cell before proceeding
   - Verify outputs match expected results
   - Fix issues immediately with no dirty patches
   - Test edge cases

10. **Create/Update README.md**:
    - Add Open in Colab badge for the notebook
    - Use pattern: `[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/USERNAME/REPO_NAME/blob/main/CLASS_NAME/notebooks/NN_topic.ipynb)`
    - Include brief description of what the notebook covers
    - List learning objectives from the notebook

11. **Quality Checks**:
   - All solutions collapsed by default
   - All activities use `##` headers (collapsible)
   - Explanations beginner-friendly yet accurate
   - Real-world AI/RAG/Agentic examples throughout

## Key Principles to Remember

- **Repository Structure**: Organize as `class_name/notebooks/` with README containing Open in Colab badges
- **Back-and-Forth Pattern**: Instructor teaches → Learner practices immediately → repeat for each concept
- **Paired Activities**: Each learner activity practices the SAME concept from its corresponding instructor activity
- **Scaffolding**: Within activities (Example 1→2→3 within each) AND across activities (Activity 1→2→3 builds up)
- **Optional Practice at End**: ONE final section with integrated challenges covering all concepts
- **Real-World Context**: Connect every concept to AI/RAG/Agentic AI applications
- **Clean Organization**: Use `#` for topics, `##` for activities (all collapsible)
- **Quality First**: Execute and verify each cell, no shortcuts
- **Accessibility**: Every notebook should be one-click openable in Google Colab via README badges
