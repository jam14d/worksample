import os
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.metrics import roc_curve, auc
from data_loader import DataLoader
from model import Model
from evaluation import Evaluator

def train(dataset_dir, img_width, img_height, epochs):
    data_loader = DataLoader(dataset_dir, img_width, img_height)
    data_loader.load_data()

    # Build model
    model = Model(img_width, img_height)
    model.build_model()

    # Define checkpoint callback to save model weights
    checkpoint_path = "model_checkpoint.weights.h5"
    checkpoint_callback = ModelCheckpoint(filepath=checkpoint_path,
                                          monitor='val_loss',
                                          save_best_only=True,
                                          save_weights_only=True,
                                          verbose=1)

    # Train model using Keras fit method
    history = model.model.fit(data_loader.train_generator,
                              epochs=epochs,
                              validation_data=data_loader.validation_generator,
                              callbacks=[checkpoint_callback])

    # Evaluate model
    evaluator = Evaluator(model.model)
    evaluator.evaluate_model(data_loader.validation_generator)

    # Save entire model (optional)
    # model.save_model()  # Uncomment this if you want to save the entire model

if __name__ == "__main__":
    dataset_dir = "/Users/jamieannemortel/archive/BreaKHis_v1/BreaKHis_v1/histology_slides/breast"
    img_width, img_height = 50, 50
    initial_epochs = 50
    additional_epochs = 0  # Set to the number of additional epochs you want

    # Initial training
    train(dataset_dir, img_width, img_height, initial_epochs)

    # Resume training with additional epochs if specified
    if additional_epochs > 0:
        train(dataset_dir, img_width, img_height, additional_epochs)
