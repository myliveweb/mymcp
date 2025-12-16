import sys
from fastmcp import FastMCP

mcp = FastMCP("My MCP Server")

@mcp.tool
def get_python_version() -> str:
    """Возвращает версию Python."""
    return f"Python version: {sys.version}"

if __name__ == "__main__":
    mcp.run()
