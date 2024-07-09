import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
ckpt_path = "internlm/internlm-xcomposer2d5-7b"
tokenizer = AutoTokenizer.from_pretrained(ckpt_path, trust_remote_code=True).cuda()
# Set `torch_dtype=torch.floatb16` to load model in bfloat16, otherwise it will be loaded as float32 and might cause OOM Error.
model = AutoModelForCausalLM.from_pretrained(
    ckpt_path, torch_dtype=torch.bfloat16, trust_remote_code=True).cuda()
model = model.eval()