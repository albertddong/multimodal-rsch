import json
import os
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
import torch
import torchvision.transforms as T
from PIL import Image

from torchvision.transforms.functional import InterpolationMode


IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


def build_transform(input_size):
    MEAN, STD = IMAGENET_MEAN, IMAGENET_STD
    transform = T.Compose(
        [
            T.Lambda(lambda img: img.convert("RGB") if img.mode != "RGB" else img),
            T.Resize((input_size, input_size), interpolation=InterpolationMode.BICUBIC),
            T.ToTensor(),
            T.Normalize(mean=MEAN, std=STD),
        ]
    )
    return transform


def find_closest_aspect_ratio(aspect_ratio, target_ratios, width, height, image_size):
    best_ratio_diff = float("inf")
    best_ratio = (1, 1)
    area = width * height
    for ratio in target_ratios:
        target_aspect_ratio = ratio[0] / ratio[1]
        ratio_diff = abs(aspect_ratio - target_aspect_ratio)
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_ratio = ratio
        elif ratio_diff == best_ratio_diff:
            if area > 0.5 * image_size * image_size * ratio[0] * ratio[1]:
                best_ratio = ratio
    return best_ratio


def dynamic_preprocess(
    image, min_num=1, max_num=6, image_size=448, use_thumbnail=False
):
    orig_width, orig_height = image.size
    aspect_ratio = orig_width / orig_height

    # calculate the existing image aspect ratio
    target_ratios = set(
        (i, j)
        for n in range(min_num, max_num + 1)
        for i in range(1, n + 1)
        for j in range(1, n + 1)
        if i * j <= max_num and i * j >= min_num
    )
    target_ratios = sorted(target_ratios, key=lambda x: x[0] * x[1])

    # find the closest aspect ratio to the target
    target_aspect_ratio = find_closest_aspect_ratio(
        aspect_ratio, target_ratios, orig_width, orig_height, image_size
    )

    # calculate the target width and height
    target_width = image_size * target_aspect_ratio[0]
    target_height = image_size * target_aspect_ratio[1]
    blocks = target_aspect_ratio[0] * target_aspect_ratio[1]

    # resize the image
    resized_img = image.resize((target_width, target_height))
    processed_images = []
    for i in range(blocks):
        box = (
            (i % (target_width // image_size)) * image_size,
            (i // (target_width // image_size)) * image_size,
            ((i % (target_width // image_size)) + 1) * image_size,
            ((i // (target_width // image_size)) + 1) * image_size,
        )
        # split the image
        split_img = resized_img.crop(box)
        processed_images.append(split_img)
    assert len(processed_images) == blocks
    if use_thumbnail and len(processed_images) != 1:
        thumbnail_img = image.resize((image_size, image_size))
        processed_images.append(thumbnail_img)
    return processed_images


def load_image(image_file, input_size=448, max_num=6):
    image = Image.open(image_file).convert("RGB")
    transform = build_transform(input_size=input_size)
    images = dynamic_preprocess(
        image, image_size=input_size, use_thumbnail=True, max_num=max_num
    )
    pixel_values = [transform(image) for image in images]
    pixel_values = torch.stack(pixel_values)
    return pixel_values


path = "OpenGVLab/InternVL-Chat-V1-5"
# If you have an 80G A100 GPU, you can put the entire model on a single GPU.
# model = (
#     AutoModel.from_pretrained(
#         path, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True, trust_remote_code=True
#     )
#     .eval()
#     .cuda()
# )
# Otherwise, you need to set device_map='auto' to use multiple GPUs for inference.
model = AutoModel.from_pretrained(
    path,
    torch_dtype=torch.bfloat16,
    low_cpu_mem_usage=True,
    trust_remote_code=True,
    device_map="auto",
).eval()

tokenizer = AutoTokenizer.from_pretrained(path, trust_remote_code=True)
# set the max number of tiles in max_num
generation_config = dict(
    num_beams=1,
    max_new_tokens=250,
    do_sample=False,
)


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()


class SummarizeVidsRequest(BaseModel):
    prompt: str
    frames: List[str]


@app.post("/summarize_video/")
async def summarize_vids(request: SummarizeVidsRequest):
    # Placeholder for your summarization logic
    prompt = request.prompt
    frames = request.frames

    # Here you would process the frames and generate the summary based on the prompt
    # For demonstration, let's just return the received data

    # multi-round multi-image conversation
    pixel_values1 = load_image(frames[0], max_num=6).to(torch.bfloat16).cuda()
    pixel_values2 = load_image(frames[1], max_num=6).to(torch.bfloat16).cuda()
    pixel_values3 = load_image(
        load_image(frames[2], max_num=6).to(torch.bfloat16).cuda()
    )
    pixel_values4 = load_image(
        load_image(frames[3], max_num=6).to(torch.bfloat16).cuda()
    )
    pixel_values = torch.cat(
        (
            pixel_values1,
            pixel_values2,
            pixel_values3,
            pixel_values4,
        ),
        dim=0,
    )

    question = prompt
    response = model.chat(
        tokenizer,
        pixel_values,
        question,
        generation_config,
        history=None,
        return_history=False,
    )
    print(question, response)

    return response


class QueryImageRequest(BaseModel):
    prompt: str
    img: str


@app.post("/single_query/")
async def summarize_vids(request: QueryImageRequest):
    # Placeholder for your summarization logic
    prompt = request.prompt
    frame = request.img

    # Here you would process the frames and generate the summary based on the prompt
    # For demonstration, let's just return the received data

    # multi-round multi-image conversation
    pixel_values = load_image(frame, max_num=6).to(torch.bfloat16).cuda()

    question = prompt
    response = model.chat(
        tokenizer,
        pixel_values,
        question,
        generation_config,
        history=None,
        return_history=False,
    )
    print(question, response)

    return response


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)