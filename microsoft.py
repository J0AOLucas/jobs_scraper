from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_microsoft_jobs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    url = f"https://jobs.careers.microsoft.com/global/en/search?lc=United%20States&d=Digital%20Solution%20Area%20Specialists&d=Digital%20Cloud%20Acquisition&d=Customer%20Success%20Account%20Mgmt&d=Digital%20Account%20Management&d=Digital%20Cloud%20Solution%20Architecture&d=Digital%20Technology%20Specialists&d=Solution%20Area%20Specialists&l=en_us&pg=1&pgSz=20&o=Relevance&flt=true"

    # Usando o webdriver-manager para gerenciar o chromedriver

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ms-List-cell"))
    )

    wait = WebDriverWait(driver, 10)

    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    job_elements = soup.find_all('div', class_='ms-List-cell')
    jobs = []

    while True:
        time.sleep(4)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find_all('div', class_='ms-List-cell')
        for job_element in job_elements:
            job_title = job_element.find('h2', class_='MZGzlrn8gfgSs8TZHhv2')
            job_stack = job_element.find('div', class_='ms-Stack')
            job_id = job_stack.get('aria-label').split()[-1] if job_stack else 'N/A'
            job_link = (f"https://jobs.careers.microsoft.com/global/en/job/{job_id}/{job_title.text}").replace(' ', '%20')
            title = job_title.text if job_title else 'N/A'
            #date_posted_element = job_element.find('span', string=lambda text: 'days ago' in text or 'month ago' in text)
            #date_posted = date_posted_element.text if date_posted_element else 'N/A'

            jobs.append({
                'company': 'Microsoft',
                'title': title,
                'link': job_link,
            })
        
        next_button = soup.find("button", {"title": "Next"})['data-is-focusable']
        if next_button and next_button == 'true':
            next_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='job-search-app']/div/div[2]/div[1]/div[2]/div[2]/div/div/div/div[3]/button/span")))
            time.sleep(3)
            driver.execute_script("arguments[0].click();", next_button)
            print(f"Going to next page...")
        else:
            driver.quit()
            break

    print('Microsoft Finished!')
    return jobs