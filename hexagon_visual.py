import cv2
import numpy as np
import math

# --- CẤU HÌNH ---
WIDTH, HEIGHT = 1920, 1080
FPS = 30
DURATION = 10
CENTER = (WIDTH // 2, HEIGHT // 2)
MAX_RADIUS = 2800

COLOR_ORANGE_GLOW = (0, 100, 255)
COLOR_ORANGE_CORE = (100, 200, 255)

class Hexagon:
    def __init__(self):
        self.radius = 5.0
        
    def update(self):
        self.radius *= 1.06

class RadialSegment:
    def __init__(self, angle):
        self.angle = angle
        self.radius = 20
        
    def update(self):
        self.radius *= 1.08

def get_hexagon_points(center, radius):
    points = []
    for i in range(6):
        angle_deg = 60 * i - 30
        angle_rad = math.radians(angle_deg)
        x = int(center[0] + radius * math.cos(angle_rad))
        y = int(center[1] + radius * math.sin(angle_rad))
        points.append([x, y])
    return np.array(points, np.int32).reshape((-1, 1, 2))

def draw_rectangular_segment(img, angle, r1, r2, thickness, color):
    """Vẽ đường thẳng dạng hình chữ nhật sắc cạnh (không bo góc)"""
    # Vector pháp tuyến để tạo độ dày
    dx = math.cos(angle)
    dy = math.sin(angle)
    nx = -dy * (thickness / 2)
    ny = dx * (thickness / 2)

    # 4 góc của hình chữ nhật
    p1 = [CENTER[0] + r1 * dx + nx, CENTER[1] + r1 * dy + ny]
    p2 = [CENTER[0] + r1 * dx - nx, CENTER[1] + r1 * dy - ny]
    p3 = [CENTER[0] + r2 * dx - nx, CENTER[1] + r2 * dy - ny]
    p4 = [CENTER[0] + r2 * dx + nx, CENTER[1] + r2 * dy + ny]

    pts = np.array([p1, p2, p3, p4], np.int32)
    cv2.fillPoly(img, [pts], color)

def create_video():
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('hexagon_visual.mp4', fourcc, FPS, (WIDTH, HEIGHT))

    hexagons = []
    segments = []
    total_frames = FPS * DURATION
    
    spawn_hex = 20
    spawn_segments = 8
    # Số lượng tia tỏa ra từ tâm
    segment_angles = np.linspace(0, 2*np.pi, 24, endpoint=False)

    print("Đang tạo video với các khối hình chữ nhật...")

    for frame_count in range(total_frames):
        frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
        glow_layer = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

        # Spawn vật thể
        if frame_count % spawn_hex == 0:
            hexagons.append(Hexagon())
        if frame_count % spawn_segments == 0:
            for a in segment_angles:
                segments.append(RadialSegment(a))

        # 1. VẼ HEXAGON (Giữ nguyên polylines vì là hình khép kín)
        for hex_obj in hexagons:
            hex_obj.update()
            pts = get_hexagon_points(CENTER, hex_obj.radius)
            
            # Glow
            thick_g = int(hex_obj.radius * 0.05) + 5
            cv2.polylines(glow_layer, [pts], True, COLOR_ORANGE_GLOW, thick_g)
            # Core
            thick_c = int(hex_obj.radius * 0.01) + 1
            cv2.polylines(frame, [pts], True, COLOR_ORANGE_CORE, thick_c)

        # 2. VẼ RADIAL SEGMENTS (Dạng hình chữ nhật)
        for seg in segments:
            seg.update()
            
            # Tính toán độ dài và độ dày theo khoảng cách (perspective)
            r1 = seg.radius
            r2 = seg.radius + (seg.radius * 0.2) + 50 # Chiều dài mảnh tăng dần khi ra xa
            
            thickness = int(seg.radius * 0.05) + 8

            # Vẽ vào lớp glow (to hơn để tỏa sáng)
            draw_rectangular_segment(glow_layer, seg.angle, r1, r2, thickness + 15, COLOR_ORANGE_GLOW)
            # Vẽ vào lớp chính
            draw_rectangular_segment(frame, seg.angle, r1, r2, thickness, COLOR_ORANGE_CORE)

        # Dọn dẹp bộ nhớ
        hexagons = [h for h in hexagons if h.radius < MAX_RADIUS]
        segments = [s for s in segments if s.radius < MAX_RADIUS]

        # Hiệu ứng Glow mượt mà
        glow_layer = cv2.GaussianBlur(glow_layer, (45, 45), 0)
        final_frame = cv2.addWeighted(frame, 1.0, glow_layer, 1.2, 0)

        out.write(final_frame)

        if frame_count % 30 == 0:
            print(f"Tiến độ: {frame_count}/{total_frames}")

    out.release()
    print("Hoàn thành! Video đã lưu thành: hexagon_visual.mp4")

if __name__ == "__main__":
    create_video()