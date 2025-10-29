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
radius_step = 8        # tốc độ lan tỏa mỗi frame
circle_color = (255, 255, 255)  # BGR
thickness = 10          # độ dày viền tròn

ret, frame = cap.read()
if not ret:
    print("Không đọc được video!")
    exit()

frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
result = segment.process(frame_rgb)
mask_init = (result.segmentation_mask > 0.3).astype(np.uint8) * 255

ys, xs = np.where(mask_init > 0)
if len(xs) == 0 or len(ys) == 0:
    print("Không phát hiện được người trong khung hình đầu!")
    exit()

x_center = int(np.mean(xs))
y_top = int(np.min(ys))
y_bottom = int(np.max(ys))
y_chest = int(y_top + 0.4 * (y_bottom - y_top))
center = (x_center, y_chest)

cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

current_radius = 0
radius_growing = True

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = segment.process(frame_rgb)
    mask_person = (result.segmentation_mask > 0.3).astype(np.uint8) * 255

    # --- Tạo mặt nạ cho viền tròn tại bán kính hiện tại ---
    circle_mask = np.zeros((height, width), dtype=np.uint8)
    # Vẽ viền tròn (anti-aliased)
    cv2.circle(circle_mask, center, int(round(current_radius)), 255, thickness, lineType=cv2.LINE_AA)

    # --- CHỈ giữ phần viền nằm trên người tại frame này ---
    visible_ring = cv2.bitwise_and(circle_mask, mask_person)

    # --- Áp hiệu ứng (render chỉ những pixel viền hợp lệ) ---
    frame_out = frame.copy()
    # Nếu muốn alpha blend mượt hơn, có thể thay thế bằng blending (hiện tại thay nguyên pixel)
    # Chỉ gán màu cho pixel của viền xuất hiện
    frame_out[visible_ring > 0] = circle_color

    out.write(frame_out)

    # --- Cập nhật bán kính: tăng cho tới max, sau đó dừng (không tạo vòng mới) ---
    if radius_growing:
        current_radius += radius_step
        if current_radius >= max_radius:
            current_radius = max_radius
            radius_growing = False  # dừng phóng to (vòng vẫn hiển thị ở bán kính max)
    # Nếu bạn muốn vòng dừng hoàn toàn (không hiển thị nữa) khi toàn bộ viền rơi ra ngoài người,
    # có thể kiểm tra `visible_ring` có còn pixel nào >0 hay không và dừng hiển thị khi =0.

cap.release()
out.release()
segment.close()
print("Video đã lưu:", output_path)
