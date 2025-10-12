#!/usr/bin/env python3
"""
================================================================================
GEMINI IMAGE GENERATOR (NANO BANANA) - COMPLETE SELF-DOCUMENTED VERSION
================================================================================
A comprehensive Python script for generating images using Google's Gemini 2.5
Flash Image model (codename "Nano Banana").

WHAT THIS SCRIPT DOES:
----------------------
1. Takes text prompts and generates AI images
2. Can edit existing images with text instructions
3. Supports multiple aspect ratios (square, widescreen, portrait, etc.)
4. Saves images locally with timestamps or custom names
5. Works with environment variables for API keys

QUICK START:
------------
1. Install dependencies:
   $ pip install google-genai Pillow python-dotenv

2. Get your API key:
   - Visit https://aistudio.google.com/apikey
   - Click "Create API key"
   - Copy the key

3. Create a .env file in your project:
   GEMINI_API_KEY=your_api_key_here

4. Run the script:
   $ python gemini_image_generator.py "A cute cat wearing a hat"

COMPLETE USAGE EXAMPLES:
------------------------
# Basic image generation (creates generated_TIMESTAMP.png)
python gemini_image_generator.py "A futuristic city at sunset"

# Generate with specific aspect ratio (16:9 for widescreen)
python gemini_image_generator.py "Mountain landscape" --aspect-ratio 16:9

# Generate portrait orientation (9:16 for mobile/stories)
python gemini_image_generator.py "Full body character" --aspect-ratio 9:16

# Generate square image (1:1 for Instagram)
python gemini_image_generator.py "Abstract art" --aspect-ratio 1:1

# Save with custom filename
python gemini_image_generator.py "Ocean waves" --output my_ocean.png

# Generate image only (no text description from AI)
python gemini_image_generator.py "A robot" --image-only

# Edit an existing image (provide image path)
python gemini_image_generator.py "Add a rainbow" --input-image photo.jpg

# Multiple input images for complex edits
python gemini_image_generator.py "Combine these" -i img1.jpg -i img2.jpg

# Debug mode to see what's happening
python gemini_image_generator.py "A castle" --verbose

# Get JSON output for automation/scripts
python gemini_image_generator.py "A flower" --json

# Use specific API key (overrides environment)
python gemini_image_generator.py "A star" --api-key YOUR_KEY

# Use Vertex AI instead of direct API
python gemini_image_generator.py "A planet" --vertex --project-id my-project

AVAILABLE ASPECT RATIOS:
------------------------
- 1:1   = Square (default, Instagram posts)
- 16:9  = Widescreen (YouTube, presentations)
- 9:16  = Portrait/Mobile (Stories, TikTok)
- 4:3   = Classic (old TV, some cameras)
- 3:4   = Portrait classic
- 2:3   = Portrait photo (common print size)
- 3:2   = Landscape photo (DSLR standard)

ERROR TROUBLESHOOTING:
----------------------
- "GEMINI_API_KEY not set" → Create .env file with your API key
- "google-genai not installed" → Run: pip install google-genai
- "No image data in response" → API issue, retry the request
- "Image file not found" → Check your --input-image path
- Authentication errors → Check your API key is valid

COST INFORMATION:
-----------------
- Each image costs approximately $0.039 USD
- Pricing: $30 per 1 million output tokens
- Each image = ~1290 tokens
- Free tier: 500 requests/day (hackathon tier)
- Monitor usage at: https://aistudio.google.com

HOW THE SCRIPT WORKS INTERNALLY:
---------------------------------
1. Loads environment variables (.env file)
2. Parses command-line arguments
3. Initializes Gemini API client
4. Sends prompt/images to API
5. Receives and processes response
6. Extracts image data
7. Saves to local file
8. Displays result information

Author: Claude Assistant
Date: December 2024
Version: 1.0.0
License: MIT
API Documentation: https://ai.google.dev/gemini-api/docs/image-generation
================================================================================
"""

