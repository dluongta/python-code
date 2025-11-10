from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# --- Cấu hình ---
W, H = 1280, 720
FONT_PATH = "C:/Windows/Fonts/arial.ttf"
TEXT = "DLUONGTA - LUONG MIND"

RECT_COLOR = (255, 255, 255)      # Hình chữ nhật màu trắng
BG_COLOR = (139, 0, 0)            # Nền đỏ sẫm (dark red)
TEXT_COLOR = (255, 165, 0)        # Chữ màu cam

ANIM_DURATION = 5                 # Thời gian animation
EXTRA_HOLD = 2                    # Giữ thêm sau khi hiện xong
TOTAL_DURATION = ANIM_DURATION + EXTRA_HOLD

# --- Tạo hình chữ và lấy vị trí ---
def create_text_image():
    img = Image.new("RGB", (W, H), BG_COLOR)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 120)
    bbox = draw.textbbox((0, 0), TEXT, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (W - text_w) // 2
    text_y = (H - text_h) // 2
    draw.text((text_x, text_y), TEXT, font=font, fill=TEXT_COLOR)
    return np.array(img), (text_x, text_y, text_w, text_h)

# --- Tạo hình chữ ---
text_img, (text_x, text_y, text_w, text_h) = create_text_image()

# --- Mask động cho rectangle ---
def rectangle_mask(t):
    """
    Mask 2D float [0,1], 0 = trong suốt, 1 = che.
    Hình chữ nhật xuất hiện từ dưới lên che chữ (vượt quá chữ một chút).
    """
    progress = min(t / ANIM_DURATION, 1)
    # Chiều cao chữ + margin để đi quá chữ một chút
    total_h = text_h + 32  
    visible_height = int(total_h * progress)
    mask = np.ones((H, W), dtype=float)
    y2 = text_y + text_h + 40   # điểm đáy hơi vượt chữ
    y1 = y2 - visible_height
    mask[y1:y2, text_x:text_x + text_w] = 0
    return mask

# --- Tạo mask clip ---
mask_clip = VideoClip(make_frame=rectangle_mask, duration=TOTAL_DURATION)
mask_clip = mask_clip.set_fps(30).set_ismask(True)

# --- Tạo rectangle clip ---
rect_clip = ColorClip(size=(W, H), color=RECT_COLOR, duration=TOTAL_DURATION)
rect_clip = rect_clip.set_mask(mask_clip)

# --- Tạo clip chữ ---
text_clip = ImageClip(text_img).set_duration(TOTAL_DURATION)

# --- Gộp lại ---
final = CompositeVideoClip([text_clip, rect_clip])
final.write_videofile("rectangle_text.mp4", fps=30)
