from rembg import remove
from PIL import Image
import io

# Đọc hình ảnh từ file
input_path = 'input-image-bg.png'  # Đường dẫn đến hình ảnh đầu vào
output_path = 'output-image-bg.png'  # Đường dẫn đến hình ảnh đầu ra

# Mở hình ảnh
with open(input_path, 'rb') as input_file:
    input_image = input_file.read()

# Xóa nền
output_image = remove(input_image)

# Lưu hình ảnh đầu ra
with open(output_path, 'wb') as output_file:
    output_file.write(output_image)
