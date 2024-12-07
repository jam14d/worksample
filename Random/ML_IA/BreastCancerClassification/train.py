import os
import pandas as pd  # Import pandas
import numpy as np  # Import numpy
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.metrics import roc_curve, auc
from data_loader import DataLoader
from model import Model
from evaluation import Evaluator

def train(dataset_dir, img_width, img_height, initial_epochs):
    data_loader = DataLoader(dataset_dir, img_width, img_height)
    
    # Load and preprocess data with upsampling
    train_df, valid_df = load_and_preprocess_data(dataset_dir)
    
    data_loader.load_data(train_df, valid_df)

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
                              epochs=initial_epochs,
                              validation_data=data_loader.validation_generator,
                              callbacks=[checkpoint_callback])

    # Evaluate model
    evaluator = Evaluator(model.model)
    evaluator.evaluate_model(data_loader.validation_generator)

    # Save model (optional, if you want to save the entire model)
    model.save_model()

def load_and_preprocess_data(dataset_dir):
    # Load original dataset
    dataset = pd.read_csv("/Users/jamieannemortel/archive/Folds.csv")  # Replace with your dataset path

    # Perform upsampling
    max_count = np.max(dataset['grp'].value_counts())
    train_df_upsampled = dataset.groupby('grp').apply(lambda x: x.sample(n=max_count, replace=True)).reset_index(drop=True)

    # Split into train and validation sets
    valid_df = train_df_upsampled.groupby('grp').apply(lambda x: x.sample(frac=0.2, random_state=42)).reset_index(drop=True)
    train_df = train_df_upsampled.drop(valid_df.index).reset_index(drop=True)

    # Assign set labels
    train_df['set'] = 'train'
    valid_df['set'] = 'valid'

    return train_df, valid_df

if __name__ == "__main__":
    dataset_dir = "/Users/jamieannemortel/archive/BreaKHis_v1/BreaKHis_v1/histology_slides/breast"
    img_width, img_height = 50, 50
    initial_epochs = 50
    additional_epochs = 0  # Set to 0 for the initial run

    # Initial training
    train(dataset_dir, img_width, img_height, initial_epochs)

    # Resume training with additional epochs
    train(dataset_dir, img_width, img_height, additional_epochs)
