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

# Read the image (with cyan background to be removed)
image_file = "fly_plane_main.png"
image = cv2.imread(image_file)

# Remove cyan background and make it transparent
image_with_transparency = remove_cyan_background(image)

# Open the video file
video_file = "video2.mp4"
video = cv2.VideoCapture(video_file)

# Get video details (frame width, height, and FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# Create a VideoWriter object to save the new video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
output_video = cv2.VideoWriter("output_video_with_overlay.mp4", fourcc, fps, (frame_width, frame_height))

# Get the dimensions of the image to overlay
img_height, img_width, _ = image_with_transparency.shape

# Loop through the video frames
while True:
    ret, frame = video.read()
    if not ret:
        break
    
    # Define the position to place the image in the top-left corner (20px offset)
    y_offset = 20
    x_offset = 20

    # Get the region of interest (ROI) from the video frame where the image will be placed
    roi = frame[y_offset:y_offset + img_height, x_offset:x_offset + img_width]

    # Separate the channels of the image and the frame
    img_b, img_g, img_r, img_alpha = cv2.split(image_with_transparency)
    frame_b, frame_g, frame_r = cv2.split(roi)

    # Apply the alpha mask to the image (overlay the image onto the frame)
    for c in range(0, 3):  # For each of the RGB channels
        frame_roi = roi[:, :, c]
        frame_roi[:] = frame_roi * (1 - img_alpha / 255) + (img_b if c == 0 else img_g if c == 1 else img_r) * (img_alpha / 255)

    # Place the image on top of the frame (using the alpha channel for transparency)
    frame[y_offset:y_offset + img_height, x_offset:x_offset + img_width] = roi

    # Write the frame into the output video
    output_video.write(frame)

# Release the video objects and close any open windows
video.release()
output_video.release()
cv2.destroyAllWindows()
