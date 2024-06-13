import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class DataLoader:
    def __init__(self, dataset_dir, img_width=50, img_height=50):
        self.dataset_dir = dataset_dir
        self.img_width = img_width
        self.img_height = img_height
        self.train_generator = None
        self.validation_generator = None

    def load_data(self, validation_split=0.2, batch_size=32):
        datagen = ImageDataGenerator(rescale=1./255, validation_split=validation_split)

        self.train_generator = datagen.flow_from_directory(
            self.dataset_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode='binary',
            subset='training'
        )

        self.validation_generator = datagen.flow_from_directory(
            self.dataset_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode='binary',
            subset='validation'
        )
