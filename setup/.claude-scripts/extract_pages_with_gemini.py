#!/usr/bin/env python3
"""
Extract markdown content from PDF page images using Gemini API.

This script provides an alternative extraction method for PDF pages that fail
with standard vision-based extraction due to content filtering or other issues.
It uses Google's Gemini API with vision capabilities to extract text, tables,
infographics, and other content from page images.

Requirements:
    - google-genai package: pip install google-generativeai
    - PIL (Pillow): pip install Pillow
    - python-dotenv: pip install python-dotenv
    - GEMINI_API_KEY environment variable set in .env file

Usage:
    python3 extract_pages_with_gemini.py

Configuration:
    Modify the failed_pages list and directory paths in main() function
    to match your specific extraction needs.

Author: Claude Code
Date: 2025-01-15
"""

import os
import sys
from pathlib import Path
from PIL import Image
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def extract_markdown_from_image(image_path: str, page_number: int) -> str:
    """
    Extract markdown content from a page image using Gemini API.

    This function sends a page image to Google's Gemini API with a detailed
    prompt instructing it to extract all text, tables, diagrams, and other
    content in markdown format. The extraction is designed to be thorough
    and preserve document structure.

    Args:
        image_path (str): Path to the image file to process
        page_number (int): Page number for the markdown header (used in output formatting)

    Returns:
        str: Markdown formatted text extracted from the image, including:
            - Page header (## Page N)
            - All visible text content
            - Tables converted to markdown table syntax
            - Descriptions of images/diagrams in [brackets]
            - Preserved structure (headers, lists, quotes, etc.)
            - Separator line (---) at the end

    Raises:
        ValueError: If GEMINI_API_KEY is not found in environment variables
        PIL.UnidentifiedImageError: If the image file cannot be opened
        Exception: For any API-related errors during extraction

    Example:
        >>> markdown = extract_markdown_from_image("page_001.png", 1)
        >>> print(markdown[:50])
        ## Page 1

        # Introduction to Theory of Knowledge
    """
    # Initialize Gemini client with API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment. Please set it in your .env file.")

    # Create Gemini client instance
    client = genai.Client(api_key=api_key)

    # Load the image file using PIL
    # This validates the image and prepares it for API transmission
    img = Image.open(image_path)

    # Create a detailed prompt that instructs Gemini how to extract content
    # The prompt emphasizes thoroughness and proper markdown formatting
    prompt = f"""Extract ALL text content from this page image and format it as markdown.

Instructions:
- Start with: ## Page {page_number}
- Extract every piece of text visible on the page
- Preserve the document structure (headers, subheaders, body text)
- Include page numbers, headers, footers
- Describe any images, diagrams, or visual elements in [brackets]
- Preserve all quotes, citations, and references
- Maintain bullet points and numbered lists
- Include any sidebar text or boxes
- Convert tables to markdown table syntax with proper alignment
- End with: ---

Be extremely thorough - do not skip any text or details."""

    # Send request to Gemini API
    # model: gemini-2.0-flash-exp provides fast vision-based extraction
    # contents: array containing the prompt text and the image
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',  # Using the latest model with vision capabilities
        contents=[prompt, img]
    )

    # Extract and return the text from the API response
    return response.text

def main():
    """
    Main function to extract markdown from failed pages.

    This function orchestrates the extraction process for pages that failed
    during initial extraction attempts. It processes each page image,
    extracts markdown content via Gemini API, and saves the results.

    Process:
        1. Define list of failed pages to extract
        2. Set up input (images) and output (markdown) directories
        3. For each page:
           - Skip if already extracted (idempotent)
           - Call extract_markdown_from_image()
           - Save result to markdown file
           - Report progress
        4. Display completion summary

    Note:
        Modify the failed_pages list and directory paths as needed for
        different textbooks or extraction batches.
    """
    # Define pages that need extraction
    # These are pages that failed during standard vision-based extraction
    # due to content filtering or other issues
    failed_pages = list(range(1, 11)) + list(range(181, 191))

    # Set up directory paths
    # image_dir: Contains PNG images of PDF pages (page_NNN.png)
    # output_dir: Will contain extracted markdown files (page_NNN.md)
    image_dir = Path('tok_oxford_textbook_pages')
    output_dir = Path('tok_oxford_textbook_extracted_pages')

    # Display extraction summary
    print(f"Extracting {len(failed_pages)} pages using Gemini API...")
    print(f"This will use approximately {len(failed_pages)} API calls\n")

    # Process each page in the failed_pages list
    for page_num in failed_pages:
        # Format page number with zero padding (e.g., 1 -> 001)
        # This ensures proper alphabetical sorting of files
        page_str = f"{page_num:03d}"
        image_path = image_dir / f"page_{page_str}.png"
        output_path = output_dir / f"page_{page_str}.md"

        # Skip if already exists (makes script idempotent/re-runnable)
        if output_path.exists():
            print(f"✓ Page {page_num} already exists, skipping...")
            continue

        try:
            # Display progress indicator (without newline for same-line status)
            print(f"Processing page {page_num}...", end=' ', flush=True)

            # Extract markdown content from the image
            markdown_content = extract_markdown_from_image(str(image_path), page_num)

            # Save markdown content to file with UTF-8 encoding
            # This ensures proper handling of special characters and symbols
            output_path.write_text(markdown_content, encoding='utf-8')

            # Report successful extraction
            print(f"✓ Saved to {output_path.name}")

        except Exception as e:
            # Log error and continue with next page
            # This prevents one failed page from stopping the entire batch
            print(f"✗ Error: {e}")
            continue

    # Display completion message
    print(f"\n✅ Extraction complete!")

if __name__ == "__main__":
    main()
