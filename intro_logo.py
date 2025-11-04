from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

W, H = 1280, 720
FONT_PATH = "C:/Windows/Fonts/arial.ttf"

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

    draw.text((x, y), text1, font=font, fill=(139, 0, 0))  
    draw.text((x+(bbox1[2]-bbox1[0]), y), text2, font=font, fill=(85, 85, 85))  
    return np.array(img)

def create_lumind_outline(fontsize, bg_color=(139, 0, 0)):
    img = Image.new("RGB", (W, H), bg_color)  
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, fontsize)

    text = "LUMIND"
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
        if s == 2.2:
            img = create_lumind_outline(fontsize) 
        else:
            img = create_lumind_image(fontsize)  
        clips.append(ImageClip(img).set_duration(0.6))
    return concatenate_videoclips(clips)

def make_flash_white():
    return ColorClip(size=(W, H), color=(255, 255, 255), duration=0.5)

def make_final_logo_with_subtitle():
    bg = ColorClip(size=(W, H), color=(255, 255, 255), duration=4)

    font_size = 130
    font = ImageFont.truetype(FONT_PATH, font_size)
    text_full = "LUONG MIND"
    text_LU = "LU"
    text_ONG = "ONG"
    text_MIND = "MIND"  

    img_temp = Image.new("RGB", (W, H), (255, 255, 255))
    draw_temp = ImageDraw.Draw(img_temp)
    w_LU = draw_temp.textlength(text_LU, font=font)
    w_ONG = draw_temp.textlength(text_ONG, font=font)
    w_MIND = draw_temp.textlength(text_MIND, font=font)
    total_w = w_LU + w_ONG + w_MIND

    start_x = (W - total_w) // 2 -  120
    y_pos = (H - font_size) // 2 -20

    def text_clip(text, color, width, offset_x):
        img = Image.new("RGB", (width, H), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((0, y_pos), text, font=font, fill=color)
        return ImageClip(np.array(img)).set_duration(4).set_position((offset_x,0))

    LU_clip = text_clip(text_LU, (139,0,0), int(w_LU), start_x)
    ONG_clip = text_clip(text_ONG, (139,0,0), int(w_ONG), start_x + w_LU)
    MIND_clip = text_clip(text_MIND, (85,85,85), int(w_MIND), start_x + w_LU + w_ONG)

    def mask_ong(t):
        mask = np.ones((H, int(w_ONG)), dtype=np.uint8) * 255
        if 1 <= t <= 2:
            progress = (t - 1)
            x_cut = int(progress * w_ONG)
            mask[:, :x_cut] = 0
        elif t > 2:
            mask[:, :] = 0
        return mask[:, :, None]

    ONG_masked = ONG_clip.set_mask(VideoClip(mask_ong, duration=4).to_mask())

    def LU_pos(t):
        factor = 1
        if t < 1:
            dx = 0
        elif 1 <= t <= 2:
            dx = w_ONG * factor * (t-1)/1
        else:
            dx = w_ONG * factor
        return (start_x + dx, 0)


    LU_moving = LU_clip.set_position(LU_pos)

    def subtitle_img():
        img = Image.new("RGB", (W, 100), (255, 255, 255))
        draw = ImageDraw.Draw(img)
        font2 = ImageFont.truetype(FONT_PATH, 50)
        text2 = "DLUONGTA - LUONG MIND"
        w_subtitle = draw.textlength(text2, font=font2)
        x_sub = (W - w_subtitle) // 2 + 10
        draw.text((x_sub, 10), text2, font=font2, fill=(139, 0, 0))
        return np.array(img)

    subtitle_static = ImageClip(subtitle_img()).set_duration(4)

    def subtitle_mask(t):
        mask = np.zeros((100, W), dtype=np.uint8)
        if 2.5 <= t <= 4.0:
            reveal_cols = int(((t - 2.5) / 1.5) * W)
            mask[:, :reveal_cols] = 255
        elif t > 4.0:
            mask[:, :] = 255
        return mask[:, :, None]

    subtitle = subtitle_static.set_mask(VideoClip(subtitle_mask, duration=4).to_mask())
    subtitle = subtitle.set_position(("center", H // 2 + 90))

    final = CompositeVideoClip([bg, LU_moving, ONG_masked, MIND_clip, subtitle])
    return final



def create_full_intro():
    stage1 = make_scale_sequence()
    stage2 = make_flash_white()
    stage3 = make_final_logo_with_subtitle()
    final = concatenate_videoclips([stage1, stage2, stage3])
    final.write_videofile("lumind_intro.mp4", fps=120)

if __name__ == "__main__":
    create_full_intro()
