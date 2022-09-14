from re import S
import streamlit as st
import pandas as pd
import all_func
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast
from PIL import Image

def app():

    st.title("Social Media Portal")

    ## Read File
    df_twitter = pd.read_csv('Data/pemilu2024.csv')
    df_twitter = df_twitter[['id','date','mentioned','hashtags','tweet_clean','username','likeCount', 'renderedContent','retweetCount']]
    df_twitter['date'] = pd.to_datetime(df_twitter['date']).dt.date
    df_twitter['media'] = 'Media Sosial'
    df_twitter['aspek'] = 'Pemilu'
    df_twitter['tweet_clean'] = df_twitter['tweet_clean'].astype(str)
    df_twitter['id'] = df_twitter['id'].astype(str)

    c1,c2,c3 = st.columns(3)

    with c1:
        topik = st.selectbox('Pilih Topik:',
            options=df_twitter['aspek'].unique()
        )

    # Filter DF berdasarkan isian topik
    df_twitter_selection = df_twitter.query(
        'aspek == @topik'
    )

    st.markdown("""---""")

    card1, card2, card3, card4 = st.columns(4)
    card1.metric("Total Tweets", "99398")
    card2.metric("Total Retweets", "217152")
    card3.metric("Total Likes", "685152")
    card4.metric("Total Replies", "13819")
    
    col1, col2, col3 = st.columns([4,1,1]) 

    # Line jumlah berita harian
    with col1:
        jumlah_muncul_per_hari = (
                df_twitter.groupby('date', as_index=False).agg(jumlah = ('id','count'))
            ) 

        line_per_hari = px.line(jumlah_muncul_per_hari,
                x = 'date',
                y = 'jumlah',
                orientation = 'v',
                title = f'<b>Tweets Harian</b>',
                color_discrete_sequence = px.colors.qualitative.Set2,
                template = 'plotly_white',
                labels={'jumlah':'Jumlah Muncul', 'date': 'Tanggal'}, 
                width = 1250,
                height = 450
            )
        line_per_hari.update_layout(
                font=dict(
                    size=12,
                ),
            )

        st.plotly_chart(line_per_hari, use_container_width=True)

    # Mention
    with col2:
        # Most Accounts Mentioned in Tweet
        mentioned = list()
        for user in df_twitter.mentioned:
            if not pd.isna(user):
                for i in ast.literal_eval(user):
                    mentioned.append(i)

        st.write('**Top 10 Akun Dimention**')
        aa = pd.DataFrame(mentioned, columns=['Accounts']).Accounts.value_counts().sort_values(ascending=False)[:10]
        st.dataframe(aa)

    # Hashtag
    with col3:
        hastags = list()
        for tags in df_twitter.hashtags:
            if not pd.isna(tags):
                for i in ast.literal_eval(tags):
                    hastags.append(i)

        st.write('**Top 10 Hashtag**')
        bb = pd.DataFrame(hastags, columns=['hastags']).hastags.value_counts().sort_values(ascending=False)[:10]
        st.dataframe(bb)

    col_1, col_2 = st.columns(2) 

    # NETWORK ANALISIS
    with col_1:
        st.write('**Network Analysis**')
        image = Image.open('Data/Network.jpeg')

        st.image(image, width=672)


    # WORDCLOUD
    with col_2:
        st.write('**Wordcloud**')
        # # Teks
        # teks_all = ' '.join(df_twitter['tweet_clean'].to_list())

        # # Wordcloud semua komentar
        # wordcloud = WordCloud(width=1600, height=1500, max_font_size=200, background_color='white', collocations=False)
        # wordcloud.generate(teks_all)

        # plt.figure(figsize=(12,10))
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis("off")
        # st.pyplot(plt)
        image = Image.open('Data/wordcloud.png')

        st.image(image)

    c1, c2 = st.columns(2) 

    # TOP LIKED
    with c1:
        st.write('**Top 5 Likes Tweet**')
        # Most Liked Tweet by Account
        like_most = df_twitter.sort_values(by='likeCount',ascending=False)[:5]
        st.table(like_most[['renderedContent', 'likeCount']].set_index('renderedContent'))

    # TOP RETWEET
    with c2:
        st.write('**Top 5 Retweeted Tweet**')
        # Most Liked Tweet by Account
        like_most = df_twitter.sort_values(by='retweetCount',ascending=False)[:5]
        st.table(like_most[['renderedContent', 'retweetCount']].set_index('renderedContent'))