from PIL import Image
import os

for img_path in os.listdir("/home/albert/multimodal-rsch-master/multimodal-rsch/network-pictures"):
    img = os.path.join('/home/albert/multimodal-rsch-master/multimodal-rsch/network-pictures/', img_path)
    img_rgba = Image.open(img)
    img_rgb = img_rgba.convert("RGB")
    img_rgb.save(os.path.join('/home/albert/multimodal-rsch-master/multimodal-rsch/dataset_images/', img_path))