import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator


class DataLoader:
    def __init__(self, dataset_dir, img_width=50, img_height=50):
        self.dataset_dir = dataset_dir
        self.img_width = img_width
        self.img_height = img_height
        self.train_generator = None
        self.validation_generator = None
        self.data_new = None  # New DataFrame to store preprocessed data

    def load_data(self, train_df, valid_df, batch_size=32):
        datagen = ImageDataGenerator(rescale=1./255)

        # Store generators for training and validation
        self.train_generator = datagen.flow_from_dataframe(
            train_df,
            x_col='file_path',
            y_col='label',
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode='binary',
            shuffle=True  # Shuffle data during training
        )

        self.validation_generator = datagen.flow_from_dataframe(
            valid_df,
            x_col='file_path',
            y_col='label',
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode='binary',
            shuffle=False  # No need to shuffle validation data
        )

    def get_data_new(self):
        return self.data_new
