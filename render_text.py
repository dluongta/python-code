import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

width, height = 1920, 1080
fps = 30
duration = 8
anim_ratio = 0.6
delay_ratio = 0.1
delay_frames = int(fps * duration * delay_ratio)
anim_frames = int(fps * duration * (anim_ratio - delay_ratio))
hold_frames = int(fps * duration * (1 - anim_ratio))
frames = delay_frames + anim_frames + hold_frames

white = (255, 255, 255)
dark_red = (0, 0, 139)
gray = (128, 128, 128)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('lumind_animation.mp4', fourcc, fps, (width, height))

font_path = "C:/Windows/Fonts/arial.ttf"
font_size = 300
font = ImageFont.truetype(font_path, font_size)

text1, text2 = "LU", "MIND"
dummy = Image.new("RGB", (width, height), (255, 255, 255))
d = ImageDraw.Draw(dummy)
b1, b2 = d.textbbox((0, 0), text1, font=font), d.textbbox((0, 0), text2, font=font)
w1, h1 = b1[2]-b1[0], b1[3]-b1[1]
w2, h2 = b2[2]-b2[0], b2[3]-b2[1]
gap = 30
total = w1 + gap + w2
x0 = (width - total) // 2
y0 = height // 2 + h1 // 2
rect_max_height = h1 + 90
start_y_top = y0 - h1 - 30

for i in range(frames):
    img = Image.new("RGB", (width, height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((x0, y0 - h1), text1, font=font, fill=(dark_red[2], dark_red[1], dark_red[0]))
    d.text((x0 + w1 + gap, y0 - h2), text2, font=font, fill=(gray[2], gray[1], gray[0]))

    if i < delay_frames:
        progress = 0
    elif i < delay_frames + anim_frames:
        progress = (i - delay_frames) / anim_frames
    else:
        progress = 1

    rect_height = int(rect_max_height * progress)

    if rect_height > 0:
        d.rectangle((x0, start_y_top, x0 + w1, start_y_top + rect_height), fill=(dark_red[2], dark_red[1], dark_red[0]))
        d.rectangle((x0 + w1 + gap, start_y_top, x0 + w1 + gap + w2, start_y_top + rect_height), fill=(gray[2], gray[1], gray[0]))

    out.write(cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR))

out.release()
print("Video 'lumind_animation.mp4' created")
