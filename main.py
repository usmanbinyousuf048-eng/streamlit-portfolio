import pandas as pd
import streamlit as st

st.set_page_config(page_title="Data Analyzer")
st.title("Data Analyzer")
uploaded_file=st.file_uploader("Upload Your CSV File",type='csv')

if uploaded_file is not None:
    df=pd.read_csv(uploaded_file)
    st.success(f"File Loaded: {uploaded_file.name} | Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    with st.sidebar:
        st.header("File Info")
        st.write(f"Rows: {df.shape[0]}")
        st.write(f"Columns: {df.shape[1]}")
        st.header("Missing Values")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if not missing.empty:
            st.write(missing)
            if st.checkbox("Remove rows with missing values"):
             df = df.dropna()
             st.success(f"Cleaned! Removed rows with missing values. New shape: {df.shape[0]} rows × {df.shape[1]} columns")
              
        else:
            st.write("No missing values ")
    st.subheader("Data preview")
    st.write(df.head(20))
    st.subheader("Data summary")
    id_cols = [col for col in df.columns if col.lower() in ["id", "index", "serial", "row","Row ID"]]
    st.dataframe(df.drop(columns=id_cols, errors="ignore").describe())
    #st.write(df.describe())
    st.subheader("Filter Data")
    column=df.columns.to_list()
    s_c=st.selectbox("select column to filter data",options=column)
    uniquevals=df[s_c].unique()
    c_v=st.selectbox("select value to filter by",options=uniquevals)
    filtered=df[df[s_c]==c_v]
    st.write(filtered)
    st.write("do you want to view auto generated plotting of data?")
    if "show_plotting" not in st.session_state:
         st.session_state.show_plotting = False
    if st.button("View Plotting Options"):
        st.session_state.show_plotting = True
    if st.session_state.show_plotting:
        numeric_cols = filtered.select_dtypes(include=["number"]).columns.tolist()
        if len(numeric_cols) == 0:
            st.warning("No numeric columns available for plotting in the filtered data.")
        else:
            x = st.selectbox("Select X-axis", options=filtered.columns.tolist())
            y = st.selectbox("Select Y-axis", options=numeric_cols)
            if st.button("See Graph"):
                if x == y:
                    st.error("X and Y cannot be the same column.")
                else:

                 st.bar_chart(filtered, x=x, y=y)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered CSV", csv, "filtered_data.csv", "text/csv")

else:
    st.write("waiting for file")