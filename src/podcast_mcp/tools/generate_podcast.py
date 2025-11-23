import os
import time
import logging
import asyncio
from typing import Any
from ..parser.script_parser import parse_script
from ..tts.tts_manager import TTSManager
from ..audio.audio_combiner import combine_segments
from ..config import Config

logger = logging.getLogger(__name__)

class GeneratePodcastTool:
    def __init__(self):
        self.tts = TTSManager()

    async def run_async(self, script: str, ctx) -> dict[str, Any]:
        """
        Executes the podcast generation flow with progress updates.
        """
        # Ensure output and temp directories exist
        Config.ensure_dirs()
        
        start_time = time.time()
        temp_files: list[str] = []
        
        try:
            # Parse script
            try:
                data = parse_script(script)
            except Exception as e:
                logger.error(f"Failed to parse script: {e}")
                return {"success": False, "error": f"Script parsing error: {str(e)}"}

            dialogue_data: list[dict[str, str]] = data.get("dialogue", [])
            language: str = data.get("language", "en")
            output_config: dict[str, Any] = data.get("output", {})

            if not dialogue_data:
                return {"success": False, "error": "No dialogue found in script"}

            # Identify all unique speakers used in the script
            used_speaker_ids = set(d["speaker"] for d in dialogue_data)
            
            # Create speaker map dynamically
            speaker_map: dict[str, dict[str, str]] = {}
            for speaker_id in used_speaker_ids:
                # We assume all speakers use the same language for now
                speaker_map[speaker_id] = {"id": speaker_id, "language": language}

            # 2. Generate Audio Segments
            total_segments = len(dialogue_data)
            
            logger.info(f"Starting generation of {total_segments} segments...")
            
            # Report initial progress
            await ctx.report_progress(progress=0, total=total_segments)
            
            for i, line in enumerate(dialogue_data):
                speaker_id = line["speaker"]
                text = line["text"]
                speaker_info = speaker_map[speaker_id]
                segment_language = speaker_info.get("language", "en")

                # Progress update
                logger.info(f"Generating segment {i+1}/{total_segments}: '{text[:50]}...'")
                await ctx.report_progress(progress=i, total=total_segments)

                segment_filename = f"segment_{i}_{int(time.time()*1000)}.wav"
                segment_path = os.path.join(Config.TEMP_DIR, segment_filename)
                temp_files.append(segment_path)
                
                # Use speaker_id directly (no voice files needed)
                # Run TTS in executor to avoid blocking
                await asyncio.to_thread(
                    self.tts.generate_segment, text, speaker_id, segment_language, segment_path
                )
                
                logger.info(f"✓ Segment {i+1}/{total_segments} complete")
                await ctx.report_progress(progress=i+1, total=total_segments)

            # 3. Combine Audio
            output_file = output_config.get("file", "podcast.wav")
            if not os.path.isabs(output_file):
                output_file = os.path.join(Config.OUTPUT_DIR, output_file)
            
            pause_ms = output_config.get("pause_ms", Config.DEFAULT_PAUSE_MS)
            output_format = output_config.get("format", Config.DEFAULT_FORMAT)
            
            final_path = await asyncio.to_thread(
                combine_segments, temp_files, pause_ms, output_file, output_format
            )
            
            duration = time.time() - start_time
            
            logger.info(f"✓ Podcast generation complete! Output: {final_path}")
            
            return {
                "success": True,
                "output_file": final_path,
                "processing_time_seconds": round(duration, 2),
                "total_segments": len(dialogue_data),
                "message": f"Successfully generated {len(dialogue_data)} segments in {round(duration, 2)}s"
            }

        except Exception as e:
            logger.exception("Generation failed")
            return {"success": False, "error": str(e)}
            
        finally:
            # Cleanup - runs even if exception occurs
            for f in temp_files:
                try:
                    if os.path.exists(f):
                        os.remove(f)
                except OSError:
                    pass

    def run(self, script: str) -> dict[str, Any]:
        """
        Executes the podcast generation flow (sync version for backwards compatibility).
        """
        # Create a minimal context that does nothing on report_progress
        class SyncContext:
            async def report_progress(self, progress: float, total: float | None = None, message: str | None = None) -> None:
                pass # No-op for sync execution

        return asyncio.run(self.run_async(script, SyncContext()))
