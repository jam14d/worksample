import streamlit as st
import pandas as pd
import plotly.express as px

# Set the title of the web app
st.title('3D Point Cloud Visualization of Spatial Biology Data')

# Sidebar options
st.sidebar.header("Options")
# Toggle for displaying contours
show_contours = st.sidebar.checkbox("Show Contours", value=False)
# Custom type names
type_names = {
    1: st.sidebar.text_input("Name for Type 1", "Neuron"),
    2: st.sidebar.text_input("Name for Type 2", "Other"),
    3: st.sidebar.text_input("Name for Type 3", "Type 3"),
    4: st.sidebar.text_input("Name for Type 4", "Type 4"),
    5: "Contour"  # Contours are always type 5
}

# Allow the user to upload a CSV file
uploaded_file = st.file_uploader("Choose a file", type=['csv'])
if uploaded_file is not None:
    # Load the CSV data into a DataFrame
    data = pd.read_csv(uploaded_file)

    # Replace type numbers with user-defined names
    data['Type'] = data['Type'].map(type_names)

    # Filter out rows where isPoint is not 1 if contours should not be shown
    if not show_contours:
        data = data[data['isPoint'] == 1]

    # Create a 3D scatter plot
    fig = px.scatter_3d(data, x='X', y='Y', z='Z', color='Type', 
                        labels={'X': 'X Coordinate', 'Y': 'Y Coordinate', 'Z': 'Z Coordinate'},
                        title="3D Visualization of Tissue Data",
                        color_discrete_map={'Contour': 'gray'},  # Ensuring contours are gray if shown
                        width=800, height=800)

    # Show the figure in the Streamlit app
    st.plotly_chart(fig)
else:
    st.write("Please upload a CSV file to visualize.")
