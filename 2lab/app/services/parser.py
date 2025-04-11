import aiohttp
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import tempfile
import networkx as nx
import os


async def fetch(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.content_type == "text/html":
                return await response.text()
    except Exception:
        return None


async def parse_links(session, url, base_domain):
    html = await fetch(session, url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        href = tag['href']
        joined_url = urljoin(url, href)
        if base_domain in urlparse(joined_url).netloc:
            links.add(joined_url.split('#')[0])
    return links


async def crawl(start_url: str, max_depth):
    visited = set()
    graph = nx.DiGraph()
    base_domain = urlparse(start_url).netloc

    async with aiohttp.ClientSession() as session:
        queue = [(start_url, 0)]
        while queue:
            current_url, depth = queue.pop(0)
            if depth > max_depth or current_url in visited:
                continue
            visited.add(current_url)
            graph.add_node(current_url)
            links = await parse_links(session, current_url, base_domain)
            for link in links:
                graph.add_edge(current_url, link)
                queue.append((link, depth + 1))
    return graph


async def generate_graphml(start_url: str, max_depth: int) -> str:
    graph = await crawl(start_url, max_depth)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".graphml", mode="w+", encoding='utf-8') as f:
        nx.write_graphml(graph, f.name)
        f.seek(0)
        content = f.read()
    try:
        os.unlink(f.name)
    except OSError:
        pass
    return content
