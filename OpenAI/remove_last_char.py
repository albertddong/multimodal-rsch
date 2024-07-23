import csv
import json

column_name = "prompt"

with open("/home/albert/multimodal-rsch-master/multimodal-rsch/dataset/testing_dataset_split.csv","r") as file:
    csv_reader = csv.DictReader(file)
    
    questions = [row[column_name] for row in csv_reader]

count = 1
for question in questions:
    print(question, count)
    count+=1

check_these = [38,39,40]


with open('/home/albert/multimodal-rsch-master/multimodal-rsch/dataset/choose_model.json', 'r') as file:
    data = json.load(file)

# Check that the length of column_values matches the number of questions
if len(questions) == len(data['questions']):
    # Update each question with the corresponding value from column_values
    for question, value in zip(data['questions'], questions):
        question['question'] = value
else:
    print("Error: The number of items in column_values does not match the number of questions.")

# Save the updated JSON back to the file
with open('/home/albert/multimodal-rsch-master/multimodal-rsch/dataset/choose_model_updated.json', 'w') as file:
    json.dump(data, file, indent=4)