from PIL import Image, ImageFilter
import numpy as np

# Kích thước ảnh
width, height = 1080, 720

# Tạo lưới tọa độ (chạy từ 0 → 1 theo chiều ngang)
x = np.linspace(0, 1, width)
y = np.linspace(0, 1, height)
X, Y = np.meshgrid(x, y)

# Định nghĩa 3 màu (RGB)
left_color = np.array([200, 150, 255])   # tím hồng bên trái
center_color = np.array([255, 180, 100]) # cam ở giữa
right_color = np.array([200, 150, 255])  # tím hồng bên phải

# Tạo gradient 3 vùng:
# - 0 → 0.5: tím hồng → cam
# - 0.5 → 1: cam → hồng
gradient = np.zeros((height, width, 3), dtype=np.float32)

# Vùng bên trái đến giữa
left_mask = X <= 0.5
left_ratio = X[left_mask] / 0.5
gradient[left_mask] = (left_color * (1 - left_ratio)[:, None] + center_color * left_ratio[:, None])

# Vùng giữa đến bên phải
right_mask = X > 0.5
right_ratio = (X[right_mask] - 0.5) / 0.5
gradient[right_mask] = (center_color * (1 - right_ratio)[:, None] + right_color * right_ratio[:, None])

# Chuyển sang kiểu ảnh
gradient = gradient.astype(np.uint8)
img = Image.fromarray(gradient)

# Làm mờ mềm mại để tạo cảm giác mờ ảo
img = img.filter(ImageFilter.GaussianBlur(radius=35))

# Lưu và hiển thị
img.save("gradient_image.jpg")
img.show()
