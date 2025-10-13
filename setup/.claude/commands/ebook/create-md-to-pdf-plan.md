---
name: create-md-to-pdf-plan
description: Convert markdown repository into professional, ready-to-sell ebook PDF
argument-hint: <repository-path> [cover-image-path] [output-path]
---

<role>
You are a world-class Ebook Production Engineer who transforms markdown repositories into professional, commercially-ready PDF ebooks optimized for digital distribution.

This command contains ALL necessary information to convert markdown repositories to professional PDFs - no external references needed.
</role>

<task>
Convert markdown repository to professional ebook PDF from: $1
Using cover image (if provided): ${2:-auto-detect}
Save execution plan to: ${3:-.project-management/ebook/md-to-pdf-execution-plan.md}
</task>

<approach>
Be thorough and professional. Guide the user through creating a publication-ready ebook by:
1. Analyzing the repository structure and content
2. Gathering requirements (cover image, page size, branding)
3. Creating a comprehensive execution plan with status tracking
4. Guiding step-by-step through the ebook generation process
5. Ensuring professional quality suitable for commercial sale
</approach>

<critical_knowledge>
## Tool Selection: wkhtmltopdf (Recommended)

**Why wkhtmltopdf:**
- Most reliable (battle-tested WebKit engine)
- Best compression (4-5x smaller than WeasyPrint)
- Stable across systems
- Handles 500+ page documents easily
- Professional output with minimal configuration

**Alternative: WeasyPrint** - Only if user needs advanced CSS Paged Media features

## Digital Reading Optimization (CRITICAL)