# ================================================================================
# IMPORTS SECTION - Each import explained
# ================================================================================

import argparse      # For parsing command-line arguments (--output, --verbose, etc.)
import json         # For JSON output format when --json flag is used
import logging      # For debug/info messages when --verbose is enabled
import os           # For reading environment variables (API keys)
import sys          # For exit codes and error handling
import time         # For measuring generation time
from datetime import datetime  # For timestamps in filenames
from io import BytesIO        # For converting binary image data to file-like object
from pathlib import Path      # For robust file path handling (cross-platform)
from typing import Optional, List, Dict, Any, Union  # Type hints for better code clarity

# ================================================================================
# DEPENDENCY CHECKS - Helps users install missing packages
# ================================================================================

# Check for Google GenAI SDK (the main API library)
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("=" * 60)
    print("Error: google-genai package not installed.")
    print("This package is required to communicate with Gemini API.")
    print("\nTo fix this, run:")
    print("  pip install google-genai")
    print("\nOr install all dependencies at once:")
    print("  pip install google-genai Pillow python-dotenv")
    print("=" * 60)
    sys.exit(1)

# Check for PIL/Pillow (image processing library)
try:
    from PIL import Image
except ImportError:
    print("=" * 60)
    print("Error: PIL (Pillow) package not installed.")
    print("This package is required to process and save images.")
    print("\nTo fix this, run:")
    print("  pip install Pillow")
    print("=" * 60)
    sys.exit(1)

# Check for python-dotenv (loads .env files)
try:
    from dotenv import load_dotenv, find_dotenv
except ImportError:
    print("=" * 60)
    print("Error: python-dotenv package not installed.")
    print("This package is required to load API keys from .env files.")
    print("\nTo fix this, run:")
    print("  pip install python-dotenv")
    print("\nNote: You can still use --api-key flag without this package")
    print("=" * 60)
    sys.exit(1)

# ================================================================================
# LOGGING CONFIGURATION - Sets up debug output for --verbose mode
# ================================================================================

# Configure how log messages appear
# Format: 2024-12-10 14:30:45,123 - INFO - Your message here
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ================================================================================
# MAIN IMAGE GENERATOR CLASS
# ================================================================================

