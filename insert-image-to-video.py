import cv2

# Load the video
video_path = 'input.mp4'
cap = cv2.VideoCapture(video_path)

# Load the image you want to overlay
overlay_image = cv2.imread('input_image.png', cv2.IMREAD_UNCHANGED)

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the coordinates where you want to insert the image
x_offset = 100  # x coordinate
y_offset = 50   # y coordinate

# Check if overlay image has an alpha channel (transparency)
if overlay_image.shape[2] == 4:
    alpha_channel = overlay_image[:, :, 3] / 255.0
    overlay_image = overlay_image[:, :, :3]  # Discard the alpha channel for blending
else:
    alpha_channel = None

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter('output_insert_image_to_video.mp4', fourcc, fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Calculate the region of interest
    roi = frame[y_offset:y_offset + overlay_image.shape[0], x_offset:x_offset + overlay_image.shape[1]]

    # Overlay the image
    if alpha_channel is not None:
        for c in range(0, 3):
            roi[:, :, c] = (alpha_channel * overlay_image[:, :, c] + (1 - alpha_channel) * roi[:, :, c])
    else:
        roi[:] = overlay_image

    # Replace the ROI on the frame with the blended ROI
    frame[y_offset:y_offset + overlay_image.shape[0], x_offset:x_offset + overlay_image.shape[1]] = roi

    # Write the frame to the output video
    out.write(frame)

    # Display the frame (optional)
    cv2.imshow('Video', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
