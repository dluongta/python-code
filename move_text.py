from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# --- Mở video gốc ---
video = VideoFileClip("video1.mp4")
width, height = video.w, video.h
duration = video.duration

# --- Nội dung chữ ---
text = """
Đạo diễn: A

Diễn viên chính:
- B
- C
- D

Sản xuất: Công ty ABC

Cảm ơn bạn đã theo dõi!
"""

# --- Tạo ảnh chứa chữ từ Pillow (không dùng ImageMagick) ---
def create_text_image(text, width, font_size=40, font_path=None, text_color="white", bg_color=(0, 0, 0, 0)):
    lines = text.strip().split("\n")
    font = ImageFont.truetype(font_path or "arial.ttf", font_size)

    # Tính chiều cao mỗi dòng
    bbox = font.getbbox("A")
    line_height = bbox[3] - bbox[1] + 10

    # Chiều cao toàn ảnh text
    img_height = line_height * len(lines)

    # Tạo ảnh RGBA nền trong suốt
    img = Image.new("RGBA", (width, img_height), bg_color)
    draw = ImageDraw.Draw(img)

    y = 0
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, y), line, font=font, fill=text_color)
        y += line_height

    return img

# --- Tạo ảnh chứa chữ ---
text_img = create_text_image(text, width - 100)
text_np = np.array(text_img)

# --- Chuyển ảnh thành clip ---
text_clip = ImageClip(text_np, transparent=True).set_duration(duration)
text_height = text_clip.h

# --- Tạo hiệu ứng chữ chạy dọc từ dưới lên ---
scroll_clip = text_clip.set_position(
    lambda t: ("center", height - (text_height + height) * t / (duration * 0.9))
).set_duration(duration)

# --- Ghép text lên video gốc ---
final = CompositeVideoClip([video, scroll_clip])

# --- Xuất video kết quả ---
final.write_videofile("move_text.mp4", fps=video.fps)
