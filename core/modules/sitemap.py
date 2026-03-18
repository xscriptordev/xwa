import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
from typing import List, Dict, Any
from core.utils.logger import logger

def fetch_sitemap_urls(base_url: str) -> List[str]:
    """Finds and parses the sitemap.xml to extract all URLs."""
    parsed = urlparse(base_url)
    sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"
    
    logger.info(f"Attempting to fetch sitemap from: {sitemap_url}")
    try:
        resp = requests.get(sitemap_url, timeout=10)
        if resp.status_code == 200:
            # Parse XML. We installed lxml so bs4 can use it.
            soup = BeautifulSoup(resp.content, "xml")
            
            # Standard sitemaps use <loc> tags for URLs
            urls = [loc.text.strip() for loc in soup.find_all("loc") if loc.text]
            logger.info(f"Successfully extracted {len(urls)} URLs from sitemap.")
            return urls
        else:
            logger.warning(f"No sitemap found at {sitemap_url} (HTTP {resp.status_code}).")
    except Exception as e:
        logger.error(f"Error fetching sitemap: {e}")
        
    return []

async def check_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Dict[str, Any]:
    """Checks the status of a single URL asynchronously."""
    async with semaphore:
        try:
            # We use GET with stream=True or HEAD to save bandwidth. HEAD is faster.
            async with session.head(url, allow_redirects=True, timeout=10) as response:
                return {
                    "url": url, 
                    "status": response.status, 
                    "ok": response.status < 400
                }
        except Exception as e:
            return {
                "url": url, 
                "status": 0, 
                "ok": False, 
                "error": str(e)
            }

async def crawl_urls_concurrently(urls: List[str], max_concurrent: int = 10) -> List[Dict[str, Any]]:
    """Crawls a list of URLs concurrently using aiohttp and a semaphore."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    # We use a custom connector to limit per-host connections if needed
    connector = aiohttp.TCPConnector(limit_per_host=max_concurrent)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check_url(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks)
        
    return list(results)

def build_url_tree(urls: List[str]) -> Dict[str, Any]:
    """Transforms a flat list of URLs into a hierarchical tree structure."""
    tree = {"_paths": []}
    
    for url in urls:
        parsed = urlparse(url)
        path = parsed.path.strip("/")
        
        if not path:
            tree["_paths"].append(url)
            continue
            
        parts = path.split("/")
        current_node = tree
        
        for part in parts:
            if part not in current_node:
                current_node[part] = {"_paths": []}
            current_node = current_node[part]
            
        current_node["_paths"].append(url)
        
    return tree

def run_sitemap_analysis(base_url: str) -> Dict[str, Any]:
    """Main entry point for sitemap and crawler analysis."""
    urls = fetch_sitemap_urls(base_url)
    
    if not urls:
        return {"urls_found": 0, "tree": {}, "broken_links": [], "scanned_count": 0}
        
    tree = build_url_tree(urls)
    
    # Limit max scans to defaults (e.g., 50) for fast CLI testing
    test_urls = urls[:50]
    logger.info(f"Validating {len(test_urls)} URLs concurrently (rate limit: 5 concurrent)...")
    
    crawl_results = asyncio.run(crawl_urls_concurrently(test_urls, max_concurrent=5))
    
    broken_links = [res for res in crawl_results if not res["ok"]]
    if broken_links:
        logger.warning(f"Found {len(broken_links)} broken links!")
    else:
        logger.info("No broken links found among scanned URLs.")
    
    return {
        "urls_found": len(urls),
        "tree_root_children": list(tree.keys()),
        "broken_links": broken_links,
        "scanned_count": len(test_urls)
    }
