import re
import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

MAX_SCRIPT_LENGTH = 100000  # 100k chars limit

def parse_script(script: str) -> dict[str, Any]:
    """
    Parse a script with <voice1> and <voice2> tags into dialogue segments.
    
    Format:
        language: en
        filename: my_podcast.wav
        
        <voice1>Text for voice 1
        <voice2>Text for voice 2
        <voice1>More text for voice 1
        
    Args:
        script: The script text with voice tags
        
    Returns:
        dict with 'dialogue' list, 'language', and optional 'filename'
    """
    if len(script) > MAX_SCRIPT_LENGTH:
        raise ValueError(f"Script too long ({len(script)} chars). Max allowed is {MAX_SCRIPT_LENGTH}.")

    # Extract language if specified (optional)
    language = "en"
    language_match = re.search(r'language:\s*(\w+)', script, re.IGNORECASE)
    if language_match:
        language = language_match.group(1)
    
    # Extract filename if specified (optional)
    filename: str | None = None
    filename_match = re.search(r'filename:\s*(.+?)(?:\n|$)', script, re.IGNORECASE)
    if filename_match:
        raw_filename = filename_match.group(1).strip()
        # Sanitize filename to prevent path traversal
        filename = os.path.basename(raw_filename)
        # Ensure .wav extension
        if not filename.endswith('.wav'):
            filename += '.wav'
    
    # Parse voice tags
    dialogue: list[dict[str, str]] = []
    
    # Check for text outside tags (e.g. intro without tag)
    first_tag_match = re.search(r'<voice\d+>', script)
    if first_tag_match:
        pre_text = script[:first_tag_match.start()].strip()
        # Remove header lines (language:, filename:) from check
        pre_text = re.sub(r'(language|filename):.*(\n|$)', '', pre_text, flags=re.IGNORECASE).strip()
        if pre_text:
            logger.warning(f"Found text outside voice tags: '{pre_text[:50]}...'. This text will be ignored.")

    # Find all <voiceN> tags with their content
    # Pattern handles both <voice1>text and <voice1>text</voice1> formats
    pattern = r'<voice(\d+)>(.*?)(?:</voice\d+>|(?=<voice\d+>)|$)'
    matches = re.findall(pattern, script, re.DOTALL)
    
    for voice_num, text in matches:
        # Strip whitespace and any remaining closing tags
        text = text.strip()
        # Remove any closing tags that might have been captured
        text = re.sub(r'</voice\d+>', '', text).strip()
        if text:  # Only add non-empty segments
            dialogue.append({
                "speaker": voice_num,  # "1", "2", "3", etc.
                "text": text
            })
    
    if not dialogue:
        raise ValueError("No dialogue found. Use <voice1>, <voice2>, etc. tags to mark dialogue.")
    
    result = {
        "language": language,
        "dialogue": dialogue,
        "output": {"file": filename or "podcast.wav"}  # Use custom filename or default
    }
    
    return result
