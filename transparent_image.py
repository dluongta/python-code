from PIL import Image

def remove_white_background(image_path, output_path):
    # Mở ảnh
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        # Nếu pixel gần như trắng (có thể tùy chỉnh ngưỡng)
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            # Thay bằng pixel trong suốt
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(output_path, "PNG")
    print(f"Saved file: {output_path}")

# Sử dụng hàm
remove_white_background("result.png", "output_image.png")
