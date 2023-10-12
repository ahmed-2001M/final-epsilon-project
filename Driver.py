# from selenium.webdriver import Firefox, FirefoxOptions, FirefoxProfile
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.support.wait import WebDriverWait
# import hashlib
# from proxyscrape import create_collector
# from selenium.webdriver.common.proxy import Proxy, ProxyType
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.common.proxy import Proxy
# import webdriver_manager


# def get_proxy():
#     collector = create_collector('default', 'http')
#     proxy = collector.get_proxy()
#     print(f'proxy is : {proxy.host}:{proxy.port}')
#     return f"{proxy.host}:{proxy.port}"


# class DRIVER:
#     _instance = None

#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super().__new__(cls)
#             options = FirefoxOptions()
#             options.page_load_strategy = 'eager'
#             options.headless = False  # Run Firefox in headless mode

#             # Set up the proxy
#             proxy = Proxy()
#             proxy.http_proxy = get_proxy()  # Use the function to get a proxy

#             # Create a Firefox profile with desired capabilities
#             profile = FirefoxProfile()
#             profile.set_preference('network.proxy.type', 1)
#             profile.set_preference('network.proxy.http', proxy.http_proxy)

#             cls.driver = Firefox(firefox_profile=profile, options=options)

#         return cls._instance

#     def set_proxy(self):
#         # Change the proxy dynamically
#         proxy = Proxy()
#         proxy.http_proxy = get_proxy()  # Use the function to get a new proxy
#         self.capabilities['proxy'] = {
#             "proxyType": "manual",
#             "httpProxy": proxy.http_proxy,
#         }

#     def change_proxy(self):
#         self.set_proxy()  # Change the proxy settings


#     def landFirstPage(self, URL):
#         self.driver.get(URL)

#     def clickLink(self, link_xpath=None, element=None):
#         if link_xpath and not element:
#             element = self.driver.find_element(By.XPATH, link_xpath)
#         # Click the link to open a new tab
#         element.click()

#         # Switch to the new tab
#         self.driver.switch_to.window(self.driver.window_handles[-1])
    
#     def waitElementLoad(self, xpath, timeout=10 , card = None):
#         try:
#             if card:
#                 element = WebDriverWait(card, timeout).until(
#                     EC.presence_of_element_located((By.XPATH, xpath))
#                 )
#             else:
#                 element = WebDriverWait(self.driver, timeout).until(
#                     EC.presence_of_element_located((By.XPATH, xpath))
#                 )
#             return element
#         except Exception as e:
#             print(f"Element not found: {xpath}")
#             return None
    
    

#     def hashing(self,data_to_hash):
#         hashed_data = hashlib.md5(data_to_hash.encode()).hexdigest()
#         return hashed_data








from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
import hashlib


class DRIVER:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            options = Options()
            options.page_load_strategy = 'eager'
            options.headless = False  # Run Firefox in headless mode
            cls.driver = Firefox(options=options)
            
        return cls._instance

    def landFirstPage(self, URL):
        self.driver.get(URL)

    def clickLink(self, link_xpath=None, element=None):
        if link_xpath and not element:
            element = self.driver.find_element(By.XPATH, link_xpath)
        # Click the link to open a new tab
        element.click()

        # Switch to the new tab
        self.driver.switch_to.window(self.driver.window_handles[-1])
    
    def waitElementLoad(self, xpath, timeout=10 , card = None):
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
    
    

    def hashing(self,data_to_hash):
        hashed_data = hashlib.md5(data_to_hash.encode()).hexdigest()
        return hashed_data

