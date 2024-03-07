import streamlit as st
import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import ConfusionMatrixDisplay, RocCurveDisplay, precision_recall_curve
from sklearn.metrics import precision_score, recall_score 

"""
Building a Machine Learning Web App with Streamlit and Python - Coursera course.

Notes:
▪️ Change catagorical data type in csv to numerical for loading features for sklearn (can use sklearn label encoder)
▪️ Target column for prediction is "type" - this is a binary value column where p stands for poisonous and e stands for edible.
▪️ Load dataset with pandas and store as pd dataframe
"""

def main():
    st.title("Binary Classification Web App")
    st.sidebar.title("Binary Classification Web App")
    st.markdown("Are your mushrooms edible or poisonous? 🍄")
    st.sidebar.markdown("Are your mushrooms edible or poisonous? 🍄")

    @st.cache(persist=True)
    #persist argument, when set flag to True --> cache stored on disk volume, then uses cache output anytime app is rerun. 
    #good for computationally expensive tasks & changing hyperparameters 
    def load_data():
        data = pd.read_csv('/Users/jamieannemortel/Downloads/mushrooms.csv')
        label = LabelEncoder()
        for col in data.columns:
            data[col] = label.fit_transform(data[col])
        return data
    df = load_data()






if __name__ == '__main__':
    main()