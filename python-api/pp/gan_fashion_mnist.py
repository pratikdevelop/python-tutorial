import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers

# Load Fashion MNIST dataset
(train_images, _), (_, _) = tf.keras.datasets.fashion_mnist.load_data()

# Normalize the images to the range [0, 1]
train_images = train_images / 255.0

# Reshape the images to add a channel dimension (28, 28, 1)
train_images = np.expand_dims(train_images, axis=-1)

# Set the batch size
batch_size = 256

def build_generator():
    model = tf.keras.Sequential([
        layers.Dense(256, activation='relu', input_shape=(100,)),
        layers.BatchNormalization(),
        layers.Dense(512, activation='relu'),
        layers.BatchNormalization(),
        layers.Dense(1024, activation='relu'),
        layers.BatchNormalization(),
        layers.Dense(784, activation='sigmoid'),  # 28x28 images
        layers.Reshape((28, 28, 1))
    ])
    return model


def build_discriminator():
    model = tf.keras.Sequential([
        layers.Flatten(input_shape=(28, 28, 1)),
        layers.Dense(128, activation='relu'),
        layers.Dense(1, activation='sigmoid')  # Binary classification
    ])
    return model

# Create models
generator = build_generator()
discriminator = build_discriminator()

# Compile the discriminator
discriminator.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0002), 
                      loss='binary_crossentropy', metrics=['accuracy'])

# Create the GAN model
discriminator.trainable = False
gan_input = layers.Input(shape=(100,))
generated_image = generator(gan_input)
gan_output = discriminator(generated_image)
gan = tf.keras.Model(gan_input, gan_output)
gan.compile(optimizer='adam', loss='binary_crossentropy')

def train_gan(epochs=10000, batch_size=256):
    for epoch in range(epochs):
        # Generate random noise as input for the generator
        noise = np.random.normal(0, 1, size=[batch_size, 100])
        
        # Generate fake images
        generated_images = generator.predict(noise)
        
        # Get a random set of real images
        idx = np.random.randint(0, train_images.shape[0], batch_size)
        real_images = train_images[idx]

        # Create labels for real and fake images
        real_labels = np.ones((batch_size, 1))
        fake_labels = np.zeros((batch_size, 1))

        # Train the discriminator
        d_loss_real = discriminator.train_on_batch(real_images, real_labels)
        d_loss_fake = discriminator.train_on_batch(generated_images, fake_labels)
        d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

        # Train the generator
        noise = np.random.normal(0, 1, size=[batch_size, 100])
        g_loss = gan.train_on_batch(noise, real_labels)

        # Print the progress
        if epoch % 1000 == 0:
            print(f"Epoch {epoch} | Discriminator Loss: {d_loss[0]:.4f} | Generator Loss: {g_loss:.4f}")
            plot_generated_images(epoch)

def plot_generated_images(epoch):
    noise = np.random.normal(0, 1, size=[16, 100])
    generated_images = generator.predict(noise)

    plt.figure(figsize=(10, 10))
    for i in range(16):
        plt.subplot(4, 4, i + 1)
        plt.imshow(generated_images[i].reshape(28, 28), cmap='gray')
        plt.axis('off')
    plt.tight_layout()
    plt.show()

# Start training the GAN
train_gan(epochs=10000, batch_size=batch_size)
