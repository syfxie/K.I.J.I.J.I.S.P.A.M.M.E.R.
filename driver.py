import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

class WebAgent:
    def __init__(self):
        # Launch Chrome with specified settings
        service = Service(executable_path="/usr/local/bin/chromedriver")
        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=service, options=options)
        
        # Wait 2 seconds between instructions
        self.driver.implicitly_wait(2)
    
    def search_kijiji(self, target_item="rtx-4090"):
        self.driver.get("http://kijiji.ca")

        search_bar = self.driver.find_element(By.ID, 'global-header-search-bar-input')

        # Enter the search term 
        search_bar.send_keys(target_item)
        search_bar.send_keys(Keys.RETURN)
        
        time.sleep(5)

        search_url = self.driver.current_url
        print(f"Search completed. Current URL: {search_url}")

    def login_kijiji(self, username, password):
        self.driver.get("http://kijiji.ca")

        # Click on the Sign In button
        sign_in_page = self.driver.find_element(By.CSS_SELECTOR, 'button[data-testid="header-sign-in"]')
        sign_in_page.click()
        email_address_box = self.driver.find_element(By.ID, 'username')
        password_box = self.driver.find_element(By.ID, 'password')
        sign_in_button = self.driver.find_element(By.CSS_SELECTOR, 'button#login-submit')
        email_address_box.send_keys(username)
        password_box.send_keys(password)
        sign_in_button.click()


    def close(self):
        # Wait for 5 seconds before closing the browser
        time.sleep(10)
        self.driver.quit()

web_agent = WebAgent()
# web_agent.search_kijiji("rtx-4090")
web_agent.login_kijiji("rosajeon82@gmail.com", "@PriceWhisper24")
web_agent.close()
