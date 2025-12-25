# scraper/clean.py
from bs4 import BeautifulSoup
import re

def clean_html(html: str) -> str:
    """
    Clean HTML by removing navigation, scripts, styles, and other noise.
    Returns cleaned text with proper spacing.
    """
    soup = BeautifulSoup(html, "html.parser")

    # remove nav, footer, script, style, ads, forms
    for sel in ["nav", "footer", "script", "style", "noscript", "form", "header", "iframe", "svg", "ads", "aside"]:
        for tag in soup.select(sel):
            tag.decompose()

    # remove common noise classes/ids (customize for your site)
    for noise in soup.select("[class*='cookie'], [id*='cookie'], [class*='subscribe'], [class*='banner']"):
        noise.decompose()

    text = soup.get_text(separator="\n")
    # Collapse whitespace and short lines
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if len(ln) > 30]  # drop very short lines
    cleaned = "\n\n".join(lines)
    return cleaned
