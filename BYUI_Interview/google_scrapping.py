from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from firebase import send_data

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

url = f"https://www.google.com/about/careers/applications/jobs/results/?category=SALES_OPERATIONS&category=SALES&category=PRODUCT_SUPPORT&category=PARTNERSHIPS&employment_type=FULL_TIME&location=United%20States&q=sales&page=1"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

page_number = 1
jobs = []

while True:
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_elements = soup.find_all('li', class_='lLd3Je')
    
    if job_elements:
        for job_element in job_elements:
            job_title = job_element.find('h3','QJPWVe').text
            job_link = job_element.find('a', 'WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb')['href']
            job_link = f"https://www.google.com/about/careers/applications/{job_link}"

            jobs.append({
                'company': 'Google',
                'title': job_title,
                'link': job_link
            })
    else:
        break
    try:
        page_number += 1
        next_button = soup.find('a', {'aria-label': 'Go to next page'})['href']
        next_page_link = f"https://www.google.com/about/careers/applications/jobs/results/?category=SALES_OPERATIONS&category=SALES&category=PRODUCT_SUPPORT&category=PARTNERSHIPS&employment_type=FULL_TIME&location=United%20States&q=sales&page={page_number}"
        driver.get(next_page_link)
        print(f"Going to next page: {next_page_link}")
        time.sleep(3)
    except:
        print("No more pages available")
        break

driver.quit()
for job in jobs:
    send_data(job)


print('Finished!')
print(len(jobs))
        