import cv2
import numpy as np

# Tạo kích thước của hình ảnh
width, height = 500, 400

# Định nghĩa các thông số
video_filename = "rotating_rectangle.mp4"
fps = 10  # Số frame mỗi giây
frame_count = 30  # Tổng số frame cho video

# Tạo video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

# Tạo font chữ
font = cv2.FONT_HERSHEY_SIMPLEX

# Vị trí và kích thước hình chữ nhật
start_point = (150, 150)
end_point = (width - 150, height - 150)
color = (0, 0, 255)  # Màu đỏ (BGR)
thickness = 5

# Tạo một ảnh nền trắng
background_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # Nền trắng

# Hàm cắt phần hình chữ nhật từ ảnh nền
def crop_rectangle(image, start_point, end_point, padding=65):
    """
    Cắt phần hình chữ nhật ra khỏi ảnh với độ đệm padding xung quanh để tránh bị cắt khuyết
    """
    # Cắt vùng lớn hơn một chút so với phần hình chữ nhật
    return image[start_point[1] - padding:end_point[1] + padding, start_point[0] - padding:end_point[0] + padding]

# Tạo video với hình chữ nhật xoay
for i in range(frame_count):
    # Mỗi frame bắt đầu với nền trắng
    image = background_image.copy()

    # Tính toán góc xoay dần từ 0 độ đến 90 độ
    angle = (i * 90) / (frame_count - 1)  # Tăng dần góc xoay từ 0 đến 90

    # Tạo một ảnh nền trắng và vẽ hình chữ nhật vào đó
    rectangle_image = np.ones((height, width, 3), dtype=np.uint8) * 255  # Nền trắng

    # Vẽ hình chữ nhật lên nền trắng
    cv2.rectangle(rectangle_image, start_point, end_point, color, thickness)

    # Tính toán điểm trung tâm và ma trận xoay cho hình chữ nhật
    center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

    # Xoay hình chữ nhật (trong ảnh nền trắng)
    rotated_rectangle = cv2.warpAffine(rectangle_image, rotation_matrix, (width, height))

    # Cắt phần hình chữ nhật đã xoay, với độ đệm để tránh bị khuyết
    cropped_rectangle = crop_rectangle(rotated_rectangle, start_point, end_point)

    # Cập nhật ảnh gốc với phần hình chữ nhật đã xoay
    # Đảm bảo rằng vùng đích có kích thước phù hợp với vùng cắt
    image[start_point[1] - 65:end_point[1] + 65, start_point[0] - 65:end_point[0] + 65] = cropped_rectangle

    # Sau khi hình chữ nhật đã xoay xong, thêm dòng chữ vào frame cuối
    if i == frame_count - 1:
        text = "Welcome to DLUONGTA"
        text_size = cv2.getTextSize(text, font, 1, 2)[0]
        text_width, text_height = text_size
        text_position = ((image.shape[1] - text_width) // 2, (image.shape[0] + text_height) // 2)
        cv2.putText(image, text, text_position, font, 1, (0, 165, 255), 2, cv2.LINE_AA)

    # Thêm frame vào video
    video_writer.write(image)

# Thêm thêm thời gian nghỉ sau khi xuất hiện chữ
# Giữ frame cuối (chữ) một thời gian dài hơn để hiển thị rõ
for _ in range(fps * 2):  # Giữ chữ hiển thị trong 2 giây
    video_writer.write(image)

# Đóng video
video_writer.release()

