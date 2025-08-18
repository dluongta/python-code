from rembg import remove
from PIL import Image
import io

# Đọc hình ảnh từ file
input_path = 'input-image-bg.png'  # Đường dẫn đến hình ảnh có nền cần thay
background_path = 'background.png'  # Đường dẫn đến hình ảnh nền mới
output_path = 'output-image-changed-bg.png'  # Đường dẫn đến hình ảnh đầu ra

# Mở hình ảnh có nền
with open(input_path, 'rb') as input_file:
    input_image = input_file.read()

# Xóa nền
output_image = remove(input_image)

# Chuyển đổi kết quả xóa nền sang định dạng ảnh
image_with_transparent_background = Image.open(io.BytesIO(output_image))

# Mở hình ảnh nền
background = Image.open(background_path)

# Điều chỉnh kích thước hình nền để khớp với kích thước hình ảnh chính
background = background.resize(image_with_transparent_background.size, Image.LANCZOS)

# Ghép hình ảnh với nền mới
combined = Image.new('RGBA', background.size)
combined.paste(background, (0, 0))
combined.paste(image_with_transparent_background, (0, 0), mask=image_with_transparent_background)

# Lưu hình ảnh đầu ra
combined.save(output_path)
