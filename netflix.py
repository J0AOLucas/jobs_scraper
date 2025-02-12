import requests

def get_netflix_jobs():
  url = f"https://explore.jobs.netflix.net/api/apply/v2/jobs?domain=netflix.com&profile=&location=United%20States&pid=790301196659&Teams=Sales%20and%20Business%20Development&domain=netflix.com&sort_by=relevance&utm_source=Netflix%20Careersite"
  response = requests.get(url)

  jobs = []

  if response.status_code == 200:
    response = response.json()
    positions = response['positions']
    for position in positions:
      title = position['name']
      link = position['canonicalPositionUrl']

      jobs.append({
        'company': 'Netflix',
        'title': title,
        'link': link
      })
      
  else:
    print(f"Error: {response.status_code}")

  print('Netflix Finished!')
  return jobs