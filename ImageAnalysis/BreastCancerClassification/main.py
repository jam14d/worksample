import os
from data_loader import DataLoader
from model import Model
from evaluation import Evaluator
from prediction import Predictor

def main():
    dataset_dir = "/Users/jamieannemortel/archive/BreaKHis_v1/BreaKHis_v1/histology_slides/breast"
    img_width, img_height = 50, 50

    # Load data
    data_loader = DataLoader(dataset_dir, img_width, img_height)
    data_loader.load_data()

    # Build model
    model = Model(img_width, img_height)
    model.build_model()

    # Train model
    epochs = 10
    model.train_model(data_loader.train_generator, data_loader.validation_generator, epochs=epochs)

    # Evaluate model
    evaluator = Evaluator(model.model)
    evaluator.evaluate_model(data_loader.validation_generator)

    # Save model
    model.save_model()

    # Predict image
    image_path = 'path_to_your_image.jpg'
    predictor = Predictor(model.model, img_width, img_height)
    predictor.predict_image(image_path)

if __name__ == "__main__":
    main()
