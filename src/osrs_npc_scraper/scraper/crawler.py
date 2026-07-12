from urllib.parse import urljoin
from dataclasses import dataclass
import asyncio

from bs4 import BeautifulSoup
import httpx

from osrs_npc_scraper.scraper.fetcher import fetch_page


@dataclass
class NPCInfo:
    """Individual extracted NPC info"""

    title: str
    url: str


def extract_npc_list(soup: BeautifulSoup, base_url: str) -> list[NPCInfo]:
    """Extracts all NPC URLs from a raw HTML page of the NPC Category table."""

    npc_list: list[NPCInfo] = []

    # individual npc list starts at second div of class "mw-category-group"
    category_group_divs = soup.find_all("div", attrs={"class": "mw-category"})
    npc_list_content = (
        category_group_divs[1]
        if len(category_group_divs) > 1
        else category_group_divs[0]
    )

    # all li elements are npc links that contain href + title
    for li in npc_list_content.find_all("li"):
        npc_anchor = li.find("a")
        if npc_anchor is None:
            continue

        npc_href = npc_anchor.get("href")
        npc_title = npc_anchor.get("title")
        if not isinstance(npc_href, str) or not isinstance(npc_title, str):
            continue

        npc_info = NPCInfo(npc_title, urljoin(base_url, npc_href))
        npc_list.append(npc_info)

    return npc_list


def extract_next_page(soup: BeautifulSoup, base_url: str) -> str | None:
    """
    Finds the URL of the next page button from a RAW HTML page of the paginated NPC Category table.
    Either returns URL or none if not found (eg. last page).
    """

    result = soup.find(name="a", string="next page")
    if result and isinstance(result.get("href"), str):
        return urljoin(base_url, str(result["href"]))

    return None


async def crawl_npc_category(
    httpx_client: httpx.AsyncClient,
    start_url: str,
    base_url: str,
    request_delay: int = 3,
) -> list[NPCInfo]:
    """Crawls through NPC category pages to get all NPC URLs and titles"""

    npc_list: list[NPCInfo] = []
    next_url = start_url

    while next_url is not None:
        # prevent hammering requests
        await asyncio.sleep(request_delay)

        response = await fetch_page(client=httpx_client, url=next_url)
        html_content = response.text
        soup = BeautifulSoup(html_content, features="html.parser")

        page_list = extract_npc_list(soup, base_url=base_url)
        npc_list.extend(page_list)
        next_url = extract_next_page(soup, base_url=base_url)

    return npc_list
