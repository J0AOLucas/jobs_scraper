from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pdb

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

url = f"https://careers.oracle.com/jobs/#en/sites/jobsearch/requisitions?keyword=Sales&lastSelectedFacet=LOCATIONS&location=United+States&locationId=300000000149325&selectedCategoriesFacet=300000001917358&selectedFlexFieldsFacets=%22AttributeChar4%7CEmployee%7C%7CAttributeChar29%7CIndividual+Contributor%22&selectedLocationsFacet=300000000149325"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(url)

jobs = []
wait = WebDriverWait(driver, 10)
soup = BeautifulSoup(driver.page_source, 'html.parser')
time.sleep(10)

while True:
    time.sleep(5)
    next_button = driver.find_elements(By.XPATH, "//div[@class='search-pagination']//button[contains(@class, 'button') and contains(@class, 'text-color-primary')]")
    if len(next_button) != 0:
        time.sleep(5)
        next_button = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div/div/main/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[2]/button")))
        next_button.click()
    else:
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        print("Collecting jobs...")

        job_elements = soup.find_all('div', class_='job-tile job-grid-item search-results job-grid-item--all-actions-visible')
        if job_elements:
            for job_element in job_elements:
                job_title = job_element.find('span', 'job-tile__title').text
                job_link = job_element.find('a', 'job-grid-item__link')['href']

                jobs.append({
                    'company': 'Oracle',
                    'title': job_title,
                    'link': job_link
                })
            break
        else:
            print('No more jobs available!')
            break

driver.quit()
for job in jobs:
    print(job)

print('Finished!')
print(len(jobs))
        