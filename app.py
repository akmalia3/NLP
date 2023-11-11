import pandas as pd
import streamlit as st
import plotly.express as px
import wordcloud
import swifter
import matplotlib.pyplot as plt

st.header('Sentiment Analysis')
st.subheader('Was the data helpful?')

excel_file = "dataset.xlsx"
sheet_name = "sentiment-analysis"

df = pd.read_excel(excel_file)
df = df.drop(['Unnamed: 0'], axis=1)

st.dataframe(df)

# Visualisasi sumber data
sumber = df['Sumber'].value_counts()
fig = px.pie(values=sumber, names=['Twitter', 'Instagram'], title="Persentase Sumber Data")

# Visualisasi jenis akun
jenis_akun = df['Jenis Akun'].value_counts()
fig_akun = px.pie(values=jenis_akun, names=['Asli','Fake'], title="Persentase Jenis Akun")

# Visuaisasi jenis kelamin
jenis_kelamin = df['Jenis Kelamin '].value_counts()
fig_jk = px.pie(values=jenis_kelamin, names=['Laki-laki','Perempuan'], title="Persentase Jenis Kelamin User")

left_column, right_column, midle_column = st.columns(3)
left_column.plotly_chart(fig, use_container_width=True)
right_column.plotly_chart(fig_akun, use_container_width=True)
midle_column.plotly_chart(fig_jk, use_container_width=True)

# Visualisasi Kategori
kategori = df['Katagori'].value_counts()
chart_kategori = px.bar(kategori, title="Kategori Pertanyaan")
st.plotly_chart(chart_kategori, use_container_width=True)

# Visualisasi tanggal komentar
fig_tgl = px.area(df['Tanggal'],  title="Waktu")
st.plotly_chart(fig_tgl, use_container_width=True)

# Visualisasi hasil sentiment
sentiment = df['sentiment'].value_counts()
fig_sentiment = px.pie(values=sentiment, names=['positive','negative'], title='Persentase Hasil Sentiment')
st.plotly_chart(fig_sentiment)

# wordcloud
from wordcloud import WordCloud

def ngrams(text):
    text = ' '.join([str(e) for e in text])
    return ''.join(text).strip() 

ngrams_data = df['text_stemming'].swifter.apply(ngrams)
ngrams_visualize = ' '.join(ngrams_data)
wordcloud = WordCloud().generate(ngrams_visualize)
plt.imshow(wordcloud)
st.plotly_chart()

