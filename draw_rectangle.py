import cv2
import numpy as np
import time

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
out = cv2.VideoWriter('led_effect_rectangle.mp4', fourcc, 15.0, (800, 600))

def record_frame(frame):
    out.write(frame)

def draw_rectangle():
    frame = np.ones((600, 800, 3), dtype=np.uint8) * 255  # White background

    x_center, y_center = 400, 300  # The center of the screen (800x600)

    rect_width, rect_height = 400, 300

    top_left = (x_center - rect_width // 2, y_center - rect_height // 2)
    top_right = (x_center + rect_width // 2, y_center - rect_height // 2)
    bottom_left = (x_center - rect_width // 2, y_center + rect_height // 2)
    bottom_right = (x_center + rect_width // 2, y_center + rect_height // 2)
    step_size = 5


    pen1_position = (top_left[0] +  rect_width // 2, top_right[1])
    pen2_position = (top_left[0] +  rect_width // 2, top_right[1])
    x1 = pen1_position[0]
    y1 = pen1_position[1]
    x2 = pen2_position[0]
    y2 = pen2_position[1]
    time.sleep(0.05)
    while x1 < top_right[0] or x2 > top_left[0]:
        if x1 < top_right[0]:
            x1+= step_size
        if x2 > top_left[0]:
            x2-= step_size
        cv2.line(frame, pen1_position, (x1,y1), (0, 0, 255), 2)
        cv2.line(frame, pen2_position, (x2,y2), (0, 0, 255), 2)
        record_frame(frame)  
        time.sleep(0.05) 

    pen1_position = top_right
    pen2_position = top_left
    x1 = pen1_position[0]
    y1 = pen1_position[1]
    x2 = pen2_position[0]
    y2 = pen2_position[1]
    time.sleep(10)
    while y1 < bottom_right[1] or y2 < bottom_left[1] :
        if y1 < bottom_right[1]:
            y1+= step_size
        if y2 < bottom_left[1]:
            y2+= step_size
        cv2.line(frame, pen1_position, (x1,y1), (0, 0, 255), 2)
        cv2.line(frame, pen2_position, (x2,y2), (0, 0, 255), 2)
        record_frame(frame)  
        time.sleep(0.05) 

    pen1_position = bottom_right
    pen2_position = bottom_left
    x1 = pen1_position[0]
    y1 = pen1_position[1]
    x2 = pen2_position[0]
    y2 = pen2_position[1]
    time.sleep(0.05)
    while x1 > top_left[0] +  rect_width // 2 - 50 or x2 < top_left[0] +  rect_width // 2 + 50:
        if x1 > top_left[0] +  rect_width // 2 - 50:
            x1-= step_size
        if x2 < top_left[0] +  rect_width // 2 + 50:
            x2+= step_size
        cv2.line(frame, pen1_position, (x1,y1), (0, 0, 255), 2)
        cv2.line(frame, pen2_position, (x2,y2), (0, 0, 255), 2)
        record_frame(frame)  
        time.sleep(0.05)  

time.sleep(0.05) 

draw_rectangle()

out.release()  

cv2.destroyAllWindows() 
