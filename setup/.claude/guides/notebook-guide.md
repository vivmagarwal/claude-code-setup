# Claude Code Jupyter Notebook Guide

## 🎯 Core Principles

When asking Claude Code to work with Jupyter notebooks, follow these fundamental principles:

1. **Always create and enable a UV environment first**
2. **Make each cell as independent as possible**
3. **Install all dependencies in the first cells using `!uv pip install`**
4. **Execute each cell before proceeding to the next**
5. **No dirty patches or ugly fixes - only solid, reliable, robust code**
6. **Verify outputs at each step**
7. **Create all dependencies upfront**
8. **Test incrementally, fix immediately**
9. **Research thoroughly using available tools before implementation**

---

## 📝 The Perfect Prompt Template

### For Creating New Notebooks

```
Create a Jupyter notebook for [specific task].

Requirements:
1. First cells MUST install dependencies using !uv pip install
2. Each cell should be as independent as possible
3. Execute each cell sequentially before writing the next
4. Show the output of each cell execution
5. If a cell fails, fix it completely before proceeding
6. No quick fixes or workarounds - write production-quality code
7. Create all required data files before starting

Cell Structure:
- Cell 1: UV environment setup and kernel installation
- Cell 2-3: Dependency installation using !uv pip install
- Cell 4+: Implementation with independent, self-contained logic

Validation:
- After each cell: "Cell X executed successfully with output: [summary]"
- Final confirmation: "All N cells executed without any errors"
- Save as: [descriptive_name]_verified.ipynb
```

### For Fixing Existing Notebooks

```
Fix this Jupyter notebook to run without errors:

Process:
1. Read the notebook and identify all dependencies
2. Create/verify all required data files exist
3. Execute cell 1 - if it fails, rewrite it properly
4. Only proceed to cell 2 after cell 1 runs perfectly
5. Continue cell-by-cell until all execute cleanly

Standards:
- No commenting out broken code
- No try/except to hide errors
- Fix root causes, not symptoms
- Each cell must be production-ready

Deliver: Fully working notebook with zero errors
```

---

## 🚀 Best Practices for Claude Code

### 1. Data Preparation First

❌ **Wrong:**
```
"Create a data analysis notebook"
```

✅ **Right:**
```
"Create a data analysis notebook. First, generate a sample dataset with 1000 rows
including columns: date, sales, region, product. Save as sales_data.csv.
Then create the notebook, executing each cell to verify it works with this data."
```

### 2. Cell-by-Cell Execution

❌ **Wrong:**
```
"Write a machine learning notebook with 10 cells"
```

✅ **Right:**
```
"Create a machine learning notebook following this workflow:
- Cell 1: Import libraries - execute and confirm all imports work
- Cell 2: Load data - execute and show shape/head
- Cell 3: EDA - execute and display visualizations
- Cell 4: Preprocessing - execute and verify transformations
Continue this pattern, executing each cell before writing the next"
```

### 3. Explicit Error Handling

❌ **Wrong:**
```
"Make this notebook work"
```

✅ **Right:**
```
"Debug this notebook with proper fixes:
1. Execute the notebook with --allow-errors flag
2. List which cells failed and why
3. For each failed cell:
   - Identify root cause (missing import, wrong data type, etc.)
   - Implement proper solution (not a workaround)
   - Verify the fix by re-executing
4. Confirm: 'All errors resolved, notebook runs cleanly'"
```

---

## 🛠️ Claude Code Notebook Workflow

### Step 1: UV Environment Setup
```
ALWAYS start with UV environment:
1. Create UV environment: uv venv
2. Activate UV environment in notebook
3. First notebook cell MUST be: !uv pip install jupyter ipykernel
4. Second/third cells: Install all project dependencies with !uv pip install
5. Use UV for ALL package installations: !uv pip install <package>
6. Register kernel: !python -m ipykernel install --user --name=.venv

Critical: Installing dependencies in the first cells ensures each cell
can run independently and the notebook is reproducible.
```

