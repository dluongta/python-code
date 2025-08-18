import cv2
import numpy as np

def insert_text_in_video(video_path, text, font_scale=1, color=(255, 255, 255), thickness=2):
  """
  Inserts text into a video.

  Args:
    video_path: Path to the video file.
    text: Text to be inserted.
    font_scale: Font scale factor.
    color: Text color in BGR format (Blue, Green, Red).
    thickness: Text thickness.

  Returns:
    None. Saves the modified video to a new file.
  """

  # Load the video
  cap = cv2.VideoCapture(video_path)

  # Get video properties
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  fps = cap.get(cv2.CAP_PROP_FPS)

  # Define codec for output video
  fourcc = cv2.VideoWriter_fourcc(*'XVID')

  # Create a VideoWriter object to save the output video
  out = cv2.VideoWriter('output_text_video.mp4', fourcc, fps, (width, height))

  # Get the font
  font = cv2.FONT_HERSHEY_SIMPLEX

  # Calculate text size and position
  text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
  text_x = (width - text_size[0]) // 2
  text_y = (height - text_size[1]) // 2

  # Process each frame
  while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
      break

    # Put text on the frame
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, thickness, cv2.LINE_AA)

    # Write the frame to the output video
    out.write(frame)

  # Release resources
  cap.release()
  out.release()
  cv2.destroyAllWindows()

# Example usage:
video_path = 'video1.mp4'  # Replace with your video file path
text_to_insert = "Hello, World!"
insert_text_in_video(video_path, text_to_insert)