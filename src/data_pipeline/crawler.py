# # import time
# # import concurrent.futures
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager
# # from bs4 import BeautifulSoup

# # from models.vertexai_content_extractor import content_extractor
# # from utils.logger import get_logger

# # logger = get_logger(__name__)

# # class SentimentNewsCrawler:

# #     def __init__(self):
# #         options = webdriver.ChromeOptions()
# #         options.add_argument("--headless")  # Run in background
# #         options.add_argument("--disable-gpu")
# #         options.add_argument("--window-size=1920x1080")
# #         options.add_argument("start-maximized")
# #         self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# #     def _scroll_and_load(self, url, max_scroll_time=10):
# #         """Scrolls the webpage to load dynamic content using WebDriverWait."""
# #         self.driver.get(url)
        
# #         # Wait for the page to load initially
# #         WebDriverWait(self.driver, 10).until(
# #             EC.presence_of_element_located((By.TAG_NAME, "body"))
# #         )

# #         last_height = self.driver.execute_script("return document.body.scrollHeight")
# #         start_time = time.time()

# #         while time.time() - start_time < max_scroll_time:
# #             # Scroll to the bottom of the page
# #             self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
# #             # Wait for new content to load
# #             try:
# #                 WebDriverWait(self.driver, 2).until(
# #                     lambda driver: self.driver.execute_script("return document.body.scrollHeight") > last_height
# #                 )
# #             except:
# #                 break  # Stop if no new content is loaded

# #             # Update the last height
# #             last_height = self.driver.execute_script("return document.body.scrollHeight")

# #         return self.driver.page_source  # Return fully loaded page HTML

# #     def _scrape_article(self, url):
# #         """Fetch and parse an article page."""
# #         html = self._scroll_and_load(url)
# #         soup = BeautifulSoup(html, "html.parser")

# #         title = soup.find("title").text.strip() if soup.find("title") else "No Title"
# #         paragraphs = soup.find_all("p")
# #         article_text = " ".join(p.text.strip() for p in paragraphs) if paragraphs else "No Content"

# #         return {
# #             "title": title,
# #             "content": article_text,
# #         }

# #     def _close(self):
# #         """Close the browser."""
# #         self.driver.quit()

# #     def __call__(self, url, *args, **kwds):
# #         """Helper function to initialize a crawler and scrape a single URL."""
# #         try:
# #             article = self._scrape_article(url)
# #             title, content = article["title"], article["content"]
# #             relevant_content = content_extractor(title, content)
# #             print('Content: ', relevant_content)
# #             return relevant_content
# #         except Exception as e:
# #             logger.exception(f"Error scraping {url}: {e}")
# #             return None
# #         finally:
# #             self._close()

# # def init_crawler(urls):
# #     """Initialize the SentimentNewsCrawler and scrape multiple URLs concurrently."""
# #     crawler = SentimentNewsCrawler()
# #     # Use ThreadPoolExecutor to crawl multiple articles concurrently
# #     with concurrent.futures.ThreadPoolExecutor() as executor:
# #         # Submit tasks for each URL
# #         future_to_url = {executor.submit(SentimentNewsCrawler(), url): url for url in urls}
        
# #         # Collect results as they complete
# #         scraped_data = []
# #         for future in concurrent.futures.as_completed(future_to_url):
# #             url = future_to_url[future]
# #             try:
# #                 relevant_content = future.result()
# #                 if relevant_content:
# #                     scraped_data.append(relevant_content)
# #             except Exception as e:
# #                 logger.exception(f"Error processing {url}: {e}")

# #     return scraped_data




# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup

# # List of financial article URLs
# urls = [
#     'https://www.benzinga.com/insights/news/25/03/44399717/exploring-the-competitive-space-apple-versus-industry-peers-in-technology-hardware-storage-amp-peri',
#     'https://www.zacks.com/commentary/2432116/90-advancing-days-offer-a-glimmer-of-hope-in-a-corrective-market',
#     'https://www.benzinga.com/markets/25/03/44345565/warren-buffetts-berkshire-hathaway-sold-134-billion-in-stocks-in-2024-timing-it-perfectly-as-recession-fe'
# ]  # Replace with actual URLs

# # Function to fetch a single page
# async def fetch(session, url):
#     headers = {"User-Agent": "Mozilla/5.0"}
#     try:
#         async with session.get(url, headers=headers, timeout=10) as response:
#             return await response.text()
#     except Exception as e:
#         print(f"Error fetching {url}: {e}")
#         return None

# # Function to parse content
# def parse(html):
#     if html:
#         soup = BeautifulSoup(html, "html.parser")
#         title = soup.find("h1").text if soup.find("h1") else "No Title"
#         content = soup.find("p").text if soup.find("p") else "No Content"
#         return {"title": title, "content": content}
#     return None

# # Main function to handle multiple requests
# async def scrape_all(urls):
#     async with aiohttp.ClientSession() as session:
#         tasks = [fetch(session, url) for url in urls]
#         htmls = await asyncio.gather(*tasks)
#         articles = [parse(html) for html in htmls if html]
#         return articles

# # Run the async scraper
# scraped_articles = asyncio.run(scrape_all(urls))
# print(scraped_articles)
