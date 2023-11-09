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

# Visualisasi Kategori
kategori = df['Katagori'].value_counts()
st.bar_chart(kategori)

# Visualisasi sumber data
sumber = df['Sumber'].value_counts()
fig = px.pie(values=sumber)
st.plotly_chart(fig)

# Visuaisasi jenis kelamin
jenis_kelamin = df['Jenis Kelamin '].value_counts()
fig_jk = px.pie(values=jenis_kelamin, names=['Laki-laki','Perempuan'])
st.plotly_chart(fig_jk)

# Visualisasi jenis akun
jenis_akun = df['Jenis Akun'].value_counts()
fig_akun = px.pie(values=jenis_akun, names=['Asli','Fake'], title="Persentase Jenis Akun")
st.plotly_chart(fig_akun)
