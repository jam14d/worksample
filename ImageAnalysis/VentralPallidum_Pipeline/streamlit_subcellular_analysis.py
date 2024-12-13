import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Title and Introduction
st.title("Subcellular Metrics Analysis")
st.markdown("""
This app provides an interactive analysis of subcellular metrics. 
Upload a CSV file and select the columns you want to analyze!
""")

# File Upload
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Load the uploaded data
    data = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded data:")
    st.dataframe(data.head())

    # Column Selection
    st.header("Column Selection")
    st.write("Select the columns for analysis:")
    available_columns = data.columns.tolist()
    selected_columns = st.multiselect("Choose columns", available_columns)

    if len(selected_columns) >= 2:
        selected_data = data[selected_columns]

        # Summary Statistics
        st.header("Summary Statistics")
        st.dataframe(selected_data.describe())

        # Plotting
        st.header("Visualizations")
        plot_type = st.selectbox("Select Plot Type", ["Histogram", "Box Plot", "Scatter Plot"])

        if plot_type == "Histogram":
            bins = st.slider("Select Number of Bins", 5, 50, 20)
            fig, ax = plt.subplots()
            selected_data.hist(bins=bins, ax=ax, layout=(1, len(selected_columns)), figsize=(12, 4))
            st.pyplot(fig)

        elif plot_type == "Box Plot":
            fig, ax = plt.subplots()
            sns.boxplot(data=selected_data, ax=ax)
            st.pyplot(fig)

        elif plot_type == "Scatter Plot":
            if len(selected_columns) >= 2:
                x_col = st.selectbox("Select X-axis column", selected_columns)
                y_col = st.selectbox("Select Y-axis column", [col for col in selected_columns if col != x_col])
                fig, ax = plt.subplots()
                sns.scatterplot(x=selected_data[x_col], y=selected_data[y_col], ax=ax)
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                st.pyplot(fig)
            else:
                st.warning("Scatter Plot requires at least two columns.")

        # Differences Analysis
        st.header("Differences Analysis")
        if len(selected_columns) == 2:
            col1, col2 = selected_columns
            selected_data["Difference"] = selected_data[col1] - selected_data[col2]
            st.write("Mean Difference:", selected_data["Difference"].mean())
            st.write("Variance in Difference:", selected_data["Difference"].var())
            st.bar_chart(selected_data["Difference"])
        else:
            st.warning("Differences Analysis is only available for two selected columns.")
    else:
        st.warning("Please select at least two columns for analysis.")
else:
    st.info("Awaiting file upload. Please upload a CSV file to get started.")
