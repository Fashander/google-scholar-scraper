from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys

def init_selenium_driver():
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   chrome_options.add_argument("--no-sandbox")
   chrome_options.add_argument("--disable-dev-shm-usage")

   # Initialize the WebDriver with the path to chromedriver
#    service = Service("/usr/local/bin/chromedriver")
   driver = webdriver.Chrome(options=chrome_options)
   return driver

def fetch_search_results(driver, query, start=0):
   base_url = "https://scholar.google.com/scholar"
   params = f"?q={query}&start={start}"

   # Use Selenium WebDriver to fetch the page
   driver.get(base_url + params)

   # Wait for the page to load
   driver.implicitly_wait(10)  # Wait for up to 10 seconds for the page to load

   # Return the page source (HTML content)
   return driver.page_source

def parse_results(html):
   soup = BeautifulSoup(html, 'html.parser')
   articles = []
   for item in soup.select('.gs_ri'):
       title = item.select_one('.gs_rt').text
       authors = item.select_one('.gs_a').text
       snippet = item.select_one('.gs_rs').text
       articles.append({'title': title, 'authors': authors, 'snippet': snippet})
   return articles

def scrape_multiple_pages(driver, query, num_pages):
    all_articles = []
    for i in range(num_pages):
        start = i * 10  # each page contains 10 results
        html_content = fetch_search_results(driver, query, start=start)
        articles = parse_results(html_content)
        all_articles.extend(articles)
    return all_articles


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python gscholar_scraper.py '<search_query>' [<num_pages>]")
        sys.exit(1)

    search_query = sys.argv[1]
    num_pages = int(sys.argv[2]) if len(sys.argv) == 3 else 1

    # Initialize the Selenium WebDriver
    driver = init_selenium_driver()

    try:
        all_articles = scrape_multiple_pages(driver, search_query, num_pages)
        df = pd.DataFrame(all_articles)
        df.to_csv('results.csv', index=False)
    finally:
       driver.quit()
