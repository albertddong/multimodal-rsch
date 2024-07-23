import torch
from transformers import AutoModel, AutoTokenizer
import json

torch.set_grad_enabled(False)

# init model and tokenizer
model = AutoModel.from_pretrained('internlm/internlm-xcomposer2d5-7b', torch_dtype=torch.bfloat16, trust_remote_code=True).cuda().eval()
tokenizer = AutoTokenizer.from_pretrained('internlm/internlm-xcomposer2d5-7b', trust_remote_code=True)
model.tokenizer = tokenizer



image_map = ["valid_01","valid_02","valid_10","valid_26","valid_30","valid_31","valid_35","invalid_03"]

file_path = '/home/albert/multimodal-rsch-master/multimodal-rsch/dataset/choose_model.json'
with open(file_path, 'r') as file:
    data = json.load(file)

grouped_questions = data['grouped_questions']
try:
        
    for index, questions in grouped_questions.items():
        print(f"Group {index}")
        if int(index) == 1:
            for question in questions:
                query = question['question']
                image = [f'/home/albert/multimodal-rsch-master/multimodal-rsch/dataset_images/{image_map[int(index)]}.png']
                print("Index: ", index)
                print(query)
                
                
                        
                with torch.autocast(device_type='cuda', dtype=torch.float16):
                    response, _ = model.chat(tokenizer, query, image, do_sample=False, num_beams=3, use_meta=True)
                print(response)
                
                question['internlm'] = response
except Exception:
    pass            

with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)




