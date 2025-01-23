import cv2

def merge_videos(video_paths, output_video_path):
    """
    Merge multiple videos and save the output video.

    Args:
        video_paths (list): List of paths to the videos to merge.
        output_video_path (str): Path to the output video.
    """
    
    out = None  # Initialize video writer

    for video_path in video_paths:
        cap = cv2.VideoCapture(video_path)

        while cap.isOpened():
            ret, frame = cap.read()

            if not ret:
                break

            if out is None:
                # Initialize VideoWriter for the output video if not already created
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                # Use 'mp4v' codec which works better for MP4 output
                out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

            # Check if the frame is valid before writing to the output video
            if frame is not None:
                out.write(frame)

        cap.release()

    if out is not None:
        out.release()

# Example usage of merge_videos function
video_paths = ['final_video_with_slider_transition.mp4', 'final_video_with_slider.mp4']  # List of input video paths
output_video_path = 'output_video.mp4'  # Path for the output video

merge_videos(video_paths, output_video_path)
