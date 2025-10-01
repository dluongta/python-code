from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1280, 720
FONT_PATH = "C:/Windows/Fonts/arial.ttf"

# ===== Vẽ chữ thường (LU đỏ, MIND xám) =====
def create_lumind_image(fontsize, bg_color=(255, 255, 255)):
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, fontsize)

    text1, text2 = "LU", "MIND"
    bbox1 = draw.textbbox((0, 0), text1, font=font)
    bbox2 = draw.textbbox((0, 0), text2, font=font)
    total_w = (bbox1[2]-bbox1[0]) + (bbox2[2]-bbox2[0])
    x = (W - total_w) // 2
    y = (H - (bbox1[3]-bbox1[1]) - fontsize*0.5) // 2

    draw.text((x, y), text1, font=font, fill=(139, 0, 0))   # đỏ sẫm
    draw.text((x+(bbox1[2]-bbox1[0]), y), text2, font=font, fill=(85, 85, 85))  # xám
    return np.array(img)

# ===== Vẽ chữ đỏ có viền trắng trên nền đỏ =====
def create_lumind_outline(fontsize, bg_color=(200, 0, 0)):
    img = Image.new("RGB", (W, H), bg_color)  # nền đỏ
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, fontsize)

    text = "LUMIND"
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (W - (bbox[2]-bbox[0])) // 2
    y = (H - (bbox[3]-bbox[1]) - fontsize*0.5) // 2

    border = 12  # độ dày viền trắng
    for dx in range(-border, border+1):
        for dy in range(-border, border+1):
            if dx*dx + dy*dy <= border*border:
                draw.text((x+dx, y+dy), text, font=font, fill=(255, 255, 255))

    # Vẽ chữ đỏ bên trong
    draw.text((x, y), text, font=font, fill=(200, 0, 0))
    return np.array(img)

# ===== Stage 1: Logo phóng to dần =====
def make_scale_sequence():
    scales = [1.0, 1.3, 1.6, 1.9, 2.2]
    clips = []
    for s in scales:
        fontsize = int(120 * s)
        if s == 2.2:
            img = create_lumind_outline(fontsize)  # chữ đỏ viền trắng trên nền đỏ
        else:
            img = create_lumind_image(fontsize)    # chữ thường
        clips.append(ImageClip(img).set_duration(0.6))
    return concatenate_videoclips(clips)

# ===== Stage 2: Flash trắng =====
def make_flash_white():
    return ColorClip(size=(W, H), color=(255, 255, 255), duration=0.5)

# ===== Stage 3: Logo cuối + pixel reveal phụ đề =====
def make_final_logo_with_subtitle():
    bg = ColorClip(size=(W, H), color=(255, 255, 255), duration=3)
    logo_img = create_lumind_image(200)
    logo_clip = ImageClip(logo_img).set_duration(3)

    def subtitle_img():
        img = Image.new("RGB", (W, 100), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(FONT_PATH, 60)
        text = "DLUONGTA - LUONG MIND"
        bbox = draw.textbbox((0, 0), text, font=font)
        x = (W - (bbox[2]-bbox[0])) // 2
        draw.text((x, 10), text, font=font, fill=(139, 0, 0))
        return np.array(img)

    subtitle_static = ImageClip(subtitle_img()).set_duration(3)

    def pixel_mask(t):
        mask = np.zeros((100, W), dtype=np.uint8)
        reveal_cols = int((t/3) * W)
        if reveal_cols > 0:
            mask[:, :reveal_cols] = 255
        return mask[:, :, None]

    subtitle = subtitle_static.set_mask(VideoClip(pixel_mask, duration=3).to_mask())
    subtitle = subtitle.set_position(("center", H//2+80))
    return CompositeVideoClip([bg, logo_clip, subtitle])

# ===== Ghép toàn bộ =====
def create_full_intro():
    stage1 = make_scale_sequence()
    stage2 = make_flash_white()
    stage3 = make_final_logo_with_subtitle()
    final = concatenate_videoclips([stage1, stage2, stage3])
    final.write_videofile("lumind_intro.mp4", fps=120)

if __name__ == "__main__":
    create_full_intro()
