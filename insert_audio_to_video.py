from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips

def insert_audio_to_video(video_path, audio_path, output_path):
    # Load video và audio
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Nếu audio ngắn hơn video → lặp lại audio
    if audio.duration < video.duration:
        # Số lần cần lặp
        repeat_count = int(video.duration // audio.duration) + 1
        audio_loop = concatenate_audioclips([audio] * repeat_count)
    else:
        audio_loop = audio

    # Cắt audio đúng bằng thời lượng video
    final_audio = audio_loop.subclip(0, video.duration)

    # Gán audio mới vào video
    final_video = video.set_audio(final_audio)

    # Xuất video mới
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print("✅ Video đã được chèn nhạc thành công.")

insert_audio_to_video("v.webm", "RemixMusic.mp3", "video_with_audio.mp4")
