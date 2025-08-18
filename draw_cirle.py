import cv2
import numpy as np
import time

# Create a VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter('loading_animation_with_gap.mp4', fourcc, 30.0, (800, 600))  # 30 FPS, 800x600 resolution

# Function to draw the loading animation (with gaps)
def draw_loading(frame, angle):
    # Create a blank white image (frame)
    frame.fill(255)  # Set the background to white

    # Center of the frame (x_center, y_center)
    x_center, y_center = 400, 300

    # Radius of the circle
    radius = 100

    # Draw the circle outline to simulate the loading ring
    cv2.circle(frame, (x_center, y_center), radius, (0, 0, 255), 6)

    # Calculate the start and end angles for the first gap (arc 1)
    gap_angle1_start = angle
    gap_angle1_end = angle + 60  # 60 degrees arc
    # Draw the first gap (arc 1)
    cv2.ellipse(frame, (x_center, y_center), (radius, radius), 0, gap_angle1_start, gap_angle1_end, (255, 255, 255), 6)

    # Calculate the start and end angles for the second gap (arc 2)
    gap_angle2_start = angle + 180  # This will be opposite of the first gap
    gap_angle2_end = gap_angle2_start + 60  # 60 degrees arc
    # Draw the second gap (arc 2)
    cv2.ellipse(frame, (x_center, y_center), (radius, radius), 0, gap_angle2_start, gap_angle2_end, (255, 255, 255), 6)

# Function to create the loading animation video
def create_loading_video():
    # Initialize the frame
    frame = np.ones((600, 800, 3), dtype=np.uint8) * 255  # White background

    # Loop to create frames of the loading animation
    for angle in range(0, 360 * 3, 10):  # Loop for 3 full rotations, change step for smoother animation
        # Draw the loading animation with gaps
        draw_loading(frame, angle)

        # Record the frame to video
        out.write(frame)

        # Pause briefly to create the animation effect (fps is 30, so it will create smooth motion)
        time.sleep(1 / 30.0)

# Create the loading animation video
create_loading_video()

# Release the video writer and save the video file
out.release()

cv2.destroyAllWindows()  # Close any OpenCV windows
