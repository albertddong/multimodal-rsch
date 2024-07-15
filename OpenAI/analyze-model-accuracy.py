import pandas as pd

# Load the CSV file
file_path = '/home/albert/multimodal-rsch-master/multimodal-rsch/updated_network_questions_answers_v5.csv'
data = pd.read_csv(file_path)

# Extracting the questions and appending them to a list
questions = data['prompt'].tolist()

# Display the questions list
for question in questions:
    print(question)