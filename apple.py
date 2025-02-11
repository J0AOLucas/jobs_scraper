from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def get_apple_jobs():
  chrome_options = Options()
  #chrome_options.add_argument("--headless")
  #chrome_options.add_argument("--disable-gpu")
  #chrome_options.add_argument("--no-sandbox")

  url = "https://jobs.apple.com/en-us/search?location=united-states-USA&team=sales-APPST-ARSS"

  service = Service(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=service, options=chrome_options)
  driver.get(url)

  jobs = []
  time.sleep(5)
  while True:
      soup = BeautifulSoup(driver.page_source, 'html.parser')
      table = soup.find('table')
      job_elements = soup.find_all('tbody')

      if job_elements:
          for job_element in job_elements:
              job_title = job_element.find('a').text
              job_link = job_element.find('a')['href']
              job_link = f"https://jobs.apple.com{job_link}"

              jobs.append({
                  'company': 'Apple',
                  'title': job_title,
                  'link': job_link,
              })
      else:
          break
      try:
          button = soup.find('span', 'next').get('class')
          if 'disabled' not in button:
            next_page_link = soup.find('li', 'pagination__next').find('a')['href']
            driver.get(next_page_link)
            print(f"Going to Next Page: {next_page_link}")
            time.sleep(3)
          else:
              break
      except:
          print("No more pages available")
          break

  driver.quit()
  print("Apple Finished!")
  return jobs

