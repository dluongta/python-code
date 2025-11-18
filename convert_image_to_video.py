from moviepy.editor import ImageClip, AudioFileClip

image = "main.png"
audio = "electro_track.mp3"

clip = ImageClip(image, duration=8)
audio_clip = AudioFileClip(audio).subclip(0, 8)

final = clip.set_audio(audio_clip)
final.write_videofile("output_video_with_music.mp4", fps=30, codec="libx264")
