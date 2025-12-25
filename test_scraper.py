# test_scraper.py
"""
Test scraper with a simple webpage to verify it's working.
"""

from scraper.clean import clean_html
from scraper.chunk import chunk_text_by_tokens
from embeddings.build_vectors import upsert_documents
import requests

def test_with_simple_page():
    """Test scraper with a simple HTML page."""
    
    # Test HTML content
    test_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body>
        <nav>Skip this navigation</nav>
        <main>
            <h1>Welcome to Our Company</h1>
            <p>We provide excellent web development services to businesses of all sizes. 
            Our team specializes in creating modern, responsive websites that engage users 
            and drive results. We have over 10 years of experience in the industry.</p>
            
            <h2>Our Services</h2>
            <p>We offer a comprehensive range of digital services including web design, 
            mobile app development, SEO optimization, and digital marketing. Each project 
            is tailored to meet the specific needs of our clients and deliver measurable results.</p>
            
            <h2>Contact Us</h2>
            <p>Our office hours are Monday to Friday, 9 AM to 6 PM. You can reach us by 
            phone at 555-1234 or email at contact@example.com. We respond to inquiries 
            within 24 hours and offer free initial consultations.</p>
        </main>
        <footer>Footer content</footer>
    </body>
    </html>
    """
    
    print("=" * 60)
    print("Testing Scraper with Sample HTML")
    print("=" * 60)
    
    # Clean HTML
    print("\n1. Cleaning HTML...")
    cleaned = clean_html(test_html)
    print(f"Cleaned text length: {len(cleaned)} characters")
    print(f"Preview:\n{cleaned[:200]}...")
    
    # Chunk
    print("\n2. Chunking text...")
    chunks = chunk_text_by_tokens(cleaned, max_tokens=450)
    print(f"Created {len(chunks)} chunks")
    
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1} ({len(chunk)} chars):")
        print(chunk[:150] + "..." if len(chunk) > 150 else chunk)
    
    # Create documents
    print("\n3. Creating document objects...")
    docs = []
    for i, chunk in enumerate(chunks):
        docs.append({
            "id": f"test#chunk{i}",
            "url": "http://test.example.com",
            "text": chunk
        })
    
    print(f"Created {len(docs)} document objects")
    
    # Upsert to FAISS
    print("\n4. Storing in FAISS...")
    upsert_documents(docs)
    
    print("\n" + "=" * 60)
    print("✅ Test completed successfully!")
    print("=" * 60)
    print("\nNow try querying: python test_query.py")

if __name__ == "__main__":
    test_with_simple_page()
