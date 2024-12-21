import requests
import os
import json

def download_file(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return response.text

url = "https://poligon.aidevs.pl/dane.txt"
file_content = download_file(url)

print(file_content)

line1, line2 = file_content.split('\n', 1)

line2 = line2.replace('\n', '')

print("Line 1:", line1)
print("Line 2:", line2)

apikey = os.getenv('AIDEVS_API_KEY')

data = {
    "task": "POLIGON",
    "apikey": apikey,
    "answer": [line1, line2]
}

json_data = json.dumps(data)
print(json_data)

response = requests.post("https://poligon.aidevs.pl/verify", data=json_data)
print(response.text)