import requests
from bs4 import BeautifulSoup

url = "https://www.cse.lk/pages/announcements/announcements.component.html"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    announcements = soup.find_all('div', class_='announcement-title')  # Adjust the class name based on actual HTML structure
    for announcement in announcements:
        print(announcement.get_text(strip=True))
else:
    print(f"Failed to retrieve announcements. Status code: {response.status_code}")
