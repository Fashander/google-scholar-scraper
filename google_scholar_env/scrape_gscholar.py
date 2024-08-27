from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys

def fetch_search_results(query, start=0):
    """
    Fetches the HTML content of Google Scholar search results using Selenium.

    Parameters:
        query (str): The search term to use on Google Scholar.
        start (int): The starting index for the search results (used for pagination).

    Returns:
        str: The HTML content of the search results page.
    """
    base_url = "https://scholar.google.com/scholar"
    params = f"?q={query}&start={start}"

    # Set up headless browser options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize the WebDriver with the path to chromedriver
    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(base_url + params)
    time.sleep(2)  # Wait for the page to load

    html = driver.page_source
    driver.quit()
    return html

def parse_results(html):
    """
    Parses the HTML content and extracts information about the articles.

    Parameters:
        html (str): The HTML content of the search results page.

    Returns:
        list: A list of dictionaries, each containing information about an article.
    """
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    for item in soup.select('.gs_ri'):
        title = item.select_one('.gs_rt').text
        authors = item.select_one('.gs_a').text
        snippet = item.select_one('.gs_rs').text
        articles.append({'title': title, 'authors': authors, 'snippet': snippet})
    return articles

def scrape_google_scholar(query, num_pages=2, delay=10):
    """
    Scrapes multiple pages of Google Scholar search results for a given query using Selenium.

    Parameters:
        query (str): The search term to use on Google Scholar.
        num_pages (int): The number of pages to scrape.
        delay (int): The delay (in seconds) between requests to avoid IP blocking.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped article data.
    """
    all_articles = []
    for start in range(0, num_pages * 10, 10):
        html_content = fetch_search_results(query, start)
        articles = parse_results(html_content)
        all_articles.extend(articles)
        time.sleep(delay)
    df = pd.DataFrame(all_articles)
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python gscholar_scraper.py '<search_query>' [<num_pages>]")
        sys.exit(1)

    search_query = sys.argv[1]
    num_pages = int(sys.argv[2]) if len(sys.argv) == 3 else 5

    results_df = scrape_google_scholar(query=search_query, num_pages=num_pages)
    print(results_df.head())
    results_df.to_csv('scholar_results.csv', index=False)
