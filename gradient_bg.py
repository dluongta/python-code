import numpy as np
from PIL import Image

def generate_insta_bg_final(filename="bg-1.png", width=1920, height=1080, is_jpeg=False):
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    u, v = np.meshgrid(x, y)
    
    u_exp = u[:, :, np.newaxis]
    v_exp = v[:, :, np.newaxis]
    
    # --- ĐÃ SỬA MÀU Ở ĐÂY ---
    magenta_top_left = np.array([230, 25, 155], dtype=np.float32) # Đổi từ xanh tím sang Hồng magenta
    magenta          = np.array([230, 25, 155], dtype=np.float32) # Hồng magenta (trên phải/giữa)
    orange_red       = np.array([255, 75, 20], dtype=np.float32)  # Cam đậm / đỏ cam
    yellow_gold      = np.array([255, 215, 10], dtype=np.float32) # Vàng sáng rực
    
    mix_factor = np.clip(u_exp * 1.6 + v_exp * 0.3, 0, 1)
    top_layer = (1 - mix_factor) * magenta_top_left + mix_factor * magenta
    # ------------------------
    
    if width > height:
        dist_yellow = np.sqrt(((u - 0.2) * 0.7)**2 + ((v - 1.15) * 1.3)**2)
        dist_yellow_exp = dist_yellow[:, :, np.newaxis]
        
        w_yellow = np.clip(1.0 - dist_yellow_exp / 0.7, 0, 1)
        w_yellow = w_yellow**2 * (3 - 2 * w_yellow)  # Làm mượt Smoothstep
        
        dist_orange = np.sqrt(((u - 0.4) * 0.8)**2 + ((v - 1.1) * 1.1)**2)
        dist_orange_exp = dist_orange[:, :, np.newaxis]
        
        w_orange = np.clip(1.0 - dist_orange_exp / 1.2, 0, 1) - w_yellow * 0.8
        w_orange = np.clip(w_orange, 0, 1)
        w_orange = w_orange**1.5 * (3 - 2 * w_orange)
        
    else:
        aspect = width / height
        dist = np.sqrt(((u - 0.35) * aspect)**2 + (v - 1.15)**2)
        dist_exp = dist[:, :, np.newaxis]
        
        w_yellow = np.clip(1.0 - dist_exp / 0.7, 0, 1)
        w_yellow = w_yellow**2 * (3 - 2 * w_yellow)
        
        w_orange = np.clip(1.0 - dist_exp / 1.2, 0, 1) - w_yellow
        w_orange = np.clip(w_orange, 0, 1)
        w_orange = w_orange**1.5 * (3 - 2 * w_orange)
        
    w_top = np.clip(1.0 - w_yellow - w_orange, 0, 1)
    
    total_w = w_top + w_orange + w_yellow + 1e-5
    w_top /= total_w
    w_orange /= total_w
    w_yellow /= total_w
    
    gradient = w_top * top_layer + w_orange * orange_red + w_yellow * yellow_gold
    
    np.random.seed(42)
    noise = np.random.normal(scale=1.2, size=gradient.shape).astype(np.float32)
    gradient = np.clip(gradient + noise, 0, 255).astype(np.uint8)
    
    img = Image.fromarray(gradient)
    if is_jpeg:
        img.save(filename, "JPEG", quality=98, subsampling=0)
    else:
        img.save(filename, "PNG", quality=100)
    print(f"✅ Đã xuất ảnh thành công: {filename} ({width}x{height})")

if __name__ == "__main__":
    generate_insta_bg_final("bg-1-1.png", width=1920, height=1080, is_jpeg=False)
    generate_insta_bg_final("bg-2-1.png", width=1080, height=1920, is_jpeg=True)