Unlike print books, digital ebooks must optimize for:
1. **Backlit Screens:** Pure monochrome (rgba(0, 0, 0, 0.84) on white #ffffff)
2. **Variable Zoom:** Users will zoom in/out
3. **Interactive Links:** Clickable TOC and cross-references
4. **Device Variety:** iPad, Kindle, Android tablets, laptops
5. **Medium.com Typography:** Research-backed readability standards

**Optimal wkhtmltopdf Settings:**
```bash
--dpi 96                    # Screen-optimal resolution (NOT 150 or 300)
--image-quality 85          # High quality, reasonable size
--enable-internal-links     # Clickable navigation
--page-size Letter          # Familiar tablet size (8.5 x 11 inches)
```

## Image Path Issues (90% of Problems)

**CRITICAL LESSON:** This single issue causes most failures.

**Problem:** Images use relative paths that break when markdown is compiled:
- `../../some-dir/image.png` (from nested files)
- `../images/photo.jpg` (from sibling directories)
- `./assets/pic.png` (from current directory)

### STEP 1: Discover Actual Image Locations

**FIRST, analyze the repository to find where images actually are:**

```bash
# Find all image references in markdown files
grep -r "!\[.*\](" /path/to/repo --include="*.md" | grep -o '([^)]*)' | sort -u

# Example output might show:
# (../../assets/images/foo.png)
# (../media/bar.jpg)
# (./pictures/baz.png)
```

**Common patterns you'll find:**
- `assets/images/` (most common)
- `media/`, `pictures/`, `img/`, `figures/`
- Mixed paths from different directory levels
- Sometimes absolute paths

### STEP 2: Full Path Resolution (Robust Strategy)

**Use this approach - it handles ANY directory structure and validates images exist:**

```python
import re
import shutil
from pathlib import Path

def fix_image_paths(
    content: str,
    markdown_file: Path,
    repo_root: Path,
    build_dir: Path
) -> str:
    """
    Robustly fix image paths by resolving to actual filesystem locations.

    Process:
    1. Find each image reference in markdown
    2. Resolve to actual file on disk (validates it exists)
    3. Copy image to build directory (preserves structure)
    4. Rewrite path to be build-relative

    Args:
        content: Markdown file content
        markdown_file: Path to the markdown file being processed
        repo_root: Root directory of the repository
        build_dir: Target build directory where compiled markdown will be

    Returns:
        Content with all image paths fixed and images copied
    """

    def resolve_and_copy(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        # Skip absolute URLs (keep unchanged)
        if image_path.startswith(('http://', 'https://', '//')):
            return match.group(0)

        # Resolve to actual file on disk
        if image_path.startswith('/'):
            # Absolute filesystem path
            source_image = Path(image_path)
        else:
            # Relative path from markdown file's location
            source_image = (markdown_file.parent / image_path).resolve()

        # Verify image exists (CRITICAL VALIDATION)
        if not source_image.exists():
            print(f"⚠️  WARNING: Image not found: {source_image}")
            print(f"    Referenced in: {markdown_file}")
            print(f"    Original path: {image_path}")
            return match.group(0)  # Keep original, will show as broken

        # Determine target path in build directory
        # Preserve directory structure relative to repo root
        try:
            rel_path = source_image.relative_to(repo_root)
            target_image = build_dir / rel_path
        except ValueError:
            # Image outside repo root - use flat structure in assets/images/
            target_image = build_dir / "assets" / "images" / source_image.name
            print(f"📁 Image outside repo, copying to: {target_image.relative_to(build_dir)}")

        # Copy image to build directory
        target_image.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image, target_image)

        # Return build-relative path for markdown
        build_relative = target_image.relative_to(build_dir)
        return f'![{alt_text}]({build_relative.as_posix()})'

    # Process all image references
    content = re.sub(
        r'!\[([^\]]*)\]\(([^\)]+)\)',
        resolve_and_copy,
        content
    )

    return content
```

**Why Full Path Resolution:**
- ✅ Works with ANY directory structure (assets, media, pictures, etc.)
- ✅ Validates each image exists before using it
- ✅ Preserves directory organization
- ✅ Copies images automatically during processing
- ✅ Clear error messages for missing images
- ✅ Handles images outside repo root gracefully
- ✅ No guessing or pattern matching needed

### STEP 3: Validation

**After fixing paths, ALWAYS validate:**

```bash
# 1. Check images were copied
find output-pdfs/build -type f \( -name "*.png" -o -name "*.jpg" \) | wc -l
# Should match or exceed source image count

# 2. Check paths in compiled markdown
grep "!\[" output-pdfs/build/complete-ebook.md | head -20
# Should show build-relative paths:
# ![Image](assets/images/foo.png)     ✓ GOOD
# ![Photo](media/bar.jpg)              ✓ GOOD
# ![Picture](../../old/path.png)       ✗ BAD - still relative!

# 3. Test HTML in browser (CRITICAL)
open output-pdfs/build/complete-ebook.html
# Check browser console for 404 errors
# Right-click any broken images → Inspect to see attempted path
```

### CRITICAL RULES:

1. **Use Full Path Resolution** - it's the most reliable approach

2. **Always validate images exist** - the function prints warnings for missing images

3. **ALWAYS use `--enable-local-file-access`** flag with wkhtmltopdf

4. **ALWAYS validate HTML before PDF** - broken images show immediately in browser

5. **Check console output** - look for "⚠️ WARNING" messages about missing images

## Professional CSS Styling - Medium.com Typography (Complete)

**CRITICAL: Use Medium.com typography for best-in-class readability**

Medium.com is the gold standard for online reading. Their typography choices are research-backed.

**Insert this CSS into HTML before PDF generation:**

```css
<style>
/* PROFESSIONAL EBOOK STYLING - Medium.com-Inspired Typography */

/* Reset and Base Styling */
* {
  box-sizing: border-box;
}

/* Page Setup */
@page {
    size: letter;
    margin: 1in 0.8in;
}

/* Body Typography - Medium's Exact Font Stack */
body {
  /* Medium's exact readable font stack */
  font-family: Charter, 'Bitstream Charter', 'Sitka Text', Cambria, Georgia, serif;
  font-size: 21px;           /* Medium's body size */
  line-height: 1.58;         /* Medium's line-height */
  letter-spacing: -0.003em;
  color: rgba(0, 0, 0, 0.84);  /* Medium's exact text color */
  background-color: #ffffff;    /* Pure white, NOT off-white */
  max-width: 740px;            /* Medium's actual content width */
  margin: 0 auto;
  padding: 60px 40px;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

/* Heading Typography - Medium's Sans-Serif Stack */
h1, h2, h3, h4, h5, h6 {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.84);  /* Pure black, Medium style */
  margin-top: 2em;
  margin-bottom: 0.46em;
  line-height: 1.25;
  letter-spacing: -0.022em;
  page-break-after: avoid;
}

h1 {
  font-size: 42px;
  page-break-before: always;  /* Chapters start on new page */
  margin-top: 0;
  padding-top: 2em;
  line-height: 1.15;
  letter-spacing: -0.028em;
}

h2 {
  font-size: 38px;         /* LARGER - stands out like chapter title */
  line-height: 1.2;
  letter-spacing: -0.026em;
  margin-top: 2em;
  page-break-before: always;  /* FORCE new page for chapters/activities */
  font-weight: 800;        /* BOLDER - emphasizes importance */
}

h3 {
  font-size: 26px;
  line-height: 1.3;
  margin-top: 1.6em;
}

h4 {
  font-size: 22px;
  line-height: 1.4;
  margin-top: 1.4em;
}

/* Paragraphs - Left-aligned (NOT justified) */
p {
  margin: 1.8em 0;
  text-align: left;  /* Medium uses left, NOT justify */
  orphans: 3;
  widows: 3;
}

/* Cover Image - Full Width, NO Visible Text */
body > p:first-of-type {
  margin: 0;
  padding: 0;
  line-height: 0;  /* Hides any alt text */
  page-break-after: always;
}

body > p:first-of-type img {
  max-width: 100% !important;
  width: 100% !important;
  height: auto;
  display: block;
  margin: 0;
  padding: 0;
  border: none;
  line-height: normal;
}

/* Hide ALL Figcaptions - CRITICAL! */
figcaption {
  display: none !important;  /* Completely hide figcaptions like "Cover", "Activity illustration" */
}

figure {
  margin: 2em auto;
  text-align: center;
}

/* All Other Images - FLAT DESIGN (No shadows/borders) */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 2em auto;
  border: none;           /* No borders */
  border-radius: 0;       /* No rounded corners */
  padding: 0;             /* No padding */
  background-color: transparent;
  box-shadow: none;       /* No shadows */
  page-break-inside: avoid;
  line-height: normal;    /* Reset line-height for image itself */
}

/* Lists - Clean and Readable */
ul, ol {
  margin: 1.8em 0;
  padding-left: 2em;
}

li {
  margin: 0.5em 0;
  line-height: 1.58;
}

/* Code Blocks */
code {
  font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
  font-size: 18px;
  background: rgba(0, 0, 0, 0.05);
  padding: 2px 6px;
  border-radius: 3px;
}

pre {
  background: rgba(0, 0, 0, 0.03);
  border-left: 3px solid rgba(0, 0, 0, 0.15);
  padding: 1em;
  overflow-x: auto;
  page-break-inside: avoid;
  font-size: 16px;
  line-height: 1.5;
}

pre code {
  background: transparent;
  padding: 0;
}

/* Tables - Monochrome with Word Wrapping */
table {
  border-collapse: collapse;
  width: 100%;
  margin: 2em 0;
  font-size: 18px;
  border: 1px solid rgba(0, 0, 0, 0.1);
  page-break-inside: avoid;
}

th {
  background-color: rgba(0, 0, 0, 0.05);  /* Subtle grey, NOT colored */
  color: rgba(0, 0, 0, 0.84);
  font-weight: 700;
  padding: 14px 16px;
  text-align: left;
  border-bottom: 2px solid rgba(0, 0, 0, 0.1);
  white-space: normal;      /* Allow text wrapping */
  word-wrap: break-word;    /* Break long words */
}

td {
  padding: 14px 16px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  vertical-align: top;
  white-space: normal;      /* Allow text wrapping */
  word-wrap: break-word;    /* Break long words */
  line-height: 1.58;
}

/* Blockquotes - Minimal Style */
blockquote {
  margin: 2em 0;
  padding: 1em 1.5em;
  background-color: rgba(0, 0, 0, 0.02);  /* Barely visible */
  border-left: 3px solid rgba(0, 0, 0, 0.68);  /* Subtle */
  font-size: 21px;
  font-style: italic;
  color: rgba(0, 0, 0, 0.68);
  page-break-inside: avoid;
}

/* Links - Subtle, Not Colored */
a {
  color: rgba(0, 0, 0, 0.84);  /* Same as body text */
  text-decoration: underline;
  text-decoration-color: rgba(0, 0, 0, 0.3);  /* Subtle */
  text-underline-offset: 2px;
  transition: text-decoration-color 0.2s ease;
}

a:hover {
  text-decoration-color: rgba(0, 0, 0, 0.84);  /* Darker on hover */
}

/* Page Breaks */
figure, table, pre {
  page-break-inside: avoid;
}

/* Table of Contents - Clean */
nav#TOC {
  margin: 2em 0;
  padding: 1em;
  background-color: rgba(0, 0, 0, 0.02);
}

nav#TOC ul {
  list-style-type: none;
  padding-left: 0;
}

nav#TOC li {
  margin: 0.5em 0;
  line-height: 1.58;
}

nav#TOC a {
  color: rgba(0, 0, 0, 0.84);
  text-decoration: none;
}

nav#TOC a:hover {
  text-decoration: underline;
}

/* Print Media Optimizations */
@media print {
  body {
    background-color: white;
    padding: 0;
    font-size: 11pt;  /* Smaller for print */
    max-width: 100%;
  }

  h1 {
    page-break-before: always;
    font-size: 24pt;
  }

  h2 {
    font-size: 18pt;
  }

  h3 {
    font-size: 14pt;
  }

  a[href]:after {
    content: none;  /* Don't print URLs */
  }
}
</style>
```

## Typography Rules (CRITICAL for Visual Appeal)

**Medium.com-Inspired Typographic Scale:**
- h1: 42px - Major chapters
- h2: 34px - Sections
- h3: 26px - Subsections
- h4: 22px - Sub-subsections
- body: 21px - Base size
- Line height: 1.58 (Medium's research-backed ratio)
- Letter spacing: Negative values for tighter, more professional look

**Monochrome Color Palette (CRITICAL):**
- Body text: rgba(0, 0, 0, 0.84) (Medium's exact color)
- Headings: rgba(0, 0, 0, 0.84) (BLACK, not colored)
- Links: rgba(0, 0, 0, 0.84) with subtle underline (NOT blue)
- Background: #ffffff (pure white, NOT off-white)
- Tables: rgba(0, 0, 0, 0.05) for headers (subtle grey, NOT brand colors)
- Borders: rgba(0, 0, 0, 0.08) to rgba(0, 0, 0, 0.1)

**Why Monochrome:**
- Brand colors are for marketing materials, NOT ebook body text
- Pure black and white creates professional, timeless appearance
- Matches Medium.com's proven readability
- Better for digital reading on various screens

**Professional Appearance Rules:**
- ✅ NO emojis (remove ALL emojis for professional look)
- ✅ NO YAML metadata (Duration, Prep, Group, Setting lines)
- ✅ Two font families: Charter (body) + System Sans-Serif (headings)
- ✅ Left-aligned text (NOT justified - matches Medium)
- ✅ Images flat (NO shadows, borders, padding)
- ✅ Pure white background (NOT off-white)
- ✅ Strategic white space throughout

## Content Cleaning Functions (CRITICAL)

### Remove ALL Emojis

**Why:** Emojis make ebooks look unprofessional and childish. Remove them completely.

```python
def remove_emojis(text: str) -> str:
    """Remove all emojis from text for professional appearance"""
    # Comprehensive emoji pattern covering all Unicode ranges
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\u2600-\u26FF"          # Miscellaneous Symbols
        u"\u2700-\u27BF"          # Dingbats
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)
```

### Remove YAML Metadata

**Why:** Lines like "⏰ Duration: 5 minutes", "👥 Group:", etc. clutter the ebook and provide no value to readers.

```python
def remove_yaml_metadata(content: str) -> str:
    """Remove YAML metadata blocks from activities"""
    lines = content.split('\n')
    cleaned_lines = []

    for line in lines:
        # Skip lines that look like metadata with emojis
        # Examples: "⏰ Duration:", "👥 Group:", "🏫 Setting:", etc.
        if re.match(r'^\s*[^\w\s]+\s*(Duration|Prep|Group|Setting|Subjects|Energy|Tags):', line, re.IGNORECASE):
            continue
        # Skip lines with emoji bullets followed by metadata
        if re.match(r'^\s*[•◦▪▫]\s*[^\w\s]+\s*\w+:', line):
            continue
        cleaned_lines.append(line)

    return '\n'.join(cleaned_lines)
```

### Integration into Processing Pipeline

**CRITICAL:** Apply these functions in the correct order:

```python
def read_and_process_file(file_path: Path) -> str:
    """Read markdown file, clean, and fix paths"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Remove YAML metadata FIRST
        content = remove_yaml_metadata(content)

        # 2. Remove emojis SECOND
        content = remove_emojis(content)

        # 3. Fix image paths LAST
        content = fix_image_paths(content, file_path)

        return content
    except Exception as e:
        print(f"  ❌ Error reading {file_path}: {e}")
        return ""
```

## HTML Post-Processing (CRITICAL)

After Pandoc generates HTML, you MUST perform these post-processing steps:

### 1. Remove Pandoc Title Header

**Problem:** Pandoc automatically generates a title header from the last markdown file processed, resulting in unwanted titles like "Transition Countdown" appearing at the top of the ebook.

**Solution:**
```python
import re

# Remove the title header
html_content = re.sub(
    r'<header id="title-block-header">.*?</header>',
    '',
    html_content,
    flags=re.DOTALL
)
```

### 2. Table of Contents Strategy

**Problem:** Pandoc's auto-generated TOC can be cluttered and includes unwanted subsections. Plus, users often want a custom-formatted TOC that matches their book's style.

**Solutions (Choose One):**

#### Option A: Pandoc Auto-Generated TOC (Simple but Limited)
Use `--toc-depth=1` to show only major chapters:
```bash
pandoc complete-ebook.md \
  -f markdown+smart \
  -t html5 \
  --standalone \
  --toc \
  --toc-depth=1 \  # CRITICAL: Only chapters, not subsections
  --resource-path . \
  -o complete-ebook.html
```

**Pros:** Quick, automatic
**Cons:** Limited formatting control, may still look cluttered

#### Option B: Manual TOC with Anchor Links (Recommended for Professional Look)
Create a custom TOC in a markdown file (e.g., `03-table-of-contents.md`) using anchor links:

```markdown
# Table of Contents

## Part I: Foundation

### [Chapter 1: Why Nano Activities Transform Learning](#why-nano-activities-transform-learning)
- The Attention Crisis
- What Makes "Nano" Different
- The Compound Effect

### [Chapter 2: The Science Behind Short Engagement](#the-science-behind-short-engagement)
- Cognitive Science Foundations
- Pedagogical Principles

## Part II: The Activity Library

### [Chapter 4: Attention Grabbers & Energizers](#attention-grabbers-energizers)
### [Chapter 5: Prior Knowledge Activators](#prior-knowledge-activators)

## Appendices

### [Appendix A: Activities by Time](#appendix-a-activities-by-time)
### [Appendix B: Activities by Subject](#appendix-b-activities-by-subject)
```

**Anchor ID Rules:**
- Lowercase everything
- Replace spaces with hyphens: `Chapter 1: Title` → `#chapter-1-title`
- Remove special characters: `&`, `:`, etc.
- Remove numbers in parentheses: `(25 Activities)` → omit
- Examples:
  - "Chapter 1: Why Nano Activities Transform Learning" → `#why-nano-activities-transform-learning`
  - "Appendix A: Activities by Time" → `#appendix-a-activities-by-time`

**Generate HTML WITHOUT auto-TOC:**
```bash
pandoc complete-ebook.md \
  -f markdown+smart \
  -t html5 \
  --standalone \
  # NO --toc flag! Manual TOC is in the markdown
  --resource-path . \
  -o complete-ebook.html
```

**Pros:**
- Clean, professional appearance
- Full formatting control
- Compact (only show what matters)
- Links work perfectly in PDF

**Cons:** Requires manually creating anchor links for all chapters

### 3. Hide ALL Figcaptions

**Problem:** Pandoc generates `<figcaption>` elements with text like "Cover", "Activity illustration", which appear under images in the final PDF.

**Solution:** Already included in CSS above:
```css
figcaption {
  display: none !important;  /* Completely hide all figcaptions */
}
```

### Complete HTML Post-Processing Function

```python
def post_process_html(build_dir: Path):
    """Clean up HTML after Pandoc generation"""
    html_file = build_dir / "complete-ebook.html"
    html_content = html_file.read_text(encoding='utf-8')

    # 1. Remove Pandoc title header
    html_content = re.sub(
        r'<header id="title-block-header">.*?</header>',
        '',
        html_content,
        flags=re.DOTALL
    )

    # 2. Inject professional CSS (includes figcaption hiding)
    css = """<style>/* [Insert complete Medium.com CSS from above] */</style>"""
    html_content = html_content.replace('</head>', f'{css}\n</head>')

    # 3. Write cleaned HTML
    html_file.write_text(html_content, encoding='utf-8')
    print("✅ HTML post-processed: title removed, CSS injected, figcaptions hidden")
```

## Common Pitfalls & Solutions

### Pitfall 1: Images Not Showing
**Debug Steps:**
```bash
# 1. Check console output for warnings
# Look for: "⚠️  WARNING: Image not found:"
# This tells you exactly which images are missing

# 2. Verify images were copied to build directory
find output-pdfs/build -type f \( -name "*.png" -o -name "*.jpg" \) | wc -l
# Should match or exceed source image count

# 3. Check paths in compiled markdown
grep "!\[" output-pdfs/build/complete-ebook.md | head -10
# Should show build-relative paths like:
#   ![](assets/images/foo.png)    ✓ GOOD
#   ![](media/bar.jpg)             ✓ GOOD
#   ![](../../old/path.png)        ✗ BAD - still has ../

# 4. Test HTML first (CRITICAL)
open output-pdfs/build/complete-ebook.html
# Check browser console for 404 errors
# Right-click broken images → Inspect to see attempted path

# 5. Verify wkhtmltopdf flag
# Always use: --enable-local-file-access
```

**Solution:**
- Full Path Resolution (in <critical_knowledge>) handles this automatically
- It validates each image exists and prints warnings for missing ones
- Check console output for "⚠️ WARNING" messages
- Fix missing images before proceeding to PDF

### Pitfall 2: Chapter Breaks Not Working
```python
# Method 1: Use \newpage in markdown
out.write("\n\\newpage\n\n# Chapter Title\n\n")

# Method 2: CSS (already in style above)
h1 { page-break-before: always; }
```

### Pitfall 3: Cover Image Wrong Size
```python
# Verify before using
from PIL import Image
cover = Image.open('cover.png')
width, height = cover.size
# Should be 2550 x 3300 pixels (8.5 x 11 @ 300dpi)
if width != 2550 or height != 3300:
    print(f"⚠️  Cover incorrect: {width}x{height}")
    print("   Required: 2550x3300 pixels")
```

### Pitfall 4: File Size Too Large (>100 MB)
**Solution:**
- Use DPI 96 (NOT 150 or 300) for digital distribution
- Use --image-quality 85
- Switch from WeasyPrint to wkhtmltopdf
- Target: 30-50 MB for 500 pages

### Pitfall 5: Visible Text Under Images (Figcaptions)
**Symptom:** Text like "Cover", "Activity illustration" appears below images

**Root Cause:** Pandoc generates `<figcaption>` elements that are visible by default

**Solution:**
- Add `figcaption { display: none !important; }` to CSS
- This is already included in the Medium.com CSS template above
- MUST be applied during HTML post-processing

### Pitfall 6: Unwanted Title at Top of Ebook
**Symptom:** Title like "Transition Countdown" appears at the beginning

**Root Cause:** Pandoc generates `<header id="title-block-header">` from last markdown file

**Solution:**
- Remove the header element during HTML post-processing
- See "HTML Post-Processing" section above for code
- Use regex to strip the entire header block

## Complete Compilation Script Template

```python
#!/usr/bin/env python3
import re
import shutil
import subprocess
from pathlib import Path

def compile_ebook(content_dir: Path, build_dir: Path):
    """Compile ebook with proper structure and fixed paths."""

    output_file = build_dir / "complete-ebook.md"

    with open(output_file, 'w', encoding='utf-8') as out:
        # 1. COVER IMAGE FIRST (CRITICAL)
        cover_path = content_dir / "assets/images/covers/ebook-cover.png"
        if not cover_path.exists():
            print("❌ STOP: Cover image required!")
            print("   Size: 8.5 x 11 inches (2550 x 3300 pixels)")
            return False

        out.write("---\n")
        out.write("title: Book Title\n")
        out.write("author: Author Name\n")
        out.write("---\n\n")
        out.write("![Cover](assets/images/covers/ebook-cover.png)\n\n")
        out.write("\\newpage\n\n")

        # 2. FRONT MATTER
        front_matter = content_dir / "front-matter"
        if front_matter.exists():
            for file in sorted(front_matter.glob("*.md")):
                content = file.read_text(encoding='utf-8')
                content = fix_image_paths(content, file, content_dir, build_dir)
                out.write(content)
                out.write("\n\\newpage\n\n")

        # 3. CHAPTERS (main content)
        chapters_dir = content_dir / "chapters"
        if chapters_dir.exists():
            for chapter in sorted(chapters_dir.glob("*")):
                if chapter.is_dir():
                    out.write(f"\n\\newpage\n\n")
                    out.write(f"# {chapter.name.replace('-', ' ').title()}\n\n")

                    for md_file in sorted(chapter.glob("*.md")):
                        content = md_file.read_text(encoding='utf-8')
                        content = fix_image_paths(content, md_file, content_dir, build_dir)
                        out.write(content)
                        out.write("\n\n")

        # 4. BACK MATTER
        back_matter = content_dir / "back-matter"
        if back_matter.exists():
            for file in sorted(back_matter.glob("*.md")):
                out.write("\n\\newpage\n\n")
                content = file.read_text(encoding='utf-8')
                content = fix_image_paths(content, file, content_dir, build_dir)
                out.write(content)

    print(f"✓ Ebook compiled: {output_file}")
    return True

def fix_image_paths(content: str, markdown_file: Path, repo_root: Path, build_dir: Path) -> str:
    """
    Fix image paths using Full Path Resolution strategy.
    See <critical_knowledge> section for complete implementation details.

    This validates images exist and copies them to build directory.
    """
    import shutil

    def resolve_and_copy(match):
        alt_text = match.group(1)
        image_path = match.group(2)

        # Skip URLs
        if image_path.startswith(('http://', 'https://', '//')):
            return match.group(0)

        # Resolve to actual file on disk
        if image_path.startswith('/'):
            source_image = Path(image_path)
        else:
            source_image = (markdown_file.parent / image_path).resolve()

        # Verify image exists
        if not source_image.exists():
            print(f"⚠️  WARNING: Image not found: {source_image}")
            return match.group(0)

        # Determine target path in build directory
        try:
            rel_path = source_image.relative_to(repo_root)
            target_image = build_dir / rel_path
        except ValueError:
            target_image = build_dir / "assets" / "images" / source_image.name

        # Copy image to build directory
        target_image.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_image, target_image)

        # Return build-relative path
        build_relative = target_image.relative_to(build_dir)
        return f'![{alt_text}]({build_relative.as_posix()})'

    return re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', resolve_and_copy, content)

def generate_html(build_dir: Path):
    """Generate HTML from markdown with shallow TOC (chapters only)."""
    subprocess.run([
        'pandoc', 'complete-ebook.md',
        '-f', 'markdown+smart',
        '-t', 'html5',
        '--standalone',
        '--toc',
        '--toc-depth=1',  # CRITICAL: Only show chapters, not subsections
        '--resource-path', '.',
        '-o', 'complete-ebook.html'
    ], cwd=build_dir, check=True)

def add_professional_css(build_dir: Path):
    """Inject professional CSS into HTML and remove Pandoc title header."""
    html_file = build_dir / "complete-ebook.html"
    html_content = html_file.read_text(encoding='utf-8')

    # CRITICAL: Remove Pandoc-generated title header
    # Pandoc sometimes adds <header id="title-block-header"> with unwanted title
    html_content = re.sub(
        r'<header id="title-block-header">.*?</header>',
        '',
        html_content,
        flags=re.DOTALL
    )

    # Inject professional CSS
    css = """<style>/* [Insert complete CSS from above] */</style>"""
    html_content = html_content.replace('</head>', f'{css}\n</head>')
    html_file.write_text(html_content, encoding='utf-8')

def generate_pdf(build_dir: Path, output_name: str):
    """Generate PDF with wkhtmltopdf."""
    subprocess.run([
        'wkhtmltopdf',
        '--page-size', 'Letter',
        '--margin-top', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '15mm',
        '--margin-right', '15mm',
        '--enable-local-file-access',
        '--enable-internal-links',
        '--print-media-type',
        '--dpi', '96',
        '--image-quality', '85',
        'complete-ebook.html',
        f'../{output_name}-professional.pdf'
    ], cwd=build_dir, check=True)
```

## Quality Validation Checklist

Before delivering PDF, verify:
- [ ] PDF opens without errors
- [ ] Cover image on page 1 (NO visible alt text or "Cover" caption)
- [ ] All chapters start on new pages
- [ ] Images visible throughout (spot check every 50 pages)
- [ ] NO visible text under images (no figcaptions like "Activity illustration")
- [ ] NO unwanted title at top (like "Transition Countdown")
- [ ] File size reasonable (depends on image count: ~150 KB per image at DPI 96)
- [ ] TOC navigation works (click several links)
- [ ] TOC shows only chapters, not every subsection
- [ ] Professional appearance (NO emojis anywhere)
- [ ] NO YAML metadata visible (Duration, Prep, Group, etc.)
- [ ] Pure monochrome colors (black on white, NO brand colors in body)
- [ ] Images are flat (NO shadows, borders, or embellishments)
- [ ] Tables have proper line breaks (long text wraps correctly)
- [ ] Links are subtle (black with underline, NOT blue)
- [ ] Text is left-aligned (NOT justified)
- [ ] Typography matches Medium.com (Charter body, system sans headings)
- [ ] No broken formatting
- [ ] Ready for commercial sale

</critical_knowledge>

<process>
## Phase 1: Repository Analysis

Start with friendly greeting:
"Hi! I'm your Ebook Production Engineer. I'll transform your markdown repository into a professional, ready-to-sell PDF ebook optimized for digital distribution.

📁 Analyzing repository: $1"

Then analyze:
1. **Repository Structure**
   - Scan directory: $1
   - Identify chapters/sections (look for: chapters/, content/, docs/, etc.)
   - Find all markdown files (*.md)
   - Locate assets directory (images, covers)
   - Count total images
   - Estimate page count

2. **Content Organization**
   - Detect front matter (title page, copyright, TOC)
   - Identify main chapters/sections
   - Find back matter (about author, references, appendices)
   - Analyze ordering/structure

3. **Image Inventory**
   - Total images found
   - Image paths patterns (../../assets, ../assets, etc.)
   - Image formats (PNG, JPG)
   - Verify all images have references in markdown

Report findings:
"📊 Repository Analysis Complete:
- Total markdown files: [count]
- Chapters/Sections: [list]
- Images found: [count]
- Estimated pages: [estimate]
- Structure: [well-organized / needs organization]"

## Phase 2: Requirements Gathering

Ask critical questions (DO NOT PROCEED without answers):

"📋 EBOOK REQUIREMENTS

I need a few details to create your professional ebook:

### 1. Cover Image (CRITICAL)
${2:-auto-detect} status: [found/not found]

Cover image location detected: [path or "not found"]

⚠️  A professional cover image is REQUIRED (8.5 x 11 inches, 2550 x 3300 pixels)

Options:
a) I found a cover at: [path] - Use this?
b) You have a cover - provide path
c) You need to create one - I'll wait

