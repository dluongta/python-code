import os
import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# Decide if to load an existing model or to train a new one
train_new_model = True

if train_new_model:
    # Loading the MNIST data set with samples and splitting it
    mnist = tf.keras.datasets.mnist
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    # Normalizing the data (making length = 1)
    X_train = tf.keras.utils.normalize(X_train, axis=1)
    X_test = tf.keras.utils.normalize(X_test, axis=1)

    # Create a neural network model
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(units=128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(units=10, activation=tf.nn.softmax))

    # Compiling and optimizing model
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Training the model
    model.fit(X_train, y_train, epochs=3)

    # Evaluating the model
    val_loss, val_acc = model.evaluate(X_test, y_test)
    print(val_loss)
    print(val_acc)

    # Saving the model
    model.save('handwritten_digits.model')
else:
    # Load the model
    model = tf.keras.models.load_model('handwritten_digits.model')

# Load custom images and predict them
image_number = 1
fig, ax = plt.subplots(figsize=(5, 5))  # Create a single subplot for one image

def on_key(event):
    global image_number
    if event.key == 'enter':
        display_image()
    elif event.key == 'escape':
        plt.close(fig)

plt.connect('key_press_event', on_key)

def display_image():
    global image_number
    try:
        img_path = f'digits/digit{image_number}.png'
        if os.path.isfile(img_path):
            # Read the image and convert to grayscale
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            # Resize the image to 28x28 pixels
            img_resized = cv2.resize(img, (28, 28))
            # Invert the image colors
            img_inverted = np.invert(np.array([img_resized]))

            # Predict the digit
            prediction = model.predict(img_inverted)
            predicted_digit = np.argmax(prediction)

            # Display the image and prediction on the canvas
            ax.clear()  # Clear the previous image
            ax.imshow(img_inverted[0], cmap=plt.cm.binary)
            ax.set_title(f'Predicted: {predicted_digit}')
            ax.axis('off')  # Hide axes
            plt.draw()  # Update the plot
            image_number += 1
        else:
            print("No more images to display.")
    except Exception as e:
        print(f"Error reading image: {e}. Proceeding with next image...")
        image_number += 1

# Initially display the first image if it exists
display_image()

plt.show()
