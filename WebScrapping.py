from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/")

def get_complaints_titles() -> list[str]:
    time.sleep(5)
    titles_list = []
    titles = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1pe7b5t-1')
    for t in titles:
        titles_list.append(t.text)
    return titles_list

def get_complaints_status() -> list[str]:
    complaints_status_list = []
    status = driver.find_elements(By.CSS_SELECTOR, 'span.sc-1pe7b5t-4')
    for s in status:
        complaints_status_list.append(s.text)
    return complaints_status_list

def get_complaints_descriptions(titles_list) -> list[str]:
    complaints_descriptions_list = []
    for title in titles_list:
        link_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//h4[text()="{title}"]/ancestor::a'))
        )
        link_element.click()
        description = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'sc-lzlu7c-17'))
        ).text
        print(description)
        complaints_descriptions_list.append(description)
        driver.get("https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/")
        time.sleep(5)

    
    return complaints_descriptions_list

titles_list = get_complaints_titles()
complaints_statuses_list = get_complaints_status()
complaints_descriptions_list = get_complaints_descriptions(titles_list)

driver.quit()