### Step 2: Research and Discovery
```
Before implementing, research thoroughly:
1. Use MCP tools to search for best practices and examples
2. Use IDE MCP to:
   - Get diagnostics from VS Code
   - Execute code in Jupyter kernel (executeCode)
   - Explore existing codebase patterns
3. Use Perplexity/WebSearch for latest documentation
4. Use Context7 for library-specific documentation
5. Use GitHub MCP for finding code examples in repositories
6. For web scraping needs: Use claude-scripts/ccpro.py if necessary
7. Document findings before implementation

IDE MCP Integration:
- Use executeCode to test code snippets in the active kernel
- Use getDiagnostics to check for errors and warnings
- Leverage VS Code integration for better code quality

Web Scraping (if needed):
- Use the CCPro script at claude-scripts/ccpro.py
- Example: from claude_scripts.ccpro import crawl
- Supports interactive authentication and deep crawling
```

### Step 3: Data Creation
```
Before writing any notebook code:
1. Generate all CSV/JSON files needed
2. Create proper directory structure
3. Verify data files are readable
4. Document data schema
```

### Step 4: Incremental Development
```
For each notebook cell:
1. Write the cell code (ensure it's as self-contained as possible)
2. For dependency cells: Use !uv pip install in the cell itself
3. Execute using: python -c "[cell code]" or in notebook directly
4. Capture and verify output
5. Fix any issues completely
6. Only then proceed to next cell

Cell Independence Guidelines:
- Each cell should be re-runnable without depending on variable state
- Import statements can be repeated in cells that use them
- Avoid relying on mutable global state between cells
- Data loading should be explicit in each cell that needs it
```

### Step 5: Full Validation
```
After all cells are written:
1. Save complete notebook
2. Execute: jupyter nbconvert --execute notebook.ipynb
3. Read executed notebook
4. Verify zero error outputs
5. Report: "All X cells executed successfully"
```

---

## 💪 Robust Code Standards

### UV Package Installation
```python
# ❌ Bad - using system pip
!pip install pandas numpy scikit-learn

# ✅ Good - using UV in notebook
!uv pip install pandas numpy scikit-learn matplotlib seaborn

# For notebooks, ALWAYS use UV:
!uv pip install jupyter ipykernel
!uv pip install -r requirements.txt  # if requirements file exists
```

### Import Management
```python
# ❌ Bad - fragile imports
from sklearn import *
import pandas

# ✅ Good - explicit, verified imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Verify imports work
print("All imports successful")
```

### Data Loading
```python
# ❌ Bad - assumes file exists
df = pd.read_csv('data.csv')

# ✅ Good - robust loading with verification
import os

data_file = 'data.csv'
if not os.path.exists(data_file):
    print(f"Creating synthetic {data_file}...")
    # Create data
    df = pd.DataFrame({...})
    df.to_csv(data_file, index=False)

df = pd.read_csv(data_file)
print(f"Loaded {len(df)} rows from {data_file}")
print(f"Columns: {df.columns.tolist()}")
```

### Error Prevention
```python
# ❌ Bad - hiding errors
try:
    model.fit(X, y)
except:
    pass  # Silent failure

# ✅ Good - proper validation
# Verify data before model training
assert X.shape[0] == y.shape[0], "X and y must have same number of samples"
assert not X.isnull().any().any(), "X contains null values"
assert len(np.unique(y)) > 1, "y must have at least 2 classes"

model.fit(X, y)
print(f"Model trained on {X.shape[0]} samples with {X.shape[1]} features")
```

---

## 📋 Example Prompts

### Example 1: Data Analysis Notebook
```
Create a data analysis notebook for customer churn analysis.

Setup:
1. Cell 1: Install jupyter and ipykernel using !uv pip install
2. Cells 2-3: Install all analysis packages using !uv pip install pandas numpy matplotlib seaborn scikit-learn
3. First create customer_data.csv with 1000 rows
   - Columns: customer_id, age, tenure, monthly_charges, total_charges, churn
4. Execute each analysis cell and show output
5. No deprecated functions or warnings

Quality standards:
- Each cell must be independently runnable
- Each visualization must display properly
- All statistics must be calculated correctly
- Code must follow PEP 8 style
- Include markdown explanations

Confirm each cell executes before proceeding to next.
```

