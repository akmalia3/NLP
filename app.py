
import pandas as pd
import streamlit as st
import plotly.express as px
import swifter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter

st.set_page_config(
    page_title="Sentiment Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",  # Use "wide" layout for a full-size dashboard
)

#st.subheader('Was the data helpful?')

excel_file = "dataset.xlsx"
df = pd.read_excel(excel_file)
df = df.drop(['Unnamed: 0'], axis=1)

# Sidebar
st.sidebar.header('Dashboard')
#st.sidebar.subheader('Sumber Data')
sumber_data = st.sidebar.radio("Pilih Sumber Data", options=df["Sumber"].unique())
df_selection = df.query("Sumber == @sumber_data")

st.header(f'😠 Sentiment Analysis {sumber_data}')
st.write('Dinas Kesehatan Kota Semarang 2022-2023')
#st.write(':angry:')

right, left = st.tabs(['Ringkasan', 'Detail Data'])
with left:
    st.write(df)

with right:
    st.markdown('#')
    pos = df_selection['sentiment'].loc[df_selection['sentiment'] == 'positive']
    neg = df_selection['sentiment'].loc[df_selection['sentiment'] == 'negative']
    count = len(df_selection)
    
    b1, b2, b3 = st.columns(3)
    b1.metric("Positive", len(pos), "Komentar")
    b2.metric("Negative", len(neg), "- Komentar")
    b3.metric("Jumlah", count, "4%")

    st.markdown("""---""")
    col1, col2 = st.columns(2)    
    with col1:
    # Visualisasi hasil sentiment
        sentiment = df_selection['sentiment'].value_counts()
        fig_sentiment = px.pie(values=sentiment, names=['positive','negative'], title=f'Persentase Hasil Sentiment pada {sumber_data}')
        fig_sentiment.update_traces(textposition='auto', textinfo='percent+label', titleposition='bottom right')
        st.plotly_chart(fig_sentiment)

    with col2:
        kategori = df_selection['Katagori'].value_counts()
        chart_kategori = px.bar(kategori, title=f"Kategori Pertanyaan pada {sumber_data}", orientation='h', template='simple_white')
        st.plotly_chart(chart_kategori, use_container_width=True)

# Visualisasi tanggal komentar
    fig_tgl = px.area(df_selection['Tanggal'],  title="Waktu", template='simple_white')
    st.plotly_chart(fig_tgl, use_container_width=True)

    jk_left, ja_middle, kt_right = st.columns(3)

    with jk_left:
    # Visuaisasi jenis kelamin
        jenis_kelamin = df_selection['Jenis Kelamin '].value_counts()
        fig_jk = px.pie(values=jenis_kelamin, names=['Laki-laki','Perempuan'], 
                title=f"Persentase Jenis Kelamin User {sumber_data}")
        st.plotly_chart(fig_jk, use_container_width=True)

    with ja_middle:
    # Visualisasi jenis akun
        jenis_akun = df_selection['Jenis Akun'].value_counts()
        fig_akun = px.pie(values=jenis_akun, names=['Asli','Fake'], title=f"Persentase Jenis Akun {sumber_data}")
        st.plotly_chart(fig_akun, use_container_width=True)

    with kt_right:
    # Visualisasi Kategori
        kategori = df_selection['Katagori'].value_counts()
        chart_kategori = px.bar(kategori, title=f"Kategori Pertanyaan pada {sumber_data}")
        st.plotly_chart(chart_kategori, use_container_width=True)

    # frequent ngrams
    df_selection['ngrams'].fillna(' ', inplace=True)
    ngram = ''.join(df_selection['ngrams'])
    
    # frequent bigrams
    df['bigrams'].fillna(' ', inplace=True)
    bigram = ''.join(df['bigrams'])
    
    # frequent trigram
    df['trigrams'].fillna(' ', inplace=True)
    trigram = ''.join(df['trigrams'])
    
    n, bi, tri = st.tabs(['ngrams', 'bigrams', 'trigrams'])
    with n:
        left, right = st.columns(2)
        with left:
            wordcloud = WordCloud(width = 2000, height = 1334,
                          random_state=1, background_color='black',#colormap='Pastel1',
                          collocations=False, normalize_plurals=False, collocation_threshold = 2, mode='RGBA', 
                          colormap='viridis').generate(ngram)#'PuBu_r'
            plt.figure(figsize=(10,10))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.subheader('wordcloud')
            st.pyplot(plt, use_container_width=True)
            #with right:
        with right:
            text = ngram.split()
            freq = Counter(text)
            data = pd.DataFrame(freq.most_common(), columns=['word', 'frequent'])
        
            fig_freq = px.bar(data.head(20), x='frequent', y='word',color='frequent', template='gridon', height=500)
            fig_freq.update_layout(yaxis={'categoryorder':'total ascending'})
            st.subheader('frequent word')
            st.plotly_chart(fig_freq, use_container_width=True)

    with bi:
        bi_left, bi_right = st.columns(2)
        with bi_left:
            wordcloud_bigrams = WordCloud(width = 2000, height = 1334,
                                  random_state=1, background_color='black',colormap='Pastel1',
                                  collocations=False, normalize_plurals=False,
                                  collocation_threshold = 2).generate(bigram)

            plt.figure(figsize=(10,10))
            plt.imshow(wordcloud_bigrams, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.subheader('wordcloud')
            st.pyplot(plt)

        with bi_right:
            #with bigram_right:
            text_bi = bigram.split()
            freq_bi = Counter(text_bi)
            data_bi = pd.DataFrame(freq_bi.most_common(), columns=['word', 'frequent'])
            data_bi.style.background_gradient(cmap='Blues')
    
            fig_bi = px.bar(data_bi.head(20), x='frequent', y='word',
                color='frequent', template='seaborn')
            fig_bi.update_layout(yaxis={'categoryorder':'total ascending'})
            st.subheader('frequent bigram')
            st.plotly_chart(fig_bi, use_container_width=True)

    with tri:
        wordcloud_trigrams = WordCloud(width = 2000, height = 1334,
                              random_state=1, background_color='white',colormap='plasma',
                              collocations=False, normalize_plurals=False,
                              collocation_threshold = 2).generate(trigram)
        # visualisasi dengan matplotlib
        plt.figure(figsize=(10,10))
        plt.imshow(wordcloud_trigrams, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot(plt)

    #with trigrams_right:
        text_tri = trigram.split()
        freq_tri = Counter(text_tri)
        data_tri = pd.DataFrame(freq_tri.most_common(), columns=['word', 'frequent'])
        data_tri.style.background_gradient(cmap='Blues')
        
        fig_tri = px.bar(data_tri.head(20), x='frequent', y='word',
            color='frequent', title="Top 40 Words Trigrams", template='plotly')
        fig_tri.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_tri, use_container_width=True)
