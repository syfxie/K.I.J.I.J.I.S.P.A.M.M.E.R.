import os

import pandas as pd
from dotenv import load_dotenv
from WebAgent import WebAgent
from Scraper import KijijiScraper
from gui import GUI

load_dotenv()

web_agent = WebAgent()
# search_url = web_agent.search_kijiji("rtx-4090")

# scraper = KijijiScraper()
#
# df = scraper.scrape(search_url)
# print(df)
df = pd.DataFrame()

web_agent.login_kijiji(
    username=os.environ.get("KIJIJI_USERNAME"),
    password=os.environ.get("KIJIJI_PASSWORD"),
)

messages = web_agent.parse_messages()

# Pause the script and keep the browser open
input("Press Enter to close the browser...")

# Close the browser after the user presses Enter
web_agent.close()

df.to_csv("data.csv", encoding="utf-8", index=False)

gui = GUI()
gui.run()