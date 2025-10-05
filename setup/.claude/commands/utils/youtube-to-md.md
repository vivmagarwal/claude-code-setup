---
description: Extract YouTube video transcript and save as markdown
argument-hint: <youtube-url> [output-file] [--timestamps]
---

Extract YouTube transcript to markdown: $ARGUMENTS

<approach>
Be helpful and efficient. Extract YouTube video transcripts and format them as clean markdown files.
Handle errors gracefully and provide clear feedback.
</approach>

<process>
1. Parse arguments from $ARGUMENTS:
   - First arg: YouTube URL (required)
   - Second arg: Output file path (optional, defaults to auto-generated)
   - Flag: --timestamps (optional, includes timestamps in output)
   - Flag: --language=XX (optional, language code like 'en', 'es', etc.)

2. Validate YouTube URL format

3. Determine output file:
   - If provided: use as-is
   - If not provided: extract video ID and create filename like `transcripts/VIDEO_ID.md`
   - Create output directory if needed

4. Check if youtube-transcript-api is installed:
   - If not, ask user: "youtube-transcript-api is required. Install it? (pip install youtube-transcript-api)"
   - Wait for confirmation before installing

5. Execute Python script using the youtube_transcript.py from `/.claude-scripts`:
   first find `/.claude-scripts`. gradually look for it into parent folders.
   
   ```bash
   python .claude-scripts/youtube_transcript.py "<url>" -o "<output-file>" [--timestamps] [--language=XX]
   ```

6. Report results:
   - Success: "✓ Transcript saved to: <output-file>"
   - Error: Show error message and suggest fixes

</process>

<output_format>
When successful, confirm:
- Video URL processed
- Output file location
- File size or word count if available
- Quick preview of first 2 lines of content

When error occurs:
- Clear error message
- Suggested fix (install library, check URL, etc.)
- Example of correct usage
</output_format>

<examples>
Example 1 - Basic usage:
User: /utils/youtube-to-md https://youtube.com/watch?v=dQw4w9WgXcQ
Assistant: [Creates transcripts/dQw4w9WgXcQ.md]
"✓ Transcript saved to: transcripts/dQw4w9WgXcQ.md
  Video: https://youtube.com/watch?v=dQw4w9WgXcQ

  Preview:
  # YouTube Transcript
  **Video ID:** dQw4w9WgXcQ"

Example 2 - Custom output file:
User: /utils/youtube-to-md https://youtube.com/watch?v=abc123 notes/video-summary.md
Assistant: [Creates notes/video-summary.md]

Example 3 - With timestamps:
User: /utils/youtube-to-md https://youtu.be/abc123 --timestamps
Assistant: [Creates transcript with timestamps]

Example 4 - Missing library:
User: /utils/youtube-to-md https://youtube.com/watch?v=abc123
Assistant: "youtube-transcript-api is not installed.
  Install it? (pip install youtube-transcript-api)

  Reply 'yes' to install."
</examples>

<error_handling>
Common errors and solutions:

1. Invalid URL:
   - Message: "Invalid YouTube URL. Please provide a valid YouTube URL."
   - Show supported formats:
     • https://youtube.com/watch?v=VIDEO_ID
     • https://youtu.be/VIDEO_ID
     • VIDEO_ID

2. Transcript not available:
   - Message: "Transcript not available for this video"
   - Suggest: Check if video has captions enabled

3. Permission error writing file:
   - Message: "Cannot write to <path>"
   - Suggest: Check directory permissions or provide different output path

4. Network error:
   - Message: "Failed to fetch transcript. Check internet connection."
   - Suggest: Retry command
</error_handling>

<validation>
Before execution:
✓ YouTube URL is valid
✓ Output directory is writable (create if needed)
✓ youtube-transcript-api is installed
✓ Python script exists at .claude-scripts/youtube_transcript.py

After execution:
✓ Output file exists
✓ File contains content (not empty)
✓ Markdown is properly formatted
</validation>

Begin extracting transcript from: $ARGUMENTS
