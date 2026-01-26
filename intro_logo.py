from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1280, 720
FONT_PATH = "C:/Windows/Fonts/arial.ttf"

# ---------- STAGE 1 : SCALE ULMIND ----------
def create_ulmind_image(fontsize, bg_color=(255, 255, 255)):
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, fontsize)

    text1, text2 = "UL", "MIND"
    bbox1 = draw.textbbox((0, 0), text1, font=font)
    bbox2 = draw.textbbox((0, 0), text2, font=font)

    total_w = (bbox1[2]-bbox1[0]) + (bbox2[2]-bbox2[0])
    x = (W - total_w) // 2
    y = (H - (bbox1[3]-bbox1[1]) - fontsize*0.5) // 2

    draw.text((x, y), text1, font=font, fill=(139, 0, 0))
    draw.text((x + (bbox1[2]-bbox1[0]), y), text2, font=font, fill=(85, 85, 85))
    return np.array(img)

def create_ulmind_outline(fontsize, bg_color=(139, 0, 0)):
    img = Image.new("RGB", (W, H), bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, fontsize)

    text = "ULMIND"
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (W - (bbox[2]-bbox[0])) // 2
    y = (H - (bbox[3]-bbox[1]) - fontsize*0.5) // 2

    border = 12
    for dx in range(-border, border+1):
        for dy in range(-border, border+1):
            if dx*dx + dy*dy <= border*border:
                draw.text((x+dx, y+dy), text, font=font, fill=(255, 255, 255))

    draw.text((x, y), text, font=font, fill=(139, 0, 0))
    return np.array(img)

def make_scale_sequence():
    scales = [1.0, 1.3, 1.6, 1.9, 2.2]
    clips = []
    for s in scales:
        fontsize = int(120 * s)
        img = create_ulmind_outline(fontsize) if s == 2.2 else create_ulmind_image(fontsize)
        clips.append(ImageClip(img).set_duration(0.6))
    return concatenate_videoclips(clips)

def make_flash_white():
    return ColorClip(size=(W, H), color=(255, 255, 255), duration=0.5)

# ---------- STAGE 3 : FINAL ULTRAMIND ----------
def make_final_logo_with_subtitle():
    bg = ColorClip(size=(W, H), color=(255, 255, 255), duration=4)

    font_size = 130
    font = ImageFont.truetype(FONT_PATH, font_size)

    text_UL = "UL"
    text_TRA = "TRA"
    text_MIND = "MIND"

    img_tmp = Image.new("RGB", (W, H), (255, 255, 255))
    draw_tmp = ImageDraw.Draw(img_tmp)

    w_UL = draw_tmp.textlength(text_UL, font=font)
    w_TRA = draw_tmp.textlength(text_TRA, font=font)
    w_MIND = draw_tmp.textlength(text_MIND, font=font)

    total_w = w_UL + w_TRA + w_MIND
    start_x = (W - total_w) // 2 - 100
    y_pos = (H - font_size) // 2 - 20

    def text_clip(text, color, width, offset_x):
        img = Image.new("RGB", (int(width), H), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, y_pos), text, font=font, fill=color)
        return ImageClip(np.array(img)).set_duration(4).set_position((offset_x, 0))

    UL_clip = text_clip(text_UL, (139, 0, 0), w_UL, start_x)
    TRA_clip = text_clip(text_TRA, (139, 0, 0), w_TRA, start_x + w_UL)
    MIND_clip = text_clip(text_MIND, (85, 85, 85), w_MIND, start_x + w_UL + w_TRA)

    def mask_tra(t):
        mask = np.ones((H, int(w_TRA)), dtype=np.uint8) * 255
        if 1 <= t <= 2:
            cut = int((t - 1) * w_TRA)
            mask[:, :cut] = 0
        elif t > 2:
            mask[:, :] = 0
        return mask[:, :, None]

    TRA_masked = TRA_clip.set_mask(VideoClip(mask_tra, duration=4).to_mask())

    def UL_pos(t):
        if t < 1:
            dx = 0
        elif 1 <= t <= 2:
            dx = w_TRA * (t - 1)
        else:
            dx = w_TRA
        return (start_x + dx, 0)

    UL_moving = UL_clip.set_position(UL_pos)

    # ---------- SUBTITLE ----------
    def subtitle_img():
        img = Image.new("RGB", (W, 100), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font2 = ImageFont.truetype(FONT_PATH, 50)
        text2 = "DLUONGTA - ULTRA MIND"
        w_sub = draw.textlength(text2, font=font2)
        x_sub = (W - w_sub) // 2 + 10
        draw.text((x_sub, 10), text2, font=font2, fill=(139, 0, 0))
        return np.array(img)

    subtitle_static = ImageClip(subtitle_img()).set_duration(4)

    def subtitle_mask(t):
        mask = np.zeros((100, W), dtype=np.uint8)
        if 2.5 <= t <= 4:
            reveal = int(((t - 2.5) / 1.5) * W)
            mask[:, :reveal] = 255
        elif t > 4:
            mask[:, :] = 255
        return mask[:, :, None]

    subtitle = subtitle_static.set_mask(VideoClip(subtitle_mask, duration=4).to_mask())
    subtitle = subtitle.set_position(("center", H // 2 + 60))

    final = CompositeVideoClip([
        bg,
        UL_moving,
        TRA_masked,
        MIND_clip,
        subtitle
    ])

    return final

# ---------- EXPORT ----------
def create_full_intro():
    stage1 = make_scale_sequence()
    stage2 = make_flash_white()
    stage3 = make_final_logo_with_subtitle()
    final = concatenate_videoclips([stage1, stage2, stage3])
    final.write_videofile("ultramind_intro.mp4", fps=120)

if __name__ == "__main__":
    create_full_intro()
