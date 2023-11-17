
import pandas as pd
import streamlit as st
import plotly.express as px
import swifter
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from wordcloud import WordCloud
from collections import Counter

st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon=":thermometer:",
    layout="wide",  # Use "wide" layout for a full-size dashboard
)

#st.subheader('Was the data helpful?')
# https://retro-tools.streamlit.app/
# https://bpmpkalsel-pmm-dashboard-71ttv1.streamlit.app/Platform_Merdeka_Mengajar

file_name = "dataset-sentiment.xlsx"
df = pd.read_excel(file_name)
df = df.drop(['Unnamed: 0'], axis=1)

st.header('🌡️Sentiment Analysis Sosial Media')
st.write('Dinas Kesehatan Kota Semarang Tahun 2022-2023')
#st.write(':angry:')

right, left = st.tabs(['Ringkasan', 'Detail Data'])
with left:
    st.write(df)

with right:
    nav1, nav2, nav3, nav4 = st.columns(4)
    with nav1:
        sumber_data = st.selectbox("Pilih Sumber Data", options=df["Sumber"].unique())
        
    with nav2:
        sentiment = st.multiselect("Pilih Sentiment", options=df["sentiment"].unique(), 
                                   default=df['sentiment'].unique())
        
    with nav3:
        month = ('Januari','Februari','Maret','April','Mei','Juni','Juli','Agustus','September',
                'Oktober','November','Desember')
        bulan = st.selectbox("Pilih Bulan", options=month)
        # df['Tanggal'] = pd.to_datetime(df['Tanggal'], format='ISO8601')
        # data = df['Tanggal'].dt.month
        # bulan = st.selectbox("Pilih Bulan", options=month)
        
    with nav4:
        #df['Tanggal'] = pd.to_datetime(df['Tanggal'])
        #year = df['Tanggal'].dt.year
        year=('2022','2023')
        tahun = st.selectbox("Pilih Tahun", options=year)

    # garis 
    st.markdown("""---""")
    
    df_selection = df.query("Sumber == @sumber_data & sentiment == @sentiment")
    pos = df_selection['sentiment'].loc[df_selection['sentiment'] == 'positive']
    neg = df_selection['sentiment'].loc[df_selection['sentiment'] == 'negative']
    count = len(df_selection)
    
    b1, b2, b3 = st.columns([0.45,0.45,0.45])
    b1.metric("Jumlah Komentar", len(pos), "+ Positive")
    b2.metric("Jumlah Komentar", len(neg), "- Negative")
    b3.metric("Jumlah", count)

    # garis 
    st.markdown("""---""")

    df_selection['ngrams'].fillna(' ', inplace=True)
    df_selection['sentiment'].fillna(' ', inplace=True)
    
    col1, col2, col3 = st.columns([2,1,1])    
    with col1:
    # Visualisasi hasil sentiment
        sentiment = df_selection['sentiment'].value_counts()
        night_colors=['#A7D397', '#FA7070']
        fig_sentiment = go.Figure()
        fig_sentiment.add_trace(go.Pie(labels=['positive','negative'], values=sentiment, hole=0.3, marker_colors=night_colors, textinfo='label+percent', hoverinfo='value'))
        fig_sentiment.update_layout(title=f'Sentiment {sumber_data}')
        st.plotly_chart(fig_sentiment)

    with col2:
        # frequent ngram word positive
        pos_review = df_selection['ngrams'][df_selection["sentiment"] == 'positive'].tolist()
        pos = ''.join(pos_review)
    
        text_pos = pos.split()
        freq_pos = Counter(text_pos)
        data2 = pd.DataFrame(freq_pos.most_common(), columns=['word', 'frequent'])
        data2.style.background_gradient(cmap='Blues')
    
        pos_freq = px.bar(data2.head(10), x='frequent', y='word',
                    color='frequent', title="Top 10 Words Positive", template='ggplot2')
        pos_freq.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(pos_freq, use_container_width=True)

    with col3:
        # frequent ngram word negative
        neg_review = df_selection['ngrams'][df_selection["sentiment"] == 'negative'].tolist()
        neg = ''.join(neg_review)

        text_neg = neg.split()
        freq_neg = Counter(text_neg)
        data3 = pd.DataFrame(freq_neg.most_common(), columns=['word', 'frequent'])
        data3.style.background_gradient(cmap='Blues')
    
        neg_freq = px.bar(data3.head(10), x='frequent', y='word', title="Top 10 Words Negative",
                         color='frequent', template='ggplot2')
        neg_freq.update_layout(yaxis={'categoryorder':'total descending'})
        st.plotly_chart(neg_freq, use_container_width=True)
        
    # Visualisasi tanggal komentar
    tgl_counts = df_selection['Tanggal'].value_counts().reset_index()
    tgl_counts.columns = ['Tanggal', 'Count']
    fig_tgl = px.area(tgl_counts, x='Tanggal', y='Count', title="Waktu", template='ggplot2')
    st.plotly_chart(fig_tgl, use_container_width=True)
    
    jk_left, ja_middle, kt_right = st.columns([1,1,2])
    with jk_left:
    # Visuaisasi jenis kelamin
        jenis_kelamin = df_selection['Jenis Kelamin'].value_counts()
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
        kategori = df_selection['Kategori'].value_counts()
        chart_kategori = px.bar(kategori, title=f"Kategori Pertanyaan pada {sumber_data}", color=kategori, template='seaborn')
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
                          random_state=1, background_color='white',#colormap='Pastel1',
                          collocations=False, normalize_plurals=False, collocation_threshold = 2, mode='RGBA', 
                          colormap='viridis').generate(ngram)#'PuBu_r'
            plt.figure(figsize=(10,10))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.subheader('Wordcloud')
            st.pyplot(plt, use_container_width=True)
            #with right:
        with right:
            text = ngram.split()
            freq = Counter(text)
            data = pd.DataFrame(freq.most_common(), columns=['word', 'frequent'])
        
            fig_freq = px.bar(data.head(20), x='frequent', y='word',color='frequent', template='gridon', height=500)
            fig_freq.update_layout(yaxis={'categoryorder':'total ascending'})
            st.subheader('Word Frequent')
            st.plotly_chart(fig_freq, use_container_width=True)

    with bi:
        bi_left, bi_right = st.columns(2)
        with bi_left:
            wordcloud_bigrams = WordCloud(width = 2000, height = 1334,
                                  random_state=1, background_color=None,colormap='Pastel1',
                                  collocations=False, normalize_plurals=False,
                                  collocation_threshold = 2).generate(bigram)

            plt.figure(figsize=(10,10))
            plt.imshow(wordcloud_bigrams, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.subheader('Bigram Wordcloud')
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
            st.subheader('Bigram Frequent')
            st.plotly_chart(fig_bi, use_container_width=True)

    with tri:
        tri_right, tri_left = st.columns(2)
        with tri_right:
            wordcloud_trigrams = WordCloud(width = 2000, height = 1334,
                              random_state=1, background_color='white',colormap='plasma',
                              collocations=False, normalize_plurals=False,
                              collocation_threshold = 2).generate(trigram)
        # visualisasi dengan matplotlib
            plt.figure(figsize=(10,10))
            plt.imshow(wordcloud_trigrams, interpolation='bilinear')
            plt.axis("off")
            plt.show()
            st.subheader('Trigram Wordcloud')
            st.pyplot(plt)

        with tri_left:
            text_tri = trigram.split()
            freq_tri = Counter(text_tri)
            data_tri = pd.DataFrame(freq_tri.most_common(), columns=['word', 'frequent'])
            data_tri.style.background_gradient(cmap='Blues')
            
            fig_tri = px.bar(data_tri.head(20), x='frequent', y='word',
                             color='frequent', title="Top 40 Words Trigrams", template='plotly')
            fig_tri.update_layout(yaxis={'categoryorder':'total ascending'})
            st.subheader('Trigram Frequent')
            st.plotly_chart(fig_tri, use_container_width=True)
