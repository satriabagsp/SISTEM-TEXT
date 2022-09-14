from re import S
import streamlit as st
import pandas as pd
import all_func
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image

def app():

    st.title("News Portal")
    # st.markdown(f'<h1 style="color:#fe9028;font-size:42px;">Pagu Anggaran</h1>', unsafe_allow_html=True)

    ## Read File
    df_berita = st.session_state["df_berita"]
    df_tokoh = st.session_state["df_tokoh"]
    df_berita['konten_clean'] = df_berita['konten_clean'].astype(str)

    # Filter
    df_tokoh_group = df_tokoh.groupby('nama_tokoh', as_index=False).count().sort_values(by=['id_berita'], ascending=False).reset_index(drop=True).rename(columns={'nama_tokoh':'Nama', 'id_berita':'Jumlah'})

    c1,c2,c3 = st.columns(3)

    with c1:
        topik = st.selectbox('Pilih Topik:',
            options=df_berita['aspek'].unique()
        )

    with c2:
        list_nama = df_tokoh_group['Nama'].drop_duplicates().to_list()
        list_nama = ['Semua'] + list_nama 
        tokoh = st.selectbox('Pilih Tokoh:',
            options = list_nama
        )

    # Filter DF berdasarkan isian topik
    df_berita_selection = df_berita.query(
        'aspek == @topik'
    )

    # Filter DF berdasarkan isian tokoh
    if tokoh == 'Semua':
        df_tokoh_selection = df_tokoh
    else:
        df_tokoh_selection = df_tokoh.query(
            'nama_tokoh == @tokoh'
        )
    list_url = df_tokoh_selection['id_berita'].to_list()

    # Filter DF berdasarkan isian topik
    df_berita_selection = df_berita.query(
        'aspek == @topik'
    )

    if tokoh == 'Semua':
        df_berita_selection = df_berita_selection
    else:
        df_tokoh_selection = df_tokoh.query(
                'nama_tokoh == @tokoh'
            )
        list_url = df_tokoh_selection['id_berita'].to_list()
        df_berita_selection = df_berita_selection[df_berita_selection['url_berita'].isin(list_url)].reset_index(drop=True)
    
    st.markdown("""---""")
    
    col1, col2, col3 = st.columns([4,1,1]) 

    # Line jumlah berita harian
    with col1:
        jumlah_muncul_per_hari = (
                df_berita_selection.groupby('tanggal', as_index=False).agg(jumlah = ('url_berita','count'))
            ) 
        jumlah_muncul_per_hari = jumlah_muncul_per_hari[jumlah_muncul_per_hari['tanggal'] != '0000-00-00']
        line_per_hari = px.line(jumlah_muncul_per_hari,
                x = 'tanggal',
                y = 'jumlah',
                orientation = 'v',
                title = f'<b>Pemberitaan Harian</b>',
                color_discrete_sequence = px.colors.qualitative.Set2,
                template = 'plotly_white',
                labels={'jumlah':'Jumlah Muncul', 'tanggal': 'Tanggal'}, 
                width = 1250,
                height = 450
            )
        line_per_hari.update_layout(
                font=dict(
                    size=12,
                ),
            )

        st.plotly_chart(line_per_hari, use_container_width=True)

    # Tokoh Berita
    with col2:
        st.write('**Top 10 Tokoh Disebut**')
        st.write(df_tokoh_group.set_index('Nama').head(10))

    # Pie sumber berita harian
    with col3:
        sumber_berita = (
                df_berita_selection.groupby(by=['sumber'], as_index=False).count()
            )
        sumber_berita = sumber_berita[['sumber', 'url_berita']].rename(columns={'sumber':'Sumber','url_berita':'Jumlah'})
        st.write('**Sumber Berita**')
        st.write(sumber_berita.set_index('Sumber'))
            
        # pie_sumber_berita = px.pie(sumber_berita,
        #         values = 'url_berita',
        #         names = 'sumber',
        #         title = f'<b>Sumber Berita</b>',
        #         width = 1250,
        #         height = 650,
        #         color_discrete_sequence = px.colors.qualitative.Set2,
        #         # template = 'plotly_white',
        #         labels={'sumber':'Sumber', 'url_berita': 'Jumlah'}, 
        #     )
        # pie_sumber_berita.update_traces(textposition='inside', textinfo='percent+label')
        # pie_sumber_berita.update_layout(
        #         font=dict(
        #             size=12,
        #         )
        #     )
        # pie_sumber_berita.update(layout_showlegend=False)
        # pie_sumber_berita.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)'})

        # st.plotly_chart(pie_sumber_berita, use_container_width=True)


    col_1, col_2 = st.columns([1,1]) 

    # WORDCLOUD
    with col_1:
        st.write('**Wordcloud Terkait**')
        # Teks
        # teks_all = ' '.join(df_berita_selection['konten_clean'].to_list())

        # # Wordcloud semua komentar
        # wordcloud = WordCloud(width=1600, height=1500, max_font_size=200, background_color='white', collocations=False)
        # wordcloud.generate(teks_all)

        # plt.figure(figsize=(12,10))
        # plt.imshow(wordcloud, interpolation='bilinear')
        # plt.axis("off")
        # st.pyplot(plt)

        image = Image.open('Data/wordcloud berita.png')
        st.image(image)


    # DATAFRAME BERITA
    with col_2:
        st.write('**Daftar Berita Terkait**')
        df_berita_selection['link'] = 'link'
        df_berita_filter = df_berita_selection[['judul_berita', 'tanggal', 'link']]
        df_berita_filter = df_berita_filter.rename(columns={'judul_berita':'Judul','tanggal':'Tanggal','link':'Link'})
        st.dataframe(df_berita_filter.set_index('Judul'))