from moviepy.editor import VideoFileClip

clip = VideoFileClip("input.mp4")
w, h = clip.size

width, height = 640, 360
x = (w - width) // 2
y = (h - height) // 2   


cropped = clip.crop(x1=x, y1=y, x2=x + width, y2=y + height)

cropped.write_videofile("output_cropped.mp4", fps=clip.fps)
