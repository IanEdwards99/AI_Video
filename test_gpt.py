from openai import OpenAI
import urllib.request
import requests
from pathlib import Path
client = OpenAI()

def extract_image_prompt(input, length=4):
    prompts = []
    for i in range(0,length):
        prompts.append((input[input.find("Prompt:")+7:input.find("###")]).strip())
        input = input[input.find("###")+3:]
    if (len(prompts) > length):
        raise Exception("Prompt list too long!") 
    return prompts

def extract_audio_prompt(input, length=4):
    audio_prompts = []
    for i in range(0,length):
        audio_prompts.append((input[input.find("!!!")+3:input.find("###")]).strip())
        input = input[input.find("###")+3:]
    if (len(audio_prompts) > length):
        raise Exception("Prompt list too long!") 
    return audio_prompts

messages=[
    {"role": "system", "content": "You are a content creator for short stories with audio overlayed on images."},
    {"role": "assistant", "content": "You will create a sci-fi short story that can be told with images and audio. The story should be clear and interesting to follow. Take your time, and follow a writer's process in which you make a draft, review it and create a final masterpiece."},
    {"role": "user", "content": "Write a sci-fi short story that can be used as the plot for an instagram reel. First write a draft story in your head without telling me, review it and produce a final interesting short story. Do NOT output anything. Keep the final story in your head."},
    {"role": "assistant", "content": "Summarize the story into 8 main parts and keep this information in your head, do NOT output this summary."},
    {"role": "user", "content": "Create an image generation prompt for each of the 8 main parts you just summarized. Display each prompt on a separate line, starting with: 'Prompt:'. Indicate the end of each prompt with ###"}
]

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages = messages
)

# print(completion.choices[0].message.content)

image_prompts = extract_image_prompt(completion.choices[0].message.content, 8)
image_prompts = list(filter(None, image_prompts))

print(image_prompts)

messages.append({"role": "assistant", "content": "You just generated these descriptions: " + completion.choices[0].message.content})
messages.append({"role": "user", "content": "Tell the story behind each image prompt. Start each image prompt's story with !!! and end each with ###"})

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=messages
)


# print(completion.choices[0].message.content)

audio_prompts = extract_audio_prompt(completion.choices[0].message.content, 8)
audio_prompts = list(filter(None, audio_prompts))
print(audio_prompts)

val = 0
scenes = []
for i in image_prompts:
    response = client.images.generate(
    model="dall-e-3",
    prompt=i,
    size="1024x1024",
    quality="standard",
    n=1,
    )

    image_url = response.data[0].url
    filename = "image_" + str(val)
    r = requests.get(image_url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    print(image_url)
    
    audio_file_name = "audio_" + str(val) + ".mp3"
    speech_file_path = Path(__file__).parent / audio_file_name
    response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=audio_prompts[val]
    )

    response.stream_to_file(speech_file_path)

    scenes.append((filename, audio_file_name))
    val += 1