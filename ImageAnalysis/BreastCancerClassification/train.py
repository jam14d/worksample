import os
from data_loader import DataLoader
from model import Model
from evaluation import Evaluator

def train(dataset_dir, img_width, img_height, epochs):
    # Load data
    data_loader = DataLoader(dataset_dir, img_width, img_height)
    data_loader.load_data()

    # Build model
    model = Model(img_width, img_height)
    model.build_model()

    # Train model
    model.train_model(data_loader.train_generator, data_loader.validation_generator, epochs=epochs)

    # Evaluate model
    evaluator = Evaluator(model.model)
    evaluator.evaluate_model(data_loader.validation_generator)

    # Save model
    model.save_model()

if __name__ == "__main__":
    dataset_dir = "/Users/jamieannemortel/Downloads/archive/BreaKHis_v1/BreaKHis_v1/histology_slides/breast"
    img_width, img_height = 50, 50
    epochs = 10
    train(dataset_dir, img_width, img_height, epochs)
