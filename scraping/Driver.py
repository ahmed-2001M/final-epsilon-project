from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import hashlib
import random

class DRIVER:
    _instance = None

    def __new__(cls): ## apply singleton pattern
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            options = webdriver.FirefoxOptions()
            options.page_load_strategy = 'eager'
            options.headless = False  
            cls.driver = cls.create_firefox_driver_with_proxy(options)
            
        return cls._instance

    @staticmethod
    def create_firefox_driver_with_proxy(options): 
        proxy_list = [
            "47.88.62.42:80"
        ]

        proxy_server = random.choice(proxy_list)
        print(proxy_server)
        print('_'*50)

        proxy = webdriver.Proxy()
        proxy.http_proxy = proxy_server

        options.proxy = proxy

        driver = webdriver.Firefox(options=options)

        return driver



    def landFirstPage(self, URL):
        self.driver.get(URL)

    def clickLink(self, link_xpath=None, element=None): ## Function for changing the driver tab to the open tab
        if link_xpath and not element:
            element = self.driver.find_element(By.XPATH, link_xpath)

        element.click()

        self.driver.switch_to.window(self.driver.window_handles[-1])

    def waitElementLoad(self, xpath, timeout=10, card=None): ## Function for waiting for element loading if it has not been loaded yet because we use the eager strategy
        try:
            if card:
                element = WebDriverWait(card, timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            else:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
            return element
        except Exception as e:
            print(f"Element not found: {xpath}")
            return None

    def hashing(self, data_to_hash): ## hash function for identifying each row in the database
        hashed_data = hashlib.md5(data_to_hash.encode()).hexdigest()
        return hashed_data

