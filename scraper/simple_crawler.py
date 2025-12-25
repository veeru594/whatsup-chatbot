# scraper/simple_crawler.py
"""
Simple web crawler for sites without sitemaps.
Crawls a website by following internal links starting from homepage.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config.settings import settings
from scraper.clean import clean_html
from scraper.chunk import chunk_text_by_tokens
from embeddings.build_vectors import upsert_documents
import time

HEADERS = {"User-Agent": settings.SCRAPE_USER_AGENT}

def is_same_domain(url, base_url):
    """Check if URL is from the same domain."""
    return urlparse(url).netloc == urlparse(base_url).netloc

def fetch_url(url):
    """Fetch URL content with timeout and headers."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  ✗ Error fetching {url}: {e}")
        return None

def extract_links(html, base_url):
    """Extract all internal links from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        # Convert relative URLs to absolute
        absolute_url = urljoin(base_url, href)
        
        # Only include same-domain links, skip anchors and special URLs
        if (is_same_domain(absolute_url, base_url) and 
            not absolute_url.endswith(('.pdf', '.jpg', '.png', '.gif', '.zip')) and
            '#' not in absolute_url):
            links.add(absolute_url)
    
    return links

def crawl_website(start_url, max_pages=20):
    """
    Crawl website starting from start_url.
    
    Args:
        start_url: Homepage URL
        max_pages: Maximum number of pages to crawl
    
    Returns:
        List of document chunks
    """
    print(f"Starting crawl from: {start_url}")
    print(f"Max pages: {max_pages}")
    
    visited = set()
    to_visit = {start_url}
    docs = []
    
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop()
        
        if url in visited:
            continue
        
        visited.add(url)
        print(f"\n[{len(visited)}/{max_pages}] Crawling: {url}")
        
        # Fetch page
        html = fetch_url(url)
        if not html:
            continue
        
        # Clean and chunk
        cleaned = clean_html(html)
        if len(cleaned) < 100:  # Skip pages with too little content
            print(f"  ⊘ Skipped (too little content)")
            continue
        
        chunks = chunk_text_by_tokens(cleaned, max_tokens=settings.MAX_CHUNK_TOKENS)
        print(f"  → Extracted {len(chunks)} chunks")
        
        # Add to documents
        for i, chunk in enumerate(chunks):
            docs.append({
                "id": f"{url}#chunk{i}",
                "url": url,
                "text": chunk
            })
        
        # Extract links for further crawling
        links = extract_links(html, start_url)
        to_visit.update(links - visited)
        
        time.sleep(0.3)  # Be polite
    
    print(f"\n✓ Crawled {len(visited)} pages")
    print(f"✓ Extracted {len(docs)} chunks total")
    
    return docs

def crawl_and_build(max_pages=20):
    """
    Main crawling pipeline:
    1. Crawl website from homepage
    2. Extract and clean content
    3. Chunk text
    4. Build embeddings and store in FAISS
    
    Args:
        max_pages: Maximum number of pages to crawl
    """
    print("=" * 60)
    print("Starting Web Crawl → Clean → Chunk → Embed pipeline")
    print("=" * 60)
    
    docs = crawl_website(settings.SITEMAP_URL, max_pages=max_pages)
    
    if not docs:
        print("\n❌ No documents extracted!")
        print("   Possible issues:")
        print("   - Website requires JavaScript (try enabling Playwright)")
        print("   - Content is filtered out by cleaning rules")
        print("   - URL is incorrect")
        return
    
    print(f"\nUpserting {len(docs)} chunks to FAISS...")
    upsert_documents(docs)
    print("\n✅ Done!")

if __name__ == "__main__":
    crawl_and_build(max_pages=20)
