import cv2
from ultralytics import YOLO

# Load model YOLO (mặc định là yolov8n.pt - nhẹ và nhanh)
model = YOLO("yolov8n.pt")

# Mở webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

window_name = "YOLOv8 Object Detection"

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc frame.")
        break

    # Nhận diện vật thể
    results = model(frame)

    # Vẽ khung nhận diện
    annotated_frame = results[0].plot()

    # Hiển thị kết quả
    cv2.imshow(window_name, annotated_frame)

    # Thoát nếu nhấn 'q' hoặc đóng cửa sổ
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
