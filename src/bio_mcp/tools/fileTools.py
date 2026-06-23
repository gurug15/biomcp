import os

import httpx
from fastapi import HTTPException
from fastmcp import Context

JAVA_API = os.getenv("JAVA_API_BASE", "http://localhost:8080")


async def _call_file_api(endpoint: str, ctx: Context, method: str = "GET", json=None) -> dict | list | str:
    """Generic helper for calling Java file-related endpoints."""
    cookie = ctx.request_context.request.headers.get("cookie")

    if not cookie:
        raise HTTPException(status_code=401, detail="No JWT cookie found")

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.request(
                method=method,
                url=f"{JAVA_API}{endpoint}",
                headers={"Cookie": cookie},
                json=json,
            )

        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Session expired")
        if response.status_code == 403:
            raise HTTPException(status_code=403, detail="Access denied")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="File not found")
        if response.status_code == 400:
            raise HTTPException(status_code=400, detail="Bad request")

        response.raise_for_status()

        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            return response.json()
        return response.text

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="File service timed out")
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail="File service unavailable")
    except httpx.HTTPStatusError as ex:
        raise HTTPException(
            status_code=ex.response.status_code,
            detail=ex.response.text or "File operation failed",
        )
    except HTTPException:
        raise
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(ex)}")


# ---------------------------------------------------------------------------
# List tools — return filenames the authenticated user owns
# ---------------------------------------------------------------------------

async def list_topology_files(ctx: Context) -> list[str]:
    """List topology files (.pdb, .gro) available for the current user."""
    return await _call_file_api("/topology/list", ctx)


async def list_trajectory_files(ctx: Context) -> list[str]:
    """List trajectory files (.xtc, .trr) available for the current user."""
    return await _call_file_api("/trajectory/list", ctx)


async def list_tpr_files(ctx: Context) -> list[str]:
    """List TPR and GRO files (.tpr, .gro) available for the current user."""
    return await _call_file_api("/tpr/list", ctx)


async def list_top_files(ctx: Context) -> list[str]:
    """List GROMACS topology include files (.top) available for the current user."""
    return await _call_file_api("/top/list", ctx)


async def list_index_files(ctx: Context) -> list[str]:
    """List GROMACS index files (.ndx) available for the current user."""
    return await _call_file_api("/index/list", ctx)


async def list_itp_files(ctx: Context) -> list[str]:
    """List auxiliary topology include files (.itp) available for the current user."""
    return await _call_file_api("/itp/list", ctx)


async def list_amber_top_files(ctx: Context) -> list[str]:
    """List AMBER topology files (.prmtop) available for the current user."""
    return await _call_file_api("/amber/top/list", ctx)


async def list_amber_traj_files(ctx: Context) -> list[str]:
    """List AMBER trajectory files (.nc, .xtc) available for the current user."""
    return await _call_file_api("/amber/traj/list", ctx)


# ---------------------------------------------------------------------------
# Delete tools
# ---------------------------------------------------------------------------

async def delete_file(filename: str, ctx: Context) -> str:
    """Delete a GROMACS file by filename for the current user.

    Args:
        filename: Name of the file to delete (e.g. 'md.xtc').
    """
    return await _call_file_api(f"/file/{filename}", ctx, method="DELETE")


async def delete_amber_file(filename: str, ctx: Context) -> str:
    """Delete an AMBER file by filename for the current user.

    Args:
        filename: Name of the AMBER file to delete (e.g. 'system.prmtop').
    """
    return await _call_file_api(f"/amber/file/{filename}", ctx, method="DELETE")


# ---------------------------------------------------------------------------
# Index file creation
# ---------------------------------------------------------------------------

async def create_index_file(topology_file: str, ctx: Context) -> str:
    """Generate a GROMACS index file (.ndx) from a topology file.

    Calls the Java backend to run 'gmx make_ndx' and returns the resulting
    index file content.

    Args:
        topology_file: Name of the topology file to generate the index from (e.g. 'protein.gro').
    """
    return await _call_file_api(
        "/file/createIndex",
        ctx,
        method="POST",
        json={"topologyFile": topology_file},
    )