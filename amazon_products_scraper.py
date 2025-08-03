from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import random

with open("amazon_links.txt", "r") as file:
    product_links = file.read().splitlines()

# User-Agent rotation
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

headers = {
    "User-Agent": random.choice(user_agents),
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  #Run in the background
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(r"C:\chromedriver-win64\chromedriver.exe") # put your chromdriver.exe path on your laptop
driver = webdriver.Chrome(service=service, options=chrome_options)

output_file = "amazon_products.json"

successful_scrapes = 0  # Counter for scraped products

# Open the JSON file in write mode
with open(output_file, "w") as json_file:
    json_file.write("[\n")  

    for index, link in enumerate(product_links):
        try:
            print(f"Scraping {index+1}/{len(product_links)}: {link}")
            driver.get(link)
            time.sleep(3)  # Wait for page load
            
            # Click dropdown to load product sizes
            try:
                dropdown_button = driver.find_element(By.CSS_SELECTOR, "span.a-button-text.a-declarative")
                dropdown_button.click()
                time.sleep(2)
            except Exception:
                pass  # If dropdown isn't found, continue scraping
            
            # Get updated HTML after interaction
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract ASIN
            asin = "N/A"
            asin_element = soup.find("span", class_="a-text-bold", string=lambda text: text and "ASIN" in text)
            if asin_element:
                asin = asin_element.find_next("span").get_text(strip=True)

            # Extract title
            title = soup.find("span", id="productTitle")
            title = title.get_text(strip=True) if title else "N/A"

            # Extract price
            price_whole = soup.find("span", class_="a-price-whole")
            price_fraction = soup.find("span", class_="a-price-fraction")
            price_whole = price_whole.get_text(strip=True) if price_whole else "N/A"
            price_fraction = price_fraction.get_text(strip=True) if price_fraction else ""
            price = price_whole + price_fraction if price_whole != "N/A" else "N/A"

            # Extract description
            description = soup.find("div", id="productDescription")
            description = description.get_text(strip=True) if description else "N/A"

            # Extract images
            images = [img["src"] for img in soup.find_all("img", class_="a-dynamic-image")]

            # Extract colors
            colors = [color["alt"] for color in soup.find_all("img", class_="imgSwatch") if color.get("alt")]

            # Extract sizes
            sizes = [li.get_text(strip=True) for li in soup.select("li.a-dropdown-item.dropdownAvailable a.a-dropdown-link")]

            # Extract reviews
            reviews = []
            review_elements = soup.find_all("div", class_="a-section celwidget")[2:]  # Skip first 2 reviews

            for review in review_elements:
                reviewer_name = review.find("span", class_="a-profile-name")
                reviewer_name = reviewer_name.get_text(strip=True) if reviewer_name else "N/A"

                rating = review.find("span", class_="a-icon-alt")
                rating = rating.get_text(strip=True).split(" ")[0] if rating else "N/A"  # Extract numeric rating

                comment = review.find("span", {"data-hook": "review-body"})
                comment = comment.get_text(strip=True) if comment else "N/A"

                review_images = [
                    img.get("data-src") or img.get("src") 
                    for img in review.find_all("img", class_="review-image-tile")
                    if "grey-pixel.gif" not in (img.get("data-src") or img.get("src"))  # Avoid placeholder images
                ]

                created_at = review.find("span", class_="review-date")
                created_at = created_at.get_text(strip=True) if created_at else "N/A"

                reviews.append({
                    "reviewer_name": reviewer_name,
                    "rating": rating,
                    "comment": comment,
                    "images": review_images,
                    "createdAt": created_at,
                })

            # Construct product data
            product_data = {
                "product_number": successful_scrapes + 1,  # Assigning a product number
                "Item_id": asin,
                "category_id": "Dress",
                "title": title,
                "images": images,
                "colors": colors,
                "price": price,
                "description": description,
                "sizes": sizes,
                "reviews": reviews,
            }

            # Append product data to JSON file
            if successful_scrapes > 0:
                json_file.write(",\n")  # Add a comma before adding the next product
            json_file.write(json.dumps(product_data, indent=4))

            successful_scrapes += 1
            print(f"Successfully Scraped ({successful_scrapes}): {title}")

            time.sleep(2)  # Small delay to avoid detection

        except Exception as e:
            print(f"Error scraping {link}: {e}")

    json_file.write("\n]")  # Close JSON array

print(f"Scraping completed! {successful_scrapes} products saved to '{output_file}'.")

driver.quit()  # Close Selenium WebDriver
