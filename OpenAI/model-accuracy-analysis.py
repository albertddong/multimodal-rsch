import pandas as pd
import base64
import requests
import json
import csv
import os

# OpenAI API Key
api_key = ""

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

data_list = []

image_map = ["valid_01","valid_02","valid_10","valid_26","valid_30","valid_31","valid_35","invalid_03"]

file_path = '/home/albert/multimodal-rsch-master/multimodal-rsch/dataset/choose_model.json'
with open(file_path, 'r') as file:
    data = json.load(file)

grouped_questions = data['grouped_questions']

for index, questions in grouped_questions.items():
    print(f"Group {index}")
    for question in questions:
        print("Index: ", index)
        query = question['question']
        internlm = question['internlm']
        internvl2 = question['internvl2']
        internvl1 = question['internvl1']

        image = f'/home/albert/multimodal-rsch-master/multimodal-rsch/dataset_images/{image_map[int(index)]}.png'
        img_encoded = encode_image(image)
        
        payload = {
            "model": "gpt-4o",
            "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f'Context: For the uploaded image, there is an associated question. I have responses from three models, each on a different line, that answer this question. I want you to rate these responses by returning the model(s) with the most accurate response. If there are multiple valid responses, return multiple model names. Finally, I want you to give a brief explanation behind your choice.\nQuestion: {query}\ninternlm: {internlm}\ninternvl2: {internvl2}\ninternvl1 {internvl1}'
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{img_encoded}"
                }
                }
            ]
            }
            ],
            "max_tokens": 1500
            }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        try:
            message_content = response.json()['choices'][0]['message']['content']
        except Exception:
            message_content = response.json()
        print(message_content)
        
        data = {f'{index}': message_content}
        data_list.append(data)

with open('/home/albert/multimodal-rsch-master/multimodal-rsch/OpenAI/model-review-response-3.json', 'w') as file:
    json.dump(data_list, file, indent=4)
    # image_path = f"/home/albert/llava-git/simple_{set_info['set_number']}.png"

    # Getting the base64 string
    # base64_image = encode_image(image_path)
