import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate and create the service client for Google Sheets and Drive
def authenticate_google_docs():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/forms"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/albert/multimodal-rsch-master/multimodal-rsch/att-form-19252f8c124f.json', scope)
    client = gspread.authorize(creds)
    return client

# Load JSON data from file
def load_json_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Create a Google Form and return the form URL and id
def create_google_form(client, title):
    form = client.create(title)
    form_url = form.responses().spreadsheet_url
    form_id = form.id
    return form_url, form_id

# Add questions to the Google Form
def add_questions_to_form(client, form_id, questions_data):
    form = client.open_by_key(form_id)
    worksheet = form.get_worksheet(0)  # Assuming questions are on the first sheet

    for question_set in questions_data['sets']:
        for question in question_set['questions']:
            if question['type'] != 'relational':
                # Add question title and description
                question_title = f"Q{question_set['set_number']}: {question['type'].capitalize()}"
                question_body = question['question']
                worksheet.append_row([question_title, question_body])

                # Add responses as linear scale questions
                for model, response in question.items():
                    if model in ['llava', 'cogvlm', 'vila'] and response:
                        response_title = response
                        # Append each response to the form as a new linear scale question
                        worksheet.append_row([response_title, '', '1', '5'])  # 1-5 scale

def main():
    client = authenticate_google_docs()
    data = load_json_data('/home/albert/multimodal-rsch-master/multimodal-rsch/QuestionDataset.json')
    form_url, form_id = create_google_form(client, "New Google Form")
    add_questions_to_form(client, form_id, data)
    print("Form created successfully. You can view it here:", form_url)

if __name__ == "__main__":
    main()