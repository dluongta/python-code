import cv2
import numpy as np
import sys

# Đọc ảnh sample và city
sample_path = 'sample.png'
city_path = 'city.jpg'

sample = cv2.imread(sample_path)
city = cv2.imread(city_path)

if sample is None:
    print(f"Not read sample image from: {sample_path}")
    sys.exit()

if city is None:
    print(f"Not read city image from: {city_path}")
    sys.exit()

# Resize city ảnh cho khớp kích thước sample
city = cv2.resize(city, (sample.shape[1], sample.shape[0]))

# ---- CHUẨN BGT: Tìm đúng màu BGR (239, 174, 0) với sai số nhỏ ----
target_color = np.array([239, 174, 0])  # BGR
tolerance = 20  # sai số +/- cho mỗi kênh

lower_bound = np.clip(target_color - tolerance, 0, 255)
upper_bound = np.clip(target_color + tolerance, 0, 255)

# Tạo mask cho vùng có màu giống target
mask = cv2.inRange(sample, lower_bound, upper_bound)

# Thay thế pixel tương ứng từ city ảnh
output = sample.copy()
output[mask != 0] = city[mask != 0]

# Lưu kết quả
cv2.imwrite('result.png', output)
# cv2.imwrite('mask.png', mask)

print("Saved file: result.png")
