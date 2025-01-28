# pip install webdriver-manager
# pip install --upgrade webdriver-manager
# pip install selenium webdriver-manager beautifulsoup4
# 


# install python.exe and select the PATH option

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from firebase import send_data
import pdb
import platform


# Configurações do navegador
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

url = f"https://jobs.careers.microsoft.com/global/en/search?q=technology%20sales&lc=United%20States&d=Technology%20Specialists&rt=Individual%20Contributor&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true"

# Usando o webdriver-manager para gerenciar o chromedriver

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CLASS_NAME, "ms-List-cell"))
)

# Espera para garantir que a página carregue completamente
driver.implicitly_wait(10)

# Pegando o HTML renderizado
html = driver.page_source

# Fechando o navegador
driver.quit()

# Usando BeautifulSoup para analisar o HTML
soup = BeautifulSoup(html, 'html.parser')
job_elements = soup.find_all('div', class_='ms-List-cell')
jobs = []

for job_element in job_elements:
    job_title = job_element.find('h2', class_='MZGzlrn8gfgSs8TZHhv2')
    job_stack = job_element.find('div', class_='ms-Stack')
    job_id = job_stack.get('aria-label').split()[-1] if job_stack else 'N/A'
    job_link = (f"https://jobs.careers.microsoft.com/global/en/job/{job_id}/{job_title.text}").replace(' ', '%20')

    #date_posted_element = job_element.find('span', string=lambda text: 'days ago' in text or 'month ago' in text)
    #description_element = job_element.find('div', class_='ms-Stack')
    #location_element = job_element.find('span', string=lambda text: 'Locations' in text)

    title = job_title.text if job_title else 'N/A'
    #link = link_element['aria-label'] if link_element else 'N/A'
    #description = description_element.text if description_element else 'N/A'
    #location = location_element.text if location_element else 'N/A'
    #date_posted = date_posted_element.text if date_posted_element else 'N/A'

    jobs.append({
        'Company': 'Microsoft',
        'title': title,
        'link': job_link,
    })

for job in jobs:
    #print(f"Description: {job['description']}")
    #print(f"Location: {job['location']}")
    #print(f"Date Posted: {job['date_posted']}")
    print('Company: Microsoft')
    print(f"Title: {job['title']}")
    print(f"Link: {job['link']}")
    print('-' * 40)

for job in jobs:
    send_data(job)

print('Finished!')