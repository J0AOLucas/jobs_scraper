# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread
# pip install \
#     google-api-python-client~=2.85.0 \
#     google-auth-oauthlib~=1.0.0 \
#     google-auth-httplib2~=0.1.0

import gspread
from google.oauth2.service_account import Credentials
from microsoft import get_microsoft_jobs
from sales_force import get_sales_force_jobs
from adobe import get_adobe_jobs
from aws import get_aws_jobs
from cisco import get_cisco_jobs
from databricks import get_databricks_jobs
from google_scraping import get_google_jobs
from hubspot import get_hubspot_jobs
from ibm import get_ibm_jobs
from oracle import get_oracle_jobs
from apple import get_apple_jobs
from netflix import get_netflix_jobs
import pdb
import time

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]

creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

sheet_id = '1XFAtnrIZGsTqvFXZZiN00huJgVikcKesrAG24Z5-9nM'
sheet = client.open_by_key(sheet_id)

response = sheet.sheet1.batch_clear(["A2:C1500"])

jobs = []
jobs.extend(get_microsoft_jobs())
jobs.extend(get_sales_force_jobs())
jobs.extend(get_adobe_jobs())
jobs.extend(get_aws_jobs())
jobs.extend(get_cisco_jobs())
jobs.extend(get_databricks_jobs())
jobs.extend(get_google_jobs())
jobs.extend(get_hubspot_jobs())
jobs.extend(get_ibm_jobs())
jobs.extend(get_oracle_jobs())
jobs.extend(get_apple_jobs())
jobs.extend(get_netflix_jobs())


cell = 2
api_pause = 0
for job in jobs:
    if api_pause >= 17:
        print('Adding pause...')
        time.sleep(70)
        api_pause = 0

    sheet.sheet1.update_cell(cell, 1, job['company'])
    sheet.sheet1.update_cell(cell, 2, job['title'])
    sheet.sheet1.update_cell(cell, 3, job['link'])
    cell += 1
    api_pause += 1

print('Jobs process Finished!')