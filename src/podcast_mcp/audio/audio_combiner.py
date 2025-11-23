from pydub import AudioSegment
import os
from typing import List

def combine_segments(segment_paths: List[str], pause_ms: int, output_path: str, format: str = "wav") -> str:
    """
    Combines multiple audio files into one with a pause between them.
    
    Args:
        segment_paths: List of paths to audio segments
        pause_ms: Duration of pause between segments in milliseconds
        output_path: Path where the combined audio will be saved
        format: Audio format (default: "wav")
        
    Returns:
        str: Path to the output file
        
    Raises:
        ValueError: If segment_paths is empty
    """
    if not segment_paths:
        raise ValueError("No segments to combine")

    combined = AudioSegment.empty()
    pause = AudioSegment.silent(duration=pause_ms)

    for i, path in enumerate(segment_paths):
        segment = AudioSegment.from_file(path)
        combined += segment
        
        # Add pause if not the last segment
        if i < len(segment_paths) - 1:
            combined += pause

    # Ensure output directory exists (if path has a directory component)
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    combined.export(output_path, format=format)
    return output_path
