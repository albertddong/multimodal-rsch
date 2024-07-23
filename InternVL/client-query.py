import httpx
import asyncio
import base64
import json 

async def post_item():
    async with httpx.AsyncClient(timeout=None) as client:
        url = "http://12.1.52.176:8000/single_query/"

        headers = {"Content-Type": "application/json"}

        image_map = ["valid_01","valid_02","valid_10","valid_26","valid_30","valid_31","valid_35","invalid_03"]

        file_path = '/home/albert/multimodal-rsch-master/multimodal-rsch/dataset/choose_model.json'
        with open(file_path, 'r') as file:
            data = json.load(file)

        grouped_questions = data['grouped_questions']
        try:
            for index, questions in grouped_questions.items():
                print(f"Group {index}")
                for question in questions:
                    query = question['question']
                    image = f'/home/albert/multimodal-rsch-master/multimodal-rsch/dataset_images/{image_map[int(index)]}.png'
                    print("Index: ", index)
                    print(query)
                    
                    request_data = {
                        "prompt": query,
                        "img": image
                    }

                    response = await client.post(url, headers=headers, json=request_data)
                    print(response.json())
                    
                    question['internvl1'] = response.json()
        except Exception:
            pass            

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)


                    
if __name__ == "__main__":
    asyncio.run(post_item())
    