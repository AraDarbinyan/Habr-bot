import re
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup

from parser.schemas import Article


HABR_BASE_URL = "https://habr.com"


async def fetch_url(
    url: str,
    session: aiohttp.ClientSession,
) -> str:
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.text()


async def get_latest_article(
    url: str,
    session: aiohttp.ClientSession,
) -> Article:
    html = await fetch_url(url, session)

    soup = BeautifulSoup(html, "lxml")

    article = soup.find(
        "article",
        class_="tm-articles-list__item",
    )

    if article is None:
        raise ValueError(
            f"Article was not found on page: {url}"
        )

    link = article.find(
        "a",
        class_="tm-title__link",
    )

    if link is None:
        raise ValueError(
            f"Article link was not found on page: {url}"
        )

    article_link = link.get("href")

    if not article_link:
        raise ValueError(
            f"Article URL was not found on page: {url}"
        )

    match = re.search(
        r"/articles/(\d+)/?",
        article_link,
    )

    if match is None:
        raise ValueError(
            f"Could not extract article ID from: {article_link}"
        )

    article_id = match.group(1)
    title = link.get_text(strip=True)
    full_url = urljoin(
        HABR_BASE_URL,
        article_link,
    )

    return Article(
        id=article_id,
        title=title,
        url=full_url,
    )
