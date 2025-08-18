from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path, output_audio_path):
    # Load the video file
    video = VideoFileClip(video_path)

    # Extract audio
    audio = video.audio

    # Write the audio to a file
    audio.write_audiofile(output_audio_path)

    # Close the video and audio clips
    audio.close()
    video.close()

# Path to the video file and desired output audio file
video_path = 'output_add_sound_video.mp4'   # Change this to your video file path
output_audio_path = 'output_sound_audio.mp3'  # Desired output audio file path

# Call the function
extract_audio_from_video(video_path, output_audio_path)