class GeminiImageGenerator:
    """
    Main class that handles all image generation operations.

    This class:
    - Manages API connection
    - Sends prompts to Gemini
    - Processes responses
    - Saves generated images

    Usage:
        generator = GeminiImageGenerator(api_key="your_key")
        result = generator.generate_image("A sunset", aspect_ratio="16:9")
    """

    # ============================================================================
    # CLASS CONSTANTS - Defines available options
    # ============================================================================

    # All supported aspect ratios with descriptions
    # Add new ratios here if Gemini adds support for more
    ASPECT_RATIOS = [
        "1:1",     # Square - Instagram posts, profile pictures
        "16:9",    # Widescreen - YouTube videos, presentations
        "9:16",    # Portrait/Mobile - Stories, TikTok, Reels
        "4:3",     # Classic TV - Older displays, some tablets
        "3:4",     # Portrait classic - Portrait photos
        "2:3",     # Portrait photo - Common print size (4x6")
        "3:2",     # Landscape photo - DSLR standard, 35mm film
    ]

    # The specific model identifier for image generation
    # This might change as Google releases new versions
    MODEL = "gemini-2.5-flash-image"

    # ============================================================================
    # INITIALIZATION - Sets up the API connection
    # ============================================================================

    def __init__(self,
                 api_key: Optional[str] = None,
                 project_id: Optional[str] = None,
                 use_vertex: bool = False,
                 location: str = 'us-central1'):
        """
        Initialize the Gemini Image Generator.

        This method:
        1. Loads API credentials (from arguments or environment)
        2. Decides whether to use direct API or Vertex AI
        3. Creates the API client connection

        Args:
            api_key: Google Gemini API key
                    (if None, looks for GEMINI_API_KEY environment variable)
            project_id: Google Cloud project ID
                       (only needed for Vertex AI, enterprise users)
            use_vertex: Whether to use Vertex AI instead of direct API
                       (Vertex AI is for enterprise/production use)
            location: Vertex AI region (us-central1, europe-west4, etc.)
                     (only matters if using Vertex AI)

        Raises:
            ValueError: If no API key is found anywhere
            RuntimeError: If API client initialization fails
        """
        # Try to get API key from: 1) function argument, 2) environment variable
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        # Project ID is optional, only for Vertex AI users
        self.project_id = project_id or os.getenv('GEMINI_PROJECT_ID')

        # Only use Vertex AI if explicitly requested
        # (Most users will use direct API with just an API key)
        self.use_vertex = use_vertex

        # Vertex AI region (data center location)
        self.location = location

        # Check that we have credentials
        if not self.api_key and not self.use_vertex:
            raise ValueError(
                "\n" + "=" * 60 + "\n"
                "GEMINI_API_KEY environment variable not set!\n\n"
                "To fix this:\n"
                "1. Get an API key from: https://aistudio.google.com/apikey\n"
                "2. Create a .env file in your project directory\n"
                "3. Add this line: GEMINI_API_KEY=your_actual_key_here\n"
                "\nOr pass the key directly:\n"
                "  python script.py 'prompt' --api-key YOUR_KEY\n"
                + "=" * 60
            )

        # Initialize the API client
        self._initialize_client()

    def _initialize_client(self):
        """
        Create the actual API client connection.

        This method handles two scenarios:
        1. Direct API access (most users) - just needs API key
        2. Vertex AI access (enterprise) - needs project ID and auth
        """
        try:
            if self.use_vertex and self.project_id:
                # Vertex AI setup (for enterprise/production use)
                logger.info(f"Initializing Vertex AI client for project: {self.project_id}")
                self.client = genai.Client(
                    vertexai=True,
                    project=self.project_id,
                    location=self.location
                )
            else:
                # Standard API setup (for most users)
                logger.info("Initializing Gemini API client with API key")
                self.client = genai.Client(api_key=self.api_key)
        except Exception as e:
            # Help user understand what went wrong
            raise RuntimeError(
                f"Failed to initialize Gemini client: {e}\n"
                "Common issues:\n"
                "- Invalid API key\n"
                "- Network connection problems\n"
                "- API service temporarily down"
            )

    # ============================================================================
    # MAIN GENERATION METHOD - The heart of the script
    # ============================================================================

    def generate_image(self,
                      prompt: str,
                      input_images: Optional[List[Union[str, Path, Image.Image]]] = None,
                      aspect_ratio: str = "1:1",
                      response_modalities: List[str] = None,
                      output_path: Optional[str] = None,
                      verbose: bool = False) -> Dict[str, Any]:
        """
        Generate an image using the Gemini API.

        This is the main method that:
        1. Takes your prompt and settings
        2. Sends them to Gemini API
        3. Gets back an image
        4. Saves it to disk
        5. Returns info about what was created

        Args:
            prompt: Text description of what you want to generate
                   Examples: "A sunset over mountains"
                            "Make the sky purple" (when editing)

            input_images: List of images to edit or combine (optional)
                         Can be file paths, Path objects, or PIL Images
                         Maximum 3 images recommended by Google

            aspect_ratio: Shape of the output image
                         "1:1" = square (default)
                         "16:9" = widescreen
                         "9:16" = portrait/mobile
                         See ASPECT_RATIOS for all options

            response_modalities: What to get back from API
                                ['Text', 'Image'] = both (default)
                                ['Image'] = just the image

            output_path: Where to save the image
                        None = auto-generate filename with timestamp
                        "my_image.png" = save with this name

            verbose: Whether to print detailed progress info
                    True = show all steps (debugging)
                    False = quiet mode (default)

        Returns:
            Dictionary containing:
                - 'image': PIL Image object (the actual image)
                - 'text': AI's text response (if requested)
                - 'path': Where image was saved
                - 'metadata': Info about generation (time, size, etc.)

        Raises:
            FileNotFoundError: If input image doesn't exist
            ValueError: If API returns no image
            RuntimeError: If generation fails
        """
        # Track how long generation takes
        start_time = time.time()

        # Warn if using non-standard aspect ratio
        # (It might still work, but these are the tested ones)
        if aspect_ratio not in self.ASPECT_RATIOS:
            logger.warning(
                f"Aspect ratio '{aspect_ratio}' not in standard ratios.\n"
                f"Standard ratios are: {', '.join(self.ASPECT_RATIOS)}\n"
                f"Proceeding anyway - it might work!"
            )

        # Step 1: Prepare the content to send to API
        # This handles both text prompts and input images
        contents = self._prepare_contents(prompt, input_images, verbose)

        # Step 2: Configure API settings
        # This sets aspect ratio and response type
        config = self._create_generation_config(aspect_ratio, response_modalities)

        # Show what we're doing if verbose mode is on
        if verbose:
            logger.info(f"Sending request to Gemini API...")
            logger.info(f"Model: {self.MODEL}")
            logger.info(f"Aspect ratio: {aspect_ratio}")
            logger.info(f"Response modalities: {config.response_modalities}")

        try:
            # Step 3: Send request to Gemini API
            # This is the actual API call that generates the image
            response = self.client.models.generate_content(
                model=self.MODEL,      # Which model to use
                contents=contents,     # Prompt and/or images
                config=config         # Settings (aspect ratio, etc.)
            )

            # Step 4: Extract image from response
            # API returns complex object, we need to pull out the image
            result = self._process_response(response, output_path, verbose)

            # Step 5: Add metadata about the generation
            # Useful for tracking what settings produced which images
            result['metadata'] = {
                'model': self.MODEL,
                'aspect_ratio': aspect_ratio,
                'generation_time': time.time() - start_time,
                'timestamp': datetime.now().isoformat(),
                'prompt': prompt,
                'input_images_count': len(input_images) if input_images else 0
            }

            if verbose:
                logger.info(f"Generation completed in {result['metadata']['generation_time']:.2f} seconds")

            return result

        except Exception as e:
            # Provide helpful error message
            logger.error(f"Generation failed: {e}")
            raise RuntimeError(
                f"Failed to generate image: {e}\n"
                "Common issues:\n"
                "- API quota exceeded (wait and retry)\n"
                "- Invalid prompt (try simpler text)\n"
                "- Network timeout (check connection)\n"
                "- Service temporarily unavailable (retry later)"
            )

    # ============================================================================
    # HELPER METHOD 1 - Prepare content for API
    # ============================================================================

    def _prepare_contents(self,
                         prompt: str,
                         input_images: Optional[List[Union[str, Path, Image.Image]]],
                         verbose: bool) -> List:
        """
        Prepare the prompt and images for sending to API.

        The API expects content in a specific format:
        - Text prompts as strings
        - Images as PIL Image objects
        - Everything in a list

        Args:
            prompt: The text description
            input_images: Optional images to include
            verbose: Whether to log progress

        Returns:
            List containing prompt and any images

        Example return value:
            ["Generate a sunset", <PIL Image>, <PIL Image>]
        """
        # Start with the text prompt
        contents = [prompt]

        # Add any input images
        if input_images:
            if verbose:
                logger.info(f"Processing {len(input_images)} input image(s)...")

            # Process each image
            for idx, img_input in enumerate(input_images):
                # Handle different input types
                if isinstance(img_input, (str, Path)):
                    # It's a file path - load the image
                    img_path = Path(img_input)
                    if not img_path.exists():
                        raise FileNotFoundError(
                            f"Image file not found: {img_path}\n"
                            f"Current directory: {Path.cwd()}\n"
                            f"Check that the path is correct!"
                        )
                    img = Image.open(img_path)

                elif isinstance(img_input, Image.Image):
                    # It's already a PIL Image object
                    img = img_input

                else:
                    # Unknown type
                    raise ValueError(
                        f"Invalid image type: {type(img_input)}\n"
                        f"Expected: file path string or PIL Image object"
                    )

                # Add to contents list
                contents.append(img)

                # Log image info if verbose
                if verbose:
                    logger.info(f"  - Image {idx+1}: {img.size[0]}x{img.size[1]} pixels")

        return contents

    # ============================================================================
    # HELPER METHOD 2 - Create API configuration
    # ============================================================================

    def _create_generation_config(self,
                                 aspect_ratio: str,
                                 response_modalities: Optional[List[str]]) -> types.GenerateContentConfig:
        """
        Create the configuration object for the API request.

        This tells the API:
        - What aspect ratio to use
        - Whether to return text, image, or both

        Args:
            aspect_ratio: Like "16:9" or "1:1"
            response_modalities: What to return from API

        Returns:
            Configuration object for the API
        """
        config_dict = {}

        # Set what we want back from the API
        if response_modalities:
            # User specified what they want
            config_dict['response_modalities'] = response_modalities
        else:
            # Default: get both text and image
            config_dict['response_modalities'] = ['Text', 'Image']

        # Set the image configuration
        # Currently only aspect_ratio is supported
        # Future versions might add resolution, quality, etc.
        config_dict['image_config'] = types.ImageConfig(
            aspect_ratio=aspect_ratio
        )

        # Create and return the config object
        return types.GenerateContentConfig(**config_dict)

    # ============================================================================
    # HELPER METHOD 3 - Process API response
    # ============================================================================

    def _process_response(self,
                         response: Any,
                         output_path: Optional[str],
                         verbose: bool) -> Dict[str, Any]:
        """
        Extract the image and text from the API response.

        The API returns a complex object with candidates, parts, etc.
        This method extracts the useful bits: the image and any text.

        Args:
            response: Raw API response object
            output_path: Where to save the image (optional)
            verbose: Whether to log progress

        Returns:
            Dictionary with 'image', 'text', and 'path' keys

        Raises:
            ValueError: If no image data in response
        """
        result = {}

        # Extract text response if present
        # The API might include a text description along with the image
        text_parts = []
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'text') and part.text:
                text_parts.append(part.text)

        if text_parts:
            result['text'] = '\n'.join(text_parts)
            if verbose:
                # Show first 200 chars of text
                preview = result['text'][:200]
                if len(result['text']) > 200:
                    preview += "..."
                logger.info(f"Text response: {preview}")

        # Extract image data
        # Image comes as binary data in inline_data
        image_parts = [
            part.inline_data.data
            for part in response.candidates[0].content.parts
            if hasattr(part, 'inline_data') and part.inline_data
        ]

        # Check we got an image
        if not image_parts:
            raise ValueError(
                "No image data found in response!\n"
                "Possible issues:\n"
                "- API error (try again)\n"
                "- Content filtered by safety settings\n"
                "- Invalid prompt"
            )

        # Convert binary data to PIL Image
        # BytesIO makes binary data act like a file
        image = Image.open(BytesIO(image_parts[0]))
        result['image'] = image

        if verbose:
            logger.info(f"Generated image size: {image.size[0]}x{image.size[1]} pixels")

        # Save image if path provided
        if output_path:
            image.save(output_path)
            result['path'] = output_path
            if verbose:
                logger.info(f"Image saved to: {output_path}")

        return result

