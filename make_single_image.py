from openai import OpenAI
import urllib.request
import requests
from pathlib import Path
import create_video
import re

client = OpenAI()
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# User input
input_story = ( 
    "Generate me a thumbnail for a video about an adult girl exploring a catan universe. Keep it simple, with just her, dressed like an adventurer. She is a fit, slim, strong african girl with light black skin, long black wirey curly hair and forehead curls and a big smile adventuring in the catan universe."
)

style_guide = (
    "Style guide for the image: Cute anime style. Picture book. Soft lighting. Warm tones. Simple colors. Soft shadows. Japanese. Picture cutout style."
    " Include Catan resource types as the backgrounds: Wheat from wheat fields, clay from quarries, stone from mountains, wood from forests and sheep from farms."
)

def generate_save_image(prompt=input_story):
    # Generate and download image
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Image style: {style_guide}\nImage Prompt: {prompt}",
            size="1024x1024"
        )
        image_url = response.data[0].url
        image_filename = DATA_DIR / f"thumbnail.png"

        """Downloads an image from a URL to a local file."""
        response = requests.get(image_url, allow_redirects=True)
        with open(image_filename, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Image generation failed for {image_filename}: {e}")

generate_save_image()



