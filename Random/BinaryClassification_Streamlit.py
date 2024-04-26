import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

def main():
    st.title('Binary Classification with Streamlit')

    # File uploader allows user to add their own CSV
    uploaded_file = st.file_uploader("Upload your CSV data", type=["csv"])
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write(data.head())

        # Preprocess the data
        if st.button("Preprocess"):
            # Convert categorical labels to numerical
            le = LabelEncoder()
            data['variety'] = le.fit_transform(data['variety'])
            st.write('Label Encoding Applied:', data.head())

            # Splitting the data into training and testing sets
            X = data.drop(columns=['variety'])
            y = data['variety']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Train a logistic regression model
            model = LogisticRegression(solver='liblinear')
            model.fit(X_train, y_train)

            # Prediction and performance evaluation
            predictions = model.predict(X_test)
            report = classification_report(y_test, predictions, target_names=le.classes_)

            st.text("Classification Report:")
            st.text(report)

            # Making a prediction
            st.subheader("Make a new prediction")
            # Create sliders for input features
            def user_input_features():
                sepal_length = st.slider('Sepal length', float(data['sepal.length'].min()), float(data['sepal.length'].max()), float(data['sepal.length'].mean()))
                sepal_width = st.slider('Sepal width', float(data['sepal.width'].min()), float(data['sepal.width'].max()), float(data['sepal.width'].mean()))
                petal_length = st.slider('Petal length', float(data['petal.length'].min()), float(data['petal.length'].max()), float(data['petal.length'].mean()))
                petal_width = st.slider('Petal width', float(data['petal.width'].min()), float(data['petal.width'].max()), float(data['petal.width'].mean()))
                return pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]], columns=['sepal.length', 'sepal.width', 'petal.length', 'petal.width'])

            df_user = user_input_features()
            if st.button('Predict'):
                prediction = model.predict(df_user)
                st.write('Predicted class:', le.inverse_transform(prediction)[0])

if __name__ == "__main__":
    main()
