import cv2
import mediapipe as mp
import numpy as np

# --- Khởi tạo Mediapipe ---
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segment = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# --- Video input/output ---
input_path = "video_sample.mp4"
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

    # --- Glow (phát sáng cam/đỏ mạnh) ---
    glow = cv2.GaussianBlur(visible_ring, (0, 0), 10)

    # Tạo màu phát sáng đỏ–cam tùy chỉnh
    glow_bgr = cv2.cvtColor(glow, cv2.COLOR_GRAY2BGR)
    glow_colored = np.zeros_like(glow_bgr)
    glow_colored[..., 2] = cv2.multiply(glow, 1.5)  
    glow_colored[..., 1] = cv2.multiply(glow, 0.7)  
    glow_colored[..., 0] = cv2.multiply(glow, 0.3)  

    # Giới hạn glow chỉ trong vùng người
    mask_glow = cv2.cvtColor(visible_ring, cv2.COLOR_GRAY2BGR)
    glow_colored = cv2.bitwise_and(glow_colored, mask_glow)

    # Tăng cường độ sáng tổng thể
    frame_out = cv2.addWeighted(frame_out, 1.0, glow_colored, 0.9, 15)

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
print("🔥 Video đã lưu:", output_path)
