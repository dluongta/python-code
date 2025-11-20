from moviepy.editor import VideoFileClip

input_gif = "output.gif"
output_mp4 = "outputVideoConvert.mp4"

clip = VideoFileClip(input_gif)

clip.write_videofile(
    output_mp4,
    codec="libx264",
    fps=24,
    bitrate="2000k"
)
