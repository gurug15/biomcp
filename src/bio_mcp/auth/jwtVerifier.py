from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier

auth = JWTVerifier(
    jwks_uri="https://your-auth-system.com/.well-known/jwks.json",
    issuer="https://your-auth-system.com", 
    audience="your-mcp-server"
)
