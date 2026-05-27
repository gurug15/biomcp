




from bio_mcp.models.gromacs import RMSDGromacsInput


def analyzeRmsd(inputArray:RMSDGromacsInput[])->list[list[list[float]]]:
    """
    to run gromacs rmsd Analysis
    """
    payload = [i.model_dump() for i in inputArray]
    graphData:list[list[list[float]]] = []
    cookies = {
        
    }



    return graphData;