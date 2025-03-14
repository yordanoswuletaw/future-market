# 

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import concurrent.futures
import time

class FinancialNewsCrawler:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in background
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scroll_and_load(self, url, max_scroll_time=10):
        """Scrolls the webpage to load dynamic content using WebDriverWait."""
        self.driver.get(url)
        
        # Wait for the page to load initially
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        start_time = time.time()

        while time.time() - start_time < max_scroll_time:
            # Scroll to the bottom of the page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            try:
                WebDriverWait(self.driver, 2).until(
                    lambda driver: self.driver.execute_script("return document.body.scrollHeight") > last_height
                )
            except:
                break  # Stop if no new content is loaded

            # Update the last height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

        return self.driver.page_source  # Return fully loaded page HTML

    def scrape_article(self, url):
        """Fetch and parse an article page."""
        html = self.scroll_and_load(url)
        soup = BeautifulSoup(html, "html.parser")

        title = soup.find("title").text.strip() if soup.find("title") else "No Title"
        paragraphs = soup.find_all("p")
        article_text = " ".join(p.text.strip() for p in paragraphs) if paragraphs else "No Content"
        timestamp = soup.find("time")["datetime"] if soup.find("time") else "No Timestamp"

        return {
            "url": url,
            "title": title,
            "content": article_text,
            "timestamp": timestamp
        }

    def close(self):
        """Close the browser."""
        self.driver.quit()

def scrape_with_crawler(url):
    """Helper function to initialize a crawler and scrape a single URL."""
    crawler = FinancialNewsCrawler()
    try:
        article = crawler.scrape_article(url)
        print(f"✅ Scraped: {article['title']}")
        return article
    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")
        return None
    finally:
        crawler.close()

# Example usage
urls = [
    "https://www.fool.com/investing/2025/03/14/generate-passive-income-low-cost-vanguard-etf-buy/",
    "https://www.fool.com/investing/2025/03/11/tale-of-two-ai-stocks-broadcom-soared-marvell-fell/"
    # Add more URLs here...
]

# Use ThreadPoolExecutor to crawl multiple articles concurrently
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Submit tasks for each URL
    future_to_url = {executor.submit(scrape_with_crawler, url): url for url in urls}
    
    # Collect results as they complete
    scraped_data = []
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            article = future.result()
            if article:
                scraped_data.append(article)
        except Exception as e:
            print(f"❌ Error processing {url}: {e}")

# Save scraped data to a JSON file
import json
with open("scraped_articles.json", "w") as f:
    json.dump(scraped_data, f, indent=4)

print(f"Scraped {len(scraped_data)} articles.")