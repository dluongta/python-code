import tkinter as tk
from PIL import Image, ImageDraw
from tkinter import filedialog
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

class HandwritingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Handwriting Digit Drawer")
        
        self.canvas_size = 280
        self.canvas = tk.Canvas(master, width=self.canvas_size, height=self.canvas_size, bg='white')
        self.canvas.pack()

        # Create a white image for drawing
        self.image = Image.new('L', (self.canvas_size, self.canvas_size), color='white')
        self.draw = ImageDraw.Draw(self.image)

        self.last_x, self.last_y = None, None
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.clear_button = tk.Button(master, text='Clear', command=self.clear_canvas)
        self.clear_button.pack()

        self.save_button = tk.Button(master, text='Save & Predict', command=self.save_and_predict)
        self.save_button.pack()

        # Load the trained model
        self.model = tf.keras.models.load_model('handwritten_digits.model')

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
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.canvas_size, self.canvas_size], fill='white')

    def save_and_predict(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.image.save(file_path)
            print(f"Image saved to {file_path}")
            self.predict_digit(file_path)

    def predict_digit(self, img_path):
        # Read the saved image and process it
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        img_resized = cv2.resize(img, (28, 28))
        img_inverted = np.invert(np.array([img_resized]))  # Invert colors

        # Predict the digit
        prediction = self.model.predict(img_inverted)
        predicted_digit = np.argmax(prediction)

        # Display prediction
        print(f"Predicted Digit: {predicted_digit}")

        # Optional: Show the image with prediction
        plt.imshow(img_inverted[0], cmap=plt.cm.binary)
        plt.title(f'Predicted: {predicted_digit}')
        plt.axis('off')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = HandwritingApp(root)
    root.mainloop()
