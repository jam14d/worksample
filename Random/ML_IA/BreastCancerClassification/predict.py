from model import Model
from imagepredictor import ImagePredictor

def predict(image_path, img_width, img_height):
    # Load model
    model = Model(img_width, img_height)
    model.load_model()  # Assuming you have a method to load the saved model

    # Predict image
    predictor = ImagePredictor(model.model, img_width, img_height)  
    predictor.predict_image(image_path)

if __name__ == "__main__":
    image_path = 'path_to_your_image.jpg'
    img_width, img_height = 50, 50
    predict(image_path, img_width, img_height)
