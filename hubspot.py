from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

url = f"https://www.hubspot.com/careers/sales/jobs?hubs_signup-url=www.hubspot.com%2Fcareers%2Fsales&hubs_signup-cta=careers-department-hero&page=1#office=san-francisco,cambridge;department=sales;roleType=individual;"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

jobs = []

while True:
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_elements = soup.find_all('li', 'sc-bdVaJa fzBexj')
    time.sleep(3)

    if job_elements:
        for job_element in job_elements:
            job_title = job_element.find('h3').text
            job_link = job_element.find('a')['href']
            job_link = f"https://www.hubspot.com{job_link}"

            jobs.append({
                'company': 'HubSpot',
                'title': job_title,
                'link': job_link
            })
        break
    else:
        break

driver.quit()

for job in jobs:
    print(job)