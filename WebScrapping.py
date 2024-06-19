from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
import time

# Função para extrair títulos das reclamações
def get_complaints():
    titles_list = []
    titles = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1pe7b5t-1')
    for t in titles:
        titles_list.append(t.text)
    return titles_list

# Função para extrair resumos das reclamações
def get_complaints_resumes():
    resume_list = []
    resumes = driver.find_elements(By.CSS_SELECTOR, 'p.sc-1pe7b5t-2')
    for r in resumes:
        resume_list.append(r.text)
    return resume_list

# Função para extrair status das reclamações
def get_complaints_status():
    complaints_status_list = []
    status = driver.find_elements(By.CSS_SELECTOR, 'span.sc-1pe7b5t-4')
    for s in status:
        complaints_status_list.append(s.text)
    return complaints_status_list

# Inicialize o WebDriver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/")

all_titles = []
all_resumes = []
all_statuses = []

while True:
    try:
        # Espera um pouco para garantir que a página carregou completamente
        time.sleep(5)

        all_titles.extend(get_complaints())
        all_resumes.extend(get_complaints_resumes())
        all_statuses.extend(get_complaints_status())
        
        # Tenta encontrar o botão de próxima página usando aria-label ou data-testid
        next_button = driver.find_element(By.XPATH, '//button[@data-testid="next-page-navigation-button"]')
        
        # Clique no botão de próxima página
        next_button.click()
    except NoSuchElementException:
        print("Botão de próxima página não encontrado. Presumivelmente, esta é a última página.")
        break
    except ElementClickInterceptedException:
        print("O botão de próxima página não pôde ser clicado. Tentando novamente...")
        time.sleep(5)
        continue

# Feche o WebDriver
driver.quit()

print(all_titles)
print(all_resumes)
print(all_statuses)
