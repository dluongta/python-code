import os
import tkinter as tk
from PIL import Image, ImageDraw
from tkinter import filedialog

class HandwritingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Handwriting Digit Drawer")

        self.canvas_size = 280
        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack()

        # Tạo ảnh trắng để vẽ
        self.image = Image.new('L', (self.canvas_size, self.canvas_size), color='white')
        self.draw = ImageDraw.Draw(self.image)

        self.last_x, self.last_y = None, None
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        # Nút Clear
        self.clear_button = tk.Button(master, text='Clear', command=self.clear_canvas)
        self.clear_button.pack()

        # Nút Save (chỉ lưu ảnh)
        self.save_button = tk.Button(master, text='Save Image', command=self.save_image)
        self.save_button.pack()

    def paint(self, event):
        x, y = event.x, event.y
        if self.last_x is not None and self.last_y is not None:
            line_width = 10
            self.canvas.create_line((self.last_x, self.last_y, x, y), fill='black', width=line_width)
            self.draw.line((self.last_x, self.last_y, x, y), fill='black', width=line_width)
        self.last_x, self.last_y = x, y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """Xóa toàn bộ nội dung trên canvas"""
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.canvas_size, self.canvas_size], fill='white')

    def save_image(self):
        """Lưu ảnh vào file PNG"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")],
            title="Save drawn digit"
        )
        if file_path:
            self.image.save(file_path)
            print(f"Ảnh đã được lưu tại: {file_path}")
            os.startfile(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = HandwritingApp(root)
    root.mainloop()
