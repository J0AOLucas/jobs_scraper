import requests

def get_databricks_jobs():
    url = "https://www.databricks.com/careers-assets/page-data/company/careers/open-positions/page-data.json?department=Sales&location=United%20States"

    # states = [
    #     "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
    #     "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
    #     "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
    #     "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
    #     "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", 
    #     "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", 
    #     "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
    # ]
    # Fazendo a requisição GET
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        jobs = data['result']['pageContext']['data']['allGreenhouseJob']['nodes']
        sale_jobs = []
        for job in jobs:
            if 'United States' in job.get('location')['name'] and 'Sales' in job.get('departments')[0]['name']:
                job_title = job.get('title')
                job_link = job.get('absolute_url')
                
                sale_jobs.append({
                    'company': 'Databricks',
                    'title': job_title,
                    'link': job_link
                })
        print('Databricks Finished!')
        return sale_jobs
    else:
        print(f"Falha ao fazer a requisição. Status Code: {response.status_code}")