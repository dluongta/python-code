import cv2
import numpy as np
import math

# --- CẤU HÌNH VIDEO ---
WIDTH, HEIGHT = 1920, 1080
FPS = 60
TOTAL_DURATION = 8.0        # Tổng thời lượng video: 8 giây
DRAW_DURATION = 6.5         # Thời gian vẽ nét: 6.5 giây (1.5 giây cuối giữ nguyên logo)
OUTPUT_FILE = "dluongta_animation.mp4"

# --- CẤU HÌNH MÀU SẮC (Định dạng BGR của OpenCV) ---
BG_COLOR = (255, 255, 255)  # Nền trắng
RED_DARK = (0, 10, 175)     # Đỏ thẫm cho chữ TS
GRAY = (125, 125, 125)      # Xám cho chữ CEND

# --- CẤU HÌNH KÍCH THƯỚC CHỮ ---
LETTER_W = 130              # Chiều rộng mỗi chữ
LETTER_H = 290              # Chiều cao mỗi chữ
GAP = 55                    # Khoảng cách giữa các chữ
THICKNESS = 18              # Độ dày nét vẽ

# Căn giữa toàn bộ dòng chữ trên khung hình
TOTAL_W = 6 * LETTER_W + 5 * GAP
START_X = (WIDTH - TOTAL_W) // 2
START_Y = (HEIGHT - LETTER_H) // 2

def get_letter_strokes():
    """Định nghĩa danh sách các nét thẳng: (x1, y1, x2, y2, color)"""
    strokes = []
    
    # Hàm phụ lấy tọa độ góc trên-trái của chữ thứ i (0 đến 5)
    def pos(i):
        x = START_X + i * (LETTER_W + GAP)
        y = START_Y
        return x, y

    w, h = LETTER_W, LETTER_H
    mid_y = h // 2

    # 1. Chữ T (Đỏ thẫm)
    x, y = pos(0)
    strokes.append((x, y, x + w, y, RED_DARK))                      # Nét ngang trên
    strokes.append((x + w // 2, y, x + w // 2, y + h, RED_DARK))    # Nét dọc giữa

    # 2. Chữ S (Đỏ thẫm)
    x, y = pos(1)
    strokes.append((x + w, y, x, y, RED_DARK))                      # Ngang trên (phải -> trái)
    strokes.append((x, y, x, y + mid_y, RED_DARK))                  # Dọc trái trên
    strokes.append((x, y + mid_y, x + w, y + mid_y, RED_DARK))      # Ngang giữa
    strokes.append((x + w, y + mid_y, x + w, y + h, RED_DARK))      # Dọc phải dưới
    strokes.append((x + w, y + h, x, y + h, RED_DARK))              # Ngang dưới

    # 3. Chữ C (Xám)
    x, y = pos(2)
    strokes.append((x + w, y, x, y, GRAY))                          # Ngang trên
    strokes.append((x, y, x, y + h, GRAY))                          # Dọc trái
    strokes.append((x, y + h, x + w, y + h, GRAY))                  # Ngang dưới

    # 4. Chữ E (Xám)
    x, y = pos(3)
    strokes.append((x + w, y, x, y, GRAY))                          # Ngang trên
    strokes.append((x, y, x, y + h, GRAY))                          # Dọc trái
    strokes.append((x, y + h, x + w, y + h, GRAY))                  # Ngang dưới
    strokes.append((x, y + mid_y, x + w, y + mid_y, GRAY))          # Ngang giữa

    # 5. Chữ N - dáng chữ Π giống ảnh (Xám)
    x, y = pos(4)
    strokes.append((x, y + h, x, y, GRAY))                          # Dọc trái (dưới -> lên)
    strokes.append((x, y, x + w, y, GRAY))                          # Ngang trên
    strokes.append((x + w, y, x + w, y + h, GRAY))                  # Dọc phải (trên -> xuống)

    # 6. Chữ D - dáng khung chữ nhật giống ảnh (Xám)
    x, y = pos(5)
    strokes.append((x, y, x, y + h, GRAY))                          # Dọc trái
    strokes.append((x, y + h, x + w, y + h, GRAY))                  # Ngang dưới
    strokes.append((x + w, y + h, x + w, y, GRAY))                  # Dọc phải
    strokes.append((x + w, y, x, y, GRAY))                          # Ngang trên

    return strokes

def create_video():
    strokes = get_letter_strokes()
    
    # Tính độ dài từng nét để tốc độ vẽ luôn đều nhau
    lengths = [math.hypot(x2 - x1, y2 - y1) for (x1, y1, x2, y2, _) in strokes]
    total_length = sum(lengths)

    # Khởi tạo trình xuất video MP4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, (WIDTH, HEIGHT))

    total_frames = int(TOTAL_DURATION * FPS)
    draw_frames = int(DRAW_DURATION * FPS)

    for frame_idx in range(total_frames):
        # Tạo khung hình nền trắng
        frame = np.full((HEIGHT, WIDTH, 3), BG_COLOR, dtype=np.uint8)

        # Tính tiến độ vẽ (từ 0.0 đến 1.0)
        progress = min(1.0, frame_idx / draw_frames)
        current_dist = progress * total_length

        accumulated = 0.0
        for (x1, y1, x2, y2, color), length in zip(strokes, lengths):
            if current_dist >= accumulated + length:
                # Vẽ trọn vẹn nét đã hoàn thành
                cv2.line(frame, (x1, y1), (x2, y2), color, THICKNESS, lineType=cv2.LINE_AA)
            elif current_dist > accumulated:
                # Vẽ một phần nét đang chạy
                ratio = (current_dist - accumulated) / length
                curr_x = int(x1 + (x2 - x1) * ratio)
                curr_y = int(y1 + (y2 - y1) * ratio)
                cv2.line(frame, (x1, y1), (curr_x, curr_y), color, THICKNESS, lineType=cv2.LINE_AA)
                break
            accumulated += length

        out.write(frame)

    out.release()
    print(f"Đã tạo xong video: {OUTPUT_FILE}")

if __name__ == "__main__":
    create_video()