import cv2
import numpy as np

# Function to remove cyan background and make it transparent
def remove_cyan_background(image):
    # Convert the image to RGB (since OpenCV uses BGR by default)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Define the range for cyan color in RGB (approximately RGB(0, 255, 255))
    lower_cyan = np.array([0, 200, 200])  # Lower bound for cyan color
    upper_cyan = np.array([100, 255, 255])  # Upper bound for cyan color

    # Create a mask for cyan pixels in the image
    mask = cv2.inRange(image_rgb, lower_cyan, upper_cyan)

    # Invert the mask: Keep everything except cyan as visible
    mask_inv = cv2.bitwise_not(mask)

    # Split the channels (Blue, Green, Red) of the image
    b, g, r = cv2.split(image)

    # Create an alpha channel using the inverted mask (0 for cyan, 255 for non-cyan)
    alpha = mask_inv

    # Merge the channels (BGR + Alpha) to create an RGBA image
    rgba = [b, g, r, alpha]

    # Merge the channels to form the final image with transparency
    dst = cv2.merge(rgba, 4)

    return dst

# Read the image
file_name = "fly_plane_main.png"  # Replace with your image file
src = cv2.imread(file_name)

# Remove cyan background and make it transparent
image_with_transparency = remove_cyan_background(src)

# Save the resulting image with a transparent background
cv2.imwrite("fly_plane_main_transparency.png", image_with_transparency)
