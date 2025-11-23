import unittest
import os
import asyncio
from unittest.mock import MagicMock, patch
import sys

# Mock pydub and TTS before importing modules that use them
sys.modules['pydub'] = MagicMock()
sys.modules['TTS.api'] = MagicMock()

from podcast_mcp.tools.generate_podcast import GeneratePodcastTool
from podcast_mcp.config import Config

class TestPipeline(unittest.TestCase):
    def setUp(self):
        pass

    @patch('podcast_mcp.tools.generate_podcast.combine_segments')
    def test_run_flow(self, mock_combine):
        tool = GeneratePodcastTool()
        
        # Mock internal components
        tool.tts.generate_segment = MagicMock()
        mock_combine.return_value = "/path/to/output.wav"
        
        script = """
<voice1>Hello</voice1>
"""
        result = tool.run(script)
        
        self.assertTrue(result["success"], f"Failed: {result.get('error')}")
        self.assertEqual(result["output_file"], "/path/to/output.wav")
        
        # Verify TTS was called
        tool.tts.generate_segment.assert_called_once()
        
        # Verify combine was called
        mock_combine.assert_called_once()

if __name__ == '__main__':
    unittest.main()