# ================================================================================
# UTILITY FUNCTION - Find .env file
# ================================================================================

def find_env_file() -> Optional[Path]:
    """
    Search for .env file in current directory or parent directories.

    This allows you to run the script from subdirectories
    and still find the .env file in the project root.

    Search order:
    1. Current directory
    2. Parent directory
    3. Grandparent directory
    4. Up to 5 levels up

    Returns:
        Path to .env file if found, None otherwise

    Example:
        If you're in /project/scripts/test/
        This will search:
        - /project/scripts/test/.env
        - /project/scripts/.env
        - /project/.env
        - /.env (up to 5 levels)
    """
    current = Path.cwd()

    # Search up to 5 parent directories
    # (Most projects aren't nested deeper than this)
    for _ in range(5):
        env_path = current / '.env'
        if env_path.exists():
            return env_path

        # Move up one directory
        parent = current.parent

        # Stop if we've reached the root
        if parent == current:
            break

        current = parent

    return None

# ================================================================================
# MAIN FUNCTION - Command-line interface
# ================================================================================

def main():
    """
    Main entry point for the script when run from command line.

    This function:
    1. Loads environment variables
    2. Parses command-line arguments
    3. Creates the generator
    4. Generates the image
    5. Displays results

    Exit codes:
    - 0: Success
    - 1: Error occurred
    """

    # ============================================================================
    # STEP 1: Load environment variables
    # ============================================================================

    # Look for .env file
    env_path = find_env_file()
    if env_path:
        # Found it - load the variables
        load_dotenv(env_path)
        logger.info(f"Loaded environment from: {env_path}")
    else:
        # Not found - try default location anyway
        # (python-dotenv will check current directory)
        load_dotenv()

    # ============================================================================
    # STEP 2: Set up command-line argument parser
    # ============================================================================

    # Create parser with description and examples
    parser = argparse.ArgumentParser(
        description="Generate images using Google's Gemini 2.5 Flash Image model (Nano Banana)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "A beautiful sunset over mountains"
  %(prog)s "Make the sky purple" --input-image photo.jpg
  %(prog)s "Abstract art" --aspect-ratio 16:9 --image-only
  %(prog)s "A futuristic city" --output future_city.png --verbose
        """
    )

    # ============================================================================
    # REQUIRED ARGUMENTS
    # ============================================================================

    parser.add_argument(
        'prompt',
        help='Text prompt for image generation or editing'
    )

    # ============================================================================
    # OPTIONAL ARGUMENTS - Each one explained
    # ============================================================================

    # Input images for editing
    parser.add_argument(
        '--input-image', '-i',
        action='append',           # Allow multiple -i flags
        dest='input_images',        # Store in args.input_images
        help='Path to input image(s) for editing (can be used multiple times, max 3 recommended)'
    )

    # Aspect ratio selection
    parser.add_argument(
        '--aspect-ratio', '-ar',
        default='1:1',              # Default to square
        choices=GeminiImageGenerator.ASPECT_RATIOS,  # Limit to valid ratios
        help='Aspect ratio for the generated image (default: 1:1)'
    )

    # Output filename
    parser.add_argument(
        '--output', '-o',
        default=None,               # None means auto-generate name
        help='Output path for the generated image (default: generated_TIMESTAMP.png)'
    )

    # Image-only mode
    parser.add_argument(
        '--image-only',
        action='store_true',        # Boolean flag
        help='Generate only image without text response'
    )

    # API key override
    parser.add_argument(
        '--api-key',
        help='Gemini API key (overrides environment variable)'
    )

    # Vertex AI project
    parser.add_argument(
        '--project-id',
        help='Google Cloud project ID (for Vertex AI)'
    )

    # Use Vertex AI
    parser.add_argument(
        '--vertex',
        action='store_true',
        help='Use Vertex AI instead of direct API'
    )

    # Vertex AI location
    parser.add_argument(
        '--location',
        default='us-central1',
        help='Vertex AI location (default: us-central1)'
    )

    # Verbose output
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    # JSON output
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output result as JSON'
    )

    # ============================================================================
    # STEP 3: Parse arguments
    # ============================================================================

    args = parser.parse_args()

    # ============================================================================
    # STEP 4: Prepare for generation
    # ============================================================================

    # Determine response modalities based on --image-only flag
    response_modalities = ['Image'] if args.image_only else ['Text', 'Image']

    # Generate default output filename if not provided
    if not args.output:
        # Create timestamp-based filename
        # Example: generated_20241210_143045.png
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = f"generated_{timestamp}.png"

    # ============================================================================
    # STEP 5: Generate the image
    # ============================================================================

    try:
        # Create generator instance
        generator = GeminiImageGenerator(
            api_key=args.api_key,
            project_id=args.project_id,
            use_vertex=args.vertex,
            location=args.location
        )

        # Generate the image
        result = generator.generate_image(
            prompt=args.prompt,
            input_images=args.input_images,
            aspect_ratio=args.aspect_ratio,
            response_modalities=response_modalities,
            output_path=args.output,
            verbose=args.verbose
        )

        # ============================================================================
        # STEP 6: Display results
        # ============================================================================

        if args.json:
            # JSON output for scripts/automation
            # Note: Can't include PIL Image object in JSON
            json_result = {
                'success': True,
                'path': result.get('path', args.output),
                'text': result.get('text', ''),
                'metadata': result['metadata']
            }
            print(json.dumps(json_result, indent=2))

        else:
            # Human-readable output
            print(f"\n✅ Image generated successfully!")
            print(f"📁 Saved to: {result.get('path', args.output)}")

            # Show text response if present
            if 'text' in result:
                print(f"\n📝 Response: {result['text']}")

            # Show generation statistics
            print(f"\n⏱️  Generation time: {result['metadata']['generation_time']:.2f} seconds")
            print(f"📐 Aspect ratio: {result['metadata']['aspect_ratio']}")
            print(f"🖼️  Image size: {result['image'].size[0]}x{result['image'].size[1]} pixels")

    except Exception as e:
        # ============================================================================
        # ERROR HANDLING - Help user understand what went wrong
        # ============================================================================

        if args.json:
            # JSON error format
            print(json.dumps({'success': False, 'error': str(e)}, indent=2))
        else:
            # Human-readable error
            print(f"\n❌ Error: {e}", file=sys.stderr)

            # Add helpful suggestions based on error
            if "API key" in str(e):
                print("\n💡 Tip: Check your API key is valid at https://aistudio.google.com")
            elif "not found" in str(e):
                print("\n💡 Tip: Check file paths are correct")
            elif "quota" in str(e).lower():
                print("\n💡 Tip: You may have exceeded your API quota. Wait and try again.")

        sys.exit(1)

# ================================================================================
# SCRIPT ENTRY POINT - This runs when script is executed directly
# ================================================================================

if __name__ == "__main__":
    # This block only runs when script is executed directly,
    # not when imported as a module
    main()

# ================================================================================
# END OF SCRIPT
# ================================================================================
#
# For developers modifying this script:
#
# 1. To add a new aspect ratio:
#    - Add it to ASPECT_RATIOS list (line ~105)
#    - No other changes needed
#
# 2. To add a new command-line option:
#    - Add parser.add_argument() in main() function
#    - Use the new arg in generate_image() call
#
# 3. To change the model:
#    - Update MODEL constant (line ~112)
#    - Check if API parameters need adjustment
#
# 4. To add new image formats:
#    - Modify Image.save() call to check extension
#    - PIL handles most formats automatically
#
# 5. Common debugging:
#    - Use --verbose flag to see all API communication
#    - Check .env file is in the right location
#    - Verify API key at https://aistudio.google.com
#
# API Rate Limits (as of Dec 2024):
# - Free tier: 500 requests per day
# - Paid tier: Based on your plan
# - Each request can take 5-15 seconds
#
# ================================================================================