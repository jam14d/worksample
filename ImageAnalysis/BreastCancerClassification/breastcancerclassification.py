import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

class BreastCancerClassifier:
    def __init__(self, dataset_dir, img_width=50, img_height=50):
        self.dataset_dir = dataset_dir
        self.img_width = img_width
        self.img_height = img_height
        self.model = None

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

    def train_model(self, epochs=10):
        self.history = self.model.fit(self.train_generator, epochs=epochs, validation_data=self.validation_generator)
        return self.history

    def evaluate_model(self):
        y_pred_proba = self.model.predict(self.validation_generator).ravel()
        y_true = self.validation_generator.classes

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

    def save_model(self, model_path='breast_cancer_classifier.h5'):
        self.model.save(model_path)
        print(f"Model saved to {model_path}")

    def load_saved_model(self, model_path='breast_cancer_classifier.h5'):
        self.model = load_model(model_path)
        print(f"Model loaded from {model_path}")

    def predict_image(self, image_path):
        img = load_img(image_path, target_size=(self.img_width, self.img_height))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = self.model.predict(img_array)
        if prediction > 0.5:
            print('Predicted class is Malignant')
        else:
            print('Predicted class is Benign')
        return prediction

def main():
    dataset_dir = "/Users/jamieannemortel/Downloads/archive/BreaKHis_v1/BreaKHis_v1/histology_slides/breast"  # Update with the path to the dataset directory
    classifier = BreastCancerClassifier(dataset_dir)
    
    classifier.load_data()
    classifier.build_model()
    classifier.train_model()
    classifier.evaluate_model()
    classifier.save_model()
    
    # To predict a new image
    image_path = 'path_to_your_image.jpg'  # Update with the path to your image file
    classifier.predict_image(image_path)
    
    # To load the model and predict again
    classifier.load_saved_model()
    classifier.predict_image(image_path)

if __name__ == "__main__":
    main()

