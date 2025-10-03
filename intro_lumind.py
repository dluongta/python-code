import cv2
import numpy as np

# ========== CẤU HÌNH ==========
WIDTH, HEIGHT = 800, 300
BG_COLOR = (255, 255, 255)
DRAW_COLOR_RED = (0, 0, 160)   # Màu đỏ đậm cho "LU"
DRAW_COLOR_GRAY = (50, 50, 50)  # Màu xám cho "MIND"
LINE_THICKNESS = 5
FRAME_DELAY = 15
CURVE_FRAME_DELAY = 0.5
END_HOLD_FRAMES = 30
FPS = 10
VIDEO_NAME = "lumind_logo.mp4"

# ========== LỚP NÉT VẼ ==========
class Stroke:
    def __init__(self, points, color, delay):
        self.points = points
        self.color = color
        self.delay = delay
        self.current_segment = 0
        self.current_step = 0
        self.done = False

    def draw_next(self, canvas):
        if self.done:
            for i in range(1, len(self.points)):
                cv2.line(canvas, self.points[i-1], self.points[i], self.color, LINE_THICKNESS)
            return

        pt1 = self.points[self.current_segment]
        pt2 = self.points[self.current_segment + 1]

        t = self.current_step + 1
        if t > self.delay:
            cv2.line(canvas, pt1, pt2, self.color, LINE_THICKNESS)
            self.current_segment += 1
            self.current_step = 0
            if self.current_segment >= len(self.points) - 1:
                self.done = True
            return
        alpha = t / self.delay
        x = int(pt1[0] * (1 - alpha) + pt2[0] * alpha)
        y = int(pt1[1] * (1 - alpha) + pt2[1] * alpha)
        cv2.line(canvas, pt1, (x, y), self.color, LINE_THICKNESS)
        self.current_step += 1

# ========== HÀM TẠO NÉT CHỮ ==========
def get_letter_strokes(x_offset):
    letters = {}
    y = 150
    size = 60
    spacing = 30
    x = x_offset

    def make_stroke_line(pt1, pt2, color, delay):
        return Stroke([pt1, pt2], color, delay)

    # L
    letters['L'] = [
        make_stroke_line((x, y - size), (x, y + size), DRAW_COLOR_RED, FRAME_DELAY),
        make_stroke_line((x, y + size), (x + size, y + size), DRAW_COLOR_RED, FRAME_DELAY),
    ]

    x += size + spacing

    # U (sửa lại để không thừa đoạn ngắn)
    letters['U'] = [
        make_stroke_line((x, y - size), (x, y + size), DRAW_COLOR_RED, FRAME_DELAY),
        make_stroke_line((x, y + size), (x + size, y + size), DRAW_COLOR_RED, FRAME_DELAY),
        make_stroke_line((x + size, y + size), (x + size, y - size), DRAW_COLOR_RED, FRAME_DELAY),
    ]

    x += size + spacing

    # M
    letters['M'] = [
        make_stroke_line((x, y + size), (x, y - size), DRAW_COLOR_GRAY, FRAME_DELAY),
        make_stroke_line((x, y - size), (x + size // 2, y), DRAW_COLOR_GRAY, FRAME_DELAY),
        make_stroke_line((x + size // 2, y), (x + size, y - size), DRAW_COLOR_GRAY, FRAME_DELAY),
        make_stroke_line((x + size, y - size), (x + size, y + size), DRAW_COLOR_GRAY, FRAME_DELAY),
    ]

    x += size + spacing

    # I (chỉ nét thẳng dọc, tránh thừa đoạn)
    letters['I'] = [
        make_stroke_line((x + size // 2, y - size), (x + size // 2, y + size), DRAW_COLOR_GRAY, FRAME_DELAY),
    ]

    x += size + spacing

    # N
    letters['N'] = [
        make_stroke_line((x, y + size), (x, y - size), DRAW_COLOR_GRAY, FRAME_DELAY),
        make_stroke_line((x, y - size), (x + size, y + size), DRAW_COLOR_GRAY, FRAME_DELAY),
        make_stroke_line((x + size, y + size), (x + size, y - size), DRAW_COLOR_GRAY, FRAME_DELAY),
    ]

    x += size + spacing

    # D
    vertical_line = [(x, y - size), (x, y + size)]
    arc_pts = cv2.ellipse2Poly((x, y), (size, size), 0, -90, 90, 10)
    arc_points = [tuple(pt) for pt in arc_pts]
    curve_stroke = Stroke(arc_points, DRAW_COLOR_GRAY, CURVE_FRAME_DELAY)
    vertical_stroke = Stroke(vertical_line, DRAW_COLOR_GRAY, FRAME_DELAY)
    letters['D'] = [vertical_stroke, curve_stroke]

    return letters

# ========== TÍNH TOÁN CĂN GIỮA ==========
def calculate_center_offset():
    size = 60
    spacing = 30
    total_width = 6 * size + 5 * spacing
    return (WIDTH - total_width) // 2

# ========== VẼ TẤT CẢ CHỮ ĐỒNG THỜI ==========
def draw_all_letters_parallel(canvas, letters):
    all_strokes = []
    for ch in "LUMIND":
        all_strokes.extend(letters[ch])

    frames = []
    all_done = False

    while not all_done:
        all_done = True
        for stroke in all_strokes:
            stroke.draw_next(canvas)
            if not stroke.done:
                all_done = False
        frames.append(canvas.copy())

    for _ in range(END_HOLD_FRAMES):
        frames.append(frames[-1].copy())

    return frames

# ========== MAIN ==========
canvas = np.full((HEIGHT, WIDTH, 3), BG_COLOR, dtype=np.uint8)
letters = get_letter_strokes(calculate_center_offset())
frames = draw_all_letters_parallel(canvas, letters)

h, w, _ = frames[0].shape
out = cv2.VideoWriter(VIDEO_NAME, cv2.VideoWriter_fourcc(*'mp4v'), FPS, (w, h))
for f in frames:
    out.write(f)
out.release()

print(f"✅ Video đã được tạo: {VIDEO_NAME}")
