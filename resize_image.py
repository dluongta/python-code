import cv2

def resize_image(input_image_path, output_image_path, new_width, new_height):
    """
    Thay đổi kích thước của hình ảnh.

    Args:
        input_image_path (str): Đường dẫn đến hình ảnh đầu vào.
        output_image_path (str): Đường dẫn đến hình ảnh đầu ra sau khi thay đổi kích thước.
        new_width (int): Độ rộng mới của hình ảnh.
        new_height (int): Độ cao mới của hình ảnh.
    """

    # Đọc hình ảnh từ đường dẫn đầu vào
    image = cv2.imread(input_image_path)

    # Thay đổi kích thước hình ảnh
    resized_image = cv2.resize(image, (new_width, new_height))

    # Lưu hình ảnh đã thay đổi kích thước vào đường dẫn đầu ra
    cv2.imwrite(output_image_path, resized_image)

# Ví dụ sử dụng hàm resize_image
input_image_path = 'input_image.png'
output_image_path = 'output_image.png'
new_width = 400
new_height = 300

resize_image(input_image_path, output_image_path, new_width, new_height)