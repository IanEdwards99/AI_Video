import argparse
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx import all as afx
from moviepy.editor import CompositeAudioClip

# Set up the argument parser
def parse_args():
    parser = argparse.ArgumentParser(description="Add music to a video and loop it.")
    parser.add_argument("--vid", help="Path to the video file", required=True)
    parser.add_argument("--aud", help="Path to the audio file", required=True)
    parser.add_argument("-v", "--volume", type=float, default=1.0, help="Volume adjustment (default is 1.0)")
    return parser.parse_args()

def main():
    # Parse the command-line arguments
    args = parse_args()

    # Load the video and audio files
    video = VideoFileClip(args.vid)
    audio = AudioFileClip(args.aud)

    # Loop the audio to fit the video duration
    loop_count = int(video.duration // audio.duration) + 1
    audio = afx.audio_loop(audio, nloops=loop_count)

    # Cut the audio to match the length of the video
    audio = audio.subclip(0, video.duration)

    # Adjust the volume of the audio
    audio = audio.volumex(args.volume)

    # Get the original audio from the video
    original_audio = video.audio

    # Combine the original audio and the new audio into a composite
    final_audio = CompositeAudioClip([original_audio, audio])

    # Set the combined audio to the video
    video = video.set_audio(final_audio)

    # Output the final video
    video.write_videofile("output_video_with_overlay_music.mp4", codec="libx264", audio_codec="aac")

if __name__ == "__main__":
    main()
