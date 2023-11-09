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

# Visualisasi sumber data
nilai = df['Sumber'].value_counts()
chart = px.pie(values=nilai, names=['Twitter','Instagram'], title='Persentase Sentiment Sosial Media Dinas Kesehatan Kota Semarang', height=500, width=1000)
chart.update_traces(textposition='auto', textinfo='percent+label', titleposition='bottom right')
st.plotly_chart(chart)
