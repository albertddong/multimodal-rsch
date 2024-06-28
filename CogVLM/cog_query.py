import requests
import json

url = "http://12.1.52.176:8006/generate"
headers = {
    "Content-Type": "application/json"
}
data = {
    "prompt": "What is the IP address of the web server as per the diagram?",
    "image": "/home/albert/llava-git/simple_2.png"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())




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
            
            data = {
                "prompt": question['question'],
                "image": f"/home/albert/llava-git/simple_{set_info['set_number']}.png"
            }

            response = requests.post(url, headers=headers, data=json.dumps(data))

            print(response.json())