import pandas as pd
import streamlit as st
import plotly.express as px

st.header('Sentiment Analysis')
st.subheader('Was the data helpful?')

excel_file = "data-preprocessing.xlsx"
sheet_name = "sentiment-analysis"

df = pd.read_excel(excel_file)
df = df.drop(['Unnamed: 0'], axis=1)

st.dataframe(df)

# Visualisasi
kategori = df['Katagori'].value_counts()
st.bar_chart(kategori, title='Kategori Pertanyaan')
