from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips
import glob
from pathlib import Path
import os

RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def mp3PNGMerge(STORY_PARTS: int, fileSaveName: Path):
    base_filename = fileSaveName.stem  # Extract base name without extension
    save_directory = fileSaveName.parent
    for i in range(0, STORY_PARTS):
        audio_file = DATA_DIR / f"audio_{i}.mp3"
        image_file = DATA_DIR / f"image_{i}.png"
        if not audio_file.exists() or not image_file.exists():
            print(f"Error: Missing file: {audio_file} or {image_file}")
            continue
        
        audio_clip = AudioFileClip(str(audio_file))
        image_clip = ImageClip(str(image_file))
        video_clip = image_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.fps = 20
        video_clip.write_videofile(str(save_directory / f"{base_filename}{i}_CLIP.mp4"))



def create_video_from_images_and_audio(number_of_story_parts: int):
    mp3PNGMerge(number_of_story_parts, DATA_DIR / "try")

    video_file_list = [DATA_DIR / f"try{i}_CLIP.mp4" for i in range(0, number_of_story_parts)]

    loaded_video_list = []
    for video in video_file_list:
        print(f"Adding video file: {video}")
        if video.exists():
            loaded_video_list.append(VideoFileClip(str(video)))
        else:
            print(f"Warning: File {video} does not exist.")
    
    if not loaded_video_list:
        print("Error: No video files to concatenate.")
        return

    final_clip = concatenate_videoclips(loaded_video_list)

    merged_video_name = RESULTS_DIR / "final"
    final_clip.write_videofile(str(merged_video_name) + ".mp4", fps=20, threads=1, codec="libx264")
    final_clip.close()  # Free memory after rendering
