# Simple Web Scraper

Ultra-minimal web scraper using Playwright. No complex structure, just simple scripts.

## Installation

```bash
pip install -r requirements.txt
playwright install chromium
```

## Usage

1. **Import your scraper in `main.py`**:
```python
from scrapers.example_scraper import ExampleScraper
```

2. **Run it**:
```bash
python main.py
```

3. **Data outputs as JSON** to console

## Creating a Scraper

Copy `scrapers/template_scraper.py` and implement 3 things:

```python
from playwright.sync_api import Page
from scrapers.base_scraper import BaseScraper

class MyScraper(BaseScraper):
    @property
    def url(self) -> str:
        return "https://example.com"
    
    @property
    def name(self) -> str:
        return "MyScraper"
    
    def parse_page(self, page: Page) -> None:
        # Extract data
        title = page.title()
        
        # Store in self.data
        self.data.append({"title": title})
```

## Structure

```
web scraper/
├── main.py              # Run this
├── scrapers/
│   ├── base_scraper.py  # Base class
│   ├── example_scraper.py
│   ├── twitter_scraper.py
│   └── template_scraper.py
└── requirements.txt
```

## Using BeautifulSoup

You can also use BeautifulSoup for parsing:

```python
def parse_page(self, page: Page) -> None:
    from bs4 import BeautifulSoup
    
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.title.string
    links = [a.get('href') for a in soup.find_all('a')]
    
    self.data.append({"title": title, "links": links})
```

## That's It!

No config files, no core modules, just simple Python scripts.
