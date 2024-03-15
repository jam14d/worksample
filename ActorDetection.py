import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.models import Sequential

# Dummy model to calculate the correct input shape for Dense layer
model_dummy = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
])

# Dummy input to simulate the input shape
dummy_input = np.zeros((1, 224, 224, 3))
output_shape = model_dummy.predict(dummy_input).shape[1]

# Actual model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(output_shape, activation='relu'),  # Dynamically adjusted input shape
    Dropout(0.5),
    Dense(1, activation='sigmoid')  # Binary output
])

'''IN PROGRESS'''

# Data preprocessing and augmentation setup
data_augmentation = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
  tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
  tf.keras.layers.experimental.preprocessing.RandomZoom(0.2),
  tf.keras.layers.experimental.preprocessing.RandomFlip("horizontal"),
  tf.keras.layers.experimental.preprocessing.RandomWidth(factor=0.2),
  tf.keras.layers.experimental.preprocessing.RandomHeight(factor=0.2),
])

# Load and preprocess training images
batch_size = 32
img_height = 224
img_width = 224

train_ds = tf.keras.utils.image_dataset_from_directory(
    directory='/Users/jamieannemortel/Desktop/Timothee Chalamet',
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size,
    label_mode='binary')

train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y)).repeat()

# Correctly calculate steps_per_epoch
train_images_count = tf.data.experimental.cardinality(train_ds).numpy() * batch_size
steps_per_epoch = train_images_count // batch_size

# Train the model
history = model.fit(
      train_ds,
      steps_per_epoch=steps_per_epoch,
      epochs=15,
      verbose=1)
