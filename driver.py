from WebAgent import WebAgent
from Scraper import KijijiScraper

web_agent = WebAgent()
search_url = web_agent.search_kijiji("rtx-4090")

scraper = KijijiScraper()

df = scraper.scrape(search_url)
print(df)
web_agent.close()

df.to_csv("data.csv", encoding='utf-8', index=False)
