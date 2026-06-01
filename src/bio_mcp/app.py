from fastmcp import FastMCP
from bio_mcp.tools.gromacsAnalysis import analyze_rmsd

mcp = FastMCP(name="BioInfo Analysis MCP")

mcp.add_tool(analyze_rmsd)

def main():
    mcp.run(transport="http", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()