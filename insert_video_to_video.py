import cv2
import numpy as np
from moviepy.editor import VideoFileClip

# Function to overlay video1 on video2, replacing blue pixels in video1 with pixels from video2
def overlay_video_on_blue(main_video_path, background_video_path, output_video_path, width, height, fps):
    cap_main = cv2.VideoCapture(main_video_path)  # Open the main video (video1)
    cap_background = cv2.VideoCapture(background_video_path)  # Open the background video (video2)
    
    # Check if the videos were opened correctly
    if not cap_main.isOpened() or not cap_background.isOpened():
        print("Error opening video files!")
        return
    
    # Get video properties
    fps = cap_background.get(cv2.CAP_PROP_FPS)
    
    # Initialize the codec and output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
    
    # Define the range for blue color in video1 (RGB: #39b6ff) in HSV
    # Convert #39b6ff to HSV
    lower_blue = np.array([90, 50, 50])  # Lower bound of blue in HSV (approximation)
    upper_blue = np.array([120, 255, 255])  # Upper bound of blue in HSV (approximation)
    
    while True:
        ret_main, frame_main = cap_main.read()
        ret_background, frame_background = cap_background.read()
        
        if not ret_main or not ret_background:
            break
        
        # Resize both frames to the specified width and height
        frame_main = cv2.resize(frame_main, (width, height))
        frame_background = cv2.resize(frame_background, (width, height))
        
        # Convert the frame of the main video (video1) to HSV (for blue detection)
        hsv_main = cv2.cvtColor(frame_main, cv2.COLOR_BGR2HSV)
        
        # Create a mask that identifies the blue areas in video1
        mask_blue = cv2.inRange(hsv_main, lower_blue, upper_blue)
        
        # Replace blue pixels from video1 with corresponding pixels from video2
        for i in range(height):
            for j in range(width):
                if mask_blue[i, j] > 0:  # If the pixel is blue (within the mask range)
                    frame_main[i, j] = frame_background[i, j]  # Replace with pixel from video2
        
        # Write the modified frame to the output video
        out.write(frame_main)
    
    # Release everything when done
    cap_main.release()
    cap_background.release()
    out.release()
    print(f"Video has been output at {output_video_path}")

# Parameters
main_video_path = 'video3.mp4'  # Path to the main video (video1)
background_video_path = 'video2.mp4'  # Path to the background video (video2)
output_video_path = 'output_video.mp4'  # Path to save the final video
width, height = 640, 480  # Resize video to this resolution
fps = 30  # Frame per second of the video (can be adjusted)

# Run the overlay function
overlay_video_on_blue(main_video_path, background_video_path, output_video_path, width, height, fps)
