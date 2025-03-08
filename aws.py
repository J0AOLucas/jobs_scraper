from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_aws_jobs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    url = f"https://www.amazon.jobs/content/en/teams/amazon-web-services/sales?role-type%5B%5D=0&category%5B%5D=Sales%2C+Advertising%2C+%26+Account+Management&employment-type%5B%5D=Full+time&country%5B%5D=US"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    page_number = 1
    jobs = []
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages_count = int(soup.find_all('li', 'css-lsly4i ehuj7it2')[-1].text)

    while True:
        for x in range(pages_count):
            
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_elements = soup.find_all('div', class_='job-card-module_root__QYXVA')

            if job_elements:
                for job_element in job_elements:
                    job_title = job_element.find('h3').text
                    job_link = job_element.find('a')['href']
                    job_link = f"https://www.amazon.jobs/en{job_link}/{job_title}"

                    jobs.append({
                        'company': 'Amazon Web Services (AWS)',
                        'title': job_title,
                        'link': job_link
                    })
            else:
                break
            
            #next_button = soup.find('button', 'e4s17lp0 css-g28onq')
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='search']/div/div[2]/div[2]/nav/button[2]/div")))
            driver.execute_script("arguments[0].click();", next_button)
            print(f"Going to next page...")
        
        break

    driver.quit()
    print('AWS Finished!')
    return jobs
        