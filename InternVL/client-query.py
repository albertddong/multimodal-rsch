import httpx
import asyncio
import base64
import json 

async def post_item():
    async with httpx.AsyncClient(timeout=None) as client:
        url = "http://12.1.52.176:8000/single_query/"
        

        headers = {"Content-Type": "application/json"}
        
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
                if question['type'] == 'complex':
                    # Print the question
                    print(question['question'])
                    
                    request_data = {
                        "prompt": question['question'],
                        "img": f"/home/albert/llava-git/simple_{set_info['set_number']}.png",
                    }
                    
                    response = await client.post(url, headers=headers, json=request_data)
                    print(response.json())
                    
if __name__ == "__main__":
    asyncio.run(post_item())
    