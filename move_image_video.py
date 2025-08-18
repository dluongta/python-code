import cv2
import numpy as np

# Function to overlay image with transparency onto video frame
def overlay_image(frame, image_with_transparency, x_offset, y_offset):
    # Get the dimensions of the image to overlay
    img_height, img_width, _ = image_with_transparency.shape

    # Check if the image fits within the video frame
    if x_offset + img_width > frame.shape[1] or y_offset + img_height > frame.shape[0]:
        return frame  # Skip if the image does not fit inside the frame

    # Extract the region of interest (ROI) from the frame where the image will be placed
    roi = frame[y_offset:y_offset + img_height, x_offset:x_offset + img_width]

    # Separate the channels of the image with transparency
    img_b, img_g, img_r, img_alpha = cv2.split(image_with_transparency)

    # Apply the alpha mask to blend the image onto the frame
    for c in range(3):  # For each of the RGB channels
        roi[:, :, c] = roi[:, :, c] * (1 - img_alpha / 255) + (img_b if c == 0 else img_g if c == 1 else img_r) * (img_alpha / 255)

    # Place the image on top of the frame using the alpha channel for transparency
    frame[y_offset:y_offset + img_height, x_offset:x_offset + img_width] = roi

    return frame

# Read the image (with transparency)
image_file = "logo.png"
image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)  # Make sure to load with transparency

# Open the video file
video_file = "output_video.mp4"
video = cv2.VideoCapture(video_file)

# Get video details (frame width, height, and FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# Create a VideoWriter object to save the new video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
output_video = cv2.VideoWriter("output_video_with_overlay.mp4", fourcc, fps, (frame_width, frame_height))

# Get the dimensions of the image to overlay
img_height, img_width, _ = image.shape

# Initialize the starting position and movement step
x_offset, y_offset = 20, 20
x_step, y_step = 20, 0  # Horizontal movement only, adjust x_step for speed

# Loop through the video frames
while True:
    ret, frame = video.read()
    if not ret:
        break

    # Update the position of the overlay image
    x_offset += x_step

    # When the image goes off the right side of the frame, reset its position to the left immediately
    if x_offset > frame_width - img_width:
        x_offset = 20  # Start from the left side immediately

    # Overlay the image with transparency onto the video frame
    frame = overlay_image(frame, image, x_offset, y_offset)

    # Write the frame into the output video
    output_video.write(frame)

# Release the video objects and close any open windows
video.release()
output_video.release()
cv2.destroyAllWindows()
