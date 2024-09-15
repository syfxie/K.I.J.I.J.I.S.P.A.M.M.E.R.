import time

import pandas as pd

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class WebAgent:
    def __init__(self, chrome_path: str = "/usr/local/bin/chromedriver"):
        # Launch Chrome with specified settings
        service = Service(executable_path=chrome_path)
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)

        # Wait 2 seconds between instructions
        self.driver.implicitly_wait(2)

    def search_kijiji(self, target_item: str = "rtx-4090") -> str:
        """Given a target item, search for it on Kijiji and print the current URL.

        Args:
            target_item (str, optional): Item to search for. Defaults to "rtx-4090".

        Returns:
            str: URL after searching for the target item
        """
        self.driver.get("http://kijiji.ca")

        search_bar = self.driver.find_element(By.ID, "global-header-search-bar-input")

        # Enter the search term
        search_bar.send_keys(target_item)
        search_bar.send_keys(Keys.RETURN)

        time.sleep(5)

        search_url = self.driver.current_url
        print(f"Search completed. Current URL: {search_url}")
        return search_url

    def navigate(self, url: str):
        """Navigate to the specified URL.

        Args:
            url (str): URL to navigate to
        """
        self.driver.get(url)

    def set_name(self, name: str):
        self.name = name
    
    def set_username(self, username: str):
        self.username = username

    def set_password(self, password: str):  
        self.password = password

    def login_kijiji(self):
        self.driver.get("http://kijiji.ca")

        # Click on the Sign In button
        sign_in_page = self.driver.find_element(
            By.CSS_SELECTOR, 'button[data-testid="header-sign-in"]'
        )
        sign_in_page.click()
        email_address_box = self.driver.find_element(By.ID, "username")
        password_box = self.driver.find_element(By.ID, "password")
        sign_in_button = self.driver.find_element(
            By.CSS_SELECTOR, "button#login-submit"
        )
        email_address_box.send_keys(self.username)
        password_box.send_keys(self.password)
        sign_in_button.click()

    def _click_messages(self) -> None:
        # Locate the SVG element using its data-testid attribute
        svg_element = self.driver.find_element(
            By.CSS_SELECTOR, 'svg[data-testid="messages-icon"]'
        )

        # Click the SVG element
        svg_element.click()

    def _parse_convo(self) -> pd.DataFrame:
        # Locate the message list container
        message_list_container = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="MessageList"]')

        # Find all the message containers within the message list
        message_elements = message_list_container.find_elements(By.CSS_SELECTOR, '[class^="messageContainer"]')

        # Initialize an empty list to store messages
        messages = []

        # Iterate over each message element and extract details
        for message_element in message_elements:
            # Extract the direction (INBOUND or OUTBOUND)
            direction = message_element.get_attribute("data-qa-message-direction")
            
            # Extract the message text (adjust this based on your actual HTML structure)
            message_text = message_element.text  # This assumes the text is directly within the message element
            
            # Add the message to the list with its direction
            messages.append({"direction": direction, "text": message_text})

        # Print the messages to verify
        for msg in messages:
            print(f"{msg['direction']}: {msg['text']}")

        return pd.DataFrame(messages)
    
    def goto_first_convo(self):
        self.navigate("https://www.kijiji.ca/m-msg-my-messages/")
        conversations = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid^="Conversation_"]')
        conversations[0].click()

    def parse_messages(self) -> pd.DataFrame:
        self._click_messages()
        conversations = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid^="Conversation_"]')
        total_convos = len(conversations)
        pprint(conversations)

        first_time = True
        df = None

        # Iterate over each conversation element and click on it
        for i in range(total_convos):
            # have to regen convo links each iteration since session id changes
            conversations = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid^="Conversation_"]')
            conversations[i].click()

            """
            perform convo parsing logic here
            """
            df = self._parse_convo() if first_time else pd.concat([df, self._parse_convo()], ignore_index=True)
            first_time = False

            time.sleep(5)
            self.driver.back()
            time.sleep(5)

        return df

    def close(self):
        # Wait for 5 seconds before closing the browser
        time.sleep(5)
        self.driver.quit()
