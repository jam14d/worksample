import os
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
from PIL import Image
import requests  # Make sure requests is installed

def load_image_from_path(image_path):
    image = Image.open(image_path)  # Open the image file
    image = image.resize((224, 224))  # Resize the image to fit the model input
    return np.array(image)/255.0  # Normalize pixel values to [0, 1]

def load_model():
    model_url = "https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/classification/4"
    return hub.KerasLayer(model_url)

def predict_image_class(image, model):
    image = np.expand_dims(image, axis=0)
    logits = model(image)
    return np.argmax(logits)

def get_imagenet_labels():
    labels_filename = 'ImageNetLabels.txt'
    if not os.path.isfile(labels_filename):
        print("Downloading ImageNet labels...")
        url = 'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt'
        response = requests.get(url)
        with open(labels_filename, 'w') as f:
            f.write(response.text)
    with open(labels_filename, 'r') as file:
        labels = file.read().split('\n')
    return labels

generic_cat_dna = "ATCGTTACGTGACGGATCACGTACGTAGCTAGCT"

def main(image_path):
    image = load_image_from_path(image_path)
    model = load_model()
    predicted_class = predict_image_class(image, model)
    labels = get_imagenet_labels()
    if 'cat' in labels[predicted_class].lower():
        print("Cat detected!")
        print("Generic Cat DNA:", generic_cat_dna)
    else:
        print("No cat detected.")

if __name__ == "__main__":
    image_path = input("Enter the path of the image file: ")
    main(image_path)
