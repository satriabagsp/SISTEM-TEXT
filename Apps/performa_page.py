import streamlit as st
import pandas as pd
import all_func
import plotly.express as px
import plotly.graph_objects as go

def app():

    st.title("Laporan Performa")
    # st.markdown(f'<h1 style="color:#fe9028;font-size:42px;">Capaian Kinerja</h1>', unsafe_allow_html=True)

    ## Read File
    df_anggaran = st.session_state["df_utama"]
    df_anggaran = df_anggaran[~df_anggaran['Satuan Kinerja'].isna()]
    df_anggaran['Persentase Realisasi Anggaran'] = round(df_anggaran['Persentase Realisasi Anggaran'] * 100, 2)
    df_anggaran['Progress Capaian Kinerja'] = round(df_anggaran['Progress Capaian Kinerja'] * 100, 2)
    df_anggaran['GAP'] = round(df_anggaran['GAP'] * 100, 2)

    # st.table(df_anggaran)
    col1, col2 = st.columns(2)

    with col1:
        uraian = st.selectbox('Pilih Kode Anggaran:',
            options=df_anggaran['Uraian'].unique()
        )

    with col2:
        bulan = st.multiselect(
            'Pilih Bulan:',
            options=df_anggaran['Bulan'].unique(),
            default=df_anggaran['Bulan'].unique(),
        )

    # Filter DF berdasarkan isian
    df_selection = df_anggaran.query(
        'Bulan == @bulan & Uraian == @uraian'
    )

    # Sort df berdasarkan tanggal
    df_selection = df_selection.sort_values(by=['Bulan Anggaran']).reset_index(drop=True)

    st.markdown("""---""")

    # CARDBOX
    cb1, cb2, cb3 = st.columns(3)
    persentase_realisasi = float(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Persentase Realisasi Anggaran'])
    persentase_kinerja = float(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Progress Capaian Kinerja'])
    gap = float(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['GAP'])

    # Metric Realisasi Kinerja
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_1 = f"""<p style='background-color: #2596ef; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {persentase_realisasi} %
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Realisasi Anggaran</style></span></p>"""

    cb1.markdown(lnk + htmlstr_1, unsafe_allow_html=True)

    # Metric Persentase Kinerja
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_2 = f"""<p style='background-color: #fe9028; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {persentase_kinerja} %
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Progress Capaian Kinerja</style></span></p>"""

    cb2.markdown(lnk + htmlstr_2, unsafe_allow_html=True)

    # Metric Target Kinerja
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_3 = f"""<p style='background-color: #f94144; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {gap} %
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>GAP</style></span></p>"""

    cb3.markdown(lnk + htmlstr_3, unsafe_allow_html=True)

    ## Bar chart performa bulanan
    bar1, bar2 = st.columns(2)

    # plot barchart bulanan
    with bar1:
        pagu_per_bulan = (
                df_selection.groupby(by=['Bulan Anggaran'], as_index=False).sum(['Persentase Realisasi Anggaran', 'Progress Capaian Kinerja', 'GAP'])
            )

        fig_pagu_per_bulan = px.bar(pagu_per_bulan,
                x = 'Bulan Anggaran',
                y = ['Persentase Realisasi Anggaran', 'Progress Capaian Kinerja', 'GAP'],
                orientation = 'v',
                title = f'<b>Performa Anggaran dan Kinerja per Bulan</b>',
                color_discrete_sequence = ['#2596ef', '#fe9028', '#f94144'],
                template = 'plotly_white',
                labels={'value':'Capaian', 'Bulan Anggaran': 'Bulan'}, 
                width = 750,
                height = 550,
            )
        fig_pagu_per_bulan.update_layout(
                font=dict(
                    size=12,
                ),
                barmode='group',
                legend_title_text='Tipe Capaian',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
        fig_pagu_per_bulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })
        # fig_pagu_per_bulan.update_yaxes(range=[0, 100])

        st.plotly_chart(fig_pagu_per_bulan, use_container_width=True)

    # plot barchart triwulanan
    with bar2:
        pagu_per_triwulan = (
                df_selection.groupby(by=['Triwulan Anggaran'], as_index=False).tail(1)
            )
        fig_pagu_per_triwulan = px.bar(pagu_per_triwulan,
                x = 'Triwulan Anggaran',
                y = ['Persentase Realisasi Anggaran', 'Progress Capaian Kinerja', 'GAP'],
                orientation = 'v',
                title = f'<b>Performa Anggaran dan Kinerja per Triwulan</b>',
                color_discrete_sequence = ['#2596ef', '#fe9028', '#f94144'],
                template = 'plotly_white',
                labels={'value':'Capaian', 'Triwulan Anggaran': 'Triwulan'}, 
                width = 750,
                height = 550
            )
        fig_pagu_per_triwulan.update_layout(
                font=dict(
                    size=12,
                ),
                barmode='group',
                legend_title_text='Tipe Capaian',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
        fig_pagu_per_triwulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })
        # fig_pagu_per_triwulan.update_yaxes(range=[,100])

        st.plotly_chart(fig_pagu_per_triwulan, use_container_width=True)


    # DATA UNTUK DITAMPILKAN DAN DIDOWNLOAD
    df_download = df_selection[['Bulan', 'Kode', 'Uraian', 'Persentase Realisasi Anggaran', 'Progress Capaian Kinerja', 'GAP', 'Referensi', 'Keterangan']]

    # df_download[['Persentase Realisasi Anggaran', 'Progress Capaian Kinerja', 'GAP']] = df_download[['Persentase Realisasi Anggaran', 'Progress Capaian Kinerja', 'GAP']].astype(float)
    # # df_download['Persentase Realisasi Anggaran'] = df_download['Persentase Realisasi Anggaran'].apply(lambda x: round(x, 2))
    # # df_download = df_download.round({'Persentase Realisasi Anggaran': 0})
    df_download['Persentase Realisasi Anggaran'] = df_download['Persentase Realisasi Anggaran'].map('{:,.3f}'.format).str.replace(".", ",")
    df_download['Progress Capaian Kinerja'] = df_download['Progress Capaian Kinerja'].map('{:,.3f}'.format).str.replace(".", ",")
    df_download['GAP'] = df_download['GAP'].map('{:,.3f}'.format).str.replace(".", ",")

    # Download Button
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df_download)

    st.download_button(
        label="Unduh Data",
        data=csv,
        file_name=f'Laporan Performa Tarakan - {uraian}.csv',
        mime='text/csv',
    )
        
    st.dataframe(df_download)
