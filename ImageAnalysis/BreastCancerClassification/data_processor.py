import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DatasetProcessor:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.dataset = None
        self.data_new = None
        self.train_df = None
        self.valid_df = None
        self.test_df = None

    def load_dataset(self):
        self.dataset = pd.read_csv(self.dataset_path)
        self.dataset['class'] = self.dataset['filename'].apply(lambda x: 'benign' if 'benign' in x else 'malignant')

    def split_dataset(self):
        # Remove 600 samples for testing
        self.test_df = self.dataset.groupby('class').sample(n=300)
        self.train_valid_df = self.dataset.drop(self.test_df.index).reset_index(drop=True)
        self.test_df = self.test_df.reset_index(drop=True)

        # Split training and validation sets
        self.valid_df = self.train_valid_df.groupby('class').apply(lambda x: x.sample(frac=0.2, random_state=42)).reset_index(drop=True)
        self.train_df = self.train_valid_df.drop(self.valid_df.index).reset_index(drop=True)

        # Assign set labels
        self.test_df['set'] = 'test'
        self.train_df['set'] = 'train'
        self.valid_df['set'] = 'valid'

        # Concatenate into one DataFrame
        self.data_new = pd.concat([self.train_df, self.valid_df, self.test_df]).reset_index(drop=True)

    def plot_distribution(self):
        # Create subplots for each set (train, valid, test)
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))

        # Plot distribution for each set
        for i, set_name in enumerate(['train', 'valid', 'test']):
            sns.countplot(data=self.data_new[self.data_new['set'] == set_name], x='class', ax=axes[i])
            axes[i].set_title(f'{set_name.capitalize()} Set')

        plt.tight_layout()
        plt.show()

    def print_class_counts(self):
        print('Training set')
        print(self.train_df['class'].value_counts())

        print('\nValidation set')
        print(self.valid_df['class'].value_counts())

        print('\nTest set')
        print(self.test_df['class'].value_counts())

if __name__ == "__main__":
    dataset_processor = DatasetProcessor("/Users/jamieannemortel/archive/Folds.csv")
    dataset_processor.load_dataset()
    dataset_processor.split_dataset()
    dataset_processor.plot_distribution()
    dataset_processor.print_class_counts()
