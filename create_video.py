from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips
import glob
import os

def mp3PNGMerge(STORY_PARTS, fileSaveName):
    for i in range(0,STORY_PARTS):
        audio_clip = AudioFileClip("data/audio_" + str(i) + ".mp3")
        image_clip = ImageClip("data/image_" + str(i))
        video_clip = image_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.fps = 20
        video_clip.write_videofile(fileSaveName + str(i) + '_CLIP.mp4')

def create_video_from_images_and_audio(number_of_story_parts):
    mp3PNGMerge(number_of_story_parts, 'data/try')

    video_files_path = os.getcwd()

    video_file_list = ["data/try" + str(i) + "_CLIP.mp4" for i in range(0,number_of_story_parts)]

    loaded_video_list = []

    for video in video_file_list:
        print(f"Adding video file:{video}")
        loaded_video_list.append(VideoFileClip(video))

    final_clip = concatenate_videoclips(loaded_video_list)

    merged_video_name = "result/final"

    final_clip.write_videofile(merged_video_name + ".mp4", fps=20, threads = 1, codec="libx264")