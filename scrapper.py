import json
import requests


def cse_scrapper():
    url = "https://www.cse.lk/api/tradeSummary"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.post(url, headers=headers)
    print(response.ok)
    return response


data = cse_scrapper().json()  

print(data)

sample_data = {'id': 405, 'name': 'EASTERN MERCHANTS PLC', 'symbol': 'EMER.N0000', 'quantity': 1, 'percentageChange': 0.0, 'change': 0.0, 
 'price': 7.2, 'previousClose': 7.2, 'high': 7.2, 'low': 7.2, 'lastTradedTime': 1746001996717, 'issueDate': '01/JAN/1982', 
 'turnover': 1094.4, 'sharevolume': 152, 'tradevolume': 4, 'marketCap': 845611200.0, 'marketCapPercentage': 0.0, 'open': 7.2, 
 'closingPrice': 7.2, 'crossingVolume': 152, 'crossingTradeVol': 4, 'status': 0}

