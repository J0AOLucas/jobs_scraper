from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

chrome_options = Options()
# chrome_options.add_argument("--headless")  # Para rodar sem interface gráfica
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox")

url = "https://careers.salesforce.com/en/jobs/?search=sales&country=United+States+of+America&team=Sales&type=Full+time&jobtype=Regular&pagesize=20#results"
page_number = 1

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

jobs = []
while True:
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_elements = soup.find_all('div', class_='card card-job')

    if job_elements:
        for job_element in job_elements:
            job_box = job_element.find('a', class_='stretched-link js-view-job')
            job_title = job_box.text.strip() if job_box else 'N/A'
            job_link = f"https://careers.salesforce.com{job_box.get('href')}" if job_box else 'N/A'

            jobs.append({
                'company': 'Sales Force',
                'title': job_title,
                'link': job_link,
            })
    else:
        break
    try:
        page_number += 1
        next_page_link = f"https://careers.salesforce.com/en/jobs/?page={page_number}&search=sales&country=United%20States%20of%20America&team=Sales&type=Full%20time&jobtype=Regular&pagesize=20#results"
        driver.get(next_page_link)
        print(f"Redirecting to next page: {next_page_link}")
        time.sleep(3)
    except:
        print("No more pages available")
        break

driver.quit()

for job in jobs:
    print(job)

print(len(jobs))
print("Finished")
