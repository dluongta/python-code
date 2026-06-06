import cv2
import numpy as np

# ========== CẤU HÌNH ==========
WIDTH, HEIGHT = 1920, 1080
BG_COLOR = (255, 255, 255)

# Cam đậm (BGR)
DRAW_COLOR = (0, 80, 255)

LINE_THICKNESS = 16

FRAME_DELAY = 12
CURVE_FRAME_DELAY = 1

END_HOLD_FRAMES = 60

FPS = 30
VIDEO_NAME = "dluongta_logo.mp4"


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
                cv2.line(
                    canvas,
                    self.points[i - 1],
                    self.points[i],
                    self.color,
                    LINE_THICKNESS,
                    cv2.LINE_AA
                )
            return

        pt1 = self.points[self.current_segment]
        pt2 = self.points[self.current_segment + 1]

        t = self.current_step + 1

        if t > self.delay:
            cv2.line(
                canvas,
                pt1,
                pt2,
                self.color,
                LINE_THICKNESS,
                cv2.LINE_AA
            )

            self.current_segment += 1
            self.current_step = 0

            if self.current_segment >= len(self.points) - 1:
                self.done = True
            return

        alpha = t / self.delay

        x = int(pt1[0] * (1 - alpha) + pt2[0] * alpha)
        y = int(pt1[1] * (1 - alpha) + pt2[1] * alpha)

        cv2.line(
            canvas,
            pt1,
            (x, y),
            self.color,
            LINE_THICKNESS,
            cv2.LINE_AA
        )

        self.current_step += 1


# ========== TẠO CHỮ ==========
def get_letter_strokes(x_offset):
    letters = {}

    size = 140
    spacing = 50

    y = HEIGHT // 2
    x = x_offset

    def line(p1, p2):
        return Stroke([p1, p2], DRAW_COLOR, FRAME_DELAY)

    # D
    arc = cv2.ellipse2Poly(
        (x, y),
        (size, size),
        0,
        -90,
        90,
        5
    )

    letters["D"] = [
        line((x, y - size), (x, y + size)),
        Stroke([tuple(p) for p in arc], DRAW_COLOR, CURVE_FRAME_DELAY),
    ]

    x += size + spacing

    # L
    letters["L"] = [
        line((x, y - size), (x, y + size)),
        line((x, y + size), (x + size, y + size)),
    ]

    x += size + spacing

    # U
    letters["U"] = [
        line((x, y - size), (x, y + size)),
        line((x, y + size), (x + size, y + size)),
        line((x + size, y + size), (x + size, y - size)),
    ]

    x += size + spacing

    # O
    arc_o = cv2.ellipse2Poly(
        (x + size // 2, y),
        (size // 2, size),
        0,
        0,
        360,
        5
    )

    letters["O"] = [
        Stroke([tuple(p) for p in arc_o], DRAW_COLOR, CURVE_FRAME_DELAY)
    ]

    x += size + spacing

    # N
    letters["N"] = [
        line((x, y + size), (x, y - size)),
        line((x, y - size), (x + size, y + size)),
        line((x + size, y + size), (x + size, y - size)),
    ]

    x += size + spacing

    # G
    arc_g = cv2.ellipse2Poly(
        (x + size // 2, y),
        (size // 2, size),
        0,
        0,
        330,
        5
    )

    letters["G"] = [
        Stroke([tuple(p) for p in arc_g], DRAW_COLOR, CURVE_FRAME_DELAY),
        line((x + size // 2, y), (x + size, y)),
    ]

    x += size + spacing

    # T
    letters["T"] = [
        line((x, y - size), (x + size, y - size)),
        line((x + size // 2, y - size), (x + size // 2, y + size)),
    ]

    x += size + spacing

    # A
    letters["A"] = [
        line((x, y + size), (x + size // 2, y - size)),
        line((x + size // 2, y - size), (x + size, y + size)),
        line((x + size // 4, y), (x + 3 * size // 4, y)),
    ]

    return letters


# ========== CĂN GIỮA ==========
def calculate_center_offset():
    size = 140
    spacing = 50

    total_width = 8 * size + 7 * spacing

    return (WIDTH - total_width) // 2


# ========== VẼ SONG SONG ==========
def draw_all_letters_parallel(canvas, letters):
    strokes = []

    for ch in "DLUONGTA":
        strokes.extend(letters[ch])

    frames = []

    done = False

    while not done:
        done = True

        for stroke in strokes:
            stroke.draw_next(canvas)

            if not stroke.done:
                done = False

        frames.append(canvas.copy())

    for _ in range(END_HOLD_FRAMES):
        frames.append(frames[-1].copy())

    return frames


# ========== MAIN ==========
canvas = np.full(
    (HEIGHT, WIDTH, 3),
    BG_COLOR,
    dtype=np.uint8
)

letters = get_letter_strokes(
    calculate_center_offset()
)

frames = draw_all_letters_parallel(
    canvas,
    letters
)

h, w, _ = frames[0].shape

out = cv2.VideoWriter(
    VIDEO_NAME,
    cv2.VideoWriter_fourcc(*"mp4v"),
    FPS,
    (w, h)
)

for frame in frames:
    out.write(frame)

out.release()

print("Đã tạo video:", VIDEO_NAME)