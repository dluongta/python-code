import tensorflow as tf
import numpy as np
from PIL import Image

# Load mô hình MobileNet đã được huấn luyện
model = tf.keras.applications.MobileNetV2(weights="imagenet")

def predict_image(image_path):
    img = Image.open(image_path).resize((224, 224))
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    predictions = model.predict(img_array)
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions)
    return decoded_predictions[0]

# Ví dụ sử dụng
result = predict_image("bird.jpg")
for label in result:
    print(f"{label[1]}: {label[2]*100:.2f}%")