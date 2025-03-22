from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
import logging

load_dotenv()

mcp = FastMCP("notion")

NOTION_BASE_URL  = os.getenv("NOTION_BASE_URL")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
NOTION_API = os.getenv("NOTION_API")
DATABSE_ID = os.getenv("DATABSE_ID")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async def create_request(url: str, method: str = "GET", data: dict = None) -> dict[str, Any] | None:
    """Make a request to the Notion API with proper error handling"""
    headers = {
        "Authorization": f"Bearer {NOTION_API}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=f"{NOTION_BASE_URL}{url}",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"HTTP error occurred: {e}")
            print(f"Request URL: {NOTION_BASE_URL}{url}")
            print(f"Request Data: {data}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

async def get_page(page_id: str) -> dict[str, Any] | None:
    """Retrieve a Notion page by ID"""
    return await create_request(f"/v1/pages/{page_id}")

async def create_page(database_id: str, properties: dict) -> dict[str, Any] | None:
    """Create a new page in a database."""
    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    logger.debug(f"Creating page in database {database_id} with properties: {properties}")
    response = await create_request("/v1/pages", method="POST", data=data)
    if response:
        logger.info(f"Page created successfully: {response}")
        return response
    else:
        logger.error("Failed to create page.")
        return None


async def update_page(page_id: str, properties: dict) -> dict[str, Any] | None:
    """Update page properties"""
    return await create_request(f"/v1/pages/{page_id}", method="PATCH", data={"properties": properties})

async def archive_page(page_id: str) -> dict[str, Any] | None:
    """Archive (delete) a page"""
    return await create_request(f"/v1/pages/{page_id}", method="PATCH", data={"archived": True})

async def get_block(block_id: str) -> dict[str, Any] | None:
    """Retrieve a block by ID"""
    return await create_request(f"/v1/blocks/{block_id}")

async def get_block_children(block_id: str) -> dict[str, Any] | None:
    """Get children blocks of a block"""
    return await create_request(f"/v1/blocks/{block_id}/children")

async def append_block_children(block_id: str, children: list) -> dict[str, Any] | None:
    """Append new child blocks to a block"""
    data = {"children": children}
    return await create_request(f"/v1/blocks/{block_id}/children", method="PATCH", data=data)

async def update_block(block_id: str, block_data: dict) -> dict[str, Any] | None:
    """Update a block's content"""
    return await create_request(f"/v1/blocks/{block_id}", method="PATCH", data=block_data)

async def delete_block(block_id: str) -> dict[str, Any] | None:
    """Delete a block"""
    return await create_request(f"/v1/blocks/{block_id}", method="DELETE")

async def query_database(database_id: str, filter_params: dict = None) -> dict[str, Any] | None:
    """Query a database with optional filters"""
    data = {"filter": filter_params} if filter_params else {}
    return await create_request(f"/v1/databases/{database_id}/query", method="POST", data=data)

async def get_database(database_id: str) -> dict[str, Any] | None:
    """Retrieve a database by ID"""
    return await create_request(f"/v1/databases/{database_id}")

async def main():
    database_id = os.getenv("DATABASE_ID")  
    if not database_id:
        logger.error("DATABASE_ID environment variable not set.")
        return

    new_page = await create_page(database_id, {
        "Name": {"title": [{"text": {"content": "MCP Test Page"}}]},
        "Description": {"rich_text": [{"text": {"content": "Description here"}}]}
    })

    
    if new_page:
        print("Page created successfully:", new_page)
    else:
        print("Failed to create page")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())