import json
import requests
import os
from openai import OpenAI

client = OpenAI(
  api_key = os.getenv("OPENAI_API_KEY")
)

def read_input_file(input_file):
    with open(input_file, 'r') as f:
        return json.load(f)

def transform_data(data):
    # Implement your transformation logic here
    transformed_data = data  # Placeholder for actual transformation
    if 'test-data' in transformed_data:
        for item in transformed_data['test-data']:
            question = item.get('question')
            answer = item.get('answer')
            if question and answer:
                item['answer'] = eval(question)
            if 'test' in item:
                questiongpt = item['test'].get('q')
                item['test']['a'] = get_answer(questiongpt)
    return transformed_data

# Function to get the answer from the LLM model
def get_answer(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Provide very short answers to the following questions, without any formating or extra characters. Always provide answers in English."},
            {"role": "user", "content": question}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content


def write_output_file(output_file, data):
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

def send_data_to_api(api_url, data):
    aidevapikey = os.getenv('AIDEVS_API_KEY')
    if not aidevapikey:
        raise ValueError("API key not found in environment variables")

    if 'apikey' in data:
        data['apikey'] = aidevapikey

    data_to_send = {
        "task": "JSON",
        "apikey": aidevapikey,
        "answer": data
    }
    response = requests.post(api_url, json=data_to_send)
    print(response.text)
    return response.status_code

def main():
    input_file = 'input.json'
    output_file = 'output.json'
    api_url = 'https://centrala.ag3nts.org/report'  # Replace with your actual API endpoint
    

    # Read input JSON file
    data = read_input_file(input_file)

    # Transform data
    transformed_data = transform_data(data)

    # Write transformed data to output JSON file
    write_output_file(output_file, transformed_data)

    # Send transformed data to API
    status_code = send_data_to_api(api_url, transformed_data)
    # if status_code == 200:
    #     print('Data successfully sent to API')
    # else:
    #     print(f'Failed to send data to API. Status code: {status_code}')

if __name__ == '__main__':
    main()