import cv2
import numpy as np

# Thông số video
width, height = 800, 400
fps = 30
duration = 6          
anim_ratio = 0.8       
anim_frames = int(fps * duration * anim_ratio)
hold_frames = int(fps * duration * (1 - anim_ratio))
frames = anim_frames + hold_frames

# Màu sắc (BGR)
white = (255, 255, 255)
dark_red = (0, 0, 139)   # đỏ sẫm
gray = (128, 128, 128)

# Khởi tạo video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('lumind_animation.mp4', fourcc, fps, (width, height))

# Cấu hình chữ
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 4
thickness = 8

# Tính vị trí trung tâm chữ
text1 = "LU"
text2 = "MIND"
size1 = cv2.getTextSize(text1, font, font_scale, thickness)[0]
size2 = cv2.getTextSize(text2, font, font_scale, thickness)[0]
gap = 10
total_width = size1[0] + gap + size2[0]
x0 = (width - total_width) // 2
y0 = height // 2 + size1[1] // 2

rect_max_height = size1[1] + 36
start_y_top = y0 - size1[1] - 20 

for i in range(frames):
    img = np.full((height, width, 3), 255, np.uint8)

    # Vẽ chữ
    cv2.putText(img, text1, (x0, y0), font, font_scale, dark_red, thickness, cv2.LINE_AA)
    cv2.putText(img, text2, (x0 + size1[0] + gap, y0), font, font_scale, gray, thickness, cv2.LINE_AA)

    if i < anim_frames:
        progress = i / anim_frames
    else:
        progress = 1.0

    rect_height = int(rect_max_height * progress)

    cv2.rectangle(img,
                  (x0, start_y_top),
                  (x0 + size1[0], start_y_top + rect_height),
                  dark_red, -1)

    cv2.rectangle(img,
                  (x0 + size1[0] + gap, start_y_top),
                  (x0 + size1[0] + gap + size2[0], start_y_top + rect_height),
                  gray, -1)

    out.write(img)

out.release()
print("Video 'lumind_animation.mp4' created")
