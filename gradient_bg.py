import numpy as np
from PIL import Image

def generate_insta_bg_final(filename="bg-1.png", width=1920, height=1080, is_jpeg=False):
    x = np.linspace(0, 1, width)
    y = np.linspace(0, 1, height)
    u, v = np.meshgrid(x, y)
    
    # Chỉ cần dùng v_exp (trục dọc) vì ta muốn màu xếp theo hàng ngang từ trên xuống
    v_exp = v[:, :, np.newaxis]
    
    blue_purple = np.array([65, 80, 245], dtype=np.float32)   # Xanh tím (trên cùng)
    magenta     = np.array([230, 25, 155], dtype=np.float32)  # Hồng magenta (lớp 2)
    orange_red  = np.array([255, 75, 20], dtype=np.float32)   # Cam đậm / đỏ cam (lớp 3)
    yellow_gold = np.array([255, 215, 10], dtype=np.float32)  # Vàng sáng rực (dưới cùng)
    
    # Chia chiều dọc thành 3 phân khúc cho 4 màu (0 -> 2.999 để tránh lỗi giới hạn ở viền)
    v_scaled = np.clip(v_exp * 3.0, 0.0, 2.9999)
    
    # Lấy phần thập phân để tính tỷ lệ blend (từ 0.0 -> 1.0 trong mỗi phân khúc)
    f = v_scaled % 1.0
    
    # Làm mượt (Smoothstep) để dải gradient hòa quyện tự nhiên hơn
    f = f**2 * (3.0 - 2.0 * f)
    
    # Tạo ma trận chứa giá trị màu
    gradient = np.zeros((height, width, 3), dtype=np.float32)
    
    # Phân khúc 1: Xanh tím -> Magenta
    mask0 = (v_scaled >= 0.0) & (v_scaled < 1.0)
    gradient += mask0 * ((1 - f) * blue_purple + f * magenta)
    
    # Phân khúc 2: Magenta -> Đỏ Cam
    mask1 = (v_scaled >= 1.0) & (v_scaled < 2.0)
    gradient += mask1 * ((1 - f) * magenta + f * orange_red)
    
    # Phân khúc 3: Đỏ Cam -> Vàng Gold
    mask2 = (v_scaled >= 2.0)
    gradient += mask2 * ((1 - f) * orange_red + f * yellow_gold)
    
    # Thêm nhiễu (noise) để khử hiện tượng phân lớp màu (banding) trên gradient
    np.random.seed(42)
    noise = np.random.normal(scale=1.2, size=gradient.shape).astype(np.float32)
    gradient = np.clip(gradient + noise, 0, 255).astype(np.uint8)
    
    # Lưu ảnh
    img = Image.fromarray(gradient)
    if is_jpeg:
        img.save(filename, "JPEG", quality=98, subsampling=0)
    else:
        img.save(filename, "PNG", quality=100)
    print(f"✅ Đã xuất ảnh thành công: {filename} ({width}x{height})")

if __name__ == "__main__":
    generate_insta_bg_final("bg-1-1.png", width=1920, height=1080, is_jpeg=False)
    generate_insta_bg_final("bg-2-1.png", width=1080, height=1920, is_jpeg=True)