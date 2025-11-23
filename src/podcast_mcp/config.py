import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

# Auto-create .env from .env.example if it doesn't exist
def ensure_env_file():
    """Create .env from .env.example if it doesn't exist."""
    # Find the project root (where manifest.json is)
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent  # src/podcast_mcp/config.py -> root

    env_file = project_root / ".env"
    env_example = project_root / ".env.example"

    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)

ensure_env_file()
load_dotenv()

class Config:
    XTTS_MODEL: str = os.getenv("XTTS_MODEL", "tts_models/multilingual/multi-dataset/xtts_v2")
    XTTS_DEVICE: str = os.getenv("XTTS_DEVICE", "cpu")
    TTS_SPEED: float = float(os.getenv("TTS_SPEED", "1.2"))
    
    # Voice configuration (best defaults: warm female + deep male)
    VOICE_1: str = os.getenv("VOICE_1", "Annmarie Nele")    # Female (warm, clear)
    VOICE_2: str = os.getenv("VOICE_2", "Damien Black")     # Male (deep, professional)
    VOICE_3: str = os.getenv("VOICE_3", "Sofia Hellen")     # Female (professional, news)
    VOICE_4: str = os.getenv("VOICE_4", "Craig Gutsy")      # Male (energetic)
    
    # Use Downloads for output and hidden temp directory
    _HOME_DIR: str = os.path.expanduser("~")
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", os.path.join(_HOME_DIR, "Downloads"))
    TEMP_DIR: str = os.getenv("TEMP_DIR", os.path.join(_HOME_DIR, ".podcast-mcp-temp"))
    
    DEFAULT_SAMPLE_RATE: int = int(os.getenv("DEFAULT_SAMPLE_RATE", "24000"))
    DEFAULT_PAUSE_MS: int = int(os.getenv("DEFAULT_PAUSE_MS", "800"))
    DEFAULT_FORMAT: str = os.getenv("DEFAULT_FORMAT", "wav")
    
    MCP_SERVER_NAME: str = os.getenv("MCP_SERVER_NAME", "podcast-mcp")
    MCP_LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")

    @classmethod
    def ensure_dirs(cls) -> None:
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
