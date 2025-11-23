# Podcast MCP 🎙️

Generate professional multi-speaker podcasts directly inside Claude Desktop.

## ✨ Features

- **Real AI Voices**: Uses high-quality voices (not robotic text-to-speech).
- **Multi-Speaker**: Supports up to 4 distinct speakers automatically.
- **Zero Config**: Works instantly after installation.
- **Privacy First**: All processing happens locally on your machine.

## 🚀 Installation

### Prerequisites

You need `uv` installed on your system via Homebrew (required for Claude Desktop to find it):

```bash
# macOS
brew install uv

# Linux/Other
# Use Homebrew on Linux, or ensure uv is in system PATH
# See: https://docs.astral.sh/uv/getting-started/installation/
```

**Important**: Installing via Homebrew ensures `uv` is in the system PATH that Claude Desktop can access.

### Install the MCP Server

1. Download **`podcast-mcp.mcpb`** from the releases.
2. Drag and drop the file into **Claude Desktop**.
3. That's it! 🎉

## 💡 Tips for Best Quality

- **Speed**: If it feels too slow, increase `TTS_SPEED` in `.env` (e.g. to 1.3 or 1.5).
- **Pauses**: You can adjust `DEFAULT_PAUSE_MS` in `.env` if the gaps between speakers are too long.
- **Remember**: Restart Claude Desktop after changing `.env` for changes to take effect.

## 💡 How to Use

Simply ask Claude to create a podcast. You don't need to worry about formats or technical details.

**Try this:**

> "Generate an audio podcast about the history of coffee."

**Works in 20+ languages** (German example):

> "Erstelle eine Audio-Podcast-Datei über die Geschichte des Kaffees."

Claude will handle everything: writing the script, assigning voices, and generating the audio file.

## ⚙️ Configuration (Optional)

The default settings work great, but you can customize them if you want.

A `.env` file is automatically created on first run. To customize:

1. Open the `podcast-mcp` folder (where Claude installed it).
2. Edit the `.env` file to customize:
   - **Voices**: Choose from 50+ available speakers.
   - **Speed**: Adjust speaking rate (default is 1.2x).
   - **Output Folder**: Change where files are saved (default: `~/Downloads`).
   - **Log Level**: Set to DEBUG for detailed logs (default: INFO).
3. Restart Claude Desktop for changes to take effect.

## ❓ FAQ

**Where are my podcasts saved?**
By default, they appear in your **Downloads** folder.

**Can I use my own voices?**
Currently, we support the built-in high-quality voices from Coqui XTTS-v2.

**Does it work offline?**
Yes! The first time you run it, it downloads the AI model (~2GB). After that, it works entirely offline.

**Where can I find debug logs?**
Claude Desktop automatically captures all logs to `~/Library/Logs/Claude/mcp-server-podcast-mcp.log`. You can view them with:
```bash
tail -f ~/Library/Logs/Claude/mcp-server-podcast-mcp.log
```
To change the log level, edit `MCP_LOG_LEVEL` in `.env` (options: DEBUG, INFO, WARNING, ERROR).

## 🙏 Acknowledgments

This project is built on excellent open source software:

- **[Coqui TTS](https://github.com/coqui-ai/TTS)** - High-quality text-to-speech with XTTS-v2 model
- **[MCP](https://github.com/modelcontextprotocol)** - Model Context Protocol for Claude integration
- **[pydub](https://github.com/jiaaro/pydub)** - Audio processing and manipulation
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package manager
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment configuration management

---

**License**: MIT | **Author**: Stefan Gasser
