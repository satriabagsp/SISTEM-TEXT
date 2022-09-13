import streamlit as st
import pandas as pd
import all_func
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def app():

    st.title("Tokoh")
    # st.markdown(f'<h1 style="color:#fe9028;font-size:42px;">Pagu Anggaran</h1>', unsafe_allow_html=True)

    ## Read File
    df_berita = st.session_state["df_berita"]
    df_tokoh = st.session_state["df_tokoh"]

    # Filter
    df_tokoh_group = df_tokoh.groupby('nama_tokoh', as_index=False).count().sort_values(by=['id_berita'], ascending=False).reset_index(drop=True).rename(columns={'nama_tokoh':'Nama', 'id_berita':'Jumlah'})

    c1,c2,c3 = st.columns(3)

    with c1:
        tokoh = st.selectbox('Pilih Tokoh:',
            options=df_tokoh_group['Nama'].unique()
        )

    with c2:
        topik = st.selectbox('Pilih Topik:',
            options=df_berita['aspek'].unique()
        )

    # Filter DF berdasarkan isian tokoh
    df_tokoh_selection = df_tokoh.query(
        'nama_tokoh == @tokoh'
    )
    list_url = df_tokoh_selection['id_berita'].to_list()

    # Filter DF berdasarkan isian topik
    df_berita_selection = df_berita.query(
        'aspek == @topik'
    )
    df_berita_selection = df_berita_selection[df_berita_selection['url_berita'].isin(list_url)].reset_index(drop=True)
    
    st.markdown("""---""")
    
    col1, col2 = st.columns([1,4]) 

    with col1:
        st.write('**10 Tokoh Paling Sering Disebut**')
        st.dataframe(df_tokoh_group.head(10))

    with col2:
        jumlah_muncul_per_hari = (
                df_berita_selection.groupby('tanggal', as_index=False).agg(jumlah = ('url_berita','count'))
            )

        line_per_hari = px.line(jumlah_muncul_per_hari,
                x = 'tanggal',
                y = 'jumlah',
                orientation = 'v',
                title = f'<b>Jumlah Nama Tokoh Muncul Harian</b>',
                color_discrete_sequence = px.colors.qualitative.Set2,
                template = 'plotly_white',
                labels={'jumlah':'Jumlah Muncul', 'tanggal': 'Tanggal'}, 
                width = 750,
                height = 450
            )
        line_per_hari.update_layout(
                font=dict(
                    size=12,
                )
            )
        # line_per_hari.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)' })

        st.plotly_chart(line_per_hari, use_container_width=True)

    col_1, col_2 = st.columns([1,1]) 

    # WORDCLOUD
    with col_1:
        st.write('**Wordcloud terkait Tokoh**')
        # Teks
        teks_all = ' '.join(df_berita_selection['konten_clean'].to_list())

        # Wordcloud semua komentar
        wordcloud = WordCloud(width=1600, height=1500, max_font_size=200, background_color='white')
        wordcloud.generate(teks_all)

        plt.figure(figsize=(12,10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot(plt)


    # DATAFRAME BERITA
    with col_2:
        st.write('**Daftar Berita dimana Tokoh Disebut**')
        df_berita_selection['link'] = 'link'
        df_berita_filter = df_berita_selection[['judul_berita', 'tanggal', 'link']]
        st.dataframe(df_berita_filter)

    #     bulan = st.multiselect(
    #         'Pilih Bulan:',
    #         options=df_anggaran['Bulan'].unique(),
    #         default=df_anggaran['Bulan'].unique(),
    #     )

    # # Filter DF berdasarkan isian
    # df_selection = df_anggaran.query(
    #     'Bulan == @bulan & Uraian == @uraian'
    # )

    # # Sort df berdasarkan tanggal
    # df_selection = df_selection.sort_values(by=['Bulan Anggaran']).reset_index(drop=True)

    

    # # CARDBOX
    # nilai_pagu = int(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Pagu Anggaran'])
    # cb1, cb2, cb3, cb4 = st.columns(4)

    # lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    # htmlstr = f"""<p style='background-color: #2596ef; 
    #                         color: #FAFAFA; 
    #                         font-size: 32px; 
    #                         border-radius: 7px; 
    #                         padding-left: 12px; 
    #                         padding-top: 18px; 
    #                         padding-bottom: 18px; 
    #                         line-height:25px;'>
    #                         Rp. {"{:,}".format(nilai_pagu).replace(",",".")}
    #                         </style><BR><span style='font-size: 14px; 
    #                         margin-top: 0;'>Nilai Pagu - {uraian}</style></span></p>"""

    # cb1.markdown(lnk + htmlstr, unsafe_allow_html=True)

    # # Cek apakah milliar atau jutaan
    # if nilai_pagu / 1000000000 >= 1:
    #     # Mengubah pagu menjadi per milliaran
    #     df_selection['Pagu Anggaran'] = df_selection['Pagu Anggaran'] / 1000000000

    #     ## Bar chart nilai pagu
    #     bar1, bar2 = st.columns(2)
    #     # plot barchart bulanan
    #     with bar1:
    #         pagu_per_bulan = (
    #                 df_selection.groupby(by=['Bulan Anggaran'], as_index=False).sum(['Pagu Anggaran'])
    #             )
    #         fig_pagu_per_bulan = px.bar(pagu_per_bulan,
    #                 x = 'Bulan Anggaran',
    #                 y = 'Pagu Anggaran',
    #                 orientation = 'v',
    #                 title = f'<b>Anggaran Pagu per Bulan</b>',
    #                 # color_discrete_sequence = px.colors.qualitative.Set2,
    #                 color_discrete_sequence = ['#2596ef', '#fe9028', '#f00e94', '#11b6c9', '#45a04e', '#45a04e'],
    #                 template = 'plotly_white',
    #                 labels={'Pagu Anggaran':'Nilai Pagu <b>(Rp. Miliar)</b>', 'Bulan Anggaran': 'Bulan'}, 
    #                 width = 750,
    #                 height = 550
    #             )
    #         fig_pagu_per_bulan.update_layout(
    #                 font=dict(
    #                     size=12,
    #                 )
    #             )
    #         fig_pagu_per_bulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

    #         st.plotly_chart(fig_pagu_per_bulan, use_container_width=True)

    #     # plot barchart triwulanan
    #     with bar2:
    #         pagu_per_triwulan = (
    #                 df_selection.groupby(by=['Triwulan Anggaran'], as_index=False).tail(1)
    #             )
    #         fig_pagu_per_triwulan = px.bar(pagu_per_triwulan,
    #                 x = 'Triwulan Anggaran',
    #                 y = 'Pagu Anggaran',
    #                 orientation = 'v',
    #                 title = f'<b>Anggaran Pagu per Triwulan</b>',
    #                 color_discrete_sequence = ['#2596ef', '#fe9028', '#f00e94', '#11b6c9', '#45a04e', '#45a04e'],
    #                 template = 'plotly_white',
    #                 labels={'Pagu Anggaran':'Nilai Pagu <b>(Rp. Miliar)</b>', 'Triwulan Anggaran': 'Triwulan'}, 
    #                 width = 750,
    #                 height = 550
    #             )
    #         fig_pagu_per_triwulan.update_layout(
    #                 font=dict(
    #                     size=12,
    #                 )
    #             )
    #         fig_pagu_per_triwulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

    #         st.plotly_chart(fig_pagu_per_triwulan, use_container_width=True)

    # elif nilai_pagu / 1000000000 < 1:
    #     # Mengubah pagu menjadi per jutaan
    #     df_selection['Pagu Anggaran'] = df_selection['Pagu Anggaran'] / 1000000

    #     ## Bar chart nilai pagu
    #     bar1, bar2 = st.columns(2)

    #     # plot barchart bulanan
    #     with bar1:
    #         pagu_per_bulan = (
    #                 df_selection.groupby(by=['Bulan Anggaran'], as_index=False).sum(['Pagu Anggaran'])
    #             )
    #         fig_pagu_per_bulan = px.bar(pagu_per_bulan,
    #                 x = 'Bulan Anggaran',
    #                 y = 'Pagu Anggaran',
    #                 orientation = 'v',
    #                 title = f'<b>Anggaran Pagu per Bulan</b>',
    #                 # color_discrete_sequence = px.colors.qualitative.Set2,
    #                 color_discrete_sequence = ['#2596ef', '#fe9028', '#f00e94', '#11b6c9', '#45a04e', '#45a04e'],
    #                 template = 'plotly_white',
    #                 labels={'Pagu Anggaran':'Nilai Pagu (Rp. Juta)', 'Bulan Anggaran': 'Bulan'}, 
    #                 width = 750,
    #                 height = 550
    #             )
    #         fig_pagu_per_bulan.update_layout(
    #                 font=dict(
    #                     size=12,
    #                 )
    #             )
    #         fig_pagu_per_bulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

    #         st.plotly_chart(fig_pagu_per_bulan, use_container_width=True)

    #     # plot barchart triwulanan
    #     with bar2:
    #         pagu_per_triwulan = (
    #                 df_selection.groupby(by=['Triwulan Anggaran'], as_index=False).tail(1)
    #             )
    #         fig_pagu_per_triwulan = px.bar(pagu_per_triwulan,
    #                 x = 'Triwulan Anggaran',
    #                 y = 'Pagu Anggaran',
    #                 orientation = 'v',
    #                 title = f'<b>Anggaran Pagu per Triwulan</b>',
    #                 color_discrete_sequence = ['#2596ef', '#fe9028', '#f00e94', '#11b6c9', '#45a04e', '#45a04e'],
    #                 template = 'plotly_white',
    #                 labels={'Pagu Anggaran':'Nilai Pagu (Rp. Juta)', 'Triwulan Anggaran': 'Triwulan'}, 
    #                 width = 750,
    #                 height = 550
    #             )
    #         fig_pagu_per_triwulan.update_layout(
    #                 font=dict(
    #                     size=12,
    #                 )
    #             )
    #         fig_pagu_per_triwulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

    #         st.plotly_chart(fig_pagu_per_triwulan, use_container_width=True)


    # ## Pie Chart Persentase Nilai Pagu
    # # plot piechart bulanan
    # if uraian == 'Total':
    #     df_total = df_anggaran.query('Bulan == @bulan')
    #     pagu_per_kode = (
    #             df_total.groupby(by=['Uraian'], as_index=False).tail(1)
    #         )
    #     pagu_per_kode = pagu_per_kode[pagu_per_kode['Uraian'] != 'Total'].reset_index(drop=True)
        
    #     fig_pagu_per_kode = px.pie(pagu_per_kode,
    #             values = 'Pagu Anggaran',
    #             names = 'Uraian',
    #             title = f'<b>Proporsi Pagu</b>',
    #             width = 1250,
    #             height = 650,
    #             color_discrete_sequence=['#2596ef', '#fe9028', '#f00e94', '#11b6c9', '#45a04e', '#45a04e'],
    #         )
    #     fig_pagu_per_kode.update_traces(textposition='inside', textinfo='percent+label')
    #     fig_pagu_per_kode.update_layout(
    #             font=dict(
    #                 size=12,
    #             )
    #         )
    #     fig_pagu_per_kode.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

    #     st.plotly_chart(fig_pagu_per_kode, use_container_width=True)

    #     df_download = df_total[['Bulan', 'Kode', 'Uraian', 'Pagu Anggaran']]
    # else:
    #     df_download = df_selection[['Bulan', 'Kode', 'Uraian', 'Pagu Anggaran']]

    #     if nilai_pagu / 1000000000 >= 1:
    #         df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'] * 1000000000
    #     elif nilai_pagu / 1000000000 < 1:
    #         df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'] * 1000000
        
    #     df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'].astype('int64')
    
    # # df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'].apply('{:.}'.format)
    # df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'].map('{:,}'.format).str.replace(",", "~").str.replace(".", ",").str.replace("~", ".")

    # # Download Button
    # def convert_df(df):
    #     # IMPORTANT: Cache the conversion to prevent computation on every rerun
    #     return df.to_csv(index=False).encode('utf-8')

    # csv = convert_df(df_download)

    # st.download_button(
    #     label="Unduh Data",
    #     data=csv,
    #     file_name=f'Pagu Tarakan - {uraian}.csv',
    #     mime='text/csv',
    # )
        
    # st.dataframe(df_download)
