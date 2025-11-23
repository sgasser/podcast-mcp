from mcp.server.fastmcp import FastMCP, Context
from .tools.generate_podcast import GeneratePodcastTool
from .config import Config
import logging

# Setup logging to stderr (MCP best practice)
# Claude Desktop automatically captures stderr logs to ~/Library/Logs/Claude/mcp-server-podcast-mcp.log
logging.basicConfig(
    level=getattr(logging, Config.MCP_LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Initialize FastMCP
mcp = FastMCP(Config.MCP_SERVER_NAME)

# Initialize tools
podcast_tool = GeneratePodcastTool()

@mcp.tool()
async def generate_podcast(script: str, ctx: Context) -> str:
    """
    Generates a podcast dialogue with AI voices.
    
    Supports 1-4 distinct speakers. Use <voice1>, <voice2>, <voice3>, <voice4> tags to mark who is speaking.
    Each voice will automatically get a unique AI voice (2 female, 2 male by default).
    
    IMPORTANT: Write numbers as words (e.g. "four to zero" instead of "4:0") to prevent pronunciation errors.
    
    Example with 2 voices:
        <voice1>Welcome to our podcast!
        <voice2>Thanks for having me.
        <voice1>Let's dive into today's topic.
    
    Example with 3 voices (panel discussion):
        <voice1>Today we're discussing AI safety.
        <voice2>I think regulation is crucial.
        <voice3>But innovation shouldn't be stifled.
        <voice1>Both valid points. Let's explore this.
        
    Optional parameters (add at the start):
        language: de
        filename: barcelona_vs_bilbao.wav
        
        <voice1>Willkommen zu unserem Podcast!
        <voice2>Danke für die Einladung.
    
    Args:
        script: The dialogue script with <voice1>, <voice2>, etc. tags
        
    Returns:
        Success message with output file path, or error message
    """
    result = await podcast_tool.run_async(script, ctx)
    
    # Convert result dict to a simple string or TOON-like response
    if result["success"]:
        return (
            f"success: true\n"
            f"output_file: {result['output_file']}\n"
            f"processing_time_seconds: {result['processing_time_seconds']}\n"
            f"total_segments: {result['total_segments']}"
        )
    else:
        return (
            f"success: false\n"
            f"error: {result.get('error')}"
        )


def main():
    mcp.run()

if __name__ == "__main__":
    main()
