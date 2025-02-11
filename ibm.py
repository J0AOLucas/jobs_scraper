from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_ibm_jobs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    url = f"https://www.ibm.com/careers/search?field_keyword_08[0]=Sales&field_keyword_18[0]=Professional&field_keyword_18[1]=Entry%20Level&field_keyword_05[0]=United%20States"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    jobs = []

    while True:
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find_all('div', 'bx--card-group__cards__col')
        time.sleep(5)

        if job_elements:
            for job_element in job_elements:
                job_title = job_element.find('div', 'bx--card__heading').text
                job_link = job_element.find('a')['href']

                jobs.append({
                    'company': 'IBM',
                    'title': job_title,
                    'link': job_link
                })
        else:
            break

        next_button_disabled = soup.find('a', {'aria-label': 'Next'})
        time.sleep(2)
        next_button_disabled = next_button_disabled.get('aria-disabled') if next_button_disabled else None
        time.sleep(3)
        if next_button_disabled != 'true':
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='IBMAccessibleItemComponents-next']")))
            time.sleep(3)
            driver.execute_script("arguments[0].click();", next_button)
            print(f"Going to next page...")
        else:
            print('No more pages available')
            break

    driver.quit()
    print('IBM Finished!')
    return jobs
        