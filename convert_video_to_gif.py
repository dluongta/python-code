from moviepy.editor import VideoFileClip

input_video = "outputVideo.mp4"
output_gif = "output.gif"

clip = VideoFileClip(input_video)

clip.write_gif(output_gif, fps=30)
