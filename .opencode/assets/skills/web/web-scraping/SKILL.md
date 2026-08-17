---
provenance:
  source: OpenCode Engineering Kit (community)
  source_url: https://github.com/devtiagoabreu/opencode-engineering-kit
  license: MIT
  verified: 2026-08-08
name: web-scraping
description: Extract web data ethically with Python, requests, BeautifulSoup, and Scrapy while respecting robots.txt and rate limits.
category: web
version: 0.1.0
author: devtiagoabreu
tags: [web-scraping, python, beautifulsoup, scrapy, requests, robots.txt, data-extraction]
compatible:
  - opencode
  - claude-code
  - cursor
requires:
  - Python 3.10+ and pip
  - Basic HTML and CSS selector knowledge
  - Understanding of HTTP requests and status codes
provides:
  - Polite scraping setup (robots.txt, rate limiting)
  - requests + BeautifulSoup parsing patterns
  - Scrapy spider templates
  - Anti-blocking and data-cleaning guidance
---

# web-scraping

## Overview

Web scraping programmatically extracts data from websites. Done well it
is a legitimate engineering tool; done badly it overloads servers and
breaches terms of service. This skill teaches the ethical baseline first
— read robots.txt, rate-limit, identify yourself — then the mechanics
with Python `requests`, `BeautifulSoup`, and `Scrapy`.

Rule of thumb: if a public API exists, use it. Scraping is for data the
site exposes publicly but does not offer via API.

## Prerequisites

- Python 3.10+ (`pip install requests beautifulsoup4 scrapy`)
- Familiarity with HTML structure and CSS selectors
- The ability to read a site's Terms of Service and robots.txt
- A storage plan for whatever volume you collect

## Usage Instructions

### 1. Respect robots.txt and Identify Yourself

Check the site's crawl rules before writing a single request. Some
paths are explicitly off-limits:

```python
import requests

url = "https://example.com/robots.txt"
r = requests.get(url, timeout=10)
print(r.text)
# Disallow: /private/   -> never crawl those paths
```

Always send a meaningful `User-Agent` that identifies your project and a
contact, so site owners can reach you:

```python
HEADERS = {
    "User-Agent": "my-research-crawler/1.0 (+https://mysite.example/contact)"
}
```

### 2. requests + BeautifulSoup

Fetch a page and extract structured fields with CSS selectors. Always
handle missing data gracefully — real HTML is messy.

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://quotes.example/author/alice",
                    headers=HEADERS, timeout=15)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

name = soup.select_one("h1.author-name")
bio = soup.select_one("div.author-bio")
print({"name": name.get_text(strip=True) if name else None,
       "bio": bio.get_text(" ", strip=True) if bio else None})
```

### 3. Rate Limiting and Retries

Throttle requests to avoid hammering the server, and retry transient
failures with exponential backoff. Sleep between pages:

```python
import time, random

for page in range(1, 6):
    resp = requests.get(f"{base}/products?page={page}",
                        headers=HEADERS, timeout=15)
    if resp.status_code == 429:
        wait = 2 ** page + random.uniform(0, 1)
        print(f"rate limited, sleeping {wait:.1f}s")
        time.sleep(wait)
        continue
    parse(resp.text)
    time.sleep(random.uniform(1.0, 2.5))
```

### 4. Scrapy Spider

Scrapy handles concurrency, retries, and pipelines for larger jobs.
It honors `ROBOTSTXT_OBEY` out of the box:

```python
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ["https://quotes.example/authors"]

    def parse(self, response):
        for author in response.css("div.author-card"):
            yield {
                "name": author.css("h2::text").get(),
                "bio": author.css("p.bio::text").get(),
            }
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

Configure politeness in `settings.py`:

```python
ROBOTSTXT_OBEY = True
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 2.0
USER_AGENT = "my-research-crawler/1.0"
```

## Best Practices

- Always check robots.txt and ToS first; never bypass logins to access private data.
- Identify yourself with a real User-Agent and contact URL.
- Cache responses locally so re-runs do not refetch unchanged pages.
- Store data in a structured format (JSON/CSV) with a source URL for provenance.
- Remove personal data fields you do not need; minimize what you keep.

## Pitfalls / Common Mistakes

- Scraping without a delay, then getting IP-banned and blocking all scrapers on the site.
- Parsing with brittle string regex instead of a parser like BeautifulSoup.
- Ignoring pagination loops, accidentally requesting an infinite sequence.
- Fetching pages behind bot walls without respecting why they exist.
- Storing scraped content verbatim when it contains copyright or personal data.

## Examples

### Example 1: Extract a table into a DataFrame

```python
import pandas as pd
dfs = pd.read_html(resp.text)
table = dfs[0]
table["price_cents"] = (table["price"].str.replace("$", "")
                        .astype(float) * 100)
print(table.head())
```

### Example 2: Only-new items via etag

```python
etag = get_cached_etag()
r = requests.get(url, headers={**HEADERS, "If-None-Match": etag}, timeout=15)
if r.status_code == 304:
    print("unchanged, use cache")
```

## References

- [robots.txt specification](https://www.rfc-editor.org/rfc/rfc9309)
- [BeautifulSoup documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Scrapy documentation](https://docs.scrapy.org/)
