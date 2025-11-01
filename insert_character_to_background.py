from PIL import Image

# Mở ảnh nền và ảnh nhân vật
background = Image.open("gradient_image.jpg").convert("RGBA")
character = Image.open("main_character.png").convert("RGBA")

# Lấy kích thước ảnh
bg_width, bg_height = background.size
char_width, char_height = character.size

# Tính vị trí để đặt nhân vật vào giữa ảnh nền
x = (bg_width - char_width) // 2
y = (bg_height - char_height) // 2

# Dán nhân vật vào ảnh nền (giữ alpha trong suốt)
background.paste(character, (x, y), character)

# Lưu kết quả
background.save("combined-image.png", format="PNG")

print("Đã chèn nhân vật vào ảnh nền và lưu thành combined-image.png")
