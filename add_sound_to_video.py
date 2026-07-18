from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

def add_music_to_video(video_path, audio_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    video_duration = video.duration

    if audio.duration < video_duration:
        loop_count = int(video_duration // audio.duration) + 1
        audio_clips = [audio] * loop_count
        audio = concatenate_audioclips(audio_clips)

    audio = audio.subclip(0, video_duration)

    video = video.set_audio(audio)

    video.write_videofile(output_path, codec='libx264', audio_codec='aac')

video_path = 'video.mp4'
audio_path = 'audio.mp3'
output_path = 'output_add_sound_video.mp4'

# Chạy hàm
add_music_to_video(video_path, audio_path, output_path)
