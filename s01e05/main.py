import requests
import openai
import os
from openai import OpenAI

client = OpenAI(
  api_key = os.getenv("OPENAI_API_KEY")
)

# Function to download text file from URL
def download_text_file(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

# Function to transform text using OpenAI
def transform_text_with_openai(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You need to transform below text. The only changes you need to do are: find name, address and age and replace it with CENZURA"},
            {"role": "user", "content": question}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content   

# Function to send transformed text to an API
def send_answer(task, aidevsapikey, answer):
    url = 'https://centrala.ag3nts.org/report'
    data = {
        "task": task,
        'apikey': aidevsapikey,  
        'answer': answer
    }
   
    resonse = requests.post(url, json=data)
    return resonse.text

def main():
    task = "CENZURA"

    aidevsapikey = os.getenv('AIDEVS_API_KEY')
    if not aidevsapikey:
        raise ValueError("AIDEVS API key not found in environment variables")
    
    text_file_url = "https://centrala.ag3nts.org/data/" + aidevsapikey + "/cenzura.txt"

    # Step 1: Download text file
    text = download_text_file(text_file_url)
    print("Downloaded text:", text)

    # Step 2: Transform text using OpenAI
    transformed_text = transform_text_with_openai(text)
    print("Transformed text:", transformed_text)

    # Step 3: Send transformed text to API
    response = send_answer(task, aidevsapikey, transformed_text)
    print("API response:", response)

if __name__ == "__main__":
    main()