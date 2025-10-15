# PDF to Markdown Extraction Guide (Vision-Based Approach)

## Overview

This guide documents a two-stage process for extracting content from PDFs using vision analysis:
1. **Stage 1**: Convert PDF pages to high-resolution images
2. **Stage 2**: Use your (claude code's) vision capabilities to analyze each image and extract content to markdown

## Why This Approach?

**Advantages:**
- Handles image-heavy PDFs that contain screenshots, graphics, and embedded content
- Preserves visual context that pure text extraction misses
- Can extract text from images within the PDF
- Better accuracy for complex layouts (tweets, social media posts, presentations, graphs, images, maths)
- No need for external API calls - uses Claude Code's built-in vision capabilities

**Best For:**
- PDFs with screenshots or social media posts
- Presentation slides with mixed content
- Documents with complex layouts
- Image-heavy marketing materials

## Stage 1: Convert PDF to Images

### Script: `convert_pdf_to_images.py`

```python
#!/usr/bin/env python3
"""
Convert PDF pages to individual PNG images for analysis.
"""

import sys
from pathlib import Path
import pymupdf  # PyMuPDF


def convert_pdf_to_images(pdf_path, output_dir=None, zoom=2.0):
    """
    Convert each page of a PDF to a PNG image.

    Args:
        pdf_path: Path to input PDF file
        output_dir: Directory to save images (default: pdf_name_pages/)
        zoom: Zoom factor for higher resolution (default: 2.0)

    Returns:
        List of image file paths
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Create output directory
    if output_dir is None:
        output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    else:
        output_dir = Path(output_dir)

    output_dir.mkdir(exist_ok=True)

    print(f"Opening PDF: {pdf_path}")
    doc = pymupdf.open(pdf_path)
    total_pages = len(doc)
    print(f"Total pages: {total_pages}")
    print(f"Output directory: {output_dir}")

    image_paths = []

    # Process each page
    for page_num in range(total_pages):
        page = doc[page_num]

        # Create a transformation matrix for higher resolution
        mat = pymupdf.Matrix(zoom, zoom)

        # Render page to pixmap (image)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        # Generate output filename with zero-padded page number
        output_path = output_dir / f"page_{page_num + 1:03d}.png"

        # Save as PNG
        pix.save(str(output_path))
        image_paths.append(output_path)

        print(f"  ✓ Page {page_num + 1}/{total_pages} -> {output_path.name}")

    doc.close()

    print(f"\n✓ Conversion complete! {len(image_paths)} images saved to: {output_dir}")
    return image_paths


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python convert_pdf_to_images.py <pdf_file> [output_dir]")
        print("\nExample:")
        print("  python convert_pdf_to_images.py document.pdf")
        print("  python convert_pdf_to_images.py document.pdf ./output_images")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        convert_pdf_to_images(pdf_path, output_dir)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### Usage

```bash
# Basic usage - creates pdf_name_pages/ directory
python convert_pdf_to_images.py document.pdf

# Specify custom output directory
python convert_pdf_to_images.py document.pdf ./custom_output_dir
```

### Requirements

```bash
# Install PyMuPDF (must be version 1.26.3+)
pip install --upgrade pymupdf
```

**Key Parameters:**
- `zoom=2.0`: Higher zoom = better resolution (2.0 recommended for text clarity)
- Output naming: `page_001.png`, `page_002.png`, etc. (zero-padded for sorting)

## Stage 2: Vision-Based Extraction

### Workflow Overview

1. Create output directory for individual page markdown files
2. Create todo list for tracking progress
3. Process images in batches (10 pages at a time recommended)
4. Extract and save each page to its own markdown file (`page_001.md`, `page_002.md`, etc.)
5. (Optional) Combine all pages into single markdown file when complete

### Step-by-Step Process

#### 1. Initialize Output Directory

```bash
# Create directory for individual page markdown files
mkdir -p document_extracted_pages

# Optionally create a header file
cat > document_extracted_pages/00_header.md << 'EOF'
# [Document Title] - Vision Extracted

Extracted from: [source_pdf_name.pdf]
Date: $(date +%Y-%m-%d)
Method: Vision-based page-by-page extraction

---

EOF
```

#### 2. Set Up Todo List

Use TodoWrite tool to create tracking tasks:
- Check required packages
- Create conversion script
- Generate page images
- Initialize output file
- Process pages in batches (e.g., 1-30, 31-52)

#### 3. Batch Processing Pattern

**Process images in batches of 10 for efficiency:**

```
# Read 10 images at once using multiple Read tool calls in parallel
Read page_001.png through page_010.png

# Extract content from all 10 pages
# Format as markdown
# Save each page to its own file (page_001.md, page_002.md, etc.)
```

**For Large PDFs (50+ pages), use parallel sub-agents in batches of 10:**

```
# Launch agents in batches of 10 for better control and monitoring
# Each batch launches 10 agents simultaneously, wait for completion, then launch next batch

For 55 pages (55 agents needed):
- Batch 1: Launch agents 1-10 (pages 1-100)
- Batch 2: Launch agents 11-20 (pages 101-200)
- Batch 3: Launch agents 21-30 (pages 201-300)
- Batch 4: Launch agents 31-40 (pages 301-400)
- Batch 5: Launch agents 41-50 (pages 401-500)
- Batch 6: Launch agents 51-55 (pages 501-550)

For 100 pages (10 agents needed):
- Batch 1: Launch all 10 agents (pages 1-100)

For 200 pages (20 agents needed):
- Batch 1: Launch agents 1-10 (pages 1-100)
- Batch 2: Launch agents 11-20 (pages 101-200)

# Each agent independently reads images and creates markdown files
# Monitor progress after each batch completes before launching next batch
# This provides better visibility and control over the extraction process
```

#### 4. Content Extraction

For each page:
1. Read the image using Read tool
2. Analyze visual content
3. Extract all text, metadata, formatting
4. Structure as markdown
5. **Save to individual page file** using bash

**Creating Individual Page Files:**

```bash
# Create separate markdown file for each page
cat > document_extracted_pages/page_001.md << 'EOF'
## Page 1

[Extracted content here with proper formatting]

- Bullet points preserved
- **Bold text** maintained
- *Italic text* maintained

---

EOF
```

**Benefits of Individual Page Files:**
- Easy to verify accuracy of specific pages
- Can reprocess individual pages without affecting others
- Progress persists if interrupted
- Perfect for parallel processing
- Simple to combine later: `cat page_*.md > complete.md`

### Content Formatting Guidelines

**For Social Media Posts (Twitter/LinkedIn):**

```markdown
### Example Tweet 1
**Author Name** (@handle)

"Tweet content goes here..."

*Posted: Time · Date · Platform*
- Retweets count
- Quote Tweets count
- Likes count
```

**For Presentations:**

```markdown
## Page X

# Slide Title

Slide content...

Key points:
- Point 1
- Point 2
```

**For Mixed Content:**

```markdown
## Page X

[Description of visual elements]

Text content extracted...

[Tables, code blocks, or special formatting as needed]
```

## Complete Workflow Examples

### Workflow A: Sequential Processing (Small PDFs, < 50 pages)

```bash
# 1. Convert PDF to images
python convert_pdf_to_images.py document.pdf

# 2. Check output
ls document_pages/
# Output: page_001.png, page_002.png, ..., page_052.png

# 3. Create output directory for markdown pages
mkdir -p document_extracted_pages

# 4. Process images in batches of 10
# - Read 10 images using Read tool (parallel calls)
# - Extract content from each
# - Save each to individual markdown file (page_001.md, page_002.md, etc.)

# 5. Combine all pages into single file (optional)
cat document_extracted_pages/page_*.md > document_complete.md

# 6. Verify output
ls document_extracted_pages/
# Output: page_001.md, page_002.md, ..., page_052.md
```

### Workflow B: Parallel Processing (Large PDFs, 50+ pages)

```bash
# 1. Convert PDF to images
python convert_pdf_to_images.py large_document.pdf

# 2. Create output directory
mkdir -p large_document_extracted_pages

# 3. Launch agents in batches of 10 for better control
# Rule of thumb: 1 agent per 10 pages, launched in batches of 10 agents
#
# For 55 pages (6 batches needed):
#   Batch 1: Launch agents 1-10 (pages 1-100)
#   Wait for completion, then...
#   Batch 2: Launch agents 11-20 (pages 101-200)
#   Wait for completion, then...
#   ... continue through Batch 6
#
# For 100 pages (1 batch of 10 agents):
#   Batch 1: Launch all 10 agents (pages 1-100)
#
# For 200 pages (2 batches needed):
#   Batch 1: Launch agents 1-10 (pages 1-100)
#   Wait for completion, then...
#   Batch 2: Launch agents 11-20 (pages 101-200)
#
# Benefits of batching:
# - Better progress monitoring between batches
# - Can verify quality of first batch before proceeding
# - Easier to debug if issues arise
# - More control over resource usage

# 4. Wait for each batch to complete before launching next batch

# 5. Combine all pages when agents finish
cat large_document_extracted_pages/page_*.md > large_document_complete.md

# 6. Verify all pages present
ls large_document_extracted_pages/ | wc -l
# Should equal total number of pages
```

**Key Points:**
- No code needed - just ask Claude Code to launch agents with appropriate prompts
- **Launch agents in batches of 10** for better control and monitoring
- Wait for each batch to complete before launching the next batch
- Each agent is independent and writes to separate files
- Batching provides better progress visibility and easier debugging

### Parallel Agent Prompts

**To launch 10 agents in parallel, use Task tool with these prompts in a SINGLE message:**

#### Agent 1 (Pages 1-10):
```
Extract pages 1-10 from document PDF to individual markdown files.

Input images: document_pages/page_001.png through page_010.png
Output directory: document_extracted_pages/

Steps:
1. Read all 10 page images using parallel Read tool calls
2. Extract ALL content with maximum accuracy - preserve every detail
3. Create individual markdown file for each page (page_001.md, page_002.md, etc.)
4. Format each page as:

## Page X

[All extracted content - text, numbers, dates, metadata, formatting]

---

ERROR HANDLING (CRITICAL):
- Process each page independently
- If ONE page fails extraction, continue with remaining pages
- Log any failed pages and report them at the end
- Do NOT let a single page failure stop the entire batch
- Save successful extractions immediately as you go

CRITICAL: Extract EVERYTHING. Don't skip any text or details.
Report back when complete, including count of successes and any failures.
```

#### Agent 2 (Pages 11-20):
```
Same prompt as Agent 1, but for pages 11-20 (page_011.png through page_020.png)
```

#### Agents 3-N:
```
Agent 3: Pages 21-30
Agent 4: Pages 31-40
Agent 5: Pages 41-50
...
Agent N: Pages (N-1)*10+1 to N*10

Scale to as many agents as needed based on page count!
```

**How to Launch (in batches of 10):**
```
Launch agents in batches of 10 for better control and monitoring.
Each batch = 10 Task tool calls in a single message.

For 55 pages (55 agents needed, 6 batches):

  BATCH 1: Launch 10 agents (pages 1-100) in one message
  Task(description="Extract pages 1-10", subagent_type="general-purpose", prompt=[Agent 1 prompt])
  Task(description="Extract pages 11-20", subagent_type="general-purpose", prompt=[Agent 2 prompt])
  ...
  Task(description="Extract pages 91-100", subagent_type="general-purpose", prompt=[Agent 10 prompt])

  [Wait for all 10 agents to complete]

  BATCH 2: Launch 10 agents (pages 101-200) in one message
  Task(description="Extract pages 101-110", subagent_type="general-purpose", prompt=[Agent 11 prompt])
  ...
  Task(description="Extract pages 191-200", subagent_type="general-purpose", prompt=[Agent 20 prompt])

  [Wait for completion]

  BATCH 3-5: Continue pattern...

  BATCH 6: Launch remaining 5 agents (pages 501-550) in one message
  Task(description="Extract pages 501-510", subagent_type="general-purpose", prompt=[Agent 51 prompt])
  ...
  Task(description="Extract pages 541-550", subagent_type="general-purpose", prompt=[Agent 55 prompt])

For 100 pages (10 agents needed, 1 batch):
  BATCH 1: Launch all 10 agents in one message

For 200 pages (20 agents needed, 2 batches):
  BATCH 1: Launch agents 1-10 (wait for completion)
  BATCH 2: Launch agents 11-20 (wait for completion)
```

**Batched Launch Benefits:**
- **Better progress visibility** between batches
- **Quality verification** - check first batch output before continuing
- **Easier debugging** - isolate issues to specific batches
- **Resource control** - pause between batches if needed
- **Clearer progress tracking** - know exactly where you are in the process

## Best Practices

### Batch Sizing
- **10 pages per agent**: Optimal for most content
- **10 agents per batch**: Launch agents in batches of 10 for better control
- **Sequential processing**: Good for PDFs under 50 pages
- **Batched parallel processing**: Recommended for PDFs over 50 pages
- **Wait between batches**: Verify quality after each batch before continuing
- **Scale to any size**: For N agents needed, launch ceil(N/10) batches
  - 55 agents = 6 batches (10+10+10+10+10+5)
  - 100 agents = 10 batches (10×10)
  - 200 agents = 20 batches (20×10)
- Monitor context limits - reduce batch size if needed

### Quality Checks
- Verify image resolution is readable (zoom=2.0 minimum)
- Check page numbering is sequential
- Ensure all pages are processed (track with todo list)

### Progress Tracking
- Use TodoWrite tool religiously
- Mark tasks as in_progress → completed
- Break large PDFs into manageable chunks (30-40 pages per task)

### Content Accuracy (HIGHEST PRIORITY)
- **Extract EVERYTHING** - don't skip any text or details
- Read entire image content thoroughly
- Preserve original formatting and structure exactly
- Include ALL metadata (dates, engagement metrics, author info, etc.)
- Note any visual elements that don't translate to text
- Double-check numbers, dates, and statistics for accuracy
- Preserve exact quotes and attributions
- **Individual page files make verification easier** - review each page's .md file

### Error Handling

**Critical Rule: One Page Failure Should Not Stop the Batch**

When processing batches of pages, it's essential that a single page failure doesn't halt the entire batch. Each page should be processed independently with proper error handling.

**Implementation Guidelines:**

1. **Process Each Page Independently**
   - Wrap each page extraction in try-catch logic
   - Continue to next page even if current page fails
   - Save successful extractions immediately

2. **Track and Report Failures**
   - Log which specific pages failed
   - Report failures at the end with counts
   - Include error messages for debugging

3. **Example Error Handling Pattern:**
   ```python
   successful_pages = []
   failed_pages = []

   for page_num in page_range:
       try:
           # Read image
           # Extract content
           # Save to markdown file
           successful_pages.append(page_num)
           print(f"✓ Page {page_num} saved")
       except Exception as e:
           failed_pages.append(page_num)
           print(f"✗ Page {page_num} failed: {e}")
           continue  # Important: continue to next page

   # Report summary
   print(f"Successfully extracted: {len(successful_pages)} pages")
   print(f"Failed: {len(failed_pages)} pages")
   if failed_pages:
       print(f"Failed pages: {failed_pages}")
   ```

4. **Agent Instructions Should Include:**
   - Explicit instruction to continue on failure
   - Request for summary report (successes + failures)
   - Clear expectation that batch completes even with errors

**Common Error Recovery:**
- If PyMuPDF version error: `pip install --upgrade pymupdf`
- If images are blurry: Increase zoom factor
- If context limit hit: Reduce batch size
- **If specific pages fail**: Retry with Gemini API (see `.claude-scripts/extract_pages_with_gemini.py`)
- **If content filtering blocks pages**: Use Gemini API as fallback (for personal/educational use only)
  - Gemini API often succeeds where other APIs are blocked
  - The script at `.claude-scripts/extract_pages_with_gemini.py` is designed for this purpose
  - Simply modify the `failed_pages` list in the script to target specific pages
  - Remember: Only use for personal learning and educational purposes, not commercial distribution

## Performance Tips

1. **Batched Launching**: Launch 10 agents at a time, wait for completion, then launch next batch
2. **Progress Monitoring**: Check output quality after first batch before proceeding
3. **No Code Needed**: Parallel processing = multiple Task tool calls with appropriate prompts
4. **Individual Page Files**: No file locking, easy verification, persistent progress
5. **Batch Read Calls**: Read 10 images at once (parallel Read tool calls within each agent)
6. **Zero-Padded Naming**: Ensures proper file sorting (page_001 not page_1)
7. **High Resolution**: zoom=2.0 provides good balance between quality and file size
8. **Easy Combination**: `cat page_*.md > complete.md` when needed

**Batch Management:**
- Launch 10 agents per batch for optimal control
- Wait for all agents in a batch to complete before launching next batch
- Verify output quality between batches
- Easier to debug and track progress with batched approach

## Troubleshooting

| Issue | Solution |
|-------|----------|
| PyMuPDF version mismatch | `pip install --upgrade pymupdf` (need 1.26.3+) |
| Images too small/blurry | Increase zoom parameter (try 3.0) |
| Missing pages | Check PDF page count matches image count |
| Edit tool ambiguity errors | Switch to `cat >>` for appending content |
| Context limit reached | Process in smaller batches, complete current batch first |

## Output Structure

**Individual Page Files (Recommended):**
```
document_extracted_pages/
├── 00_header.md (optional)
├── page_001.md
├── page_002.md
├── page_003.md
├── ...
└── page_052.md

# Combine when needed:
document_complete.md (generated from: cat page_*.md > complete.md)
```

**Advantages:**
- Each page independently verifiable
- Easy to reprocess specific pages
- Perfect for parallel processing
- Progress persists through interruptions
- Better version control (git diff per page)

## When NOT to Use This Approach

- **Pure text PDFs**: Use pymupdf4llm or similar text extraction tools
- **Searchable PDFs with good structure**: Standard text extraction is faster
- **Very large PDFs (500+ pages)**: Consider chunking or alternative methods
- **When speed is critical**: Text extraction is much faster than vision analysis

## Quick Reference

### For Small PDFs (< 50 pages):
```bash
# 1. Convert to images
python convert_pdf_to_images.py document.pdf

# 2. Create output directory
mkdir -p document_extracted_pages

# 3. Tell Claude Code: "Process all pages in batches of 10, save each to individual markdown file"

# 4. Combine (optional)
cat document_extracted_pages/page_*.md > complete.md
```

### For Large PDFs (50+ pages):
```bash
# 1. Convert to images
python convert_pdf_to_images.py large_doc.pdf

# 2. Create output directory
mkdir -p large_doc_extracted_pages

# 3. Launch agents in batches of 10
#
# For 55 pages (55 agents needed):
#   BATCH 1: "Launch agents 1-10 to extract pages 1-100"
#   [Wait for completion]
#   BATCH 2: "Launch agents 11-20 to extract pages 101-200"
#   [Wait for completion]
#   ... continue through BATCH 6
#
# For 100 pages (10 agents needed):
#   BATCH 1: "Launch all 10 agents to extract pages 1-100"
#
# For 200 pages (20 agents needed):
#   BATCH 1: "Launch agents 1-10 to extract pages 1-100"
#   [Wait for completion]
#   BATCH 2: "Launch agents 11-20 to extract pages 101-200"
#
# Benefits of batching:
# - Monitor progress between batches
# - Verify quality before continuing
# - Better control and debugging

# 4. Combine when all batches are done
cat large_doc_extracted_pages/page_*.md > complete.md
```

**No code needed for parallel processing** - just use appropriate prompts with Task tool!
**Launch in batches of 10** for better control and progress monitoring!

## Summary

This vision-based approach excels at extracting content from visually complex PDFs where traditional text extraction fails. The two-stage process (PDF → Images → Individual Page Markdown Files) ensures high-fidelity content capture while leveraging Claude Code's vision capabilities efficiently.

**Key Success Factors:**
1. **High-resolution image conversion** (zoom=2.0+)
2. **Individual page markdown files** for easy verification and parallel processing
3. **Batch processing** (10 pages per batch)
4. **Parallel sub-agents** for large PDFs (just use prompts - no code needed!)
5. **Maximum accuracy** - extract EVERYTHING, verify each page file
6. **Rigorous progress tracking** with todo lists
7. **Consistent markdown formatting** across all page files

**Processing Speed:**
- Sequential (< 50 pages): ~1-2 minutes per 10 pages
- Parallel with batching (50-100 pages): ~2-3 minutes per batch, 1 batch = 100 pages
- Parallel with batching (200 pages): ~4-6 minutes total (2 batches of 10 agents each)
- Parallel with batching (550 pages): ~12-18 minutes total (6 batches, verify between batches)

**Batched Processing Approach:**
- Launch 10 agents per batch for optimal control
- Wait for each batch to complete before launching next
- Verify output quality between batches
- Better progress visibility and debugging capability

**Accuracy Priority:**
Individual page files make it easy to verify accuracy - you can review each `page_XXX.md` file to ensure all information was captured completely and correctly. Batching allows you to verify quality after each batch of 100 pages.