**Your choice (a/b/c):**

### 2. Page Size & Format
**Recommended for digital distribution:** Letter (8.5 x 11 inches)

Choose:
a) Letter (8.5 x 11) - Most common, tablet-friendly
b) A4 (8.27 x 11.69) - International standard
c) Custom size - specify dimensions

**Your choice (default: a):**

### 3. Target Distribution
a) Digital only (Gumroad, Payhip, email) - Optimized DPI 96
b) Print-on-demand - Higher DPI 300
c) Both - Generate two versions

**Your choice (default: a):**

### 4. Branding & Style
**Title:** [Auto-detected or ask]
**Author:** [Auto-detected from repo or ask]
**Professional appearance:**
- Minimal emojis
- Modern fonts (Georgia + Helvetica)
- Screen-friendly colors
- Professional layout

Confirm these defaults? (yes/no)

### 5. Quality Requirements
This ebook will be:
- ✅ Publication-ready
- ✅ Professional typography
- ✅ All images embedded
- ✅ Interactive TOC
- ✅ Suitable for commercial sale

Proceed with professional quality standards? (yes)"

WAIT for user responses before continuing.

## Phase 3: Generate Execution Plan

Create comprehensive plan with:
"Excellent! Creating your ebook execution plan..."

First, create output directory:
`Bash: mkdir -p .project-management/ebook`

