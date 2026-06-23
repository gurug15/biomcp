from typing import Optional

from pydantic import BaseModel, Field


class RMSDGromacsInput(BaseModel):
    topologyFileName: str  = Field(...,min_length=1, description="topology filename can't be blank")
    trajectoryFileName: str  = Field(...,min_length=1, description="topology filename can't be blank")
    indexFileName: Optional[str] = None
    outputfileName: Optional[str] = None
    grouplsfit: Optional[int] = None
    groupRMSD: Optional[int] = None
    firstFrameno: int = Field(default=0, ge=0)
    lastFrameNo: Optional[int] = None
    
    fitMethod: Optional[str] = None
    dt: Optional[float] = None
    skip: Optional[int] = None
    
    massWeighted: bool = False
    noPbc: bool = False


class RmsfGromacsUserInput(BaseModel):
    topologyFileName:str = Field(...,min_length=1,description="Topology filename can't be blank")
    trajectoryFileName:str = Field(...,min_length=1,description="Trajectory filename can't be blank")
    outputfileName:Optional[str] = None
    indexFileName:Optional[str] = None
    logFileName:Optional[str] = None

    grouplsfit:Optional[int] = None
    firstFrameno:Optional[int] = Field(default=0, ge=0)
    lastFrameNo:Optional[int] = None

    superimpose:bool = False 
    residueRMSF:bool = False

class GyrateGromacsUserInput(BaseModel):
    topologyFileName: str = Field(
        ..., min_length=1,
        description="topology filename can't be blank"
    )

    trajectoryFileName: str = Field(
        ..., min_length=1,
        description="trajectory fileName can't be blank"
    )

    outputfileName: Optional[str] = None
    indexFileName: Optional[str] = None

    firstFrameno: int = Field(default=0, ge=0)
    lastFrameNo: Optional[int] = None

    grouplsfit: Optional[int] = None


class SasaGromacsUserInput(BaseModel):
    topologyFileName: str = Field(
        ..., min_length=1,
        description="topology filename can't be blank"
    )

    trajectoryFileName: str = Field(
        ..., min_length=1,
        description="trajectory fileName can't be blank"
    )

    # output files
    outputfileName: Optional[str] = None
    outputResFileName: Optional[str] = None
    outputAtomFileName: Optional[str] = None
    outputDGFileName: Optional[str] = None
    logFileName: Optional[str] = None

    # optional
    indexFileName: Optional[str] = None
    groupIndex: Optional[int] = None
    tvGroupIndex: Optional[int] = None

    # parameters
    probeRadius: Optional[float] = None
    ndots: Optional[int] = None
    pbc: Optional[bool] = None
    surface: Optional[bool] = None
    output: Optional[bool] = None

    # time range
    beginTime: Optional[float] = None
    endTime: Optional[float] = None
    skip: Optional[int] = None

class HBondGromacsUserInput(BaseModel):
    topologyFileName: str = Field(
        ...,
        min_length=1,
        description="Topology file name is required (must be .tpr, e.g. MD.tpr)"
    )

    trajectoryFileName: str = Field(
        ...,
        min_length=1,
        description="Trajectory file name is required (e.g. MD.xtc or MD.trr)"
    )

    proteinGroupName: str = Field(
        ...,
        min_length=1,
        description="Protein group name is required (e.g. 'Protein')"
    )

    ligandGroupName: str = Field(
        ...,
        min_length=1,
        description="Ligand group name is required (e.g. 'LIG' or 'MOL')"
    )

    # Optional
    indexFileName: Optional[str] = None

    # Output files
    outputNumFileName: str = "hbnum"
    outputDistFileName: str = "hbdist"
    outputAngFileName: str = "hbang"
    outputDanFileName: str = "hbdan"

    # Parameters
    cutoff: Optional[float] = Field(
        default=None,
        ge=0.35,
        description="Cutoff must be >= 0.35 nm (GROMACS hard limit)"
    )

    beginTime: Optional[int] = Field(
        default=None,
        ge=0,
        description="Begin time must be >= 0 ps"
    )

    endTime: Optional[int] = Field(
        default=None,
        ge=0,
        description="End time must be >= 0 ps"
    )

    timeStep: Optional[int] = Field(
        default=None,
        ge=1,
        description="Time step must be at least 1 ps"
    )

    generatePlot: bool = True