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

# Initialize the starting position and movement step
x_offset, y_offset = 20, 20
x_step, y_step = 20, 0  # Horizontal movement only
frame_count = 0
max_frames = int(fps * 5)  # Overlay visible for 5 seconds

# Loop through the video frames
while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_count += 1

    # Update the position of the overlay image
    x_offset += x_step

    # Skip rendering the overlay if it moves out of bounds
    if x_offset + img_width > frame_width or x_offset < 0:
        # Write the current frame without overlay
        output_video.write(frame)
        continue

    # Apply overlay only for the specified duration
    if frame_count <= max_frames:
        # Get the region of interest (ROI) from the video frame where the image will be placed
        roi = frame[y_offset:y_offset + img_height, x_offset:x_offset + img_width]

        # Separate the channels of the image and the frame
        img_b, img_g, img_r, img_alpha = cv2.split(image_with_transparency)

        # Apply the alpha mask to the image (overlay the image onto the frame)
        for c in range(3):  # For each of the RGB channels
            roi[:, :, c] = roi[:, :, c] * (1 - img_alpha / 255) + (img_b if c == 0 else img_g if c == 1 else img_r) * (img_alpha / 255)

        # Place the image on top of the frame (using the alpha channel for transparency)
        frame[y_offset:y_offset + img_height, x_offset:x_offset + img_width] = roi

    # Write the frame into the output video
    output_video.write(frame)


# Release the video objects and close any open windows
video.release()
output_video.release()
cv2.destroyAllWindows()
