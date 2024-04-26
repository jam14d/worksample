#Using a multiclass dataset and creating a binary problem with a dictionary :) 
#a work in progress 

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, RocCurveDisplay
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt

def main():
    st.title('Binary Classification: Is the Thing versus IsNot the Thing')

    # File uploader allows user to add their own CSV
    uploaded_file = st.file_uploader("Upload your CSV data", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        # Display the first few rows of the uploaded dataset
        st.write("Data Preview:", data.head())
        
        # Preprocess the data: Binarize the 'variety' column
        data['variety_detailed'] = data['variety']  # Make a copy of the variety column
        dic_setosa = {'Iris-versicolor': 'not Setosa', 'Iris-virginica': 'not Setosa', 'Iris-setosa': 'Setosa'}
        data['variety'] = data['variety'].replace(dic_setosa)
        st.write("Updated Class Distribution:", data['variety'].value_counts())

        # Encode labels
        le = LabelEncoder()
        data['variety'] = le.fit_transform(data['variety'])
        st.write("Unique classes after encoding:", pd.unique(data['variety']))  # Debug print
        
        # Data splitting
        X = data.drop(columns=['variety', 'variety_detailed'])
        y = data['variety']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Model training
        model = LogisticRegression(solver='liblinear')
        model.fit(X_train, y_train)
        
        # Predictions and evaluation
        predictions = model.predict(X_test)
        report = classification_report(y_test, predictions)
        st.text("Classification Report:")
        st.text(report)

        # Confusion Matrix
        cm = confusion_matrix(y_test, predictions)
        st.write("Confusion Matrix:", cm)

        # ROC Curve
        if len(np.unique(y_test)) == 2:  # Check if y_test has exactly two classes
            proba = model.predict_proba(X_test)[:, 1]
            fpr, tpr, thresholds = roc_curve(y_test, proba)
            roc_auc = auc(fpr, tpr)

            fig, ax = plt.subplots()
            RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='Logistic Regression').plot(ax=ax)
            st.pyplot(fig)
        else:
            st.error("ROC Curve Error: Expected binary classes but got more.")

if __name__ == "__main__":
    main()
