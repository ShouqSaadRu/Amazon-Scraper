import requests
from bs4 import BeautifulSoup
import time


base_url = "https://www.amazon.com/s?k=dress&i=fashion&rh=n%3A7141123011%2Cp_n_feature_thirty-two_browse-bin%3A121075131011&dc&crid=3FCZGFMNFAG9K&qid=1737742124&rnid=121075130011&sprefix=dress%2Caps%2C244&xpid=mJxXUyT_v99GO&ref=sr_pg_PAGE_NUMBER"

# File to store product links
output_file = "amazon_links.txt"

# Loop through all 400 pages
for page in range(1, 401):  
    print(f"Scraping page {page}...")
    
    
    url = base_url.replace("PAGE_NUMBER", str(page))
    
    # Make the HTTP request
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    
    if response.status_code != 200:
        print(f"Failed to fetch page {page}: Status Code {response.status_code}")
        continue
    
    
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Find all product links
    product_links = soup.find_all("a", class_="a-link-normal s-no-outline")
    
    # Append links to the file
    with open(output_file, "a") as file:
        for link in product_links:
            product_url = "https://www.amazon.com" + link.get("href")
            file.write(product_url + "\n")
    
    # Pause to avoid detection
    time.sleep(2)

print(f"Scraping completed. Product links saved in '{output_file}'.")
