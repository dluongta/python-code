from PIL import Image, ImageFilter
import numpy as np

# Kích thước ảnh
width, height = 1080, 720

# Tạo lưới toạ độ
x = np.linspace(0, 1, width)
y = np.linspace(0, 1, height)
X, Y = np.meshgrid(x, y)

# Màu trung tâm (tím) và màu viền (cam)
center_color = np.array([180, 120, 255])  # tím nhạt
edge_color = np.array([255, 180, 120])    # cam nhạt

# Khoảng cách từ tâm để tạo hiệu ứng mờ dần
distance = np.sqrt((X - 0.5)**2 + (Y - 0.5)**2)
distance = distance / distance.max()

# Trộn màu theo khoảng cách
gradient = (center_color * (1 - distance[..., None]) + edge_color * distance[..., None]).astype(np.uint8)

# Tạo ảnh (Pillow tự nhận mode RGB nếu mảng có shape (h, w, 3))
img = Image.fromarray(gradient)

# Làm mờ mềm mại
img = img.filter(ImageFilter.GaussianBlur(radius=25))

# Lưu ảnh
img.save("gradient_background.jpg")

img.show()
