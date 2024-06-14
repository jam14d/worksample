import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Function to upsample training data
def upsample_training_data(train_df):
    # Upsampling training dataset
    max_count = np.max(train_df['grp'].value_counts())
    train_df_upsampled = train_df.groupby('grp').apply(lambda x: x.sample(n=max_count, replace=True)).reset_index(drop=True)
    
    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Create a grid of 1 row and 2 columns
    sns.countplot(data=train_df, x='grp', ax=axs[0])  # Plot on the first subplot
    axs[0].set_title('Class Distribution Before Upsampling')
    axs[0].set_xlabel('Class')
    axs[0].set_ylabel('Count')
    
    sns.countplot(data=train_df_upsampled, x='grp', ax=axs[1])  # Plot on the second subplot
    axs[1].set_title('Distribution of Classes After Upsampling')
    axs[1].set_xlabel('Class')
    axs[1].set_ylabel('Count')
    
    plt.tight_layout()  # Adjust layout to prevent overlap of titles and labels
    plt.show()
    
    return train_df_upsampled

if __name__ == "__main__":
    # Load the dataset
    train_df = pd.read_csv("/Users/jamieannemortel/archive/Folds.csv")  # Replace with your dataset path
    
    # Perform upsampling and plot the distribution before and after upsampling
    train_df_upsampled = upsample_training_data(train_df)
    
    # Optionally, you can save the upsampled dataset to a new CSV file
    train_df_upsampled.to_csv("upsampled_train_dataset.csv", index=False)
