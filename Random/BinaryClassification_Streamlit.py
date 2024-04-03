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



#Building a Machine Learning Web App with Streamlit and Python - Coursera course.

#Notes:
#▪️ Change catagorical data type in csv to numerical for loading features for sklearn (can use sklearn label encoder)
#▪️ Target column for prediction is "type" - this is a binary value column where p stands for poisonous and e stands for edible.
#▪️ Load dataset with pandas and store as pd dataframe

def main():
    st.title("Binary Classification Web App")
    st.sidebar.title("Binary Classification Web App")
    st.markdown("Are your mushrooms edible or poisonous? 🍄")
    st.sidebar.markdown("Are your mushrooms edible or poisonous? 🍄")

    #load data function and st decorator
    @st.cache_data(persist=True)
    #persist argument, when set flag to True --> cache stored on disk volume, then uses cache output anytime app is rerun. 
    #good for computationally expensive tasks & changing hyperparameters 
    def load_data():
        data = pd.read_csv('/Users/jamieannemortel/Downloads/mushrooms.csv')
        label = LabelEncoder()
        for col in data.columns:
            data[col] = label.fit_transform(data[col])
        return data
    #splt function and st decorator
    @st.cache_data(persist=True)
    #use trusty ol pandas 
    #create target vector y use "type" (indexed via dataframe)
    #use pandas drop method, drop column "type"
    
    #data is set up like: 
    #1st row: type: cap_shape, cap_surface, etc.
    #2nd row: p: x, s, etc.
    #3rd row: e: x, s, etc. 

    #use sklearn to create xtrain,xtest, ytrain,ytest
    #optionally specific test size 
    #set random state argument to ensure reproducibility in splits
    def split(df):
            y = df.type
            x = df.drop(columns=['type'])
            x_train, x_test, y_train, y_test = train_test_split(x,y, test_size=0.3, random_state =0)
            return x_train, x_test, y_train, y_test
    #plot user selected evaluation metrics onto web app
    def plot_metrics

    #call split function on df (load ya split data)
    df = load_data()
    x_train, x_test, y_train, y_test = split(df)

    if st.sidebar.checkbox("Show raw data", False):
        st. subheader("Mushroom Data Set Classification")






if __name__ == '__main__':
    main()
