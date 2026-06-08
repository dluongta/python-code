import cv2
import numpy as np
import random

# --- CẤU HÌNH VIDEO FULL HD ---
W, H = 1920, 1080         # ĐÃ ĐỔI: Độ phân giải Full HD (16:9)
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

# --- HÀM VẼ HÌNH ẢNH (Tăng kích cỡ size một chút để cân đối với Full HD) ---
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

# ĐÃ ĐỔI: Mở rộng các dải sóng xa hơn để bao phủ màn hình Full HD rộng lớn
waves = [0, 150, 300, 450, 600, 750, 900] 
v_emit = 5   # Đuy trì / tăng tốc độ sóng phát ra dọc theo trục đứng/ngang
v_side = 6   # Tăng tốc độ hoa/lá chạy sang 2 bên để chuyển động mượt mà trên khung hình lớn

print("Đang tiến hành tạo video Full HD (Quá trình này có thể mất vài giây)...")

for frame in range(total_frames):
    # Tạo nền trắng
    img = np.full((H, W, 3), 255, dtype=np.uint8)

    # Vẽ mờ các đường trục và đường chéo hướng dẫn (sử dụng LINE_AA để nét vẽ mượt, không bị răng cưa)
    cv2.line(img, (0, cy), (W, cy), (235, 235, 235), 1, lineType=cv2.LINE_AA)
    cv2.line(img, (cx, 0), (cx, H), (235, 235, 235), 1, lineType=cv2.LINE_AA)
    cv2.line(img, (0, 0), (W, H), (235, 235, 235), 1, lineType=cv2.LINE_AA)
    cv2.line(img, (W, 0), (0, H), (235, 235, 235), 1, lineType=cv2.LINE_AA)

    # Cập nhật vị trí các làn sóng và sinh ra hoa/lá
    for i in range(len(waves)):
        waves[i] += v_emit
        if waves[i] > 1000: # ĐÃ ĐỔI: Tăng giới hạn reset sóng phù hợp với chiều rộng màn hình (W=1920)
            waves[i] = 0 

        d = waves[i]
        
        # Tạo hoa lá mới sau mỗi 3 khung hình
        if frame % 3 == 0:
            size = random.randint(14, 24) # ĐÃ ĐỔI: Tăng kích thước vật thể để hiển thị đẹp trên màn hình lớn
            p_type = 'flower' if random.random() > 0.3 else 'leaf'
            color = random.choice(colors)

            # 1. Từ trục TRÊN, chạy sang trái/phải
            if cy - d >= 0:
                particles.append({'x': cx, 'y': cy - d, 'vx': -v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})
                particles.append({'x': cx, 'y': cy - d, 'vx': v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})

            # 2. Từ trục DƯỚI, chạy sang trái/phải
            if cy + d <= H:
                particles.append({'x': cx, 'y': cy + d, 'vx': -v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})
                particles.append({'x': cx, 'y': cy + d, 'vx': v_side, 'vy': 0, 'type': p_type, 'color': color, 'size': size, 'axis': 'y'})

            # 3. Từ trục TRÁI, chạy lên/xuống
            if cx - d >= 0:
                particles.append({'x': cx - d, 'y': cy, 'vx': 0, 'vy': -v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})
                particles.append({'x': cx - d, 'y': cy, 'vx': 0, 'vy': v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})

            # 4. Từ trục PHẢI, chạy lên/xuống
            if cx + d <= W:
                particles.append({'x': cx + d, 'y': cy, 'vx': 0, 'vy': -v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})
                particles.append({'x': cx + d, 'y': cy, 'vx': 0, 'vy': v_side, 'type': p_type, 'color': color, 'size': size, 'axis': 'x'})

    # Cập nhật và lọc các hạt va chạm đường chéo hoặc ra khỏi màn hình
    new_particles = []
    for p in particles:
        p['x'] += p['vx']
        p['y'] += p['vy']

        dx_dist = abs(p['x'] - cx)
        dy_dist = abs(p['y'] - cy)

        keep = True
        # Điều kiện biến mất khi chạm tới đường chéo góc 45 độ (|x| = |y|)
        if p['axis'] == 'y' and dx_dist >= dy_dist:
            keep = False
        elif p['axis'] == 'x' and dy_dist >= dx_dist:
            keep = False
            
        # Loại bỏ nếu bay hoàn toàn ra ngoài biên màn hình lớn
        if p['x'] < 0 or p['x'] > W or p['y'] < 0 or p['y'] > H:
            keep = False

        if keep:
            new_particles.append(p)
            if p['type'] == 'flower':
                draw_flower(img, p['x'], p['y'], p['size'], p['color'])
            else:
                draw_leaf(img, p['x'], p['y'], p['size'])

    particles = new_particles

    # Ghi từng khung hình chất lượng cao vào video
    out.write(img)

# Hoàn tất tiến trình
out.release()
print("Hoàn tất! Video Full HD 'intro_video.mp4' dài 30s với nền trắng đã được xuất thành công.")