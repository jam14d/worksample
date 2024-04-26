import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import numpy as np


#class imbalance i think, i'll come back to this another time!

def main():
    st.title('Binary Classification: Is the Thing versus IsNot the Thing')

    # File uploader allows user to add their own CSV
    uploaded_file = st.file_uploader("Upload your CSV data", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        # Display the original class distribution
        st.write("Original Class Distribution:", data['variety'].value_counts())

        # Binarize the 'variety' column to convert it into a binary classification problem
        data['variety'] = data['variety'].map({'Iris-setosa': 'Setosa', 'Iris-versicolor': 'Not Setosa', 'Iris-virginica': 'Not Setosa'})
        st.write("Binarized Class Distribution:", data['variety'].value_counts())

        # Encode labels
        le = LabelEncoder()
        data['variety'] = le.fit_transform(data['variety'])

        # Data splitting
        X = data.drop(columns=['variety'])
        y = data['variety']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        
        st.write("Train Class Distribution:", y_train.value_counts())
        st.write("Test Class Distribution:", y_test.value_counts())

        # Model training
        if np.unique(y_train).size > 1:  # Check if there are at least two classes in the training set
            model = LogisticRegression(solver='liblinear')
            model.fit(X_train, y_train)
            
            # Predictions and evaluation
            predictions = model.predict(X_test)
            st.write("Classification Report:")
            st.text(classification_report(y_test, predictions))
            st.write("Confusion Matrix:")
            st.write(confusion_matrix(y_test, predictions))
        else:
            st.error("Insufficient classes in training data!")

if __name__ == "__main__":
    main()
