import cv2

# Đọc video
cap = cv2.VideoCapture("rectangle_text.mp4")

# Lấy thông tin video
fps = int(cap.get(cv2.CAP_PROP_FPS))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Tạo video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("rectangle_text_reversed.mp4", fourcc, fps, (width, height))

# Đọc tất cả frame vào danh sách
frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()

# Ghi ngược các frame
for frame in reversed(frames):
    out.write(frame)

out.release()
print("Video reversed!")
