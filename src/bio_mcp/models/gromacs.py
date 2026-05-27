from typing import Optional

from pydantic import BaseModel, Field


class RMSDGromacsInput(BaseModel):
    topologyFileName: str  = Field(...,min_length=1, description="topology filename can't be blank")
    trajectoryFileName: str  = Field(...,min_length=1, description="topology filename can't be blank")
    indexFileName:Optional[str]
    outputfileName:Optional[str]
    grouplsfit:Optional[int]
    groupRMSD:Optional[int]
    firstFrameno: int = Field(default=0, ge=0)
    lastFrameNo: Optional[int] = None
    
    fitMethod: Optional[str] = None
    dt: Optional[float] = None
    skip: Optional[int] = None
    
    massWeighted: bool = False
    noPbc: bool = False