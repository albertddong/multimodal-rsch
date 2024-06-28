import torch
import requests
from PIL import Image
from transformers import AutoModelForCausalLM, LlamaTokenizer
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()

device = "cuda"
model_name = "THUDM/cogvlm-chat-hf"
tokenizer = LlamaTokenizer.from_pretrained('lmsys/vicuna-7b-v1.5')
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True
).to(device).eval()

# Define the request model
class GenerateRequest(BaseModel):
    prompt: str
    image: str
    

# chat example
"""
image = Image.open("/home/albert/llava-git/simple_1.png").convert('RGB')
inputs = model.build_conversation_input_ids(tokenizer, query=query, history=[], images=[image])  # chat mode
inputs = {
    'input_ids': inputs['input_ids'].unsqueeze(0).to('cuda'),
    'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to('cuda'),
    'attention_mask': inputs['attention_mask'].unsqueeze(0).to('cuda'),
    'images': [[inputs['images'][0].to('cuda').to(torch.bfloat16)]],
}


question = "Considering the setup shown, explain how data might flow from the Web Server Windows 2003 to the Media PC, detailing any intermediate devices or networks it must pass through."
image_path = "/home/albert/llava-git/simple_1.png"
"""
def get_input(input_question, image_path):
    query = f"You are an assistant who perfectly describes images. Please answer the question in detail. {input_question}"
    image = Image.open(image_path).convert('RGB')

    inputs = model.build_conversation_input_ids(tokenizer, query=query, history=[], images=[image])  # chat mode
    inputs = {
    'input_ids': inputs['input_ids'].unsqueeze(0).to('cuda'),
    'token_type_ids': inputs['token_type_ids'].unsqueeze(0).to('cuda'),
    'attention_mask': inputs['attention_mask'].unsqueeze(0).to('cuda'),
    'images': [[inputs['images'][0].to('cuda').to(torch.bfloat16)]],
    }
    return inputs

# Define the generate endpoint
@app.post("/generate")
async def generate_response(query: GenerateRequest):
    try:
        inputs = get_input(query.prompt, query.image)
        gen_kwargs = {"max_length": 2048, "do_sample": False}
        
        with torch.no_grad():
            outputs = model.generate(**inputs, **gen_kwargs)
            outputs = outputs[:, inputs['input_ids'].shape[1]:]
            print(tokenizer.decode(outputs[0]))
            return tokenizer.decode(outputs[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Run the app with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="12.1.52.176", port=8006)