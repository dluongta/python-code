import torch
from torchvision import models, transforms
from PIL import Image
import numpy as np

model = models.segmentation.deeplabv3_resnet101(pretrained=True).eval()

input_image = Image.open("main-1.png").convert("RGB")
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])
input_tensor = preprocess(input_image).unsqueeze(0)

with torch.no_grad():
    output = model(input_tensor)['out'][0]
output_predictions = output.argmax(0).byte().cpu().numpy()

mask = (output_predictions == 15).astype(np.uint8) * 255
mask_image = Image.fromarray(mask).convert("L")

image_np = np.array(input_image)
mask_np = np.array(mask_image)
image_rgba = np.dstack((image_np, mask_np))
result = Image.fromarray(image_rgba)
result.save("output_transparent.png")

print("Đã tách người khỏi nền thành công với nền trong suốt!")
