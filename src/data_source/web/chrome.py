from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ChromeDriverDataSource():
    """ Representa... """

    def __init__(self, path_driver: str, url: str):

        service = Service(path_driver)
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Argumento para maximizar a janela do Chrome
        
        self._url = url
        self._driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def open(self):
        """ """
        self._driver.get(self._url)

    def close(self):
        """ """
        self._driver.quit()
        
    def execute_js(self, script, element):
        self._driver.execute_script(script, element)
    
    def localize_element_css(self, wait_time: int, id_locator: str):
        """ """
        try:
            element = WebDriverWait(self._driver, wait_time).until(EC.visibility_of_element_located((By.CSS_SELECTOR, id_locator)))
            return element
        
        except Exception:
            return None
        
    def extract_html(self, element):
        return element.get_attribute('innerHTML')
