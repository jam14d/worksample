import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class DatasetAnalyzer:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.dataset = None
        self.class_counts = None

    def load_dataset(self):
        self.dataset = pd.read_csv(self.dataset_path)
        self.dataset['class'] = self.dataset['filename'].apply(lambda x: 'benign' if 'benign' in x else 'malignant')

    def analyze_dataset(self):
        # Count the number of samples for each class
        self.class_counts = self.dataset['class'].value_counts()

    def plot_class_distribution(self):
        plt.figure(figsize=(16, 6))

        # Plot for number of samples for each class
        plt.subplot(1, 2, 2)
        sns.barplot(x=self.class_counts.index, y=self.class_counts.values)
        plt.xlabel("Class")
        plt.ylabel("Number of Samples")
        plt.title("Number of Samples for Benign and Malignant Classes")

        plt.tight_layout()  # Adjust layout to prevent overlapping
        plt.show()

    def print_class_counts(self):
        print("Number of samples for each class:")
        for class_name, count in self.class_counts.items():
            print(f"{class_name.capitalize()}: {count}")

if __name__ == "__main__":
    dataset_analyzer = DatasetAnalyzer("/Users/jamieannemortel/archive/Folds.csv")
    dataset_analyzer.load_dataset()
    dataset_analyzer.analyze_dataset()
    dataset_analyzer.plot_class_distribution()
    dataset_analyzer.print_class_counts()
