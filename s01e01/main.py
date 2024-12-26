import requests
from openai import OpenAI
import os
from bs4 import BeautifulSoup

# Set your OpenAI API key
client = OpenAI(
  api_key = os.getenv("OPENAI_API_KEY")
)


# Function to get the question from the page
def get_question():
    response = requests.get('https://xyz.ag3nts.org/')
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        question_paragraph = soup.find('p', id='human-question')
        if question_paragraph:
            return question_paragraph.text.strip().replace('Question:', '')
        else:
            raise Exception('Question not found on the page')
    else:
        raise Exception('Failed to retrieve question')

# Function to get the answer from the LLM model
def get_answer(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Provide very short answers to the following questions, without any formating or extra characters, only numbers."},
            {"role": "user", "content": question}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content

# Function to send the answer as a POST request
def send_answer(answer):
    url = 'https://xyz.ag3nts.org/'
    data = {
        'username': 'tester',
        'password': '574e112a',  
        'answer': int(answer)
    }
    
    response = requests.post(url, data=data)

    if response.status_code == 200:
        print('Answer submitted successfully')
        print(f"Response: {response.text}")
    else:
        raise Exception('Failed to submit answer')

def main():
    try:
        question = get_question()
        print(f"Question: {question}")
        answer = get_answer(question)
        print(f"Answer: {answer}")
        send_answer(answer)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()