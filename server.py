import os
import httpx
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("Beacon CRM Bridge")

BEACON_API_BASE = os.getenv("BEACON_API_BASE", "https://api.beaconcrm.io/v1")
BEACON_API_KEY = os.getenv("BEACON_API_KEY")

@mcp.tool()
async def search_beacon_contacts(query: str) -> str:
    """
    Search for contacts in Beacon CRM by name, email, or keyword.
    
    Args:
        query: The search term or email to look up.
    """
    url = f"{BEACON_API_BASE}/people"
    headers = {
        "Authorization": f"Bearer {BEACON_API_KEY}",
        "Accept": "application/json"
    }
    params = {"term": query}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return str(response.json())
        else:
            return f"Error communicating with Beacon CRM: {response.status_code} - {response.text}"

if __name__ == "__main__":
    mcp.run()
