import cv2
import mediapipe as mp
import numpy as np

# --- Khởi tạo Mediapipe ---
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segment = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# --- Video input/output ---
input_path = "output_video_with_music.mp4"
output_path = "output_effect.mp4"

cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print("Không mở được video!")
    exit()

width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS) or 30.0

out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

# --- Cấu hình viền tròn ---
max_radius = 2000       # bán kính lớn nhất
radius_step = 40        # tốc độ lan tỏa mỗi frame
circle_color = (0, 140, 255)  # màu cam BGR
thickness = 8           # độ dày viền

# --- Xác định vị trí người ---
ret, frame = cap.read()
if not ret:
    print("Không đọc được video!")
    exit()

frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
result = segment.process(frame_rgb)
mask_init = (result.segmentation_mask > 0.3).astype(np.uint8) * 255

ys, xs = np.where(mask_init > 0)
if len(xs) == 0 or len(ys) == 0:
    print("Không phát hiện được người trong khung hình")
    exit()

x_center = int(np.mean(xs))
y_top = int(np.min(ys))
y_bottom = int(np.max(ys))
y_chest = int(y_top + 0.5 * (y_bottom - y_top))
center = (x_center, y_chest)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

current_radius = 0
radius_growing = True

# --- Xử lý từng frame ---
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # --- Tính thời gian hiện tại của video (ms) ---
    current_time_ms = cap.get(cv2.CAP_PROP_POS_MSEC)
    current_time_sec = current_time_ms / 1000.0

    video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    start_time = video_duration / 2
    if current_time_sec < start_time:
        out.write(frame)
        continue


    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = segment.process(frame_rgb)
    mask_person = (result.segmentation_mask > 0.3).astype(np.uint8) * 255

    # --- Tạo viền "điện giật" hình chữ nhật dọc ---
    rect_mask = np.zeros((height, width), dtype=np.uint8)

    # Kích thước cơ bản của khung điện giật
    rect_width = int(20000)   # điều chỉnh tỷ lệ chiều ngang
    rect_height = int(current_radius * 1.6)  # điều chỉnh tỷ lệ chiều dọc

    # Tạo mép chữ nhật (4 cạnh)
    amplitude = 15      # độ rung điện
    smoothness = 20     # mật độ dao động cạnh
    phase = cv2.getTickCount() / cv2.getTickFrequency() * 4.0

    # Tạo cạnh trên & dưới
    x = np.linspace(-rect_width // 2, rect_width // 2, 200)
    noise_top = np.sin(x / 10 + phase) * amplitude + np.random.uniform(-5, 5, size=x.shape)
    noise_bottom = np.sin(x / 8 + phase + np.pi) * amplitude + np.random.uniform(-5, 5, size=x.shape)

    top_pts = np.stack((center[0] + x, center[1] - rect_height // 2 + noise_top), axis=1).astype(np.int32)
    bottom_pts = np.stack((center[0] + x, center[1] + rect_height // 2 + noise_bottom), axis=1).astype(np.int32)

    # Tạo cạnh trái & phải
    y = np.linspace(-rect_height // 2, rect_height // 2, 200)
    noise_left = np.sin(y / 12 + phase) * amplitude + np.random.uniform(-5, 5, size=y.shape)
    noise_right = np.sin(y / 9 + phase + np.pi / 2) * amplitude + np.random.uniform(-5, 5, size=y.shape)

    left_pts = np.stack((center[0] - rect_width // 2 + noise_left, center[1] + y), axis=1).astype(np.int32)
    right_pts = np.stack((center[0] + rect_width // 2 + noise_right, center[1] + y), axis=1).astype(np.int32)

    # Gộp 4 cạnh lại thành khung điện
    pts = np.concatenate([top_pts, right_pts, bottom_pts[::-1], left_pts[::-1]]).reshape((-1, 1, 2))

    # Vẽ viền điện giật
    cv2.polylines(rect_mask, [pts], isClosed=True, color=255, thickness=thickness, lineType=cv2.LINE_AA)

    # --- Giữ phần viền trên người ---
    visible_ring = cv2.bitwise_and(rect_mask, mask_person)

    # --- Áp màu viền chính ---
    frame_out = frame.copy()
    frame_out[visible_ring > 0] = circle_color

    # --- Glow (phát sáng mạnh kiểu LED) ---
    glow_base = visible_ring.copy()

    # 3 lớp bloom
    glow1 = cv2.GaussianBlur(glow_base, (0, 0), 15)
    glow2 = cv2.GaussianBlur(glow_base, (0, 0), 35)
    glow3 = cv2.GaussianBlur(glow_base, (0, 0), 60)

    # Tô màu glow (đỏ–cam rực)
    def colorize(mask, r, g, b):
        c = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        c[..., 2] = mask * r
        c[..., 1] = mask * g
        c[..., 0] = mask * b
        return c

    glow1 = colorize(glow1, 1.0, 0.5, 0.2)
    glow2 = colorize(glow2, 1.3, 0.4, 0.1)
    glow3 = colorize(glow3, 1.6, 0.3, 0.0)

    # Tăng cường – blend từng lớp
    frame_out = cv2.addWeighted(frame_out, 1.0, glow1, 0.6, 0)
    frame_out = cv2.addWeighted(frame_out, 1.0, glow2, 0.5, 0)
    frame_out = cv2.addWeighted(frame_out, 1.0, glow3, 0.45, 0)

    out.write(frame_out)

    # --- Cập nhật bán kính ---
    if radius_growing:
        current_radius += radius_step
        if current_radius >= max_radius:
            current_radius = max_radius
            radius_growing = False

cap.release()
out.release()
segment.close()

# --- Ghép lại âm thanh gốc bằng ffmpeg ---
import subprocess

final_output = "output_effect_with_audio.mp4"

cmd = [
    "ffmpeg",
    "-y",
    "-i", output_path,        # video đã xử lý (không có tiếng)
    "-i", input_path,         # video gốc (có tiếng)
    "-c:v", "copy",           # giữ nguyên video đã xử lý
    "-c:a", "aac",            # copy âm thanh AAC
    "-map", "0:v:0",          # lấy video từ file 0
    "-map", "1:a:0",          # lấy audio từ file 1
    final_output
]
subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("🎧 Video có âm thanh đã lưu:", final_output)

print("🔥 Video đã lưu:", output_path)
