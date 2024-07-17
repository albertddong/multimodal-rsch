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
# Load the CSV file
file_path = '/home/albert/multimodal-rsch-master/multimodal-rsch/updated_network_questions_answers_v5.csv'
print(sorted(os.listdir('/home/albert/multimodal-rsch-master/multimodal-rsch/network-pictures')))
with open("demo_gpt_response.csv", "w") as f:
    for img_path in sorted(os.listdir('/home/albert/multimodal-rsch-master/multimodal-rsch/network-pictures')):
        print(img_path)
        img_encoded = encode_image(os.path.join('/home/albert/multimodal-rsch-master/multimodal-rsch/network-pictures',img_path))
        payload = {
            "model": "gpt-4o",
            "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": f"Give me 5 question answer pairs for the following network diagram. Each answer should be detailed and in complete sentences. Add in a mix of normal questions and harder questions that go beyond identifying things on the screen and require multiple sentences. I want the output in a very specific format, including the image path, the question, and the response. An example of the output you would give for a single question/answer pair is: '/home/albert/multimodal-rsch-master/multimodal-rsch/network-pictures/{img_path}, Identify the IP address of the router RI and the subnet it belongs to, The IP address of router R1 is 10.1.52.3, and it belongs to the subnet 10.1.52.0/24. This subnet indicates that the network has 256 IP addresses, ranging from 10.1.52.0 to 10.1.52.255, with 10.1.52.0 being the network address and 10.1.52.255 being the broadcast address.'"
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
        f.write(message_content)

    # image_path = f"/home/albert/llava-git/simple_{set_info['set_number']}.png"

    # Getting the base64 string
    # base64_image = encode_image(image_path)

data = pd.read_csv(file_path)

# Extracting the questions and appending them to a list
questions = data['prompt'].tolist()

# Display the questions list
for question in questions:
    print(question)