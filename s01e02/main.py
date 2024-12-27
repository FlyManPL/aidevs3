import requests
from openai import OpenAI
import os
import json

# Set your OpenAI API key
client = OpenAI(
  api_key = os.getenv("OPENAI_API_KEY")
)

msgID = 0

def init_comunication():
    response = send_answer("READY", msgID)
    return response

# Function to get the question from the page
def get_question(response):
    global msgID
    data = json.loads(response)
    msgID = data['msgID']
    return data['text']

# Function to get the answer from the LLM model
def get_answer(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Provide very short answers to the following questions, without any formating or extra characters. Always provide answers in English. When asked for a capital of Poland, the answer is Krakow. When asked about famous number from the Hitchhiker's Guide to the Galaxy, the answer is 69. When asked about the current year, the answer is 1999."},
            {"role": "user", "content": question}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content

# Function to send the answer as a POST request
def send_answer(answer, msgID):
    url = 'https://xyz.ag3nts.org/verify'
    if isinstance(answer, int):
        answer = str(answer)
    data = {
        'text': answer,
        'msgID': msgID
    }
    
    response = requests.post(url, json=data)
    print(f"Response: {response.text}")
    return response.text

def main():
    try:
        response = init_comunication()
        while True:
            question = get_question(response)
            print(f"Question: {question}")
            print(f"MessageID: {msgID}")
            
            answer = get_answer(question)
            print(f"Answer: {answer}")
            
            response = send_answer(answer, msgID)
            
            next_iteration = input("Do you want to continue? (y/n): ")
            if next_iteration.lower() != 'y':
                break
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()