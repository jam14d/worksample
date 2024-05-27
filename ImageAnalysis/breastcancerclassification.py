import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

class BreastCancerClassifier:
    def __init__(self, dataset_dir, img_width=50, img_height=50):
        self.dataset_dir = dataset_dir
        self.img_width = img_width
        self.img_height = img_height
        self.model = None

    def load_data(self, validation_split=0.2, batch_size=32):
        datagen = ImageDataGenerator(rescale=1./255, validation_split=validation_split)

        train_generator = datagen.flow_from_directory(
            self.dataset_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode='binary',
            subset='training'
        )

        validation_generator = datagen.flow_from_directory(
            self.dataset_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=batch_size,
            class_mode='binary',
            subset='validation'
        )

        return train_generator, validation_generator

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

    def evaluate_model(self, validation_generator):
        y_pred_proba = self.model.predict(validation_generator).ravel()
        y_true = validation_generator.classes

        fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
        roc_auc = auc(fpr, tpr)

        # Plot ROC curve
        plt.figure()
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic (ROC) Curve')
        plt.legend(loc="lower right")
        plt.show()

def main():
    dataset_dir = "/Users/jamieannemortel/Downloads/archive/BreaKHis_v1/BreaKHis_v1/histology_slides/breast"  # Update with the path to the dataset directory
    classifier = BreastCancerClassifier(dataset_dir)
    
    train_generator, validation_generator = classifier.load_data()
    classifier.build_model()
    history = classifier.train_model(train_generator, validation_generator)
    classifier.evaluate_model(validation_generator)

if __name__ == "__main__":
    main()
