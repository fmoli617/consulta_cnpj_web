from data_source.web.chrome import ChromeDriverDataSource
from app.configurations import get_configuration_by_path
from bs4 import BeautifulSoup

class WebAccess():
    """ Representa... """

    def __init__(self, driver: ChromeDriverDataSource = None):
        """ """
        self._driver = driver or ChromeDriverDataSource(**get_configuration_by_path('data_access/web'))

    def open(self):
        """ """
        self._driver.open()
    
    def close(self):
        """ """
        self._driver.close()
    
    def click(self, localizador: str):
        """ """
        element = self._driver.localize_element_css(1, localizador)
        
        if element:
            element.click()
    
    
    def write_js(self, info: str, localizador: str):
        """ """
        element = self._driver.localize_element_css(1, localizador)
        
        if element:
            self._driver.execute_js(f"arguments[0].value = '{info}';", element)
    
    def list_info_extract_table(self, localizador: str):
        """ """
        try:
            element = self._driver.localize_element_css(1, localizador)
            html = self._driver.extract_html(element)
            soup = BeautifulSoup(html, 'html.parser')
            tags_b = soup.find_all('b')
            info = [tag.get_text() for tag in tags_b]   
            info.append('Sucesso')
            
        except Exception as e:
            info = ['','','','','','','','','','','','','','','','','','','','','','','','','','','','CNPJ Invalido']
        

        return info
        
        
        
        
        
        
        
        
            