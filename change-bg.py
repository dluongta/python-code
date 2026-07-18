from rembg import remove
from PIL import Image
import io

input_path = 'input-image-bg.png'  
background_path = 'background.png'  
output_path = 'output-image-changed-bg.png'  

with open(input_path, 'rb') as input_file:
    input_image = input_file.read()

output_image = remove(input_image)

image_with_transparent_background = Image.open(io.BytesIO(output_image))

background = Image.open(background_path)

background = background.resize(image_with_transparent_background.size, Image.LANCZOS)

combined = Image.new('RGBA', background.size)
combined.paste(background, (0, 0))
combined.paste(image_with_transparent_background, (0, 0), mask=image_with_transparent_background)

combined.save(output_path)
