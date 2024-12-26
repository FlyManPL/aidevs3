import requests
import os
import json
import logging

logging.basicConfig(level=logging.ERROR)

def download_file(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except requests.RequestException as e:
        logging.error(f"Error downloading file: {e}")
        return None

def process_file_content(file_content):
    try:
        lines = file_content.split('\n')
        if len(lines) < 2:
            raise ValueError("File content does not contain enough lines")
        
        line1, line2 = lines[0], lines[1].replace('\n', '')

        logging.info(f"Line 1: {line1}")
        logging.info(f"Line 2: {line2}")

        return line1, line2
    except ValueError as e:
        logging.error(f"Error processing file content: {e}")
        return None, None

def send_post_request(line1, line2):
    try:
        apikey = os.getenv('AIDEVS_API_KEY')
        if not apikey:
            raise ValueError("API key not found in environment variables")

        data = {
            "task": "POLIGON",
            "apikey": apikey,
            "answer": [line1, line2]
        }

        json_data = json.dumps(data)
        logging.info(json_data)

        response = requests.post("https://poligon.aidevs.pl/verify", json=data)
        response.raise_for_status()  # Check if the request was successful
        logging.info(response.text)
    except ValueError as e:
        logging.error(f"Error: {e}")
    except requests.RequestException as e:
        logging.error(f"Error sending POST request: {e}")

def main():
    url = "https://poligon.aidevs.pl/dane.txt"
    file_content = download_file(url)

    if file_content:
        line1, line2 = process_file_content(file_content)
        if line1 and line2:
            send_post_request(line1, line2)
    else:
        logging.error("Failed to download file content.")

if __name__ == "__main__":
    main()