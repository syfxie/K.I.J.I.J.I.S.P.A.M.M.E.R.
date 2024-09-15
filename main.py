# from WebAgent import *
# from Scraper import *
import pandas as pd
import time
from orchestrator import Orchestrator
from gui import GUI

if __name__ == "__main__":
    print("start gui")
    gui = GUI()
    print("end gui")
    
    print('main looping')
    gui.root.mainloop()
    print('done main loop')
    
    # gui.root.wait_variable(gui.can_retrieve_input)
    # print('done waiting')

    # Run computations using the selected value
    selected_value = gui.can_retrieve_input.get()

    print("input received from gui")
    input_data = gui.retrieve_input()
    print("input data received: ", input_data)
    
    orchestrator = Orchestrator(count=2)
    time.sleep(10)
    orchestrator.close()


    # web_agent = WebAgent()
    # scraper = KijijiScraper()

    # search_url = web_agent.search_kijiji("rtx-4090")
    
    # df = scraper.scrape_search_result(search_url)

    # web_agent.close()
    # df.to_excel("data.xlsx", engine="xlsxwriter", index=False)

    # web_agent = WebAgent()
    # # search_url = web_agent.search_kijiji("rtx-4090")

    # # scraper = KijijiScraper()
    # #
    # # df = scraper.scrape(search_url)
    # # print(df)
    # df = pd.DataFrame()

    # web_agent.login_kijiji(
    #     username="",
    #     password="",
    # )

    # messages = web_agent.parse_messages()

    # # Pause the script and keep the browser open
    # input("Press Enter to close the browser...")

    # # Close the browser after the user presses Enter
    # web_agent.close()

    # messages.to_excel("data.xlsx", engine="xlsxwriter", index=False)
