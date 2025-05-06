import requests

url = "http://54.253.28.141:8000/structured_data/structured_company_data.json"
response = requests.get(url)

print(response.status_code)
print(response.json())