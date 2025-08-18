from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

def add_music_to_video(video_path, audio_path, output_path):
    # Tải video và audio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Tính toán thời gian video
    video_duration = video.duration

    # Lặp lại nhạc để khớp với video
    if audio.duration < video_duration:
        loop_count = int(video_duration // audio.duration) + 1
        audio_clips = [audio] * loop_count
        audio = concatenate_audioclips(audio_clips)

    # Cắt âm thanh để khớp với độ dài video
    audio = audio.subclip(0, video_duration)

    # Gán âm thanh cho video
    video = video.set_audio(audio)

    # Xuất video mới
    video.write_videofile(output_path, codec='libx264', audio_codec='aac')

# Đường dẫn đến video và âm thanh
video_path = 'input.mp4'
audio_path = 'sound.mp3'
output_path = 'output_add_sound_video.mp4'

# Chạy hàm
add_music_to_video(video_path, audio_path, output_path)
