import torch
from transformers import AutoModel, AutoTokenizer

torch.set_grad_enabled(False)

# init model and tokenizer
model = AutoModel.from_pretrained('internlm/internlm-xcomposer2d5-7b', torch_dtype=torch.bfloat16, trust_remote_code=True).cuda().eval()
tokenizer = AutoTokenizer.from_pretrained('internlm/internlm-xcomposer2d5-7b', trust_remote_code=True)
model.tokenizer = tokenizer

query = ''
image = ['/home/albert/multimodal-rsch-master/multimodal-rsch/network-pictures/valid_05.png']
with torch.autocast(device_type='cuda', dtype=torch.float16):
    response, _ = model.chat(tokenizer, query, image, do_sample=False, num_beams=3, use_meta=True)
print(response)
#The infographic is a visual representation of various facts about Dubai. It begins with a statement about Palm Jumeirah, highlighting it as the largest artificial island visible from space. It then provides a historical context, noting that in 1968, there were only a few cars in Dubai, contrasting this with the current figure of more than 1.5 million vehicles. 
#The infographic also points out that Dubai has the world's largest Gold Chain, with 7 of the top 10 tallest hotels located there. Additionally, it mentions that the crime rate is near 0%, and the income tax rate is also 0%, with 20% of the world's total cranes operating in Dubai. Furthermore, it states that 17% of the population is Emirati, and 83% are immigrants.
#The Dubai Mall is highlighted as the largest shopping mall in the world, with 1200 stores. The infographic also notes that Dubai has no standard address system, with no zip codes, area codes, or postal services. It mentions that the Burj Khalifa is so tall that its residents on top floors need to wait longer to break fast during Ramadan. 
#The infographic also includes information about Dubai's climate-controlled City, with the Royal Suite at Burj Al Arab costing $24,000 per night. Lastly, it notes that the net worth of the four listed billionaires is roughly equal to the GDP of Honduras.