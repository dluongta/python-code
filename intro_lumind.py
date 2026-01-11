import cv2
import numpy as np

# ========== CẤU HÌNH ==========
WIDTH, HEIGHT = 1280, 720
BG_COLOR = (255, 255, 255)
DRAW_COLOR_RED = (0, 0, 160)     # U L
DRAW_COLOR_GRAY = (50, 50, 50)   # MIND
LINE_THICKNESS = 8
FRAME_DELAY = 15
CURVE_FRAME_DELAY = 1
END_HOLD_FRAMES = 30
FPS = 10
VIDEO_NAME = "ulmind_logo.mp4"

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

# ========== TẠO CHỮ ==========
def get_letter_strokes(x_offset):
    letters = {}
    size = 100
    spacing = 50
    y = HEIGHT // 2
    x = x_offset

    def line(p1, p2, color):
        return Stroke([p1, p2], color, FRAME_DELAY)

    # U
    letters['U'] = [
        line((x, y - size), (x, y + size), DRAW_COLOR_RED),
        line((x, y + size), (x + size, y + size), DRAW_COLOR_RED),
        line((x + size, y + size), (x + size, y - size), DRAW_COLOR_RED),
    ]
    x += size + spacing

    # L
    letters['L'] = [
        line((x, y - size), (x, y + size), DRAW_COLOR_RED),
        line((x, y + size), (x + size, y + size), DRAW_COLOR_RED),
    ]
    x += size + spacing

    # M
    m_width = size + 20
    letters['M'] = [
        line((x, y + size), (x, y - size), DRAW_COLOR_GRAY),
        line((x, y - size), (x + m_width // 2, y + size), DRAW_COLOR_GRAY),
        line((x + m_width // 2, y + size), (x + m_width, y - size), DRAW_COLOR_GRAY),
        line((x + m_width, y - size), (x + m_width, y + size), DRAW_COLOR_GRAY),
    ]
    x += m_width + spacing

    # I
    letters['I'] = [
        line((x + size // 2, y - size), (x + size // 2, y + size), DRAW_COLOR_GRAY),
    ]
    x += size + spacing

    # N
    letters['N'] = [
        line((x, y + size), (x, y - size), DRAW_COLOR_GRAY),
        line((x, y - size), (x + size, y + size), DRAW_COLOR_GRAY),
        line((x + size, y + size), (x + size, y - size), DRAW_COLOR_GRAY),
    ]
    x += size + spacing

    # D
    arc = cv2.ellipse2Poly((x, y), (size, size), 0, -90, 90, 15)
    letters['D'] = [
        Stroke([(x, y - size), (x, y + size)], DRAW_COLOR_GRAY, FRAME_DELAY),
        Stroke([tuple(p) for p in arc], DRAW_COLOR_GRAY, CURVE_FRAME_DELAY),
    ]

    return letters

# ========== CĂN GIỮA ==========
def calculate_center_offset():
    size = 100
    spacing = 50
    total_width = 6 * size + 5 * spacing
    return (WIDTH - total_width) // 2

# ========== VẼ SONG SONG ==========
def draw_all_letters_parallel(canvas, letters):
    strokes = []
    for ch in "ULMIND":
        strokes.extend(letters[ch])

    frames = []
    done = False
    while not done:
        done = True
        for s in strokes:
            s.draw_next(canvas)
            if not s.done:
                done = False
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

print("✅ Video đã tạo:", VIDEO_NAME)
