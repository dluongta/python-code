import cv2

cap = cv2.VideoCapture("lumind_animation.mp4")

fps = int(cap.get(cv2.CAP_PROP_FPS))
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("lumind_animation_reversed.mp4", fourcc, fps, (width, height))

frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)

cap.release()

for frame in reversed(frames):
    out.write(frame)

out.release()
print("Video completed:lumind_animation_reversed.mp4")
