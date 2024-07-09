import base64
import requests
import json

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
# Load the JSON data from the file
with open('/home/albert/multimodal-rsch-master/multimodal-rsch/QuestionDataset.json', 'r') as file:
    question_data = json.load(file)

# Iterate through each set in the data
for set_info in question_data['sets']:
    # Print the set number
    print(f"Set Number: {set_info['set_number']}")
    
    # Iterate through each question in the set
    for question in set_info['questions']:
        # Check if the question is not of type 'relational'
        if question['type'] != 'relational':
            # Print the question
            print(question['question'])
            
            image_path = f"/home/albert/llava-git/simple_{set_info['set_number']}.png"

            # Getting the base64 string
            base64_image = encode_image(image_path)

            
            payload = {
            "model": "gpt-4o",
            "messages": [
              {
                "role": "user",
                "content": [
                  {
                    "type": "text",
                    "text": "What’s in this image?"
                  },
                  {
                    "type": "image_url",
                    "image_url": {
                      "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                  }
                ]
              }
            ],
            "max_tokens": 150
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            print(response.json())
  


  

  
