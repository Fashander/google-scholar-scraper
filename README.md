# Google Scholar Scraper

This Python script allows you to scrape search results from Google Scholar using Selenium and BeautifulSoup. It handles pagination, retrieves article titles, authors, and snippets, and stores the results in a CSV file.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/google-scholar-scraper.git
   cd google-scholar-scraper
   ```

2. **Install Python Packages**

   Install the required Python packages using `pip`:

   ```bash
   pip install beautifulsoup4 pandas selenium
   ```

3. **Download ChromeDriver**

   Download the ChromeDriver that matches your installed version of Google Chrome. You can download it from [here](https://sites.google.com/chromium.org/driver/). After downloading, make sure to place it in a directory included in your system’s PATH, or specify the path in the script.

## Usage

1. **Running the Script**

   You can run the script from the command line. The basic usage is:

   ```bash
   python gscholar_scraper.py '<search_query>' [<num_pages>]
   ```

   - `<search_query>`: The search term you want to scrape.
   - `[<num_pages>]` (optional): The number of pages to scrape. If not provided, the script defaults to scraping just the first page.

2. **Example**

   To scrape 3 pages of results for the search term "machine learning", run:

   ```bash
   python gscholar_scraper.py "machine learning" 3
   ```

3. **Output**

   The script will save the scraped data in a file called `results.csv` in the same directory. The CSV file will contain the following columns:
   - `title`: The title of the article.
   - `authors`: The authors of the article.
   - `snippet`: A brief snippet or abstract from the article.
