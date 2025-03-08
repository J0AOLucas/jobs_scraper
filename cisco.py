from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

def get_cisco_jobs():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox")

    url = f"https://jobs.cisco.com/jobs/SearchJobs/sales?21178=%5B169482%5D&21178_format=6020&21181=%5B9013351%5D&21181_format=6023&listFilterMode=1"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    jobs = []
    wait = WebDriverWait(driver, 10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    while True:
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find('tbody').find_all('tr')
        time.sleep(5)

        if job_elements:
            for job_element in job_elements:
                job_title = job_element.find('td').text
                job_link = job_element.find('a')['href']

                jobs.append({
                    'company': 'Cisco',
                    'title': job_title,
                    'link': job_link
                })
        else:
            break

        next_button = soup.find('a', 'pagination_item')
        time.sleep(2)
        if next_button:
            link = next_button['href']
            driver.get(link)
            print(f"Going to next page...")
        else:
            print('No more pages available')
            break

    driver.quit()
    print('Cisco Finished!')
    return jobs
        