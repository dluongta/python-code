import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle
from matplotlib.path import Path

# Màu cam đậm → cam nhạt
start_color = np.array([1.0, 0.4, 0.0])  # Cam đậm
end_color   = np.array([1.0, 0.8, 0.6])  # Cam nhạt


# === Gradient theo đường chéo cho bất kỳ hình dạng nào === #
def draw_shape_with_diagonal_gradient(filename, shape_path_func, bounds, resolution=500):
    # Grid tọa độ ảnh
    x = np.linspace(bounds[0], bounds[1], resolution)
    y = np.linspace(bounds[2], bounds[3], resolution)
    X, Y = np.meshgrid(x, y)

    # Tạo gradient theo đường chéo
    gradient = (X + Y - X.min() - Y.min()) / (X.max() + Y.max() - X.min() - Y.min())
    gradient = np.clip(gradient, 0, 1)

    # Mask điểm bên trong hình
    points = np.stack((X.flatten(), Y.flatten()), axis=-1)
    shape_path = shape_path_func()
    mask = shape_path.contains_points(points).reshape(resolution, resolution)

    # Tạo ảnh RGBA từ gradient + mask
    image = np.ones((resolution, resolution, 4))
    for i in range(3):  # RGB channels
        image[..., i] = start_color[i] * (1 - gradient) + end_color[i] * gradient
    image[..., 3] = mask.astype(float)  # Alpha (mask)

    # Vẽ ảnh
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(image, extent=bounds)
    ax.set_xlim(bounds[0], bounds[1])
    ax.set_ylim(bounds[2], bounds[3])
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Saved: {filename}")
    


# === Hàm tạo hình === #

# 1. Hình chữ nhật
def rectangle_path():
    rect = Rectangle((-1, -0.5), 2, 1)
    return Path(rect.get_verts())

# 2. Hình tròn
def circle_path():
    circle = Circle((0, 0), 1)
    return Path.circle(center=(0, 0), radius=1)

# 3. Hình lục giác
def hexagon_path():
    angles = np.linspace(0, 2 * np.pi, 7)
    x = np.cos(angles)
    y = np.sin(angles)
    return Path(np.column_stack((x, y)))

# === Vẽ và lưu === #
# draw_shape_with_diagonal_gradient("circle_gradient.png", circle_path, bounds=(-1.2, 1.2, -1.2, 1.2))
draw_shape_with_diagonal_gradient("rectangle_gradient.png", rectangle_path, bounds=(-1.2, 1.2, -0.8, 0.8))
draw_shape_with_diagonal_gradient("hexagon_gradient.png", hexagon_path, bounds=(-1.2, 1.2, -1.2, 1.2))
# Màu gradient từ cam đậm → cam nhạt
start_color = np.array([1.0, 0.4, 0.0])
end_color   = np.array([1.0, 0.8, 0.6])

def draw_circle_diagonal_gradient(filename, radius=1.0, resolution=1000):
    # Grid điểm ảnh
    x = np.linspace(-radius, radius, resolution)
    y = np.linspace(-radius, radius, resolution)
    X, Y = np.meshgrid(x, y)

    # Tạo mask tròn chính xác bằng công thức (x^2 + y^2 <= r^2)
    mask = (X**2 + Y**2) <= radius**2

    # Tạo gradient theo đường chéo
    gradient = (X + Y - X.min() - Y.min()) / (X.max() + Y.max() - X.min() - Y.min())
    gradient = np.clip(gradient, 0, 1)

    # Tạo ảnh RGBA
    image = np.ones((resolution, resolution, 4))
    for i in range(3):
        image[..., i] = start_color[i] * (1 - gradient) + end_color[i] * gradient
    image[..., 3] = mask.astype(float)

    # Vẽ ảnh
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(image, extent=(-radius, radius, -radius, radius))
    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_aspect('equal')
    ax.axis('off')

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', transparent=True)
    plt.close()
    print(f"Saved: {filename}")

# Chạy hàm
draw_circle_diagonal_gradient("circle_gradient.png")