import numpy as np
from PIL import Image

def generate_insta_bg_final(filename="bg-1.png", width=1920, height=1080, is_jpeg=False):
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    u, v = np.meshgrid(x, y)
    
    u_exp = u[:, :, np.newaxis]
    v_exp = v[:, :, np.newaxis]
    
    # --- ĐÃ CẬP NHẬT 4 LỚP MÀU TỪ DƯỚI LÊN TRÊN ---
    yellow_orange    = np.array([255, 190, 15], dtype=np.float32) # Lớp 1 (Dưới cùng): Cam vàng
    bright_orange    = np.array([255, 135, 15], dtype=np.float32) # Lớp 2: Cam tươi
    orange_red       = np.array([255, 75, 20], dtype=np.float32)  # Lớp 3: Đỏ cam
    
    # Lớp 4 (Trên cùng) - Giữ nguyên dải Đỏ hồng/Đỏ cam của bạn
    magenta_top_left = np.array([255, 30, 90], dtype=np.float32) # Đỏ hồng
    magenta          = np.array([255, 30, 90], dtype=np.float32) # Đỏ cam
    # -----------------------------------------------
    
    mix_factor = np.clip(u_exp * 1.6 + v_exp * 0.3, 0, 1)
    top_layer = (1 - mix_factor) * magenta_top_left + mix_factor * magenta
    
    # Tính toán tọa độ ĐỐI XỨNG và phân bổ độ lan tỏa cho 4 lớp
    if width > height:
        # 1. Lan tỏa của Cam vàng (ở đáy)
        dist_yo = np.sqrt(((u - 0.5) * 0.6)**2 + ((v - 1.15) * 1.5)**2)
        dist_yo_exp = dist_yo[:, :, np.newaxis]
        
        w_yo = np.clip(1.0 - dist_yo_exp / 0.5, 0, 1)
        w_yo = w_yo**2 * (3 - 2 * w_yo)
        
        # 2. Lan tỏa của Cam tươi
        dist_bo = np.sqrt(((u - 0.5) * 0.7)**2 + ((v - 1.1) * 1.2)**2)
        dist_bo_exp = dist_bo[:, :, np.newaxis]
        
        w_bo = np.clip(1.0 - dist_bo_exp / 0.9, 0, 1) - w_yo * 0.85
        w_bo = np.clip(w_bo, 0, 1)
        w_bo = w_bo**1.5 * (3 - 2 * w_bo)
        
        # 3. Lan tỏa của Đỏ cam
        dist_or = np.sqrt(((u - 0.5) * 0.8)**2 + ((v - 1.05) * 1.0)**2)
        dist_or_exp = dist_or[:, :, np.newaxis]
        
        w_or = np.clip(1.0 - dist_or_exp / 1.4, 0, 1) - (w_bo + w_yo) * 0.75
        w_or = np.clip(w_or, 0, 1)
        w_or = w_or**1.5 * (3 - 2 * w_or)
        
    else:
        aspect = width / height
        dist = np.sqrt(((u - 0.5) * aspect)**2 + (v - 1.15)**2)
        dist_exp = dist[:, :, np.newaxis]
        
        # 1. Cam vàng
        w_yo = np.clip(1.0 - dist_exp / 0.45, 0, 1)
        w_yo = w_yo**2 * (3 - 2 * w_yo)
        
        # 2. Cam tươi
        w_bo = np.clip(1.0 - dist_exp / 0.8, 0, 1) - w_yo * 0.85
        w_bo = np.clip(w_bo, 0, 1)
        w_bo = w_bo**1.5 * (3 - 2 * w_bo)
        
        # 3. Đỏ cam
        w_or = np.clip(1.0 - dist_exp / 1.3, 0, 1) - (w_bo + w_yo) * 0.75
        w_or = np.clip(w_or, 0, 1)
        w_or = w_or**1.5 * (3 - 2 * w_or)
        
    # 4. Trọng số lớp trên cùng (phần còn lại)
    w_top = np.clip(1.0 - w_yo - w_bo - w_or, 0, 1)
    
    # Chuẩn hóa tổng trọng số luôn bằng 1
    total_w = w_top + w_or + w_bo + w_yo + 1e-5
    w_top /= total_w
    w_or /= total_w
    w_bo /= total_w
    w_yo /= total_w
    
    # Trộn 4 lớp màu
    gradient = w_top * top_layer + w_or * orange_red + w_bo * bright_orange + w_yo * yellow_orange
    
    # Thêm nhiễu hạt để khử banding (phân lớp màu)
    np.random.seed(42)
    noise = np.random.normal(scale=1.2, size=gradient.shape).astype(np.float32)
    gradient = np.clip(gradient + noise, 0, 255).astype(np.uint8)
    
    # Xuất ảnh
    img = Image.fromarray(gradient)
    if is_jpeg:
        img.save(filename, "JPEG", quality=98, subsampling=0)
    else:
        img.save(filename, "PNG", quality=100)
    print(f"✅ Đã xuất ảnh thành công: {filename} ({width}x{height})")

if __name__ == "__main__":
    generate_insta_bg_final("bg-1-1.png", width=1920, height=1080, is_jpeg=False)
    generate_insta_bg_final("bg-2-1.png", width=1080, height=1920, is_jpeg=True)