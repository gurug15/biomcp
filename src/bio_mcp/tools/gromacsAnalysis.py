import asyncio
import os

import httpx
from fastapi import HTTPException
from fastmcp import Context

from bio_mcp.models.gromacs import (
    GyrateGromacsUserInput,
    HBondGromacsUserInput,
    RMSDGromacsInput,
    RmsfGromacsUserInput,
    SasaGromacsUserInput,
)

JAVA_API = os.getenv("JAVA_API_BASE", "http://localhost:8080")


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

async def _fetch_file_list(cookie: str, endpoint: str) -> list[str]:
    """Fetch available filenames from a Java list endpoint. Returns [] on any error."""
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.get(
                f"{JAVA_API}{endpoint}",
                headers={"Cookie": cookie},
            )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass
    return []


async def _check_filename(
    cookie: str,
    filename: str | None,
    list_endpoint: str,
    label: str,
) -> str | None:
    """Return an error string when filename is provided but absent from the server.
    Returns None when the file exists or filename is empty/None.
    """
    if not filename:
        return None
    available = await _fetch_file_list(cookie, list_endpoint)
    if filename not in available:
        avail_str = ", ".join(available) if available else "none found"
        return f"{label} '{filename}' not found. Available files: [{avail_str}]"
    return None



async def _call_analysis_api(
          endpoint:str,
          inputs:list,
          ctx:Context
)->list:
    """Generic  helper for calling java analysis endpoints"""


    try:
        # print("token::::::-",ctx.request_context.meta.jwt)
        request = ctx.request_context.request.headers.get("cookie")
        cookie = request
        
        if not cookie:
            raise HTTPException(status_code=401, detail="No JWT cookie found")
        
        payload = [
            item.model_dump(exclude_none=True)
            for item in inputs
        ]

        async with httpx.AsyncClient(timeout=300) as client:
            response  = await client.post(
                  f"{JAVA_API}{endpoint}",
                  headers={"Cookie":cookie},
                  json=payload
             )
        if response.status_code == 401:
             raise HTTPException(
                  status_code=401,
                  detail="session Expired"
             )
        if response.status_code == 403:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )
        if response.status_code == 500:
            body = response.text[:400] if response.text else "no details"
            raise HTTPException(
                status_code=500,
                detail=(
                    f"Analysis failed on the server. "
                    f"Please verify the filenames are correct and the files exist. "
                    f"Server response: {body}"
                ),
            )

        response.raise_for_status()

        return response.json()


    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Analysis timed out"
        )

    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail="Analysis service unavailable"
        )

    except httpx.HTTPStatusError as ex:
        raise HTTPException(
            status_code=ex.response.status_code,
            detail=(
                ex.response.text
                if ex.response.text
                else "Analysis failed"
            ),
        )

    except HTTPException:
        raise

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(ex)}"
        )
          



async def analyze_rmsd(
    inputs: list[RMSDGromacsInput],
    ctx: Context,
) -> list:
    """Run GROMACS RMSD analysis."""
    if inputs:
        cookie = ctx.request_context.request.headers.get("cookie", "")
        first = inputs[0]
        errors = [
            e for e in await asyncio.gather(
                _check_filename(cookie, first.topologyFileName, "/topology/list", "Topology file"),
                _check_filename(cookie, first.trajectoryFileName, "/trajectory/list", "Trajectory file"),
                _check_filename(cookie, first.indexFileName, "/index/list", "Index file"),
            ) if e
        ]
        if errors:
            raise HTTPException(status_code=422, detail=" | ".join(errors))
    return await _call_analysis_api("/analysis/rmsdGromacs", inputs, ctx)


async def analyze_rmsf(
    inputs: list[RmsfGromacsUserInput],
    ctx: Context,
) -> list:
    """Run GROMACS RMSF analysis."""
    if inputs:
        cookie = ctx.request_context.request.headers.get("cookie", "")
        first = inputs[0]
        errors = [
            e for e in await asyncio.gather(
                _check_filename(cookie, first.topologyFileName, "/topology/list", "Topology file"),
                _check_filename(cookie, first.trajectoryFileName, "/trajectory/list", "Trajectory file"),
                _check_filename(cookie, first.indexFileName, "/index/list", "Index file"),
            ) if e
        ]
        if errors:
            raise HTTPException(status_code=422, detail=" | ".join(errors))
    return await _call_analysis_api("/analysis/rmsfGromacs", inputs, ctx)


async def analyze_gyrate(
    inputs: list[GyrateGromacsUserInput],
    ctx: Context,
) -> list:
    """Run GROMACS radius of gyration analysis."""
    if inputs:
        cookie = ctx.request_context.request.headers.get("cookie", "")
        first = inputs[0]
        errors = [
            e for e in await asyncio.gather(
                _check_filename(cookie, first.topologyFileName, "/topology/list", "Topology file"),
                _check_filename(cookie, first.trajectoryFileName, "/trajectory/list", "Trajectory file"),
                _check_filename(cookie, first.indexFileName, "/index/list", "Index file"),
            ) if e
        ]
        if errors:
            raise HTTPException(status_code=422, detail=" | ".join(errors))
    return await _call_analysis_api("/analysis/gyrateGromacs", inputs, ctx)



async def analyze_hbond(
    inputs: list[HBondGromacsUserInput],
    ctx: Context,
) -> list:
    """Run GROMACS hydrogen bond analysis."""
    if inputs:
        cookie = ctx.request_context.request.headers.get("cookie", "")
        first = inputs[0]
        # hbond uses TPR files for topology, not .pdb/.gro
        errors = [
            e for e in await asyncio.gather(
                _check_filename(cookie, first.topologyFileName, "/tpr/list", "TPR/topology file"),
                _check_filename(cookie, first.trajectoryFileName, "/trajectory/list", "Trajectory file"),
                _check_filename(cookie, first.indexFileName, "/index/list", "Index file"),
            ) if e
        ]
        if errors:
            raise HTTPException(status_code=422, detail=" | ".join(errors))
    return await _call_analysis_api("/analysis/hbondGromacs", inputs, ctx)
      

async def analyze_sasa(inputs: list[SasaGromacsUserInput], ctx: Context) -> list:
    """Run GROMACS SASA (Solvent Accessible Surface Area) analysis."""
    if inputs:
        cookie = ctx.request_context.request.headers.get("cookie", "")
        first = inputs[0]
        errors = [
            e for e in await asyncio.gather(
                _check_filename(cookie, first.topologyFileName, "/topology/list", "Topology file"),
                _check_filename(cookie, first.trajectoryFileName, "/trajectory/list", "Trajectory file"),
                _check_filename(cookie, first.indexFileName, "/index/list", "Index file"),
            ) if e
        ]
        if errors:
            raise HTTPException(status_code=422, detail=" | ".join(errors))
    return await _call_analysis_api("/analysis/sasa", inputs, ctx)