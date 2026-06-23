from fastmcp import FastMCP
from bio_mcp.tools.gromacsAnalysis import analyze_gyrate, analyze_hbond, analyze_rmsd, analyze_rmsf, analyze_sasa
from bio_mcp.tools.fileTools import (
    list_topology_files, list_trajectory_files, list_tpr_files,
    list_top_files, list_index_files, list_itp_files,
    list_amber_top_files, list_amber_traj_files,
    delete_file, delete_amber_file, create_index_file,
)

mcp = FastMCP(name="BioInfo Analysis MCP")

# GROMACS analysis tools
mcp.tool(title="RMSD Analysis")(analyze_rmsd)
mcp.tool(title="RMSF Fluctuations")(analyze_rmsf)
mcp.tool(title="Solvent Accessible Surface Area")(analyze_sasa)
mcp.tool(title="Radius of Gyration")(analyze_gyrate)
mcp.tool(title="Hydrogen Bond Tracker")(analyze_hbond)

# File listing tools
mcp.tool(title="List Topology Files")(list_topology_files)
mcp.tool(title="List Trajectory Files")(list_trajectory_files)
mcp.tool(title="List TPR Files")(list_tpr_files)
mcp.tool(title="List TOP Files")(list_top_files)
mcp.tool(title="List Index Files")(list_index_files)
mcp.tool(title="List ITP Files")(list_itp_files)
mcp.tool(title="List AMBER Topology Files")(list_amber_top_files)
mcp.tool(title="List AMBER Trajectory Files")(list_amber_traj_files)

# File management tools
mcp.tool(title="Delete GROMACS File")(delete_file)
mcp.tool(title="Delete AMBER File")(delete_amber_file)
mcp.tool(title="Create GROMACS Index File")(create_index_file)

def main():
    mcp.run(transport="http", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()