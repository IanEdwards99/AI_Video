from openai import OpenAI
import urllib.request
import requests
from pathlib import Path
import create_video

client = OpenAI()
STORY_PARTS = 15
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

# User input
input_story = (
    "Tell the history of a sentient humanoid cat empire evolving from tribal to medieval to modern to sci-fi technology. "
    "No humans exist. Include conflict with fascist hedgehogs and communist dogs. Focus on broad conflicts and progression of the cat race."
)

# Helper Functions
def extract_prompts(text, length=5):
    """Extracts image and audio prompts from generated story parts text."""
    prompts = []
    for _ in range(length):
        try:
            image_prompt = (text[text.find("Image Prompt: ") + 14:text.find("###")]).strip()
            text = text[text.find("###") + 3:]
            audio_prompt = (text[text.find("Audio: ") + 7:text.find("###")]).strip()
            text = text[text.find("###") + 3:]
            prompts.append((image_prompt, audio_prompt))
        except Exception as e:
            print(f"Prompt extraction error: {e}")
            break
    return prompts[:length]

def generate_story_parts(input_story, style_guide, story_parts=5):
    """Generates story parts with visual and audio prompts for each part."""
    messages = [
        {"role": "system", "content": "You are a story creator, generating an engaging narrative with visual and audio prompts. Avoid cliches."},
        {"role": "assistant", "content": f"Write a story about {input_story} with emotional depth and a consistent narrative arc."},
        {"role": "user", "content": f"Write the entire story in {story_parts} parts, focusing on plot progression."},
        {"role": "assistant", "content": (
            f"Generate {story_parts} distinct story parts. Each should include: "
            "1) An image generation prompt starting with 'Image Prompt: '. Keep art style, time period, and environment consistent across prompts. "
            "2) A storytelling audio prompt starting with 'Audio: '. Use '###' to mark the end of each prompt. "
            "Example format: Part 1\nImage Prompt: A large frog.###\nAudio: Sitting quietly on a lily pad was a large frog named Joe.###"
        )}
    ]
    completion = client.chat.completions.create(model="gpt-4-turbo", messages=messages)

    # Append results for further refinement
    messages.append({"role": "assistant", "content": "Generated prompts: " + completion.choices[0].message.content})
    messages.append({
        "role": "user",
        "content": (
            f"Refine these prompts to maintain thematic and stylistic consistency. "
            f"The story is about: {input_story}. Maintain consistency in style as per: {style_guide}. "
            "Ensure all image prompts and audio retain consistent details. Keep the format exactly the same."
        )
    })
    completion = client.chat.completions.create(model="gpt-4-turbo", messages=messages)

    return extract_prompts(completion.choices[0].message.content, story_parts)

def generate_style_guide(input_story):
    """Generates a style guide for the image prompts based on the story context."""
    messages = [
        {"role": "user", "content": (
            f"Describe an image art style for the story '{input_story}', similar to digital paintings with soft lighting, warm tones, "
            "soft shadows, impressionistic brushstrokes, and detailed creatures. Specify depicted elements (e.g., cats, dogs) and exclusions (e.g., humans). "
            "Provide a succinct style summary."
        )}
    ]
    completion = client.chat.completions.create(model="gpt-4-turbo", messages=messages)
    return completion.choices[0].message.content

def download_image(url, filename):
    """Downloads an image from a URL to a local file."""
    try:
        response = requests.get(url, allow_redirects=True)
        with open(filename, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Image download failed for {filename}: {e}")

def download_audio(audio_text, filename):
    """Generates and downloads audio from given text."""
    try:
        response = client.audio.speech.create(model="tts-1-hd", voice="fable", input=audio_text)
        response.stream_to_file(filename)
    except Exception as e:
        print(f"Audio generation failed for {filename}: {e}")

#******# Main script #*******#

# Generate a style guide based on the input story
style_guide = generate_style_guide(input_story)
print("Generated Style Guide:\n", style_guide)

# Generate story parts with image and audio prompts
prompts = generate_story_parts(input_story, style_guide, STORY_PARTS)

# Process each story part to generate images and audio
for idx, (image_prompt, audio_prompt) in enumerate(prompts):
    print(f"Processing Part {idx + 1}")
    print(f"Image Prompt: {image_prompt}")
    print(f"Audio Prompt: {audio_prompt}")

    # Generate and download image
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"{style_guide}\nImage Prompt: {image_prompt}",
            size="1024x1024"
        )
        image_url = response.data[0].url
        image_filename = DATA_DIR / f"image_{idx}.png"
        download_image(image_url, image_filename)
    except Exception as e:
        print(f"Image generation failed for Part {idx + 1}: {e}")

    # Generate and download audio
    audio_filename = DATA_DIR / f"audio_{idx}.mp3"
    download_audio(audio_prompt, audio_filename)

# Create video from images and audio
create_video.create_video_from_images_and_audio(STORY_PARTS)

#******# End of Main script #*******#
