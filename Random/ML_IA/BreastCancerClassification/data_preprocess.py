import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

def load_dataset(dataset_path):
    """
    Load the dataset from the specified path and preprocess it.

    Parameters:
    - dataset_path (str): Path to the dataset CSV file.

    Returns:
    - pd.DataFrame: Preprocessed dataset.
    """
    dataset = pd.read_csv(dataset_path)
    dataset['class'] = dataset['filename'].apply(lambda x: 'benign' if 'benign' in x else 'malignant')
    return dataset

def split_dataset(dataset):
    """
    Split the dataset into training, validation, and test sets.

    Parameters:
    - dataset (pd.DataFrame): Dataset to split.

    Returns:
    - pd.DataFrame: Concatenated dataset with set labels.
    """
    # Remove 600 samples for testing
    test_df = dataset.groupby('class').sample(n=300)
    train_valid_df = dataset.drop(test_df.index).reset_index(drop=True)
    test_df = test_df.reset_index(drop=True)

    # Split training and validation sets
    valid_df = train_valid_df.groupby('class').apply(lambda x: x.sample(frac=0.2, random_state=42)).reset_index(drop=True)
    train_df = train_valid_df.drop(valid_df.index).reset_index(drop=True)

    # Assign set labels
    test_df['set'] = 'test'
    train_df['set'] = 'train'
    valid_df['set'] = 'valid'

    # Concatenate into one DataFrame
    data_new = pd.concat([train_df, valid_df, test_df]).reset_index(drop=True)
    
    return data_new

def plot_distribution(data_new):
    """
    Plot the distribution of classes in the training, validation, and test sets.

    Parameters:
    - data_new (pd.DataFrame): Concatenated dataset with set labels.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    # Plot distribution for each set
    for i, set_name in enumerate(['train', 'valid', 'test']):
        sns.countplot(data=data_new[data_new['set'] == set_name], x='class', ax=axes[i])
        axes[i].set_title(f'{set_name.capitalize()} Set')

    plt.tight_layout()
    plt.show()

def print_class_counts(data_new):
    """
    Print the class counts for the training, validation, and test sets.

    Parameters:
    - data_new (pd.DataFrame): Concatenated dataset with set labels.
    """
    print('Training set')
    print(data_new[data_new['set'] == 'train']['class'].value_counts())

    print('\nValidation set')
    print(data_new[data_new['set'] == 'valid']['class'].value_counts())

    print('\nTest set')
    print(data_new[data_new['set'] == 'test']['class'].value_counts())

def preprocess_data(dataset_path, upsample=True):
    """
    Perform data preprocessing including loading, splitting, and optionally upsampling.

    Parameters:
    - dataset_path (str): Path to the dataset CSV file.
    - upsample (bool): Whether to apply upsampling. Default is True.
    """
    # Load dataset
    dataset = load_dataset(dataset_path)

    # Split dataset
    data_new = split_dataset(dataset)

    # Optionally, apply upsampling
    if upsample:
        max_count = data_new['class'].value_counts().max()
        data_new = data_new.groupby('class').apply(lambda x: x.sample(n=max_count, replace=True)).reset_index(drop=True)

    # Plot distribution of classes
    plot_distribution(data_new)

    # Print class counts for each set
    print_class_counts(data_new)

    # Optionally, you can save the upsampled dataset to a new CSV file
    output_path = Path(dataset_path).parent / "upsampled_train_dataset.csv"
    data_new.to_csv(output_path, index=False)
    print(f"Upsampled dataset saved to {output_path}")

if __name__ == "__main__":
    dataset_path = "/Users/jamieannemortel/archive/Folds.csv"  # Replace with your dataset path
    preprocess_data(dataset_path)
