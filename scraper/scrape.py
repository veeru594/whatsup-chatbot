# scraper/scrape.py
import asyncio
from playwright.async_api import async_playwright
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re
import time

from scraper.clean import clean_html
from scraper.chunk import chunk_text_by_tokens
from embeddings.build_vectors import upsert_documents
from config.settings import settings


# ----------------------
# Helper: Extract all internal links
# ----------------------
def extract_internal_links(url, html):
    soup = BeautifulSoup(html, "html.parser")
    base = f"{urlparse(url).scheme}://{urlparse(url).netloc}"

    links = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]

        # absolute
        if href.startswith("http"):
            if urlparse(href).netloc == urlparse(url).netloc:
                links.add(href)

        # relative
        elif href.startswith("/"):
            links.add(urljoin(base, href))

    return links


# ----------------------
# Main scraping logic using Playwright
# ----------------------
async def scrape_all_pages(start_url):
    print("Launching Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        visited = set()
        to_visit = set([start_url])
        documents = []

        while to_visit:
            url = to_visit.pop()
            if url in visited:
                continue
            visited.add(url)

            print(f"Scraping: {url}")
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
                await page.wait_for_timeout(1500)  # allow JS to settle

                html = await page.content()

                # extract internal links to expand crawl
                links = extract_internal_links(start_url, html)
                to_visit.update(links - visited)

                # clean text
                cleaned = clean_html(html)
                chunks = chunk_text_by_tokens(cleaned, max_tokens=settings.MAX_CHUNK_TOKENS)

                for i, chunk in enumerate(chunks):
                    documents.append({
                        "id": f"{url}#chunk{i}",
                        "url": url,
                        "text": chunk
                    })

            except Exception as e:
                print(f"Error scraping {url}: {e}")

        await browser.close()

    return documents


# ----------------------
# Pipeline runner
# ----------------------
def crawl_and_build():
    start_url = settings.SITEMAP_URL  # in this case your homepage
    print("Starting FULL BROWSER SCRAPE on:", start_url)

    documents = asyncio.run(scrape_all_pages(start_url))

    print(f"Total chunks extracted: {len(documents)}")
    if len(documents) == 0:
        print("WARNING: No chunks found. Something is wrong.")
        return

    print("Upserting into ChromaDB (Overwrite Mode)...")
    upsert_documents(documents, overwrite=True)

    print("Done. Vector DB updated successfully.")
