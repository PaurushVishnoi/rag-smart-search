import os
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
ROOT_PAGE_ID = os.getenv("ROOT_PAGE_ID")

# Initialize Notion client
notion = Client(auth=NOTION_TOKEN)

# ---------------------------------------------------
# 1️⃣  Function: Get all child pages from parent page
# ---------------------------------------------------
def get_all_child_pages(parent_page_id: str):
    """
    Fetch all child pages under a Notion parent page.
    Returns a list of tuples: [(title, page_id), ...]
    """
    results = notion.blocks.children.list(block_id=parent_page_id)["results"]
    pages = []

    for block in results:
        if block["type"] == "child_page":
            title = block["child_page"]["title"]
            page_id = block["id"]
            pages.append((title, page_id))
    
    return pages

def get_page_text(page_id):
    results = notion.blocks.children.list(block_id=page_id)["results"]
    lines = []
    for block in results:
        if "rich_text" in block[block["type"]]:
            for t in block[block["type"]]["rich_text"]:
                lines.append(t["plain_text"])
    
    return "\n".join(lines)



