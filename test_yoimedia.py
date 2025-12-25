# test_yoimedia.py
"""
Test scraping yoimedia.com specifically.
"""

from scraper.simple_crawler import crawl_and_build

if __name__ == "__main__":
    print("🌐 Testing YoiMedia.com Scraper")
    print("=" * 60)
    print("\nThis will:")
    print("1. Crawl https://www.yoimedia.com/")
    print("2. Follow internal links (max 20 pages)")
    print("3. Clean and chunk content")
    print("4. Store in FAISS vector database")
    print("\n" + "=" * 60)
    
    input("Press ENTER to start...")
    
    crawl_and_build(max_pages=20)
