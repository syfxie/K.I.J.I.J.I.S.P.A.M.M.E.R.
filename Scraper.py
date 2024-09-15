import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List

load_dotenv()

class KijijiScraper:
    def __init__(self):
        self.api_key = os.environ.get("SCRAPPER_API")
    
    # def scrape_search_result(self, base_url: str) -> pd.DataFrame:
    #     def find_nth(string, substring, n):
    #         if (n == 1):
    #             return string.find(substring)
    #         else:
    #             return string.find(substring, find_nth(string, substring, n - 1) + 1)
        
    #     fifth_slash = find_nth(base_url, "/", 5)

    #     df = None
    #     first_time = True
    #     # Just scrape the first page for now
    #     for page_num in range(1, 1):
    #         search_url = base_url[:fifth_slash] + f"/page-{page_num}" + base_url[fifth_slash:]
    #         page_url = f"https://api.scraperapi.com?api_key={self.api_key}&url={search_url}"
    #         response = requests.get(page_url)

    #         print(f"Scraping Page: {page_url}")

    #         print("HERE")
    #         if response.status_code != 200:
    #             print("EXITING")
    #             print(f"Error: Page {page_num} not found (status code: {response.status_code}). Stopping.")
    #             break
            
    #         listings_df = self.scrape_listings_page(search_url)
    #         for _, row in listings_df.iterrows():
    #             listing_url = row["URL"]
    #             print("WORKING ON URL: ", listing_url)
    #             listing_df = self.scrape_listing(listing_url)
    #             df = listing_df if first_time else pd.concat([df, listing_df], ignore_index=True)
    #             first_time = False
        
    #     return df

    # Collect all URLs from a product search
    def scrape_listings_page(self, base_url: str) -> pd.DataFrame:
        df = pd.DataFrame(columns=["URL"])
        url = f"https://api.scraperapi.com?api_key={self.api_key}&url={base_url}"
        response = requests.get(url)

        # Check for successful request
        if response.status_code != 200:
            print(
                f"Error: Unable to retrieve the page. Status code: {response.status_code}"
            )
            return pd.DataFrame()

        soup = BeautifulSoup(response.content, "html.parser")

        listings = soup.find("ul", {"data-testid": "srp-search-list"}).find_all("li")
        for listing in listings:            
            listing_url = (
                listing.find("a", {"data-testid": "listing-link"})["href"]
                if listing.find("a", {"data-testid": "listing-link"})
                else "URL not found"
            )
            
            if listing_url == "URL not found":
                continue

            listing_url = f"kijiji.ca{listing_url}"

            print(listing_url)
            df = pd.concat([df, pd.DataFrame({"URL": [listing_url]})], ignore_index=True)

        return df

    # Collect title, price, description, url from a product listing url
    def scrape_listing(self, base_url: str) -> pd.DataFrame:
        print(f"Scraping listing: {base_url}")
        url = f"https://api.scraperapi.com?api_key={self.api_key}&url={base_url}"
        response = requests.get(url)

        # Check for successful request
        if response.status_code != 200:
            print(
                f"Error: Unable to retrieve the page. Status code: {response.status_code}"
            )
            return pd.DataFrame()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract data with error handling
        main_url = base_url
        title = (
            soup.find("h1", {"itemprop": "name"}).text
            if soup.find("h1", {"itemprop": "name"})
            else "Title not found"
        )
        price = (
            soup.find("span", {"itemprop": "price"}).text
            if soup.find("span", {"itemprop": "price"})
            else "Price not found"
        )
        description = (
            soup.find("div", {"itemprop": "description"}).get_text(strip=True)
            if soup.find("div", {"itemprop": "description"})
            else "Description not found"
        )

        # Create a simple DataFrame with the extracted data
        data = {
            "URL": [main_url],
            "Title": [title],
            "Price": [price],
            "Description": [description],
        }

        df = pd.DataFrame(data)
        return df
