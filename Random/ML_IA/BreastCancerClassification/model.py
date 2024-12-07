from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

class Model:
    def __init__(self, img_width=50, img_height=50):
        self.img_width = img_width
        self.img_height = img_height
        self.model = None

    def build_model(self):
        self.model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_width, self.img_height, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dropout(0.5),
            Dense(1, activation='sigmoid')
        ])

        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def train_model(self, train_generator, validation_generator, epochs=10):
        history = self.model.fit(train_generator, epochs=epochs, validation_data=validation_generator)
        return history

    def save_model(self, model_path='breast_cancer_classifier.h5'):
        self.model.save(model_path)
        print(f"Model saved to {model_path}")
