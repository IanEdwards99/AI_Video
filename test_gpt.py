from openai import OpenAI
import urllib.request
import requests
from pathlib import Path
import create_video
client = OpenAI()

STORY_PARTS = 20

input_story = "a world in which animals evolved to be sentient. No humans exist. Describe the story of cats evolving from primal cats to a medieval society of cats. Include a central cat figure to cat history that was crucial to uniting cat kingdoms. Include some details about warfare against dogs. Make it a cliff hanger ending about the possible fall of the cat kingdom due to dog invasions. Keep it medieval with swords, bows and magic."

def extract_prompts(input, length=4):
    prompts = []
    for i in range(0, length):
        image_prompt = (input[input.find("Image Prompt: ") + 14:input.find("###")]).strip()
        input = input[input.find("###")+3:]
        audio_prompt = (input[input.find("Audio: ") + 7:input.find("###")]).strip()  # Adjusted for audio prompt being storytelling
        input = input[input.find("###")+3:]
        prompts.append((image_prompt, audio_prompt))
    return prompts[:length]

messages=[
    {"role": "system", "content": "You are a story creator, generating an interesting exciting narrative with corresponding visual and audio prompts. Avoid cliches."},
    {"role": "assistant", "content": "Write a story about " + input_story + "that flows naturally, adding emotional depth and maintaining a consistent narrative arc."},
    {"role": "user", "content": "Write the entire story with a beginning, middle, and end. Focus on emotional moments and plot progression."},
    {"role": "assistant", "content": "Now split the story into " + str(STORY_PARTS) + " parts. Each part should flow narratively. Make sure there are 20 distinct parts."},
    {"role": "user", "content": "For each part (" + str(STORY_PARTS) + " parts), generate two things: First, an image generation prompt starting with 'Image Prompt: '. Make sure the image generation prompt keeps the same art style as the rest of the image prompts, and any characters created remain consistent in appearance in subsequent images. Ensure the images reflect the time period and technology of the story. Keep in mind the entire narrative when creating the image. Secondly, create the story text as the audio starting with 'Audio: '. Mark the end of the 'Image Prompt: ' part with '###' and mark the end of the 'Audio: ' part with '###'. Do not add any extra formatting or tags. Here is an example of the desired output: Part 1\nImage Prompt: A large frog.###\nAudio: Sitting quietly on a lily pad was a large frog called Joe.###"}
]

completion = client.chat.completions.create(
  model="gpt-4-turbo",
  messages = messages
)

print(completion.choices[0].message.content)

prompts = extract_prompts(completion.choices[0].message.content, STORY_PARTS)

for idx, (image, audio) in enumerate(prompts):
    print(f"Part {idx+1} Image Prompt: {image}")
    print(f"Part {idx+1} Storytelling (Audio): {audio}")

scenes = []
for idx, (image_prompt, audio_prompt) in enumerate(prompts):
    response = client.images.generate(
    model="dall-e-3",
    prompt=image_prompt,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    filename = "data/image_" + str(idx)
    r = requests.get(image_url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    
    audio_file_name = "data/audio_" + str(idx) + ".mp3"
    speech_file_path = audio_file_name
    response = client.audio.speech.create(
    model="tts-1-hd",
    voice="fable",
    input=audio_prompt
    )

    response.stream_to_file(speech_file_path)

print("-----------------------------------------\nGenerating video from images and audio:\n-----------------------------------------")
create_video.create_video_from_images_and_audio(STORY_PARTS)