#!/usr/bin/env python3
"""
YouTube Transcript Extractor - Download transcripts with intelligent fallback

FEATURES:
  ✓ Title-based filenames (not cryptic video IDs)
  ✓ Playlist support (download entire playlists)
  ✓ Multi-language support (hindi, spanish, etc)
  ✓ Playwright fallback (bypasses API blocks)
  ✓ User-agent rotation (appear as different browsers)
  ✓ Auto-resume (skip existing files)
  ✓ Rate limit handling with exponential backoff

QUICK START:
  # Single video
  python youtube_transcript.py "VIDEO_URL" -o output.md

  # Entire playlist
  python youtube_transcript.py "PLAYLIST_URL" -o transcripts/

  # With timestamps
  python youtube_transcript.py "VIDEO_URL" -o output.md --timestamps

  # Different language
  python youtube_transcript.py "VIDEO_URL" -o output.md --language=hi

PLAYWRIGHT FALLBACK:
  When YouTube API fails (rate limits, IP blocks), the script automatically:
  1. Launches a real browser
  2. Opens the video page
  3. Clicks "Show transcript" button
  4. Extracts transcript from page

  Works even when completely IP-blocked! Enabled by default.
  Disable with: --use-playwright-fallback false

DEPENDENCIES:
  pip install youtube-transcript-api yt-dlp pytube playwright
  playwright install chromium

RATE LIMITING TIPS:
  <10 videos:   --delay 1.0
  10-50 videos: --delay 2.0 (default)
  50+ videos:   --delay 3.0 --max-retries 5
  100+ videos:  --delay 5.0 (run overnight)

PROGRAMMATIC USE:
  from youtube_transcript import fetch_transcript, save_transcript

  markdown = fetch_transcript("VIDEO_URL", include_timestamps=True)
  save_transcript("VIDEO_URL", "output.md", use_playwright_fallback=True)
"""

import re
import sys
import time
import logging
import argparse
from typing import Optional, Dict, List
from urllib.parse import urlparse, parse_qs
from datetime import timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    print("Error: youtube-transcript-api not installed.")
    print("Install with: pip install youtube-transcript-api")
    sys.exit(1)

try:
    from pytube import Playlist
    PYTUBE_AVAILABLE = True
except ImportError:
    PYTUBE_AVAILABLE = False

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

# User agent pool for rotation (appear as different browsers/devices)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
]


def get_random_user_agent() -> str:
    """Get a random user agent from the pool."""
    import random
    return random.choice(USER_AGENTS)


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    """
    # Pattern 1: youtube.com/watch?v=VIDEO_ID
    if 'youtube.com/watch' in url:
        parsed = urlparse(url)
        query_params = parse_qs(parsed.query)
        if 'v' in query_params:
            return query_params['v'][0]

    # Pattern 2: youtu.be/VIDEO_ID
    if 'youtu.be/' in url:
        parsed = urlparse(url)
        return parsed.path.lstrip('/')

    # Pattern 3: youtube.com/embed/VIDEO_ID or youtube.com/v/VIDEO_ID
    if 'youtube.com/embed/' in url or 'youtube.com/v/' in url:
        parsed = urlparse(url)
        return parsed.path.split('/')[-1]

    # If it's just a video ID
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url):
        return url

    return None


def sanitize_filename(title: str, max_length: int = 100) -> str:
    """
    Sanitize video title to create a valid filename.

    Args:
        title: Video title
        max_length: Maximum filename length (default: 100)

    Returns:
        Sanitized filename
    """
    # Remove invalid filename characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)

    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)

    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')

    # Truncate to max length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].rsplit(' ', 1)[0]  # Cut at last space

    # If empty after sanitization, use default
    if not sanitized:
        sanitized = "untitled"

    return sanitized


def fetch_video_title(url: str) -> Optional[str]:
    """
    Fetch video title from YouTube URL using yt-dlp.

    Args:
        url: YouTube video URL

    Returns:
        Video title or None if failed
    """
    try:
        import subprocess
        import json

        video_id = extract_video_id(url)
        if not video_id:
            return None

        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Use yt-dlp to fetch video metadata
        result = subprocess.run(
            ['yt-dlp', '--dump-json', '--no-download', '--quiet', video_url],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get('title')

        return None
    except Exception:
        # If title fetch fails, return None to fallback to video ID
        return None


def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS or MM:SS format."""
    td = timedelta(seconds=int(seconds))
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"


