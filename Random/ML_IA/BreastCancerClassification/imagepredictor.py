import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

#encapsulates all functionalities related to image prediction

class ImagePredictor:
    def __init__(self, model, img_width=50, img_height=50):
        self.model = model
        self.img_width = img_width
        self.img_height = img_height

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
