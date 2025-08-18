from PIL import Image, ImageDraw, ImageFont

# Load the image
image_path = 'input_image.png'  # Replace with your image path
image = Image.open(image_path)

# Prepare to draw on the image
draw = ImageDraw.Draw(image)

# Define the text and font
text = "Hello, World!"
font_size = 36
font = ImageFont.load_default()  # You can also specify a TTF font file

# Define text position
text_position = (50, 50)  # (x, y) coordinates

# Choose a text color (RGB)
text_color = (0, 0, 0)  # Black color

# Add text to image
draw.text(text_position, text, fill=text_color, font=font)

# Save the modified image
image.save('output_text_image.png')  # Save the new image
image.show()  # Optionally display the image
