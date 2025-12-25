# test_playwright_yoimedia.py
"""
Test Playwright scraper on yoimedia.com
"""

from scraper.playwright_crawler import crawl_and_build

if __name__ == "__main__":
    print("🌐 Testing YoiMedia.com with Playwright (JavaScript Rendering)")
    print("=" * 60)
    print("\nThis will:")
    print("1. Launch headless Chromium browser")
    print("2. Render JavaScript on each page")
    print("3. Extract content from fully-loaded pages")
    print("4. Crawl up to 20 pages")
    print("5. Store chunks in FAISS")
    print("\n" + "=" * 60)
    print("\nStarting in 2 seconds...\n")
    
    import time
    time.sleep(2)
    
    crawl_and_build(max_pages=20)
