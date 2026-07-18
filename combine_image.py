import cv2

def insert_image(main_image_path, insert_image_path, output_image_path, x, y, width, height):
    """Inserts an image into another image at specified coordinates, width, and height.

    Args:
        main_image_path (str): Path to the main image file.
        insert_image_path (str): Path to the image to insert.
        output_image_path (str): Path to save the output image.
        x (int): X-coordinate of the top-left corner of the inserted image.
        y (int): Y-coordinate of the top-left corner of the inserted image.
        width (int): Width of the inserted image.
        height (int): Height of the inserted image.
    """

    main_image = cv2.imread(main_image_path)

    insert_image = cv2.imread(insert_image_path)

    insert_image = cv2.resize(insert_image, (width, height))

    roi = main_image[y:y+height, x:x+width]

    roi = cv2.addWeighted(roi, 0, insert_image, 1, 0)

    main_image[y:y+height, x:x+width] = roi

    cv2.imwrite(output_image_path, main_image)

main_image_path = 'input_image.png'
insert_image_path = 'output_image.png'
output_image_path = 'output_combined_image.png'
x = 100 
y = 200  
width = 300  
height = 200  

insert_image(main_image_path, insert_image_path, output_image_path, x, y, width, height)