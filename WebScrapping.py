# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# service = ChromeService(executable_path = ChromeDriverManager().install())
# driver = webdriver.Chrome(service = service)
# driver.get("https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/?pagina=50")

# def get_complaints_titles():
#     titles_list = []
#     titles = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1pe7b5t-1')
#     for t in titles:
#         titles_list.append(t.text)
#     return titles_list

# def get_complaints_statuses():
#     complaints_status_list = []
#     status = driver.find_elements(By.CSS_SELECTOR, 'span.sc-1pe7b5t-4')
#     for s in status:
#         complaints_status_list.append(s.text)
#     return complaints_status_list

# def get_complaints_descriptions(titles_list, actual_url):
#     complaints_descriptions_list = []
#     for title in titles_list:
#         # time.sleep(5)
#         h4_elements = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1pe7b5t-1')
#         link_element = None
#         for h4 in h4_elements:
#             if h4.text == title:
#                 link_element = h4.find_element(By.XPATH, './ancestor::a')
#                 break
#         if link_element:
#             link_element.click()
#             try:
#                 description = WebDriverWait(driver, 10).until(
#                     EC.visibility_of_element_located((By.CLASS_NAME, 'sc-lzlu7c-17'))
#                 ).text
#                 complaints_descriptions_list.append(description)
#             except TimeoutException:
#                 print("Timed out waiting for description.")

#             driver.get(actual_url)
#             overlay_status = get_overlay_status()
#             print(f'Retornando a pagina com todas as reclamações, status do overlay = {overlay_status}')
#             time.sleep(3)
#             if overlay_status == 'block':
#                 time.sleep(90)
#     return complaints_descriptions_list

# def get_overlay_status() -> str:
#     get_overlay = driver.find_element(By.ID, 'sec-overlay')
#     get_overlay_status = get_overlay.value_of_css_property('display')
#     return get_overlay_status

# all_retrived_titles = []
# all_retrived_statuses = []
# all_retrived_descriptions = []

# def Main():
#     while True:
#         actual_url = driver.current_url
#         time.sleep(3)
#         overlay_status = get_overlay_status()
#         print(f'Pagina passada com sucesso, status do overlay = {overlay_status}')
#         if overlay_status == 'block':
#             time.sleep(90)
#         titles_list = get_complaints_titles()
#         if not titles_list:
#             print('Sem mais ocorrencias, fechando o driver.')
#             break
#         statuses_list = get_complaints_statuses()
#         description_list = get_complaints_descriptions(titles_list, actual_url)

#         all_retrived_titles.extend(titles_list)
#         all_retrived_statuses.extend(statuses_list)
#         all_retrived_descriptions.extend(description_list)

#         try:
#             time.sleep(3)
#             if overlay_status == 'block':
#                 time.sleep(90)
#             next_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="next-page-navigation-button"]'))
#             )
#             driver.execute_script('arguments[0].scrollIntoView(true)', next_button)
#             time.sleep(4)
#             next_button.click()
#         except ElementClickInterceptedException:
#             print('Não foi possível clicar no botão. Tentando novamente')
#             time.sleep(2)

#     driver.quit()
#     return all_retrived_titles, all_retrived_statuses, all_retrived_descriptions

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import time

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.reclameaqui.com.br/empresa/correios/lista-reclamacoes/")

def get_complaints_titles():
    titles_list = []
    titles = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1pe7b5t-1')
    for t in titles:
        titles_list.append(t.text)
    return titles_list

def get_complaints_statuses():
    complaints_status_list = []
    status = driver.find_elements(By.CSS_SELECTOR, 'span.sc-1pe7b5t-4')
    for s in status:
        complaints_status_list.append(s.text)
    return complaints_status_list

def get_complaints_descriptions(titles_list, actual_url):
    complaints_descriptions_list = []
    for title in titles_list:
        h4_elements = driver.find_elements(By.CSS_SELECTOR, 'h4.sc-1pe7b5t-1')
        link_element = None
        for h4 in h4_elements:
            if h4.text == title:
                link_element = h4.find_element(By.XPATH, './ancestor::a')
                break
        if link_element:
            link_element.click()
            try:
                description = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, 'sc-lzlu7c-17'))
                ).text
                complaints_descriptions_list.append(description)
            except TimeoutException:
                print("Timed out waiting for description.")
            driver.get(actual_url)
            overlay_status = get_overlay_status()
            print(f'Retornando a pagina com todas as reclamações, status do overlay = {overlay_status}')
            time.sleep(3)
            if overlay_status == 'block':
                time.sleep(90)
    return complaints_descriptions_list

def get_overlay_status() -> str:
    get_overlay = driver.find_element(By.ID, 'sec-overlay')
    get_overlay_status = get_overlay.value_of_css_property('display')
    return get_overlay_status

def Main():
    all_retrived_titles = []
    all_retrived_statuses = []
    all_retrived_descriptions = []
    while True:
        actual_url = driver.current_url
        time.sleep(3)
        overlay_status = get_overlay_status()
        print(f'Pagina passada com sucesso, status do overlay = {overlay_status}')
        if overlay_status == 'block':
            time.sleep(90)
        titles_list = get_complaints_titles()
        if not titles_list:
            print('Sem mais ocorrencias, fechando o driver.')
            break
        statuses_list = get_complaints_statuses()
        description_list = get_complaints_descriptions(titles_list, actual_url)

        all_retrived_titles.extend(titles_list)
        all_retrived_statuses.extend(statuses_list)
        all_retrived_descriptions.extend(description_list)

        try:
            time.sleep(3)
            if overlay_status == 'block':
                time.sleep(90)
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="next-page-navigation-button"]'))
            )
            driver.execute_script('arguments[0].scrollIntoView(true)', next_button)
            time.sleep(4)
            next_button.click()
        except ElementClickInterceptedException:
            print('Não foi possível clicar no botão. Tentando novamente')
            time.sleep(2)

    driver.quit()
    return all_retrived_titles, all_retrived_statuses, all_retrived_descriptions