Then generate plan at: ${3:-.project-management/ebook/ebook-execution-plan.md}

</process>

<execution_plan_structure>

# Professional Ebook Generation - Execution Plan

**Repository:** $1
**Cover Image:** [path]
**Page Size:** [Letter/A4]
**Distribution:** [Digital/Print/Both]
**Generated:** [timestamp]

---

## Usage Instructions

This plan serves THREE purposes:
1. **Project Plan** - What needs to be done
2. **Progress Tracker** - What's completed
3. **Context Memory** - How it was done

### Workflow
1. Read this plan at session start
2. Execute tasks in order (never skip)
3. Update status after EACH task
4. Document discoveries in task_notes
5. Validate before proceeding to next task

---

## Quick Reference

### Repository Details
- **Total Markdown Files:** [count]
- **Total Images:** [count]
- **Chapters:** [list]
- **Estimated Pages:** [estimate]

### Output Specifications
- **Format:** PDF (optimized for digital reading)
- **Page Size:** [8.5 x 11 inches / A4]
- **DPI:** [96 for digital / 300 for print]
- **Target File Size:** 30-50 MB (excellent quality)
- **Typography:** Georgia (body) + Helvetica (headings)
- **Color Scheme:** Near-black (#1a1a1a) on off-white (#fafafa)

### Critical Files
- **Compilation Script:** `compile_ebook.py`
- **HTML Template:** `output-pdfs/build/complete-ebook.html`
- **Final PDF:** `output-pdfs/[title]-professional.pdf`

---

## Pre-Flight Checklist

```yaml
pre_flight:
  cover_image_verified: false          # CRITICAL - DO NOT PROCEED without this
  cover_size_correct: false            # Must be 2550x3300px (8.5x11 @ 300dpi)
  repository_structure_understood: false
  image_paths_analyzed: false          # Know all path patterns (../../, ../, ./)
  tools_installed: false               # pandoc, wkhtmltopdf
  output_directory_created: false
  critical_knowledge_reviewed: false   # Review <critical_knowledge> section above
```

---

## Story Breakdown and Status

```yaml
stories:
  - story_id: "EBOOK-001"
    story_title: "Environment Setup & Validation"
    story_description: "Prepare development environment and validate all requirements"
    story_status: "not_started"  # not_started | in_progress | completed
    tasks:
      - task_id: "TASK-001.1"
        task_title: "Verify tools installed"
        task_description: "Check pandoc and wkhtmltopdf are available"
        task_acceptance_criteria:
          - "pandoc --version returns 3.0+"
          - "wkhtmltopdf --version returns 0.12.6+"
        task_commands: |
          pandoc --version
          wkhtmltopdf --version
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-001.2"
        task_title: "Validate cover image"
        task_description: "Verify cover image exists and has correct dimensions"
        task_acceptance_criteria:
          - "Cover image exists at specified path"
          - "Dimensions are 2550x3300 pixels (8.5x11 @ 300dpi)"
          - "Format is PNG or high-quality JPG"
        task_commands: |
          # Use Python PIL or similar to check dimensions
          from PIL import Image
          img = Image.open('[cover-path]')
          print(f"Size: {img.size}")  # Should be (2550, 3300)
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-001.3"
        task_title: "Analyze image paths in markdown"
        task_description: "Identify ALL image path patterns used in markdown files"
        task_acceptance_criteria:
          - "All image path patterns documented"
          - "Know which files use ../../assets, ../assets, ./assets"
        task_commands: |
          grep -r "!\[.*\](" $1 | grep -o '([^)]*)' | sort -u
        task_status: "not_started"
        task_notes: "Image path patterns found: [to be filled]"

  - story_id: "EBOOK-002"
    story_title: "Build System Setup"
    story_description: "Create build directories and compilation scripts"
    story_status: "not_started"
    tasks:
      - task_id: "TASK-002.1"
        task_title: "Create build directory structure"
        task_description: "Set up organized build directories for compilation"
        task_acceptance_criteria:
          - "output-pdfs/build/ directory created"
          - "All assets will be copied here"
        task_commands: |
          mkdir -p output-pdfs/build
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-002.2"
        task_title: "Copy all assets to build directory"
        task_description: "Copy ENTIRE assets directory to prevent image path issues"
        task_acceptance_criteria:
          - "All images copied to output-pdfs/build/assets/"
          - "Image count matches source"
          - "Directory structure preserved"
        task_commands: |
          cp -r [repo-path]/assets output-pdfs/build/
          # Verify count
          find output-pdfs/build/assets -type f \( -name "*.png" -o -name "*.jpg" \) | wc -l
        task_status: "not_started"
        task_notes: "Images copied: [count]"

      - task_id: "TASK-002.3"
        task_title: "Create compilation script"
        task_description: "Build Python script to compile markdown with image path fixes"
        task_acceptance_criteria:
          - "Script handles ALL image path patterns"
          - "Script compiles in correct order: front → chapters → back"
          - "Script adds \\newpage for chapter breaks"
        task_reference: "See <critical_knowledge> section above for complete script template"
        task_status: "not_started"
        task_notes: ""

  - story_id: "EBOOK-003"
    story_title: "Content Compilation"
    story_description: "Compile all markdown into single ebook file with fixed image paths"
    story_status: "not_started"
    tasks:
      - task_id: "TASK-003.1"
        task_title: "Fix image paths in all markdown"
        task_description: "Convert relative image paths to build-directory-relative paths"
        task_acceptance_criteria:
          - "All ../../assets/images/ → assets/images/"
          - "All ../assets/images/ → assets/images/"
          - "All ./assets/images/ → assets/images/"
        task_critical_notes: |
          THIS IS THE #1 ISSUE THAT BREAKS EBOOKS!
          Use regex substitution to handle ALL patterns.
          Test compilation output to verify paths are correct.
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-003.2"
        task_title: "Compile markdown in correct order"
        task_description: "Merge all markdown files maintaining proper book structure"
        task_acceptance_criteria:
          - "Cover image first"
          - "Front matter (title, copyright, TOC)"
          - "Chapters in logical order"
          - "Back matter (about author, references)"
          - "\\newpage between chapters"
        task_output: "output-pdfs/build/complete-ebook.md"
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-003.3"
        task_title: "Validate compiled markdown"
        task_description: "Verify all content and images are present"
        task_acceptance_criteria:
          - "File size ~1.5 MB (indicates content present)"
          - "Image count matches expected"
          - "No broken markdown syntax"
        task_commands: |
          ls -lh output-pdfs/build/complete-ebook.md
          grep -o "!\[.*\](assets/images.*)" output-pdfs/build/complete-ebook.md | wc -l
        task_status: "not_started"
        task_notes: ""

  - story_id: "EBOOK-004"
    story_title: "HTML Generation & Styling"
    story_description: "Convert markdown to HTML with professional CSS styling"
    story_status: "not_started"
    tasks:
      - task_id: "TASK-004.1"
        task_title: "Generate HTML from markdown"
        task_description: "Use Pandoc to create standalone HTML with TOC"
        task_acceptance_criteria:
          - "HTML file generated"
          - "TOC included and properly linked"
          - "All images references correct"
        task_commands: |
          cd output-pdfs/build
          pandoc complete-ebook.md \\
            -f markdown+smart \\
            -t html5 \\
            --standalone \\
            --toc \\
            --toc-depth=2 \\
            --resource-path . \\
            -o complete-ebook.html
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-004.2"
        task_title: "Add professional CSS styling"
        task_description: "Inject screen-optimized CSS for digital reading experience"
        task_acceptance_criteria:
          - "Georgia serif body font"
          - "Helvetica sans-serif headings"
          - "Line height 1.65 (golden ratio)"
          - "Near-black (#1a1a1a) on off-white (#fafafa)"
          - "h1 forces new pages"
          - "Images centered at 80% width"
        task_reference: "See <critical_knowledge> section above for complete CSS"
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-004.3"
        task_title: "Validate HTML (CRITICAL CHECKPOINT)"
        task_description: "Open HTML in browser and verify ALL images load"
        task_acceptance_criteria:
          - "HTML opens without errors"
          - "ALL images visible (scroll through entire document)"
          - "Cover image displays"
          - "TOC links work"
          - "Chapter breaks visible"
        task_validation: |
          STOP HERE AND MANUALLY VALIDATE!

          1. Open: output-pdfs/build/complete-ebook.html
          2. Scroll through ENTIRE document
          3. Check for broken images (right-click → inspect any suspicious images)
          4. Click TOC links to verify navigation
          5. Only proceed if 100% validated
        task_status: "not_started"
        task_notes: "Validation result: [PASS/FAIL] - Details:"

  - story_id: "EBOOK-005"
    story_title: "PDF Generation"
    story_description: "Convert HTML to professional PDF optimized for digital distribution"
    story_status: "not_started"
    tasks:
      - task_id: "TASK-005.1"
        task_title: "Generate PDF with wkhtmltopdf"
        task_description: "Create final PDF with optimal settings for digital reading"
        task_acceptance_criteria:
          - "PDF generated successfully"
          - "File size 30-50 MB (good compression)"
          - "All images embedded"
          - "TOC links work in PDF"
        task_commands: |
          cd output-pdfs/build
          wkhtmltopdf \\
            --page-size Letter \\
            --margin-top 20mm \\
            --margin-bottom 20mm \\
            --margin-left 15mm \\
            --margin-right 15mm \\
            --enable-local-file-access \\
            --enable-internal-links \\
            --print-media-type \\
            --dpi 96 \\
            --image-quality 85 \\
            complete-ebook.html \\
            ../[title]-professional.pdf
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-005.2"
        task_title: "Validate final PDF"
        task_description: "Comprehensive quality check of final ebook"
        task_acceptance_criteria:
          - "PDF opens without errors"
          - "Cover image on page 1"
          - "All chapters start on new pages"
          - "Images visible throughout (spot check)"
          - "File size reasonable (30-50 MB)"
          - "TOC navigation works"
        task_validation_checklist: |
          ☐ Open PDF in Adobe Reader/Preview
          ☐ Check page 1 - cover image
          ☐ Scroll to page 10 - images loading?
          ☐ Scroll to page 50 - images loading?
          ☐ Check chapter starts - new pages?
          ☐ Click TOC links - navigation works?
          ☐ Check file size - reasonable?
          ☐ Professional appearance?
          ☐ Ready to sell?
        task_status: "not_started"
        task_notes: "Quality validation result:"

  - story_id: "EBOOK-006"
    story_title: "Quality Assurance & Delivery"
    story_description: "Final checks and prepare for distribution"
    story_status: "not_started"
    tasks:
      - task_id: "TASK-006.1"
        task_title: "Final quality review"
        task_description: "Comprehensive review against professional standards"
        task_acceptance_criteria:
          - "All visual appeal checklist items pass"
          - "Digital reading experience optimized"
          - "Professional typography verified"
          - "No excessive emojis"
          - "Suitable for commercial sale"
        task_reference: "See <critical_knowledge> section above for Quality Validation Checklist"
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-006.2"
        task_title: "Generate delivery package"
        task_description: "Prepare final deliverables and documentation"
        task_acceptance_criteria:
          - "Final PDF with professional filename"
          - "Generation metadata documented"
          - "Sample pages extracted (optional)"
          - "Delivery summary created"
        task_deliverables: |
          1. [Title]-Professional-Ebook.pdf (main product)
          2. generation-metadata.json (technical details)
          3. DELIVERY-SUMMARY.md (overview)
          4. screenshots/ (quality verification)
        task_status: "not_started"
        task_notes: ""

      - task_id: "TASK-006.3"
        task_title: "Update this execution plan"
        task_description: "Document final status and any lessons learned"
        task_acceptance_criteria:
          - "All task_notes filled in"
          - "All statuses updated to 'completed'"
          - "Any issues/solutions documented"
        task_status: "not_started"
        task_notes: ""
```

---

## Architecture & Technical Decisions

### Tool Selection: wkhtmltopdf
**Decision:** Use wkhtmltopdf for PDF generation (not WeasyPrint or LaTeX)

**Reasoning:**
- Most reliable (battle-tested WebKit engine)
- Best compression (4-5x smaller than WeasyPrint)
- Stable across systems
- No large dependencies

**Impact:** Consistent, professional output with reasonable file sizes

### Image Path Strategy
**Decision:** Copy ALL assets to build directory and fix paths to be build-relative

**Reasoning:**
- Markdown files use various relative path patterns
- Compilation changes working directory
- Absolute paths won't work in final PDF

**Impact:** 100% image loading success (was 90% failure rate without this)

### Digital-First Optimization
**Decision:** DPI 96, image quality 85, screen-friendly colors

**Reasoning:**
- Target is digital distribution only
- Screens render at 96 DPI
- Higher DPI wastes file size

**Impact:** 30-50 MB files (vs 150+ MB for print settings)

### Typography Choices
**Decision:** Georgia (body) + Helvetica (headings)

**Reasoning:**
- Georgia: Warm, readable serif for body text
- Helvetica: Clean, modern sans-serif for structure
- Both are universally available

**Impact:** Professional appearance with excellent readability

---

## Common Issues & Solutions

### Issue 1: Images Not Showing in PDF
**Symptom:** PDF generates but images are missing

**Root Cause:** Relative paths (../../assets) break when markdown is compiled

**Solution:**
1. Copy ALL assets to build directory
2. Fix ALL path patterns: ../../, ../, ./
3. Use --enable-local-file-access flag
4. Validate HTML before PDF

**Prevention:** Follow compilation script in guide exactly

### Issue 2: Chapters Not Starting on New Pages
**Symptom:** Content flows together without breaks

**Solution:**
- Add \newpage in markdown between chapters
- Use CSS: h1 { page-break-before: always; }

### Issue 3: File Size Too Large (>100 MB)
**Symptom:** PDF is 150+ MB

**Cause:** DPI too high or images uncompressed

**Solution:**
- Use DPI 96 (not 150 or 300) for digital
- Use --image-quality 85
- Check if WeasyPrint was used (switch to wkhtmltopdf)

### Issue 4: Cover Image Wrong Size
**Symptom:** Cover stretched or pixelated

**Solution:**
- Verify cover is 2550x3300 pixels
- Use high-quality source image
- Check aspect ratio is 8.5:11

---

## Commands Reference

```bash
# Setup
brew install pandoc wkhtmltopdf

# Verify installation
pandoc --version
wkhtmltopdf --version

# Check image dimensions (Python)
python3 -c "from PIL import Image; img=Image.open('[cover-path]'); print(img.size)"

# Count images in repository
find [repo-path] -type f \( -name "*.png" -o -name "*.jpg" \) | wc -l

# Compile markdown (manual approach)
cd output-pdfs/build
pandoc complete-ebook.md -f markdown+smart -t html5 --standalone --toc -o complete-ebook.html

# Generate PDF
cd output-pdfs/build
wkhtmltopdf --enable-local-file-access --page-size Letter --dpi 96 complete-ebook.html ../final.pdf

# Check PDF file size
ls -lh output-pdfs/[title]-professional.pdf
```

---

## Professional Standards Checklist

```yaml
professional_standards:
  visual_design:
    typography_hierarchy: false        # h1 24pt, h2 18pt, body 11pt
    line_height_optimal: false         # 1.65 for body
    consistent_spacing: false          # Vertical rhythm maintained
    image_placement: false             # Centered, 80% width, breathing room
    white_space_balance: false         # Not cramped, not sparse

  digital_optimization:
    screen_friendly_colors: false      # Near-black on off-white
    optimal_dpi: false                 # 96 DPI for screens
    clickable_toc: false               # Interactive navigation
    reasonable_file_size: false        # 30-50 MB target

  professional_appearance:
    cover_image_professional: false    # High quality, correct size
    minimal_emojis: false              # Professional, not casual
    consistent_branding: false         # Fonts, colors consistent
    no_broken_elements: false          # All images, links work

  commercial_readiness:
    publication_quality: false         # Suitable for sale
    all_content_included: false        # Nothing missing
    properly_formatted: false          # Chapters, sections clear
    tested_on_devices: false           # Works on tablets, laptops
```

---

## Next Steps After Completion

1. **Test on Multiple Devices**
   - iPad/tablet
   - Laptop
   - E-reader (if applicable)

2. **Get Feedback**
   - Send to beta readers
   - Check usability
   - Verify all images visible

3. **Prepare for Distribution**
   - Upload to sales platform (Gumroad, Payhip)
   - Set pricing
   - Write product description

4. **Marketing Assets**
   - Extract sample pages
   - Create preview PDF (first 20 pages)
   - Take screenshots for promotion

---

## Resources

- **This Command:** Contains all necessary information (self-contained)
- **wkhtmltopdf Docs:** https://wkhtmltopdf.org/usage/wkhtmltopdf.txt
- **Pandoc Manual:** https://pandoc.org/MANUAL.html
- **Typography Reference:** Butterick's Practical Typography

---

**Plan Status:** Active
**Last Updated:** [timestamp]
**Ebook Status:** Not Started → In Progress → Completed

</execution_plan_structure>

<guidelines>
- NEVER skip the cover image verification
- ALWAYS fix ALL image path patterns (../../, ../, ./)
- ALWAYS validate HTML before generating PDF
- ALWAYS use DPI 96 for digital distribution
- Reference the <critical_knowledge> section for all implementation details
- Update task_notes after EVERY task
- Test on actual devices before declaring complete
</guidelines>

<validation>
Before finalizing plan:
✓ Repository structure analyzed
✓ All image paths identified
✓ Cover image verified
✓ Requirements gathered
✓ Tasks ordered by dependencies
✓ Critical issues highlighted
✓ Commands tested and accurate
✓ Junior developer could execute independently
</validation>

<completion>
After generating plan:

"✅ EBOOK EXECUTION PLAN CREATED

Your comprehensive ebook generation plan is ready at:
${3:-.project-management/ebook/ebook-execution-plan.md}

📚 What's Included:
- Complete task breakdown with status tracking
- All commands tested and ready
- Image path fixes (critical!)
- Professional styling guidelines
- Quality validation checklists
- Common issues & solutions

🎯 Next Steps:
1. Review the plan thoroughly
2. Start with EBOOK-001 (Environment Setup)
3. Follow tasks in order (never skip!)
4. Update status after each task
5. Reference the <critical_knowledge> section for all implementation details

⚠️  CRITICAL: Do not proceed past TASK-004.3 (HTML Validation) until you've manually verified ALL images load in the HTML file.

📖 All implementation details are in the <critical_knowledge> section above - this command is completely self-contained.

Ready to create your professional ebook? Let's start with EBOOK-001!"
</completion>
