import cv2
import numpy as np
import math
from moviepy.editor import VideoFileClip

# ======================
# FILE PATH
# ======================
video_path = "output_effect_with_audio.mp4"
overlay_path = "output_image.png"

temp_video = "final_effect.mp4"
final_video = "final_effect_with_audio.mp4"

# ======================
# LOAD VIDEO
# ======================
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# ======================
# LOAD OVERLAY (PNG RGBA)
# ======================
overlay = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)

def overlay_png(bg, fg, x, y, scale):
    scale = max(scale, 0.05)  # tránh scale = 0

    new_w = int(fg.shape[1] * scale)
    new_h = int(fg.shape[0] * scale)

    if new_w < 2 or new_h < 2:
        return bg

    fg = cv2.resize(fg, (new_w, new_h), interpolation=cv2.INTER_AREA)

    h, w = fg.shape[:2]

    # === Crop nếu vượt khung ===
    x1 = max(x, 0)
    y1 = max(y, 0)
    x2 = min(x + w, bg.shape[1])
    y2 = min(y + h, bg.shape[0])

    fg_x1 = x1 - x
    fg_y1 = y1 - y
    fg_x2 = fg_x1 + (x2 - x1)
    fg_y2 = fg_y1 + (y2 - y1)

    if fg_x2 <= fg_x1 or fg_y2 <= fg_y1:
        return bg

    fg_crop = fg[fg_y1:fg_y2, fg_x1:fg_x2]

    alpha = fg_crop[:, :, 3] / 255.0

    for c in range(3):
        bg[y1:y2, x1:x2, c] = (
            alpha * fg_crop[:, :, c] +
            (1 - alpha) * bg[y1:y2, x1:x2, c]
        )

    return bg


# ======================
# VIDEO WRITER
# ======================
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(temp_video, fourcc, fps, (W, H))

# ======================
# MAIN LOOP
# ======================
for i in range(total_frames):
    ret, frame = cap.read()
    if not ret:
        break

    t = i / fps

    zoom_left = 1.0 + 0.08 * math.sin(t * 2)
    zoom_right = 1.0 + 0.08 * math.sin(t * 2 + math.pi)

    big_scale = 0.35
    small_scale = 0.18

    # ===== NHÓM TRÊN TRÁI =====
    frame = overlay_png(
        frame, overlay,
        int(W * 0.05), int(H * 0.05),
        big_scale * zoom_left
    )

    frame = overlay_png(
        frame, overlay,
        int(W * 0.8), int(H * 0.65),
        small_scale * zoom_left
    )

    # ===== NHÓM TRÊN PHẢI =====
    frame = overlay_png(
        frame, overlay,
        int(W * 0.60), int(H * 0.05),
        big_scale * zoom_right
    )

    frame = overlay_png(
        frame, overlay,
        int(W * 0.10), int(H * 0.65),
        small_scale * zoom_right
    )

    out.write(frame)

cap.release()
out.release()

# ======================
# ADD AUDIO BACK
# ======================
video = VideoFileClip(video_path)
new_video = VideoFileClip(temp_video).set_audio(video.audio)
new_video.write_videofile(final_video, codec="libx264", audio_codec="aac")

print("DONE:", final_video)
