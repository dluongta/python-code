import numpy as np
from PIL import Image

def generate_insta_bg_final(filename="bg-1.png", width=1920, height=1080, is_jpeg=False):
    # 1. Tạo lưới tọa độ chuẩn hóa (0 -> 1)
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    u, v = np.meshgrid(x, y)
    
    u_exp = u[:, :, np.newaxis]
    v_exp = v[:, :, np.newaxis]
    
    # 2. Bộ màu chuẩn Instagram rực rỡ
    blue_purple = np.array([65, 80, 245], dtype=np.float32)   # Xanh tím (trên trái)
    magenta     = np.array([230, 25, 155], dtype=np.float32)  # Hồng magenta (trên phải/giữa)
    orange_red  = np.array([255, 75, 20], dtype=np.float32)   # Cam đậm / đỏ cam (lan rộng bên phải/lên trên)
    yellow_gold = np.array([255, 215, 10], dtype=np.float32)  # Vàng sáng rực (vòng ngang dưới trái)
    
    # 3. Lớp nền phía trên: Ép xanh tím góc trên trái, không lan sang phải
    # - Nhân u_exp với 1.6 để rút ngắn độ lan sang phải (chuyển sang magenta nhanh hơn)
    # - Cộng thêm v_exp * 0.3 để ép xanh tím không tràn xuống dưới
    mix_factor = np.clip(u_exp * 1.6 + v_exp * 0.3, 0, 1)
    top_layer = (1 - mix_factor) * blue_purple + mix_factor * magenta
    
    # 4. Phân tách thuật toán tự động theo tỉ lệ khung hình
    if width > height:
        # --- DÀNH CHO ẢNH NGANG (1920x1080) ---
        dist_yellow = np.sqrt(((u - 0.2) * 0.7)**2 + ((v - 1.15) * 1.3)**2)
        dist_yellow_exp = dist_yellow[:, :, np.newaxis]
        
        w_yellow = np.clip(1.0 - dist_yellow_exp / 0.55, 0, 1)
        w_yellow = w_yellow**2 * (3 - 2 * w_yellow)  # Làm mượt Smoothstep
        
        dist_orange = np.sqrt(((u - 0.4) * 0.8)**2 + ((v - 1.1) * 1.1)**2)
        dist_orange_exp = dist_orange[:, :, np.newaxis]
        w_orange = np.clip(1.0 - dist_orange_exp / 0.95, 0, 1) - w_yellow * 0.8
        w_orange = np.clip(w_orange, 0, 1)
        w_orange = w_orange**1.5 * (3 - 2 * w_orange)
        
    else:
        # --- DÀNH CHO ẢNH DỌC (1080x1920) ---
        aspect = width / height
        dist = np.sqrt(((u - 0.35) * aspect)**2 + (v - 1.15)**2)
        dist_exp = dist[:, :, np.newaxis]
        
        w_yellow = np.clip(1.0 - dist_exp / 0.55, 0, 1)
        w_yellow = w_yellow**2 * (3 - 2 * w_yellow)
        
        w_orange = np.clip(1.0 - dist_exp / 0.95, 0, 1) - w_yellow
        w_orange = np.clip(w_orange, 0, 1)
        w_orange = w_orange**1.5 * (3 - 2 * w_orange)
        
    # 5. Trọng số phần trên cùng (Xanh tím / Hồng)
    w_top = np.clip(1.0 - w_yellow - w_orange, 0, 1)
    
    # Chuẩn hóa tổng trọng số để các màu hòa quyện tuyệt đối 100%
    total_w = w_top + w_orange + w_yellow + 1e-5
    w_top /= total_w
    w_orange /= total_w
    w_yellow /= total_w
    
    # Tổng hợp màu sắc
    gradient = w_top * top_layer + w_orange * orange_red + w_yellow * yellow_gold
    
    # 6. Thêm hạt nhiễu mịn (noise) để chống hiện tượng vỡ dải màu (Color banding)
    np.random.seed(42)
    noise = np.random.normal(scale=1.2, size=gradient.shape).astype(np.float32)
    gradient = np.clip(gradient + noise, 0, 255).astype(np.uint8)
    
    # 7. Lưu file ảnh
    img = Image.fromarray(gradient)
    if is_jpeg:
        # subsampling=0 giúp giữ nguyên độ rực rỡ cho sắc cam/đỏ trên định dạng JPG
        img.save(filename, "JPEG", quality=98, subsampling=0)
    else:
        img.save(filename, "PNG", quality=100)
    print(f"✅ Đã xuất ảnh thành công: {filename} ({width}x{height})")

if __name__ == "__main__":
    # Tạo ảnh ngang (Full HD 1920x1080 - PNG)
    generate_insta_bg_final("bg-1-2.png", width=1920, height=1080, is_jpeg=False)
    
    # Tạo ảnh dọc (Story/Reels 1080x1920 - JPG chất lượng cao)
    generate_insta_bg_final("bg-2-2.jpg", width=1080, height=1920, is_jpeg=True)