import streamlit as st
import pandas as pd
import all_func
import plotly.express as px
import plotly.graph_objects as go

def app():

    st.title("Target dan Realisasi Anggaran")
    # st.markdown(f'<h1 style="color:#fe9028;font-size:42px;">Target dan Realisasi Anggaran</h1>', unsafe_allow_html=True)
    # st.markdown("""---""")

    ## Read File
    df_anggaran = st.session_state["df_utama"]
    
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
    nilai_pagu = int(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Pagu Anggaran'])
    nilai_target = int(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Target Anggaran'])
    nilai_realisasi = int(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Realisasi Anggaran'])
    persen_realisasi = round(float(df_selection.drop_duplicates(subset=['Uraian'], keep='last')['Persentase Realisasi Anggaran']) * 100, 2)
    cb1, cb2, cb3, cb4 = st.columns(4)

    # Metric Nilai Pagu
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_1 = f"""<p style='background-color: #2596ef; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            Rp. {"{:,}".format(nilai_pagu).replace(",",".")}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Nilai Pagu</style></span></p>"""

    cb1.markdown(lnk + htmlstr_1, unsafe_allow_html=True)

    # Metric Nilai Target
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_2 = f"""<p style='background-color: #fe9028; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            Rp. {"{:,}".format(nilai_target).replace(",",".")}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Nilai Target</style></span></p>"""

    cb2.markdown(lnk + htmlstr_2, unsafe_allow_html=True)

    # Metric Nilai Realisasi
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_3 = f"""<p style='background-color: #45a04e; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            Rp. {"{:,}".format(nilai_realisasi).replace(",",".")}
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Nilai Realisasi</style></span></p>"""

    cb3.markdown(lnk + htmlstr_3, unsafe_allow_html=True)

    # Metric Persentase
    lnk = '<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.1/css/all.css" crossorigin="anonymous">'
    htmlstr_4 = f"""<p style='background-color: #45a04e; 
                            color: #FAFAFA; 
                            font-size: 32px; 
                            border-radius: 7px; 
                            padding-left: 12px; 
                            padding-top: 18px; 
                            padding-bottom: 18px; 
                            line-height:25px;'>
                            {persen_realisasi} %
                            </style><BR><span style='font-size: 14px; 
                            margin-top: 0;'>Persentase Realisasi</style></span></p>"""

    cb4.markdown(lnk + htmlstr_4, unsafe_allow_html=True)

    ## Bar chart nilai pagu
    bar1, bar2 = st.columns(2)

    # Cek apakah milliar atau jutaan
    if nilai_pagu / 1000000000 >= 1:
        # Mengubah anggaran per milliaran
        df_selection['Pagu Anggaran'] = df_selection['Pagu Anggaran'] / 1000000000
        df_selection['Target Anggaran'] = df_selection['Target Anggaran'] / 1000000000
        df_selection['Realisasi Anggaran'] = df_selection['Realisasi Anggaran'] / 1000000000

        # plot barchart bulanan
        with bar1:
            pagu_per_bulan = (
                    df_selection.groupby(by=['Bulan Anggaran'], as_index=False).sum(['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran'])
                )

            fig_pagu_per_bulan = px.bar(pagu_per_bulan,
                    x = 'Bulan Anggaran',
                    y = ['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran'],
                    orientation = 'v',
                    title = f'<b>Target dan Realisasi Anggaran per Bulan</b>',
                    color_discrete_sequence = ['#2596ef', '#fe9028', '#45a04e', '#f00e94', '#11b6c9'],
                    template = 'plotly_white',
                    labels={'value':'Nilai <b>(Rp. Miliar)</b>', 'Bulan Anggaran': 'Bulan'}, 
                    width = 750,
                    height = 550,
                )
            fig_pagu_per_bulan.update_layout(
                    font=dict(
                        size=12,
                    ),
                    barmode='group',
                    legend_title_text='Tipe Anggaran',
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

        # plot barchart triwulan
        with bar2:
            pagu_per_triwulan = (
                    df_selection.groupby(by=['Triwulan Anggaran'], as_index=False).tail(1)
                )
            fig_pagu_per_triwulan = px.bar(pagu_per_triwulan,
                    x = 'Triwulan Anggaran',
                    y = ['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran'],
                    orientation = 'v',
                    title = f'<b>Target dan Realisasi Anggaran per Triwulan</b>',
                    color_discrete_sequence = ['#2596ef', '#fe9028', '#45a04e', '#f00e94', '#11b6c9'],
                    template = 'plotly_white',
                    labels={'value':'Nilai <b>(Rp. Miliar)</b>', 'Triwulan Anggaran': 'Triwulan'}, 
                    width = 750,
                    height = 550
                )
            fig_pagu_per_triwulan.update_layout(
                    font=dict(
                        size=12,
                    ),
                    barmode='group',
                    legend_title_text='Tipe Anggaran',
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

    elif nilai_pagu / 1000000000 < 1:
        # Mengubah pagu menjadi per jutaan
        df_selection['Pagu Anggaran'] = df_selection['Pagu Anggaran'] / 1000000
        df_selection['Target Anggaran'] = df_selection['Target Anggaran'] / 1000000
        df_selection['Realisasi Anggaran'] = df_selection['Realisasi Anggaran'] / 1000000

        # plot barchart bulanan
        with bar1:
            pagu_per_bulan = (
                    df_selection.groupby(by=['Bulan Anggaran'], as_index=False).sum(['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran'])
                )

            fig_pagu_per_bulan = px.bar(pagu_per_bulan,
                    x = 'Bulan Anggaran',
                    y = ['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran'],
                    orientation = 'v',
                    title = f'<b>Target dan Realisasi Anggaran per Bulan</b>',
                    color_discrete_sequence = ['#2596ef', '#fe9028', '#45a04e', '#f00e94', '#11b6c9'],
                    template = 'plotly_white',
                    labels={'value':'Nilai <b>(Rp. Juta)</b>', 'Bulan Anggaran': 'Bulan'}, 
                    width = 750,
                    height = 550,
                )
            fig_pagu_per_bulan.update_layout(
                    font=dict(
                        size=12,
                    ),
                    barmode='group',
                    legend_title_text='Tipe Anggaran',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    )
                )

            fig_pagu_per_bulan.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })
            # fig_pagu_per_bulan.update_layout(yaxis_tickformat = 'M')

            st.plotly_chart(fig_pagu_per_bulan, use_container_width=True)

        # plot barchart triwulan
        with bar2:
            pagu_per_triwulan = (
                    df_selection.groupby(by=['Triwulan Anggaran'], as_index=False).tail(1)
                )
            fig_pagu_per_triwulan = px.bar(pagu_per_triwulan,
                    x = 'Triwulan Anggaran',
                    y = ['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran'],
                    orientation = 'v',
                    title = f'<b>Target dan Realisasi Anggaran per Triwulan</b>',
                    color_discrete_sequence = ['#2596ef', '#fe9028', '#45a04e', '#f00e94', '#11b6c9'],
                    template = 'plotly_white',
                    labels={'value':'Nilai <b>(Rp. Juta)</b>', 'Triwulan Anggaran': 'Triwulan'}, 
                    width = 750,
                    height = 550
                )
            fig_pagu_per_triwulan.update_layout(
                    font=dict(
                        size=12,
                    ),
                    barmode='group',
                    legend_title_text='Tipe Anggaran',
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

    ## Pie Chart Persentase Nilai Pagu
    if uraian == 'Total':
        df_total = df_anggaran.query('Bulan == @bulan')
        pagu_per_kode = (
                df_total.groupby(by=['Uraian'], as_index=False).tail(1)
            )
        pagu_per_kode = pagu_per_kode[pagu_per_kode['Uraian'] != 'Total'].reset_index(drop=True)

        fig_pagu_per_kode = px.pie(pagu_per_kode,
                values = 'Realisasi Anggaran',
                names = 'Uraian',
                title = f'<b>Proporsi Realisasi</b>',
                width = 1250,
                height = 650,
                color_discrete_sequence=['#2596ef', '#fe9028', '#45a04e', '#f00e94', '#11b6c9'],
                # color_discrete_sequence = ['#0083B8'] * len(pagu_per_triwulan),
                # template = 'plotly_white',
                # labels={'pagu_anggaran':'Pagu', 'triwulan_anggaran': 'Triwulan'}, 
            )
        fig_pagu_per_kode.update_traces(textposition='inside', textinfo='percent+label')
        fig_pagu_per_kode.update_layout(
                font=dict(
                    size=12,
                )
            )
        fig_pagu_per_kode.update_layout({ 'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': '#2c2f38', })

        st.plotly_chart(fig_pagu_per_kode, use_container_width=True)

        df_download = df_total[['Bulan', 'Kode', 'Uraian', 'Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran', 'Persentase Realisasi Anggaran']]
    else:
        df_download = df_selection[['Bulan', 'Kode', 'Uraian', 'Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran', 'Persentase Realisasi Anggaran']]

        if nilai_pagu / 1000000000 >= 1:
            df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'] * 1000000000
            df_download['Target Anggaran'] = df_download['Target Anggaran'] * 1000000000
            df_download['Realisasi Anggaran'] = df_download['Realisasi Anggaran'] * 1000000000
        elif nilai_pagu / 1000000000 < 1:
            df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'] * 1000000
            df_download['Target Anggaran'] = df_download['Target Anggaran'] * 1000000
            df_download['Realisasi Anggaran'] = df_download['Realisasi Anggaran'] * 1000000
        
        df_download[['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran']] = df_download[['Pagu Anggaran', 'Target Anggaran', 'Realisasi Anggaran']].astype('int64')

    df_download['Pagu Anggaran'] = df_download['Pagu Anggaran'].map('{:,}'.format).str.replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    df_download['Target Anggaran'] = df_download['Target Anggaran'].map('{:,}'.format).str.replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    df_download['Realisasi Anggaran'] = df_download['Realisasi Anggaran'].map('{:,}'.format).str.replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    df_download['Persentase Realisasi Anggaran'] = df_download['Persentase Realisasi Anggaran'] * 100
    df_download['Persentase Realisasi Anggaran'] = df_download['Persentase Realisasi Anggaran'].map('{:,.4f}'.format).str.replace(".", ",")

    # Download Button
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df_download)

    st.download_button(
        label="Unduh Data",
        data=csv,
        file_name=f'Target dan Realisasi Anggaran Tarakan - {uraian}.csv',
        mime='text/csv',
    )
        
    st.dataframe(df_download)
