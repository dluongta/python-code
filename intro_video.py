import cv2
import numpy as np
import random

# --- CẤU HÌNH VIDEO FULL HD ---
W, H = 1920, 1080         # Độ phân giải Full HD (16:9)
cx, cy = W // 2, H // 2   # Tọa độ tâm màn hình
fps = 30                  # Số khung hình trên giây
duration = 30             # Thời lượng video (giây)
total_frames = fps * duration

# Khởi tạo công cụ ghi video chất lượng cao
out = cv2.VideoWriter('intro_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (W, H))

# --- MÀU SẮC TƯƠI SÁNG (Định dạng BGR) ---
colors = [
    (180, 105, 255), # Hồng tươi
    (0, 255, 255),   # Vàng
    (255, 255, 0),   # Xanh Cyan (Xanh lơ)
    (0, 165, 255),   # Cam
    (255, 100, 100), # Xanh dương nhạt
    (200, 200, 255)  # Trắng hồng
]

# --- HÀM VẼ HÌNH ẢNH ---
def draw_flower(img, x, y, size, color):
    """Vẽ một bông hoa sắc nét"""
    for angle in range(0, 360, 60):
        rad = np.deg2rad(angle)
        px = int(x + np.cos(rad) * size * 0.7)
        py = int(y + np.sin(rad) * size * 0.7)
        cv2.circle(img, (px, py), int(size * 0.5), color, -1, lineType=cv2.LINE_AA)
    cv2.circle(img, (int(x), int(y)), int(size * 0.4), (0, 255, 255), -1, lineType=cv2.LINE_AA)

def draw_leaf(img, x, y, size):
    """Vẽ một chiếc lá bầu dục"""
    cv2.ellipse(img, (int(x), int(y)), (int(size), int(size * 0.3)), 45, 0, 360, (50, 205, 50), -1, lineType=cv2.LINE_AA)

# --- LOGIC CHUYỂN ĐỘNG ---
particles = []
waves = [0, 150, 300, 450, 600, 750, 900] 
v_emit = 5   
v_side = 6   

print("Đang tiến hành tạo video Full HD...")

for frame in range(total_frames):
    # Tạo nền trắng (Màu 255, 255, 255)
    img = np.full((H, W, 3), 255, dtype=np.uint8)

    # --- ĐÃ XÓA CÁC ĐƯỜNG KẺ Ở ĐÂY ĐỂ CHÚNG KHÔNG HIỆN LÊN ---
    # Nếu bạn muốn chúng màu trắng, có thể dùng (255, 255, 255) nhưng xóa đi là cách tốt nhất.
    # cv2.line(img, (0, cy), (W, cy), (255, 255, 255), 1, lineType=cv2.LINE_AA)
    # cv2.line(img, (cx, 0), (cx, H), (255, 255, 255), 1, lineType=cv2.LINE_AA)
    # cv2.line(img, (0, 0), (W, H), (255, 255, 255), 1, lineType=cv2.LINE_AA)
    # cv2.line(img, (W, 0), (0, H), (255, 255, 255), 1, lineType=cv2.LINE_AA)

    # Cập nhật vị trí các làn sóng và sinh ra hoa/lá
    for i in range(len(waves)):
        waves[i] += v_emit
        if waves[i] > 1000: 
            waves[i] = 0 

        d = waves[i]
        
        if frame % 3 == 0:
            size = random.randint(14, 24) 
            p_type = 'flower' if random.random() > 0.3 else 'leaf'
            color = random.choice(colors)

            if cy - d >= 0:
                particles.append({'x': cx, 'y': cy - d, 'vx': -v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})
                particles.append({'x': cx, 'y': cy - d, 'vx': v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})

            if cy + d <= H:
                particles.append({'x': cx, 'y': cy + d, 'vx': -v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})
                particles.append({'x': cx, 'y': cy + d, 'vx': v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})

            if cx - d >= 0:
                particles.append({'x': cx - d, 'y': cy, 'vx': 0, 'vy': -v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})
                particles.append({'x': cx - d, 'y': cy, 'vx': 0, 'vy': v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})

            if cx + d <= W:
                particles.append({'x': cx + d, 'y': cy, 'vx': 0, 'vy': -v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})
                particles.append({'x': cx + d, 'y': cy, 'vx': 0, 'vy': v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})

    # Cập nhật hạt
    new_particles = []
    for p in particles:
        p['x'] += p['vx']
        p['y'] += p['vy']

        dx_dist = abs(p['x'] - cx)
        dy_dist = abs(p['y'] - cy)

        keep = True
        # Logic: Hạt biến mất khi chạm tới đường chéo ảo góc 45 độ
        if p['axis'] == 'y' and dx_dist >= dy_dist:
            keep = False
        elif p['axis'] == 'x' and dy_dist >= dx_dist:
            keep = False
            
        if p['x'] < 0 or p['x'] > W or p['y'] < 0 or p['y'] > H:
            keep = False

        if keep:
            new_particles.append(p)
            if p['type'] == 'flower':
                draw_flower(img, p['x'], p['y'], p['size'], p['color'])
            else:
                draw_leaf(img, p['x'], p['y'], p['size'])

    particles = new_particles
    out.write(img)

out.release()
print("Hoàn tất! Video 'intro_video.mp4' không hiện đường kẻ đã được tạo.")