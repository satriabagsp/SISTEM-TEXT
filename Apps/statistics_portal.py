from re import S
import streamlit as st
import pandas as pd
import all_func
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def app():

    st.title("Statistics Portal")

    ## Read File
    df_berita = st.session_state["df_berita"]
    df_twitter = st.session_state["df_twitter"]

    # Clean
    df_berita = df_berita[df_berita['tanggal'] >= '2022-01-01']
    df_berita = df_berita[['url_berita','konten_clean','tanggal','sentimen_berita']].rename(columns={'url_berita':'id','sentimen_berita':'sentiment', 'tanggal':'date','konten_clean':'suara'})
    df_berita['media'] = 'Berita Online'
    df_twitter = df_twitter[['id','renderedContent','date','sentiment']].rename(columns={'renderedContent':'suara'})
    df_twitter['media'] = 'Media Sosial'
    df_twitter['id'] = df_twitter['id'].astype(str)
    df_all = pd.concat([df_berita,df_twitter])
    df_all['date'] = pd.to_datetime(df_all['date']).dt.date
    df_all['aspek'] = 'Pemilu'

    # Pilihan (Dropdownlist)
    c1,c2,c3 = st.columns(3)
    with c1:
        topik = st.selectbox('Pilih Topik:',
            options=df_all['aspek'].unique()
        )


    # Filter DF berdasarkan isian topik
    df_all_selection = df_all.query(
        'aspek == @topik'
    )
    
    st.markdown("""---""")
    
    card1, card2, card3, card4 = st.columns(4)
    card1.metric("Suara Berita Online", len(df_all_selection[df_all_selection.media == 'Berita Online']))
    card2.metric("Suara Media Sosial", len(df_all_selection[df_all_selection.media == 'Media Sosial']))
    
    col1, col2= st.columns([4,2]) 

    # Line jumlah berita harian
    with col1:
        jumlah_muncul_per_hari = (
                df_all_selection.groupby(['media', 'date'], as_index=False).agg(jumlah = ('id','count'))
            ) 
        jumlah_muncul_per_hari = jumlah_muncul_per_hari[jumlah_muncul_per_hari['date'] != '0000-00-00']
        line_per_hari = px.line(jumlah_muncul_per_hari,
                x = 'date',
                y = 'jumlah',
                color='media',
                orientation = 'v',
                title = f'<b>Jumlah Suara menurut Media</b>',
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

    with col2:
        jumlah_sentimen_per_media = (
                df_all_selection.groupby(['media', 'sentiment'], as_index=False).agg(jumlah = ('id','count'))
            ) 
        line_per_hari = px.bar(jumlah_sentimen_per_media,
                x = 'media',
                y = 'jumlah',
                color='sentiment',
                orientation = 'v',
                title = f'<b>Jumlah Sentimen menurut Media</b>',
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


    col_1, col_2 = st.columns([1,1]) 

    with col_1:
        jumlah_sentimen = (
                df_all_selection.groupby(['sentiment'], as_index=False).agg(jumlah = ('id','count'))
            ) 
        pie_sumber_berita = px.pie(jumlah_sentimen,
                values = 'jumlah',
                names = 'sentiment',
                title = f'<b>Sentimen</b>',
                width = 1250,
                height = 650,
                color_discrete_sequence = px.colors.qualitative.Set2,
                # template = 'plotly_white',
                labels={'sentiment':'Sentimen Suara', 'jumlah': 'Jumlah'}, 
            )
        pie_sumber_berita.update_traces(textposition='inside', textinfo='percent+label')
        pie_sumber_berita.update_layout(
                font=dict(
                    size=12,
                )
            )
        # pie_sumber_berita.update(layout_showlegend=False)
        pie_sumber_berita.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

        st.plotly_chart(pie_sumber_berita, use_container_width=True)


    # DATAFRAME ISI
    with col_2:
        st.write('**Isi Suara**')
        
        st.dataframe(df_all[['media','date','suara','sentiment']].sample(100))