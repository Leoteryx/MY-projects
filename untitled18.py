# -*- coding: utf-8 -*-
"""GAN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yqKjLKIpEv4EbrtYJEaiAdePb47Iq1xi
"""

!pip install tensorflow

import cv2
import numpy as np
import os

# Define the path to your dataset directory
data_dir = '/content/drive/MyDrive/gan/crop_images/jute'  # Update with your dataset path

# Define the desired image size
image_size = (128, 128)

# Create a list to store preprocessed images
preprocessed_images = []

# Loop through each subdirectory in the dataset directory
for class_name in os.listdir(data_dir):
    class_dir = os.path.join(data_dir, class_name)

    if os.path.isdir(class_dir):
        # Loop through each image in the class subdirectory
        for filename in os.listdir(class_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                try:
                    # Load the image using OpenCV
                    image_path = os.path.join(class_dir, filename)
                    image = cv2.imread(image_path)

                    # Resize the image to the desired size
                    image = cv2.resize(image, image_size)

                    # Normalize pixel values to the range [-1, 1]
                    image = (image.astype(np.float32) - 127.5) / 127.5

                    # Add the preprocessed image to the list
                    preprocessed_images.append(image)

                    # Print the filename for debugging
                    print(f"Processed: {filename}")

                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

# Convert the list of images to a NumPy array
preprocessed_images = np.array(preprocessed_images)

# Verify the shape of the preprocessed images
print("Shape of preprocessed_images:", preprocessed_images.shape)

import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.datasets import mnist  # Replace with your dataset

# Data Preprocessing
# Replace this with your data loading and preprocessing code
(train_images, _), (_, _) = mnist.load_data()
train_images = (train_images.astype(np.float32) - 127.5) / 127.5  # Normalize to range [-1, 1]

# Generator
def build_generator():
    model = models.Sequential()
    model.add(layers.Dense(7 * 7 * 256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((7, 7, 256)))

    model.add(layers.Conv2DTranspose(128, (5, 5), strides=(1, 1), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(64, (5, 5), strides=(2, 2), padding='same', use_bias=False))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv2DTranspose(1, (5, 5), strides=(2, 2), padding='same', use_bias=False, activation='tanh'))

    return model

# Discriminator
def build_discriminator():
    model = models.Sequential()
    model.add(layers.Conv2D(64, (5, 5), strides=(2, 2), padding='same',
                                     input_shape=[28, 28, 1]))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv2D(128, (5, 5), strides=(2, 2), padding='same'))
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model

# Loss function
cross_entropy = tf.keras.losses.BinaryCrossentropy(from_logits=True)

# Generator and Discriminator
generator = build_generator()
discriminator = build_discriminator()

# Optimizers
generator_optimizer = tf.keras.optimizers.Adam(1e-4)
discriminator_optimizer = tf.keras.optimizers.Adam(1e-4)

# Training Loop
def train_step(images):
    noise = tf.random.normal([BATCH_SIZE, 100])

    with tf.GradientTape() as gen_tape, tf.GradientTape() as disc_tape:
        generated_images = generator(noise, training=True)

        real_output = discriminator(images, training=True)
        fake_output = discriminator(generated_images, training=True)

        gen_loss = cross_entropy(tf.ones_like(fake_output), fake_output)
        disc_loss = cross_entropy(tf.ones_like(real_output), real_output) + cross_entropy(tf.zeros_like(fake_output), fake_output)

    gradients_of_generator = gen_tape.gradient(gen_loss, generator.trainable_variables)
    gradients_of_discriminator = disc_tape.gradient(disc_loss, discriminator.trainable_variables)

    generator_optimizer.apply_gradients(zip(gradients_of_generator, generator.trainable_variables))
    discriminator_optimizer.apply_gradients(zip(gradients_of_discriminator, discriminator.trainable_variables))

# Training Loop
EPOCHS = 100
BATCH_SIZE = 64

for epoch in range(EPOCHS):
    for batch in range(len(train_images) // BATCH_SIZE):
        batch_images = train_images[batch * BATCH_SIZE:(batch + 1) * BATCH_SIZE]
        train_step(batch_images)

# Save and Load Models (optional)
generator.save('generator_model.h5')
discriminator.save('discriminator_model.h5')

# Generate Images (Optional)
def generate_and_save_images(generator, epoch, test_input):
    predictions = generator(test_input, training=False)
