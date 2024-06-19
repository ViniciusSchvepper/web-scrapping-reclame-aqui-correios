from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_complaints_titles():
    titles_list = []
    titles = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1pe7b5t-1')
    for t in titles:
        titles_list.append(t.text)
    return titles_list

def get_complaints_status():
    complaints_status_list = []
    status = driver.find_elements(By.CSS_SELECTOR, 'span.sc-1pe7b5t-4')
    for s in status:
        complaints_status_list.append(s.text)
    return complaints_status_list

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = service)
driver.get("https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/")

titles_list = get_complaints_titles()
complaints_status_list = get_complaints_status()


driver.quit()