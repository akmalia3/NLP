import pandas as pd
import streamlit as st
import plotly.express as px

st.header('Sentiment Analysis')
st.subheader('Was the data helpful?')

exel_file = "data-preprocessing.xlsx"
sheet_name = "sentiment-analysis"

df = pd.read_excel(excel_file)

st.dataframe(df)
