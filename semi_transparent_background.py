import cv2
import numpy as np

# Open the video file
video_file = "video2.mp4"
video = cv2.VideoCapture(video_file)

# Get video details (frame width, height, and FPS)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = video.get(cv2.CAP_PROP_FPS)

# Create a VideoWriter object to save the new video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
output_video = cv2.VideoWriter("output_video_with_orange_background.mp4", fourcc, fps, (frame_width, frame_height))

# Define the semi-transparent orange background
orange_background = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
orange_background[:] = [0, 165, 255]  # Pure orange color
alpha_orange = 0.2  # Transparency level (0.0 to 1.0)

# Loop through the video frames
while True:
    ret, frame = video.read()
    if not ret:
        break

    # Blend the frame with the orange background
    blended_frame = cv2.addWeighted(frame, 1 - alpha_orange, orange_background, alpha_orange, 0)

    # Write the frame into the output video
    output_video.write(blended_frame)

# Release the video objects and close any open windows
video.release()
output_video.release()
cv2.destroyAllWindows()