def is_playlist_url(url: str) -> bool:
    """Check if URL is a playlist URL."""
    return 'list=' in url or '/playlist?' in url


def extract_playlist_id(url: str) -> Optional[str]:
    """Extract playlist ID from YouTube URL."""
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    if 'list' in query_params:
        return query_params['list'][0]

    return None


def fetch_playlist_videos(playlist_url: str) -> List[str]:
    """
    Fetch all video URLs from a YouTube playlist.

    Args:
        playlist_url: YouTube playlist URL

    Returns:
        List of video URLs
    """
    if not PYTUBE_AVAILABLE:
        raise ImportError("pytube is required for playlist support. Install with: pip install pytube")

    try:
        playlist = Playlist(playlist_url)
        return list(playlist.video_urls)
    except Exception as e:
        raise Exception(f"Failed to fetch playlist videos: {str(e)}")


def fetch_transcript(
    url: str,
    include_timestamps: bool = False,
    language: str = 'en',
    preserve_formatting: bool = True
) -> str:
    """
    Fetch and format YouTube video transcript as markdown.

    Args:
        url: YouTube video URL or video ID
        include_timestamps: Include timestamps in output (default: False)
        language: Preferred language code (default: 'en')
        preserve_formatting: Preserve paragraph breaks (default: True)

    Returns:
        Formatted markdown string
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Invalid YouTube URL: {url}")

    try:
        # Fetch transcript using the new API (instance-based)
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        # Try to get transcript in requested language, fall back to auto-generated
        try:
            transcript = transcript_list.find_transcript([language])
        except Exception:
            # Get any available transcript
            try:
                transcript = transcript_list.find_generated_transcript(['en'])
            except Exception:
                # If no English, try to get any available transcript
                transcript = transcript_list.find_transcript(transcript_list.build()[0]['language_code'])

        fetched_transcript = api.fetch(video_id, languages=[transcript.language_code], preserve_formatting=preserve_formatting)

        # Build markdown output
        markdown_lines = []
        markdown_lines.append("# YouTube Transcript\n")
        markdown_lines.append(f"**Video ID:** {video_id}")
        markdown_lines.append(f"**URL:** https://www.youtube.com/watch?v={video_id}")
        markdown_lines.append(f"**Language:** {fetched_transcript.language_code}")
        markdown_lines.append(f"**Generated:** {'Yes' if fetched_transcript.is_generated else 'No'}\n")
        markdown_lines.append("---\n")

        if include_timestamps:
            # Format with timestamps
            for snippet in fetched_transcript.snippets:
                timestamp = format_timestamp(snippet.start)
                text = snippet.text.strip()
                markdown_lines.append(f"**[{timestamp}]** {text}\n")
        else:
            # Format as continuous text with paragraph breaks
            if preserve_formatting:
                current_paragraph = []
                last_end_time = 0

                for snippet in fetched_transcript.snippets:
                    text = snippet.text.strip()
                    start_time = snippet.start

                    # Detect paragraph breaks (gap > 2 seconds or ending punctuation)
                    time_gap = start_time - last_end_time
                    ends_sentence = text.endswith(('.', '!', '?'))

                    current_paragraph.append(text)

                    if (time_gap > 2.0 or ends_sentence) and len(' '.join(current_paragraph)) > 100:
                        markdown_lines.append(' '.join(current_paragraph) + '\n')
                        current_paragraph = []

                    last_end_time = start_time + snippet.duration

                # Add remaining paragraph
                if current_paragraph:
                    markdown_lines.append(' '.join(current_paragraph) + '\n')
            else:
                # Simple format: all text together
                all_text = ' '.join([snippet.text.strip() for snippet in fetched_transcript.snippets])
                markdown_lines.append(all_text)

        return '\n'.join(markdown_lines)

    except Exception as e:
        raise Exception(f"Failed to fetch transcript: {str(e)}")


def fetch_transcript_playwright(
    url: str,
    include_timestamps: bool = False,
    headless: bool = True
) -> str:
    """
    Fallback method: Fetch transcript using Playwright browser automation.
    This bypasses API restrictions by actually opening the video page.

    Args:
        url: YouTube video URL
        include_timestamps: Include timestamps in output
        headless: Run browser in headless mode (default: True)

    Returns:
        Formatted markdown string
    """
    if not PLAYWRIGHT_AVAILABLE:
        raise ImportError("Playwright is required for fallback. Install with: pip install playwright && playwright install chromium")

    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError(f"Invalid YouTube URL: {url}")

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    logger.info(f"Using Playwright fallback for: {video_url}")

    try:
        with sync_playwright() as p:
            # Launch browser with random user agent
            browser = p.chromium.launch(headless=headless)
            context = browser.new_context(
                user_agent=get_random_user_agent(),
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()

            # Navigate to video
            logger.info("  Opening video page...")
            page.goto(video_url, wait_until='domcontentloaded')
            page.wait_for_timeout(3000)  # Wait for page to settle

            # Scroll down to load transcript button
            page.evaluate("window.scrollBy(0, 300)")
            page.wait_for_timeout(1000)

            # Try to find and click transcript button
            transcript_button_selectors = [
                'button[aria-label*="transcript" i]',
                'button[aria-label*="Show transcript" i]',
                'ytd-video-description-transcript-section-renderer button',
                '#primary-button button:has-text("Show transcript")',
            ]

            clicked = False
            for selector in transcript_button_selectors:
                try:
                    logger.info(f"  Looking for transcript button: {selector}")
                    button = page.wait_for_selector(selector, timeout=5000)
                    if button and button.is_visible():
                        logger.info("  Clicking transcript button...")
                        button.click()
                        clicked = True
                        break
                except Exception:
                    continue

            if not clicked:
                raise Exception("Could not find transcript button on page")

            # Wait for transcript panel to load
            page.wait_for_timeout(2000)

            # Extract transcript segments
            logger.info("  Extracting transcript...")
            transcript_segments = page.evaluate('''() => {
                // Try multiple selectors for transcript items
                const selectors = [
                    'ytd-transcript-segment-renderer',
                    '.ytd-transcript-segment-renderer',
                    '[class*="transcript-segment"]'
                ];

                let segments = [];
                for (const selector of selectors) {
                    const elements = document.querySelectorAll(selector);
                    if (elements.length > 0) {
                        elements.forEach(segment => {
                            const timeElement = segment.querySelector('[class*="time"], .segment-timestamp');
                            const textElement = segment.querySelector('[class*="text"], .segment-text');

                            if (textElement) {
                                segments.push({
                                    time: timeElement ? timeElement.textContent.trim() : '',
                                    text: textElement.textContent.trim()
                                });
                            }
                        });
                        if (segments.length > 0) break;
                    }
                }

                return segments;
            }''')

            browser.close()

            if not transcript_segments or len(transcript_segments) == 0:
                raise Exception("No transcript segments found")

            logger.info(f"  Extracted {len(transcript_segments)} segments")

            # Format as markdown
            markdown_lines = []
            markdown_lines.append("# YouTube Transcript\n")
            markdown_lines.append(f"**Video ID:** {video_id}")
            markdown_lines.append(f"**URL:** {video_url}")
            markdown_lines.append("**Source:** Playwright Fallback\n")
            markdown_lines.append("---\n")

            if include_timestamps:
                for segment in transcript_segments:
                    time_str = segment['time']
                    text = segment['text']
                    markdown_lines.append(f"**[{time_str}]** {text}\n")
            else:
                # Group into paragraphs
                current_paragraph = []
                for segment in transcript_segments:
                    text = segment['text']
                    current_paragraph.append(text)

                    if text.endswith(('.', '!', '?')) and len(' '.join(current_paragraph)) > 100:
                        markdown_lines.append(' '.join(current_paragraph) + '\n')
                        current_paragraph = []

                if current_paragraph:
                    markdown_lines.append(' '.join(current_paragraph) + '\n')

            return '\n'.join(markdown_lines)

    except Exception as e:
        raise Exception(f"Playwright fallback failed: {str(e)}")


def save_transcript(
    url: str,
    output_file: str,
    include_timestamps: bool = False,
    language: str = 'en',
    use_playwright_fallback: bool = True
) -> str:
    """
    Fetch transcript and save to file with automatic Playwright fallback.

    Args:
        url: YouTube video URL
        output_file: Path to output markdown file
        include_timestamps: Include timestamps in output
        language: Preferred language code
        use_playwright_fallback: Use Playwright as fallback when API fails (default: True)

    Returns:
        Path to saved file
    """
    markdown = None
    api_error = None

    # Try API first
    try:
        markdown = fetch_transcript(url, include_timestamps, language)
    except Exception as e:
        api_error = str(e)
        logger.warning(f"  API failed: {api_error[:100]}")

        # Try Playwright fallback if enabled
        if use_playwright_fallback and PLAYWRIGHT_AVAILABLE:
            try:
                logger.info("  Attempting Playwright fallback...")
                markdown = fetch_transcript_playwright(url, include_timestamps)
            except Exception as fallback_error:
                logger.error(f"  Playwright fallback also failed: {str(fallback_error)[:100]}")
                raise Exception(f"Both API and Playwright failed. API: {api_error[:50]}, Playwright: {str(fallback_error)[:50]}")
        else:
            # Re-raise original error if fallback not available/enabled
            raise Exception(api_error)

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)

    return output_file


def batch_fetch(
    urls: List[str],
    output_dir: str = '.',
    include_timestamps: bool = False,
    language: str = 'en',
    delay: float = 1.0,
    max_retries: int = 3,
    skip_existing: bool = True,
    use_playwright_fallback: bool = True
) -> Dict[str, str]:
    """
    Fetch multiple transcripts with rate limiting and retry logic.

    Args:
        urls: List of YouTube URLs
        output_dir: Directory to save transcripts
        include_timestamps: Include timestamps in output
        language: Preferred language code
        delay: Delay between requests in seconds (default: 1.0)
        max_retries: Maximum number of retries per video (default: 3)
        skip_existing: Skip videos that already have transcript files (default: True)
        use_playwright_fallback: Use Playwright as fallback when API fails (default: True)

    Returns:
        Dictionary mapping URLs to output file paths
    """
    import os
    results = {}
    total = len(urls)

    for idx, url in enumerate(urls, 1):
        logger.info(f"Processing video {idx}/{total}: {url}")

        video_id = extract_video_id(url)
        if not video_id:
            logger.warning(f"Skipping invalid URL: {url}")
            results[url] = None
            continue

        # Try to fetch video title, fallback to video ID
        title = fetch_video_title(url)
        if title:
            filename = sanitize_filename(title)
            logger.info(f"  Title: {title}")
        else:
            filename = video_id
            logger.warning(f"  Could not fetch title, using video ID: {video_id}")

        output_file = os.path.join(output_dir, f"{filename}.md")

        # Skip if file already exists and skip_existing is True
        if skip_existing and os.path.exists(output_file):
            file_size = os.path.getsize(output_file)
            if file_size > 100:  # File has content (> 100 bytes)
                print(f"⏭  [{idx}/{total}] Skipping (already exists): {filename}.md")
                results[url] = output_file
                continue

        # Retry logic with exponential backoff
        for attempt in range(max_retries):
            try:
                save_transcript(url, output_file, include_timestamps, language, use_playwright_fallback)
                results[url] = output_file
                print(f"✓ [{idx}/{total}] Saved: {filename}.md")

                # Delay between successful requests to avoid rate limiting
                if idx < total:
                    time.sleep(delay)
                break

            except Exception as e:
                error_msg = str(e)

                # Check if it's a rate limit error
                if 'blocking' in error_msg.lower() or 'blocked' in error_msg.lower():
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"  Rate limited. Waiting {wait_time:.1f}s before retry {attempt + 1}/{max_retries}")
                    time.sleep(wait_time)

                    if attempt == max_retries - 1:
                        logger.error(f"✗ [{idx}/{total}] Failed after {max_retries} attempts: {filename}")
                        logger.error("  Error: Rate limit exceeded")
                        results[url] = None
                else:
                    # Non-rate-limit error, log and skip
                    logger.error(f"✗ [{idx}/{total}] Failed: {filename}")
                    logger.error(f"  Error: {error_msg[:100]}")
                    results[url] = None
                    break

    return results


def fetch_playlist_transcripts(
    playlist_url: str,
    output_dir: str = '.',
    include_timestamps: bool = False,
    language: str = 'en',
    delay: float = 2.0,
    max_retries: int = 3,
    use_playwright_fallback: bool = True
) -> Dict[str, str]:
    """
    Fetch transcripts for all videos in a playlist.

    Args:
        playlist_url: YouTube playlist URL
        output_dir: Directory to save transcripts
        include_timestamps: Include timestamps in output
        language: Preferred language code
        delay: Delay between requests in seconds
        max_retries: Maximum number of retries per video
        use_playwright_fallback: Use Playwright as fallback when API fails (default: True)

    Returns:
        Dictionary mapping video URLs to output file paths
    """
    import os

    print("Fetching playlist videos...")
    video_urls = fetch_playlist_videos(playlist_url)
    print(f"Found {len(video_urls)} videos in playlist")
    print(f"Using {delay}s delay between requests and max {max_retries} retries per video")
    print(f"Playwright fallback: {'Enabled' if use_playwright_fallback else 'Disabled'}\n")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Download all transcripts
    return batch_fetch(video_urls, output_dir, include_timestamps, language, delay, max_retries, True, use_playwright_fallback)


def main():
    """CLI interface for YouTube transcript extraction."""
    parser = argparse.ArgumentParser(
        description='Extract YouTube video transcripts as markdown. Supports both individual videos and playlists.'
    )
    parser.add_argument(
        'url',
        help='YouTube video URL, playlist URL, or video ID'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path for single video (default: prints to stdout). For playlists, this is treated as output directory.'
    )
    parser.add_argument(
        '-t', '--timestamps',
        action='store_true',
        help='Include timestamps in output'
    )
    parser.add_argument(
        '-l', '--language',
        default='en',
        help='Preferred language code (default: en)'
    )
    parser.add_argument(
        '--no-formatting',
        action='store_true',
        help='Disable paragraph formatting'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=2.0,
        help='Delay between requests in seconds to avoid rate limiting (default: 2.0)'
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Maximum number of retries per video on errors (default: 3)'
    )
    parser.add_argument(
        '--use-playwright-fallback',
        type=lambda x: x.lower() in ['true', '1', 'yes'],
        default=True,
        help='Use Playwright browser automation as fallback when API fails (default: True)'
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        default=True,
        help='Run Playwright in headless mode (default: True)'
    )

    args = parser.parse_args()

    try:
        # Check if URL is a playlist
        if is_playlist_url(args.url):
            # Handle playlist
            output_dir = args.output if args.output else 'transcripts'
            print(f"Detected playlist URL. Downloading all transcripts to: {output_dir}")
            results = fetch_playlist_transcripts(
                args.url,
                output_dir=output_dir,
                include_timestamps=args.timestamps,
                language=args.language,
                delay=args.delay,
                max_retries=args.max_retries,
                use_playwright_fallback=args.use_playwright_fallback
            )

            # Summary
            successful = sum(1 for v in results.values() if v is not None)
            total = len(results)
            print(f"\n✓ Downloaded {successful}/{total} transcripts to {output_dir}/")
        else:
            # Handle single video
            if args.output:
                # Save to file (with Playwright fallback support)
                save_transcript(
                    args.url,
                    args.output,
                    include_timestamps=args.timestamps,
                    language=args.language,
                    use_playwright_fallback=args.use_playwright_fallback
                )
                print(f"✓ Transcript saved to: {args.output}")
            else:
                # Print to stdout (API only, no fallback for stdout)
                markdown = fetch_transcript(
                    args.url,
                    include_timestamps=args.timestamps,
                    language=args.language,
                    preserve_formatting=not args.no_formatting
                )
                print(markdown)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
