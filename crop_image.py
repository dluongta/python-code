import cv2

def crop_image(input_image_path, output_image_path, x, y, width, height):
    """
    Cắt một phần của hình ảnh.

    Args:
        input_image_path (str): Đường dẫn đến hình ảnh đầu vào.
        output_image_path (str): Đường dẫn đến hình ảnh đầu ra sau khi cắt.
        x (int): Tọa độ x của góc trên bên trái của phần cần cắt.
        y (int): Tọa độ y của góc trên bên trái của phần cần cắt.
        width (int): Chiều rộng của phần cần cắt.
        height (int): Chiều cao của phần cần cắt.
    """

    image = cv2.imread(input_image_path)

    cropped_image = image[y:y+height, x:x+width]

    cv2.imwrite(output_image_path, cropped_image)

input_image_path = 'input_image.png'
output_image_path = 'output_crop_image.png'
x = 200  
y = 150   
width = 400 
height = 250  

crop_image(input_image_path, output_image_path, x, y, width, height)