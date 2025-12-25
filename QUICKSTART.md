# Quick Start Commands

## 1. Setup Environment
```bash
python setup_env.py
# Then edit .env with your actual credentials
```

## 2. Install Dependencies
```bash
pip install -r requirements.txt
```

## 3. Build Vector Database
```bash
python -c "from scraper.scrape import crawl_and_build; crawl_and_build()"
```

## 4. Start Server
```bash
python main.py
```

## 5. Test (in new terminal)
```bash
python test_webhook.py
```

---

## Minimum Required .env Variables for Testing

```env
OPENAI_API_KEY=sk-your-actual-key
SITEMAP_URL=https://yourwebsite.com/sitemap.xml
WHATSAPP_TOKEN=dummy  # Can be dummy for local testing
WHATSAPP_PHONE_ID=dummy  # Can be dummy for local testing
```

---

## Common Commands

### Re-scrape website
```bash
python -c "from scraper.scrape import crawl_and_build; crawl_and_build()"
```

### Test specific query
```bash
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"entry":[{"changes":[{"value":{"messages":[{"from":"test","text":{"body":"YOUR QUESTION HERE"}}]}}]}]}'
```

### Check server health
```bash
curl http://localhost:8000/
```
