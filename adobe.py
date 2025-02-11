from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_adobe_jobs():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    url = f"https://careers.adobe.com/us/en/search-results?qcountry=United%20States%20of%20America"

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(url)

    jobs = []

    wait = WebDriverWait(driver, 10)

    # Click on filter teams
    teams_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Teams')]")))
    teams_button.click()
    time.sleep(2)

    # Whrite the word 'sales'
    search_box = wait.until(EC.presence_of_element_located((By.ID, "facetInput_5")))
    search_box.send_keys("Sales")
    time.sleep(2)

    # Click on 'sales option'
    sales_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='Teams-0']")))
    sales_checkbox.click()
    time.sleep(3)

    # selection role type
    role_type_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Role Type')]")))
    driver.execute_script("arguments[0].click();", role_type_button)
    time.sleep(2)

    role_type_checkbox = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='RoleTypeBody']/div/div[2]/fieldset/ul/li[1]/label")))
    driver.execute_script("arguments[0].click();", role_type_checkbox)
    time.sleep(5)

    while True:
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_elements = soup.find_all('li', class_='jobs-list-item')

        if job_elements:
            for job_element in job_elements:
                job_box = job_element.find('div', 'information')
                job_title = job_box.find('button')['aria-label'].split("ADOBU")[0].strip() if job_box else 'N/A'
                job_link = job_box.find('a', 'au-target')['href'].strip()

                jobs.append({
                    'company': 'Adobe',
                    'title': job_title,
                    'link': job_link
                })
        else:
            break
        try:
            next_button = soup.find('a', 'au-target')
            next_page_link = soup.find('a', {'aria-label': 'View next page'})['href']
            driver.get(soup.find('a', {'aria-label': 'View next page'})['href'])
            print(f"Going to next page: {next_page_link}")
            time.sleep(3)
        except:
            print("No more pages available")
            break

    driver.quit()

    print('Finished!')
    return jobs