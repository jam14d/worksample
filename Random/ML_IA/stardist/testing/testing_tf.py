import tensorflow as tf

# Define a simple Sequential model
model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(10, activation='relu', input_shape=(10,)),
  tf.keras.layers.Dense(1)
])

# Print model summary
model.summary()
