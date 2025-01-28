# pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread
# pip install \
#     google-api-python-client~=2.85.0 \
#     google-auth-oauthlib~=1.0.0 \
#     google-auth-httplib2~=0.1.0

import gspread
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets'
]
creds = Credentials.from_service_account_file('credentials.json', scopes=scopes)
client = gspread.authorize(creds)

shet_id = "1XFAtnrIZGsTqvFXZZiN00huJgVikcKesrAG24Z5-9nM"
sheet = client.open_by_key(shet_id)

# Coletando celulas
values_list = sheet.sheet1.row_values(5)
list = [{'Company': 'Google',
'Title': 'Senior Junior',
'Link': "https://api/global/en/job/1800077/Senior%20Technology%20Specialist%20-%20Business%20Applications"}]

sheet.sheet1.update_cell(6,1, list[0]['Company'])
sheet.sheet1.update_cell(6,2, list[0]['Title'])
sheet.sheet1.update_cell(6,3, list[0]['Link'])

val = sheet.acell('B1').value

print("Processo concluido com sucesso!")