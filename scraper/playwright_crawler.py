# scraper/playwright_crawler.py
"""
Playwright-based web crawler for JavaScript-rendered websites.
Uses headless browser to render pages before extracting content.
"""

from playwright.sync_api import sync_playwright
from urllib.parse import urljoin, urlparse
from config.settings import settings
from scraper.clean import clean_html
from scraper.chunk import chunk_text_by_tokens
from embeddings.build_vectors import upsert_documents
import time

def is_same_domain(url, base_url):
    """Check if URL is from the same domain."""
    return urlparse(url).netloc == urlparse(base_url).netloc

def crawl_with_playwright(start_url, max_pages=20):
    """
    Crawl website using Playwright for JavaScript rendering.
    
    Args:
        start_url: Homepage URL
        max_pages: Maximum number of pages to crawl
    
    Returns:
        List of document chunks
    """
    print(f"Starting Playwright crawl from: {start_url}")
    print(f"Max pages: {max_pages}")
    print("(This will open a headless browser to render JavaScript)\n")
    
    visited = set()
    to_visit = {start_url}
    docs = []
    
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=settings.SCRAPE_USER_AGENT,
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        while to_visit and len(visited) < max_pages:
            url = to_visit.pop()
            
            if url in visited:
                continue
            
            visited.add(url)
            print(f"[{len(visited)}/{max_pages}] Crawling: {url}")
            
            try:
                # Navigate and wait for page to load
                page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait a bit more for dynamic content
                page.wait_for_timeout(1000)
                
                # Get rendered HTML
                html = page.content()
                
                # Clean and chunk
                cleaned = clean_html(html)
                
                if len(cleaned) < 100:
                    print(f"  ⊘ Skipped (too little content: {len(cleaned)} chars)")
                    continue
                
                chunks = chunk_text_by_tokens(cleaned, max_tokens=settings.MAX_CHUNK_TOKENS)
                print(f"  → Extracted {len(chunks)} chunks ({len(cleaned)} chars)")
                
                # Add to documents
                for i, chunk in enumerate(chunks):
                    docs.append({
                        "id": f"{url}#chunk{i}",
                        "url": url,
                        "text": chunk
                    })
                
                # Extract links from rendered page
                links = page.eval_on_selector_all(
                    'a[href]',
                    '(elements) => elements.map(e => e.href)'
                )
                
                # Filter and add new links
                for link in links:
                    absolute_url = urljoin(start_url, link)
                    if (is_same_domain(absolute_url, start_url) and 
                        absolute_url not in visited and
                        not absolute_url.endswith(('.pdf', '.jpg', '.png', '.gif', '.zip')) and
                        '#' not in absolute_url):
                        to_visit.add(absolute_url)
                
                time.sleep(0.5)  # Be polite
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
                continue
        
        browser.close()
    
    print(f"\n✓ Crawled {len(visited)} pages")
    print(f"✓ Extracted {len(docs)} chunks total")
    
    return docs

def crawl_and_build(max_pages=20):
    """
    Main Playwright crawling pipeline:
    1. Crawl website using headless browser
    2. Extract and clean rendered content
    3. Chunk text
    4. Build embeddings and store in FAISS
    
    Args:
        max_pages: Maximum number of pages to crawl
    """
    print("=" * 60)
    print("Playwright Crawl → Clean → Chunk → Embed pipeline")
    print("=" * 60)
    
    docs = crawl_with_playwright(settings.SITEMAP_URL, max_pages=max_pages)
    
    if not docs:
        print("\n❌ No documents extracted!")
        print("   Check if:")
        print("   - URL is accessible")
        print("   - Content cleaning rules are too aggressive")
        print("   - Website blocks automated access")
        return
    
    print(f"\nUpserting {len(docs)} chunks to FAISS...")
    upsert_documents(docs)
    print("\n✅ Done!")

if __name__ == "__main__":
    crawl_and_build(max_pages=20)