### Example 2: Machine Learning Pipeline
```
Build a complete ML pipeline notebook.

Requirements:
1. Cell 1: !uv pip install jupyter ipykernel
2. Cell 2: !uv pip install scikit-learn pandas numpy matplotlib seaborn
3. Generate synthetic classification dataset (1000 samples, 10 features)
4. Cell-by-cell execution with output verification:
   - Imports and setup (can be repeated in cells that need them)
   - Data loading and validation
   - EDA with visualizations
   - Feature engineering
   - Model training
   - Evaluation metrics
   - Predictions on test set

Standards:
- Each cell must be self-contained and re-runnable
- Use only stable sklearn APIs
- Proper train/test split
- No data leakage
- Clear metric reporting

Execute each cell and confirm output before writing next cell.
```

### Example 3: Debugging Complex Notebook
```
Fix this scientific computing notebook:

Approach:
1. Identify all dependencies (libraries, data files, configs)
2. Create missing resources
3. Execute cell 1
   - If error: Fix root cause properly
   - If warning: Resolve it correctly
   - If success: Show output and proceed
4. Repeat for all cells

No acceptable workarounds:
- No commenting out broken code
- No suppressing warnings without fixing
- No empty except blocks
- No hardcoded paths

Final delivery: Clean notebook with professional-quality code
```

---

## 🔍 Verification Checklist

Before considering a notebook complete, Claude Code should verify:

- [ ] All required data files created and accessible
- [ ] Every import statement executes without error
- [ ] Each cell runs independently and in sequence
- [ ] No deprecation warnings
- [ ] No hardcoded paths (use relative paths)
- [ ] Proper error messages for edge cases
- [ ] Outputs match expected results
- [ ] Code follows consistent style
- [ ] Memory-efficient operations
- [ ] Reproducible results (set random seeds)

---

## 🚨 Common Pitfalls to Avoid

### 1. Writing Everything Then Testing
❌ Don't write 20 cells then test
✅ Test each cell immediately

### 2. Ignoring Warnings
❌ Don't suppress warnings with `warnings.filterwarnings('ignore')`
✅ Fix the cause of warnings

### 3. Quick Fixes
❌ Don't use `try/except: pass` to skip errors
✅ Solve the actual problem

### 4. Missing Dependencies
❌ Don't assume data files exist
✅ Create all requirements upfront

### 5. Version Conflicts
❌ Don't ignore package version issues
✅ Ensure compatible versions

---

## 🎯 The Ultimate Goal

When Claude Code completes a notebook task, you should be able to:

1. Clone the repository
2. Run `jupyter nbconvert --execute notebook.ipynb`
3. See it execute perfectly with zero errors
4. Get meaningful, correct outputs
5. Understand the code without debugging

**Remember:** Quality over speed. A properly working notebook with 5 cells is better than a broken notebook with 50 cells.

---

## 📚 Quick Reference Card

```bash
# Commands Claude Code uses for notebooks

# Execute entire notebook
jupyter nbconvert --execute notebook.ipynb --to notebook --output executed.ipynb

# Execute with timeout
jupyter nbconvert --execute notebook.ipynb --ExecutePreprocessor.timeout=600

# Execute allowing errors (for debugging)
jupyter nbconvert --execute notebook.ipynb --allow-errors

# Test individual cell
python -c "
# cell code here
"

# Verify execution
python -c "
import nbformat
nb = nbformat.read('notebook.ipynb', as_version=4)
errors = sum(1 for cell in nb.cells
             if cell.cell_type == 'code'
             for output in cell.get('outputs', [])
             if output.get('output_type') == 'error')
print(f'Errors found: {errors}')
"
```

---

## 📌 Summary

**The golden rule for Claude Code and notebooks:**

> "Execute each cell successfully before writing the next. No exceptions, no shortcuts, no dirty fixes."

This ensures you always receive working, professional-quality notebooks that run perfectly from top to bottom.