# Amazon Scraper

This project is a two-step Amazon product scraper built using Python, `requests`, `BeautifulSoup`, and `Selenium`. It scrapes product links from Amazon search results (like dresses), and then visits each product page to extract detailed information including item ID, title, images, colors, prices, description, sizes, and reviews including(reviewer_name, rating, comment, images, createdAt)



## Features

- Scrapes Amazon result pages
- Extracts full product page details using Selenium
- Retrieves:
  - Title
  - ASIN
  - Price
  - Description
  - Available sizes and colors
  - Images
  - reviews
- Outputs all product data to a JSON file

---

## Technologies Used

| Tool/Library        | Purpose                                       |
|---------------------|-----------------------------------------------|
| `requests`          | Fetch HTML from Amazon search result pages   |
| `BeautifulSoup`     | Parse HTML for product links and data         |
| `Selenium`          | Automate full browser to extract JS-rendered content |
| `ChromeDriver`      | Driver used by Selenium to control Chrome     |
| `json`              | Format and store product data                 |

---

## How It Works

### Step 1: `link_scraper.py`

- Uses `requests` and `BeautifulSoup` to crawl Amazon pages.
- Extracts product links using HTML parsing.
- Saves all product URLs to `amazon_links.txt`.

### Step 2: `amazon_products_scraper.py`

- Loads product URLs from `amazon_links.txt`.
- Uses `Selenium` + `ChromeDriver` to simulate a user browsing each page.
- Extracts product details and reviews.
- Saves everything in structured JSON format in `amazon_products.json`.

---
## Setup

1. Install required packages:

2. Download the appropriate [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/) for your Chrome version and place its path in the script.

3. Run the scripts in order:
- `scrape_links.py` — collects product URLs
- `amazon_products_scraper.py` — extracts product details using Selenium
---
## Why Use Selenium?

Many product details (like dynamic sizes, colors, images, or reviews) are **loaded via JavaScript** after the page appears.  
Since `requests` can’t render JavaScript, we use **Selenium** with **ChromeDriver** to fully load and interact with the page just like a real browser.

---

## Disclaimer
Web scraping can be a gray area and may violate the terms of service of many websites. This project is intended for educational and personal research purposes only. Please use it responsibly and be mindful of the load your requests place on the website's servers.

