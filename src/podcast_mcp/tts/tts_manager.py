import os
import logging
import threading
from typing import Any, Optional
from ..config import Config

# Try importing TTS, but don't fail immediately if not present (allows for testing without full install)
try:
    from TTS.api import TTS
except ImportError:
    TTS = None

logger = logging.getLogger(__name__)

class TTSManager:
    _instance: Optional["TTSManager"] = None
    _lock: threading.Lock = threading.Lock()
    _model: Any = None
    
    # Get speaker names from config
    @property
    def SPEAKERS(self) -> dict[str, str]:
        return {
            "1": Config.VOICE_1,
            "2": Config.VOICE_2,
            "3": Config.VOICE_3,
            "4": Config.VOICE_4
        }

    def __new__(cls) -> "TTSManager":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(TTSManager, cls).__new__(cls)
        return cls._instance

    def load_model(self) -> None:
        """Loads the TTS model if not already loaded."""
        if self._model is None:
            with self._lock:
                if self._model is None:
                    if TTS is None:
                        raise ImportError("Coqui TTS is not installed. Please install 'coqui-tts'.")
                    
                    logger.info(f"Loading TTS model: {Config.XTTS_MODEL} on {Config.XTTS_DEVICE}")
                    self._model = TTS(model_name=Config.XTTS_MODEL).to(Config.XTTS_DEVICE)
                    logger.info("Model loaded successfully")

    def generate_segment(self, text: str, speaker_id: str, language: str, output_path: str) -> str:
        """
        Generate speech using standard TTS speakers (no voice cloning).
        
        Args:
            text: Text to synthesize
            speaker_id: "1", "2", "3", or "4" for different voices
            language: Language code (e.g., "en", "de")
            output_path: Where to save the audio file
            
        Returns:
            str: Path to the generated audio file
        """
        if self._model is None:
            self.load_model()
        
        # Get speaker name from mapping
        speaker_name = self.SPEAKERS.get(speaker_id, self.SPEAKERS["1"])
        
        logger.info(f"Generating TTS: '{text[:30]}...' (speaker={speaker_name}, lang={language})")
        
        # Use standard TTS without voice cloning
        # Note: TTS model inference might not be thread-safe depending on implementation/device
        # but the singleton access is now safe.
        # We might want to lock inference too if the underlying library isn't thread safe,
        # but for now we assume it handles it or we accept the risk for parallel requests.
        # Given this is a local tool, high concurrency is unlikely.
        if self._model:
             self._model.tts_to_file(
                text=text,
                speaker=speaker_name,
                language=language,
                file_path=output_path,
                speed=Config.TTS_SPEED
            )
        return output_path
