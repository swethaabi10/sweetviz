import os
import pandas as pd
import streamlit as st
import sweetviz as sv

st.set_page_config(page_title="DataSweetViz App", layout="wide")

st.title("DataSweetViz App")
st.write("Upload a CSV or Excel file to generate an interactive Sweetviz report.")

uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    file_extension = uploaded_file.name.split(".")[-1].lower()

    try:
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file type. Please upload a CSV or XLSX file.")
            st.stop()

        st.subheader("Preview of Uploaded Data")
        st.dataframe(df.head())

        st.subheader("Dataset Information")
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")

        st.write("Generating Sweetviz report...")

        report_path = "sweetviz_report.html"
        report = sv.analyze(df)
        report.show_html(filepath=report_path, open_browser=False)

        st.success("Sweetviz report generated successfully.")

        with open(report_path, "rb") as file:
            st.download_button(
                label="Download Sweetviz Report",
                data=file,
                file_name="sweetviz_report.html",
                mime="text/html",
                on_click=st.balloons
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")

else:
    st.info("Please upload a CSV or Excel file to begin.")
