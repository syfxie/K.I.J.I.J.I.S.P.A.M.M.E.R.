import os
import pandas as pd
import requests
from bs4 import BeautifulSoup


class KijijiScraper:
    def __init__(self):
        self.api_key = os.environ.get("SCRAPPER_API")

    def scrape(self, base_url: str) -> pd.DataFrame:
        df = pd.DataFrame(columns=["price", "description"])
        url = f"https://api.scraperapi.com?api_key={self.api_key}&url={base_url}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("li", {"data-testid": "listing-card-list-item"})
        for listing in listings:
            # Get the price
            price = listing.find("p", {"data-testid": "listing-price"})

            # Get the image alt (description)
            image = listing.find("img", {"data-testid": "listing-card-image"})

            # Print the price and description
            if price and image:
                print(f"Price: {price.text.strip()}, Description: {image['alt']}")
                df = df.append(
                    {"price": price.text.strip(), "description": image["alt"]},
                    ignore_index=True,
                )

        return df
