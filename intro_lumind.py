import cv2
import numpy as np

# ========== CẤU HÌNH ==========
WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (255, 255, 255)

RED_DARK = (0, 0, 180)   # đỏ thẫm (BGR)
GRAY = (120, 120, 120)   # xám

LINE_THICKNESS = 16

FRAME_DELAY = 10
END_HOLD_FRAMES = 180

FPS = 30
VIDEO_NAME = "dluongta_logo.mp4"


# ========== LỚP NÉT VẼ ==========
class Stroke:
    def __init__(self, p1, p2, color):
        self.p1 = p1
        self.p2 = p2
        self.color = color
        self.step = 0
        self.done = False

    def draw_next(self, canvas):
        if self.done:
            cv2.line(canvas, self.p1, self.p2, self.color, LINE_THICKNESS, cv2.LINE_AA)
            return

        t = self.step / FRAME_DELAY
        if t >= 1:
            cv2.line(canvas, self.p1, self.p2, self.color, LINE_THICKNESS, cv2.LINE_AA)
            self.done = True
            return

        x = int(self.p1[0] + (self.p2[0] - self.p1[0]) * t)
        y = int(self.p1[1] + (self.p2[1] - self.p1[1]) * t)

        cv2.line(canvas, self.p1, (x, y), self.color, LINE_THICKNESS, cv2.LINE_AA)

        self.step += 1


# ========== TẠO CHỮ (CHỈ NÉT THẲNG) ==========
def get_letter_strokes(x_offset):
    letters = {}

    size = 140
    spacing = 60
    y = HEIGHT // 2
    x = x_offset

    def L(p1, p2, color):
        return Stroke(p1, p2, color)

    # ===== T (đỏ) =====
    letters["T"] = [
        L((x, y - size), (x + size, y - size), RED_DARK),
        L((x + size//2, y - size), (x + size//2, y + size), RED_DARK),
    ]
    x += size + spacing

    # ===== S (đỏ - dạng vuông) =====
    letters["S"] = [
        L((x + size, y - size), (x, y - size), RED_DARK),
        L((x, y - size), (x, y), RED_DARK),
        L((x, y), (x + size, y), RED_DARK),
        L((x + size, y), (x + size, y + size), RED_DARK),
        L((x + size, y + size), (x, y + size), RED_DARK),
    ]
    x += size + spacing

    # ===== C =====
    letters["C"] = [
        L((x + size, y - size), (x, y - size), GRAY),
        L((x, y - size), (x, y + size), GRAY),
        L((x, y + size), (x + size, y + size), GRAY),
    ]
    x += size + spacing

    # ===== E =====
    letters["E"] = [
        L((x, y - size), (x, y + size), GRAY),
        L((x, y - size), (x + size, y - size), GRAY),
        L((x, y), (x + size, y), GRAY),
        L((x, y + size), (x + size, y + size), GRAY),
    ]
    x += size + spacing

    # ===== N =====
    letters["N"] = [
        L((x, y + size), (x, y - size), GRAY),
        L((x, y - size), (x + size, y + size), GRAY),
        L((x + size, y + size), (x + size, y - size), GRAY),
    ]
    x += size + spacing

    # ===== D ===== (vuông, không cong)
    letters["D"] = [
        L((x, y - size), (x, y + size), GRAY),
        L((x, y - size), (x + size, y - size), GRAY),
        L((x + size, y - size), (x + size, y + size), GRAY),
        L((x + size, y + size), (x, y + size), GRAY),
    ]

    return letters


# ========== CĂN GIỮA ==========
def calculate_center_offset():
    size = 140
    spacing = 60
    total_width = 6 * size + 5 * spacing
    return (WIDTH - total_width) // 2


# ========== VẼ ==========
def draw_all(canvas, letters):
    strokes = []

    for ch in "TSCEND":
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
frames = draw_all(canvas, letters)

h, w, _ = frames[0].shape

out = cv2.VideoWriter(
    VIDEO_NAME,
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (w, h)
)

for f in frames:
    out.write(f)

out.release()

print("Đã tạo video:", VIDEO_NAME)