import streamlit as st
import pandas as pd
import all_func
import plotly.express as px
import plotly.graph_objects as go

def app():

    st.title("Capaian Kinerja")
    # st.markdown(f'<h1 style="color:#fe9028;font-size:42px;">Capaian Kinerja</h1>', unsafe_allow_html=True)

    ## Read File
    df_anggaran = st.session_state["df_utama"]
    df_caput = df_anggaran[~df_anggaran['Satuan Kinerja'].isna()]
    df_caput[['Target Kinerja', 'Progress Capaian Kinerja']] = df_caput[['Target Kinerja', 'Progress Capaian Kinerja']].astype(float)
    df_caput['Capaian Kinerja'] = df_caput['Target Kinerja'] * df_caput['Progress Capaian Kinerja']


    col1, col2 = st.columns(2)

    with col1:
        uraian = st.selectbox('Pilih Kode Anggaran:',
            options=df_caput['Uraian'].unique()
        )

    with col2:
        bulan = st.multiselect(
            'Pilih Bulan:',
            options=df_caput['Bulan'].unique(),
            default=df_caput['Bulan'].unique(),
        )

    # Filter DF berdasarkan isian
    df_selection = df_caput.query(
        'Bulan == @bulan & Uraian == @uraian'
    )

    # Sort df berdasarkan tanggal
    df_selection = df_selection.sort_values(by=['Bulan Anggaran']).reset_index(drop=True)

    st.markdown("""---""")

    # CARDBOX
    cb1, cb2, cb3, cb4 = st.columns(4)
    target_kinerja = round(float(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Target Kinerja']), 2)
    persentase_kinerja = round(float(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Progress Capaian Kinerja']) * 100, 2)
    realisasi_kinerja = round(float(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Realisasi Kinerja']), 2)
    satuan_kinerja = df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Satuan Kinerja'].to_list()[0]
    referensi_kinerja = df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Referensi'].to_list()[0]
    keterangan_kinerja = df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Keterangan'].to_list()[0]

    # Metric Realisasi Kinerja
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_1 = f"""<p style='background-color: #45a04e; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {realisasi_kinerja}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Realisasi Kinerja</style></span></p>"""

    cb2.markdown(lnk + htmlstr_1, unsafe_allow_html=True)

    # Metric Persentase Kinerja
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_2 = f"""<p style='background-color: #45a04e; 
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

    cb3.markdown(lnk + htmlstr_2, unsafe_allow_html=True)

    # Metric Target Kinerja
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_3 = f"""<p style='background-color: #fe9028; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {target_kinerja}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Target Kinerja</style></span></p>"""

    cb1.markdown(lnk + htmlstr_3, unsafe_allow_html=True)

    # Metric Satuan
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_4 = f"""<p style='background-color: #f00e94; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {satuan_kinerja}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Satuan Kinerja</style></span></p>"""

    cb4.markdown(lnk + htmlstr_4, unsafe_allow_html=True)

    # Metric Keterangan
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_5 = f"""<p style='background-color: #11b6c9; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {keterangan_kinerja}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Keterangan</style></span></p>"""

    st.markdown(lnk + htmlstr_5, unsafe_allow_html=True)

    ## Bar chart nilai pagu
    bar1, bar2 = st.columns(2)

    # plot barchart bulanan
    with bar1:
        pagu_per_bulan = (
                df_selection.groupby(by=['Bulan Anggaran'], as_index=False).sum(['Target Kinerja', 'Capaian Kinerja'])
            )

        fig_pagu_per_bulan = px.bar(pagu_per_bulan,
                x = 'Bulan Anggaran',
                y = ['Target Kinerja', 'Capaian Kinerja'],
                orientation = 'v',
                title = f'<b>Realisasi Kinerja per Bulan</b>',
                color_discrete_sequence = ['#fe9028', '#45a04e'],
                template = 'plotly_white',
                labels={'value':'Progress Capaian (%)', 'Bulan Anggaran': 'Bulan'}, 
                width = 750,
                height = 550,
            )
        fig_pagu_per_bulan.update_layout(
                font=dict(
                    size=12,
                ),
                barmode='group',
                legend_title_text='Tipe Kinerja',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
        fig_pagu_per_bulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

        st.plotly_chart(fig_pagu_per_bulan, use_container_width=True)

    # plot barchart bulanan
    with bar2:
        pagu_per_triwulan = (
                df_selection.groupby(by=['Triwulan Anggaran'], as_index=False).tail(1)
            )
        fig_pagu_per_triwulan = px.bar(pagu_per_triwulan,
                x = 'Triwulan Anggaran',
                y = ['Target Kinerja', 'Capaian Kinerja'],
                orientation = 'v',
                title = f'<b>Realisasi Kinerja per Triwulan</b>',
                color_discrete_sequence = ['#fe9028', '#45a04e'],
                template = 'plotly_white',
                labels={'value':'Progress Capaian (%)', 'Triwulan Anggaran': 'Triwulan'}, 
                width = 750,
                height = 550
            )
        fig_pagu_per_triwulan.update_layout(
                font=dict(
                    size=12,
                ),
                barmode='group',
                legend_title_text='Tipe Kinerja',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
        fig_pagu_per_triwulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

        st.plotly_chart(fig_pagu_per_triwulan, use_container_width=True)


    # DATA UNTUK DITAMPILKAN DAN DIDOWNLOAD
    df_download = df_selection[['Bulan', 'Kode', 'Uraian', 'Target Kinerja', 'Satuan Kinerja', 'Realisasi Kinerja', 'Progress Capaian Kinerja', 'GAP', 'Referensi', 'Keterangan']]
    df_download['Realisasi Kinerja'] = df_download['Realisasi Kinerja'].map('{:,.3f}'.format).str.replace(".", ",")
    df_download['Target Kinerja'] = df_download['Target Kinerja'].map('{:,.3f}'.format).str.replace(".", ",")
    df_download['Progress Capaian Kinerja'] = df_download['Progress Capaian Kinerja'] * 100
    df_download['Progress Capaian Kinerja'] = df_download['Progress Capaian Kinerja'].map('{:,.3f}'.format).str.replace(".", ",")
    df_download['GAP'] = df_download['GAP'] * 100
    df_download['GAP'] = df_download['GAP'].map('{:,.3f}'.format).str.replace(".", ",")


    # Download Button
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df_download)

    st.download_button(
        label="Unduh Data",
        data=csv,
        file_name=f'Capaian Kinerja (Output) Tarakan - {uraian}.csv',
        mime='text/csv',
    )
        
    st.dataframe(df_download)
