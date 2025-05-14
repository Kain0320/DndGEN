import requests
import base64
from io import BytesIO
from PIL import Image

def generate_character_image(prompt, save_path="/Users/user/DNDGEN/DndGEN/dnd/portraits/portraits.png"):
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 512,
        "height": 768,
        "sampler_index": "Euler a",
        "cfg_scale": 7.5,
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        r = response.json()

        image_data = base64.b64decode(r['images'][0])
        image = Image.open(BytesIO(image_data))
        image.save(save_path)
        print(f"🖼️ Obrázek uložen do {save_path}")
        return save_path
    except Exception as e:
        print(f"❌ Chyba při generování obrázku: {e}")
        return None
    
prompt = "portrait of a red dragonborn sorcerer, fantasy art, detailed, dramatic lighting"
img_path = generate_character_image(prompt)