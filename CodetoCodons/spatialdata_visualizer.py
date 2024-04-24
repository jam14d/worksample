import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title of the web app
st.title('3D Point Cloud Visualization of Spatial Biology Data')

# Allow the user to upload a CSV file
uploaded_file = st.file_uploader("Choose a file", type=['csv'])
if uploaded_file is not None:
    # Load the CSV data into a DataFrame
    data = pd.read_csv(uploaded_file)

    # Filter out rows where isPoint is not 1 (assuming we only want to visualize points)
    data = data[data['isPoint'] == 1]

    # Create a 3D scatter plot
    fig = px.scatter_3d(data, x='X', y='Y', z='Z', color='Type', 
                        labels={'X': 'X Coordinate', 'Y': 'Y Coordinate', 'Z': 'Z Coordinate'},
                        title="3D Visualization of Tissue Data",
                        width=800, height=800)

    # Show the figure in the Streamlit app
    st.plotly_chart(fig)
else:
    st.write("Please upload a CSV file to visualize.")

