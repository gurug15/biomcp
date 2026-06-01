# bio_mcp/tools/gromacs.py
import os
from fastapi import Depends, HTTPException
import httpx
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_headers
from typing import Annotated

from bio_mcp.models.gromacs import RMSDGromacsInput

from fastmcp import FastMCP, Context

JAVA_API = os.getenv("JAVA_API_BASE", "http://localhost:8080")

        
async def analyze_rmsd(
        inputs: list[RMSDGromacsInput],
        ctx: Context
    ) -> list:
        """Run GROMACS RMSD analysis."""
        # get cookie from request
        request = ctx.request_context.request
        cookie = request.headers.get("cookie")
        
        print("COOKIE:", cookie)
        
        if not cookie:
            raise HTTPException(status_code=401, detail="No JWT cookie found")

        payload = [i.model_dump(exclude_none=True) for i in inputs]

        async with httpx.AsyncClient() as c:
            r = await c.post(
                f"{JAVA_API}/analysis/rmsdGromacs",
                headers={"Cookie": cookie},
                json=payload,
            )
            if r.status_code == 401:
                raise HTTPException(status_code=401, detail="Session expired")
            r.raise_for_status()
            return r.json()
    