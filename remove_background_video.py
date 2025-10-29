import cv2
import mediapipe as mp
import numpy as np

# --- Khởi tạo Mediapipe ---
mp_selfie_segmentation = mp.solutions.selfie_segmentation
segment = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# --- Đọc video đầu vào ---
input_path = "video_sample.mp4"
output_path = "output_blue.mp4"

cap = cv2.VideoCapture(input_path)
if not cap.isOpened():
    print("Không thể mở video! Kiểm tra lại đường dẫn:", input_path)
    exit()

# --- Lấy thông tin video ---
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps    = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

if fps == 0 or np.isnan(fps):
    fps = 30.0

print(f"Video: {width}x{height}, {fps:.2f} FPS, {frame_count} frames")

# --- Tạo video đầu ra ---
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

# --- Xử lý từng frame ---
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = segment.process(frame_rgb)
    mask = result.segmentation_mask

    # Làm mượt mặt nạ
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    condition = mask > 0.3  # ngưỡng tách người

    # Tạo nền xanh dương
    blue_bg = np.zeros_like(frame, dtype=np.uint8)
    blue_bg[:] = (255, 0, 0)

    # Kết hợp
    output_frame = np.where(condition[..., None], frame, blue_bg)

    out.write(output_frame)

# --- Giải phóng ---
cap.release()
out.release()

print("Đã lưu video thành công tại:", output_path)
