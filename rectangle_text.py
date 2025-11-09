from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# --- Cấu hình ---
W, H = 1280, 720
FONT_PATH = "C:/Windows/Fonts/arial.ttf"
TEXT = "HELLO WORLD"
RECT_COLOR = (200, 200, 200)  # Màu rectangle
BG_COLOR = (255, 255, 255)    # Nền trắng
TEXT_COLOR = (0, 0, 0)        # Chữ đen
ANIM_DURATION = 5             # thời gian animation rectangle
PAUSE_DURATION = 0.5            # thời gian giữ cuối
TOTAL_DURATION = ANIM_DURATION + PAUSE_DURATION

# --- Tạo hình chữ ---
def create_text_image():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 100)
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((W - w)//2, (H - h)//2), TEXT, font=font, fill=TEXT_COLOR)
    return np.array(img)

# --- Layer rectangle che chữ bằng mask ---
def rectangle_mask(t):
    """
    Trả về mask 2D float [0,1], 0 = trong suốt, 1 = che
    """
    progress = min(t / ANIM_DURATION, 1)  # chỉ animate trong ANIM_DURATION
    current_h = int(H/2 * (1 - progress))
    mask = np.ones((H, W), dtype=float)
    center_y = H // 2
    mask[center_y - current_h:center_y + current_h, :] = 0
    return mask

# --- VideoClip mask ---
mask_clip = VideoClip(make_frame=rectangle_mask, duration=TOTAL_DURATION)
mask_clip = mask_clip.set_fps(30)
mask_clip = mask_clip.set_ismask(True)

# --- Rectangle clip ---
rect_clip = ColorClip(size=(W,H), color=RECT_COLOR, duration=TOTAL_DURATION)
rect_clip = rect_clip.set_mask(mask_clip)

# --- Text clip ---
text_clip = ImageClip(create_text_image()).set_duration(TOTAL_DURATION)

# --- Composite ---
final = CompositeVideoClip([text_clip, rect_clip])
final.write_videofile("rectangle_text.mp4", fps=30)
