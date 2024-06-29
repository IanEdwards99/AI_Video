from moviepy.editor import AudioFileClip, ImageClip, VideoFileClip, concatenate_videoclips
import glob
import os

def mp3PNGMerge(fileSaveName):
    for i in range(0,4):
        audio_clip = AudioFileClip("audio_" + str(i) + ".mp3")
        image_clip = ImageClip("image_" + str(i))
        video_clip = image_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration
        video_clip.fps = 30
        video_clip.write_videofile(fileSaveName + str(i) + '_CLIP.mp4')

mp3PNGMerge('try')

video_files_path = os.getcwd()

video_file_list = ["try0_CLIP.mp4", "try1_CLIP.mp4", "try2_CLIP.mp4","try3_CLIP.mp4"]

loaded_video_list = []

for video in video_file_list:
    print(f"Adding video file:{video}")
    loaded_video_list.append(VideoFileClip(video))

final_clip = concatenate_videoclips(loaded_video_list)

merged_video_name = "final"

final_clip.write_videofile(merged_video_name + ".mp4", fps=30, threads = 1, codec="libx264")