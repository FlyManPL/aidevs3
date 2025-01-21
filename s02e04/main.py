import os
import requests
import base64
from openai import OpenAI

client = OpenAI(
  api_key = os.getenv("OPENAI_API_KEY")
)

def concatenate_files(folder_path):
    result = ""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    stripped_line = line.strip()
                    if stripped_line:  # Check if the line is not empty
                        result += f"- {stripped_line}\n"
    return result

def send_answer(task, aidevsapikey, answer):
    url = 'https://centrala.ag3nts.org/report'
    data = {
        "task": task,
        'apikey': aidevsapikey,  
        'answer': answer
    }
   
    response = requests.post(url, json=data)
    return response.text

def get_text_from_audio(path):
    audio_file= open(path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    return transcription.text

def get_text_from_image(path):
    image_file= open(path, "rb")
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
                {'role': 'user','content': [{'type': 'image_url',"image_url": {"url": f"data:image/jpeg;base64,{base64_image}",'detail': 'high'}},{'type': 'text','text': 'Extract text from the image. Return only the text and nothing else.'}]}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content 


def get_category(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f'''<prompt_objective>
                            Classify Polish factory reports into exactly one of three categories ('people', 'hardware', 'none') based on mentions of human capture or hardware repairs, while ignoring software-related content and fact catalogs.
                            </prompt_objective>
                            
                            <prompt_rules>
                            1. MUST return ONLY one of these exact values: 'people', 'hardware', 'none'
                            2. MUST return ONLY the word - no explanations, punctuation, or additional text
                            3. CLASSIFICATION PRIORITIES:
                               - ANY mention of captured people → 'people'
                               - Hardware repairs (without people) → 'hardware'
                               - Everything else → 'none'
                            4. AUTOMATIC 'none' TRIGGERS:
                               - Software-related content
                               - Fact catalogs
                               - Ambiguous content
                            5. KEYWORD TRIGGERS:
                               People: schwytano, intruz, ślad, obecność, włamanie
                               Hardware: naprawa, usterka sprzętowa, awaria fizyczna, uszkodzenie mechaniczne
                            </prompt_rules>
                            
                            <prompt_examples>
                            USER: "Schwytano 2 intruzów w sektorze B4."
                            AI: people
                            
                            USER: "Naprawa uszkodzonego zaworu w pompie P45."
                            AI: hardware
                            
                            USER: "Aktualizacja oprogramowania sterowników."
                            AI: none
                            
                            USER: "Wykryto ślady obecności w maszynowni. Uszkodzona skrzynka bezpieczników."
                            AI: people
                            
                            USER: "Katalog faktów technicznych: uszkodzenia mechaniczne kwartał 3."
                            AI: none
                            
                            USER: "Usterka sprzętowa wywołana przez próbę włamania."
                            AI: people
                            
                            USER: "System bezpieczeństwa wykrył ruch w sektorze C. Awaria kamery 5."
                            AI: people
                            
                            USER: "Przegląd techniczny urządzeń - wszystko sprawne."
                            AI: none
                            </prompt_examples>
                            
                            <conflict_resolution>
                            1. People mentions ALWAYS override hardware mentions
                            2. Hardware issues only count if NO people-related content
                            3. ANY ambiguity results in 'none'
                            4. Software/fact catalogs are 'none' regardless of other content
                            </conflict_resolution>
                            '''
            },
            {"role": "user", "content": question}
        ],
        max_tokens=100
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    task = "kategorie"
    aidevsapikey = os.getenv('AIDEVS_API_KEY')

    facts_path = '.\\data\\facts'
    facts = concatenate_files(facts_path)

    data_folder_path = '.\\data'

    categories = {"people": [], "hardware": [], "none": []}

    # for filename in os.listdir(data_folder_path):
    #     if filename.endswith('.mp3'):
    #         file_path = os.path.join(data_folder_path, filename)
    #         text = get_text_from_audio(file_path)
    #         new_txt_filename = filename + '.txt'
    #         new_txt_file_path = os.path.join(data_folder_path, new_txt_filename)
    #         with open(new_txt_file_path, 'w', encoding='utf-8') as new_txt_file:
    #             new_txt_file.write(text)

    # for filename in os.listdir(data_folder_path):
    #     if filename.endswith('.png'):
    #         file_path = os.path.join(data_folder_path, filename)
    #         text = get_text_from_image(file_path)
    #         new_txt_filename = filename + '.txt'
    #         new_txt_file_path = os.path.join(data_folder_path, new_txt_filename)
    #         with open(new_txt_file_path, 'w', encoding='utf-8') as new_txt_file:
    #             new_txt_file.write(text)

    for filename in os.listdir(data_folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(data_folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                category = get_category(content)
                if category in categories:
                    categories[category].append(filename)

    for category in categories:
        categories[category] = [value.replace('.mp3.txt', '.mp3').replace('.png.txt', '.png') for value in categories[category]]
    
    categories[category].sort()

    response = send_answer(task, aidevsapikey, categories)
    print("API response:", response)