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
'''
from wordcloud import WordCloud
def ngrams(text):
    text = ' '.join([str(e) for e in text]) # ubah nested list menjadi string
    return ''.join(text).strip()

df['ngrams'] = df['text_stemming'].swifter.apply(ngrams)
ngram = ' '.join(df['ngrams'])

wordcloud = WordCloud(width = 2000, height = 1334,
                      random_state=1, background_color='black',colormap='Pastel1',
                      collocations=False, normalize_plurals=False,
                      collocation_threshold = 2).generate(ngram)

visualisasi
plt.figure(figsize=(10,10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
st.pyplot()
'''

# frequents word
from collections import Counter

data = pd.read_csv('word-frequents.csv')
data = data.drop(['Unnamed: 0'], axis=1)
st.dataframe(data)

# visualisasi frequent word
import plotly.express as px

fig_freq = px.bar(data.head(40), x='frequent', y='word',
            color='frequent', title="Top 40 Words")
fig_freq.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_freq, use_container_width=True)

# frequent word positive
df['ngrams'].fillna(' ', inplace=True)
df['sentiment'].fillna(' ', inplace=True)
pos_review = df['ngrams'][df["sentiment"] == 'positive'].tolist()
pos = ''.join(pos_review)

text = pos.split()
freq = Counter(text)
data2 = pd.DataFrame(freq.most_common(), columns=['word', 'frequent'])
data2.style.background_gradient(cmap='Blues')
st.dataframe(data2)
