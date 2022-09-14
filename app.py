from email.policy import default
from sklearn.feature_selection import SelectFromModel
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
import yaml
from PIL import Image
import all_func
import plotly.express as px
from Apps import capaian_kinerja_page, datamaster_page, target_realisasi_page, performa_page, tokoh
from deta import Deta  # Import Deta
import io

# Fullscreen
im = Image.open("Image/page_icon.png")
st.set_page_config(
        page_title="MOCKUP - ANALISIS TEKS PEMILU",
        page_icon=im,
        layout="wide",
    )

# Remove Whitespace, hamburger, and "Made with streamlit"
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             .css-18e3th9 {
#                     padding-top: 0rem;
#                     padding-bottom: 10rem;
#                     padding-left: 5rem;
#                     padding-right: 5rem;
#                 }
#                .css-1d391kg {
#                     padding-top: 3.5rem;
#                     padding-right: 1rem;
#                     padding-bottom: 3.5rem;
#                     padding-left: 1rem;
#                 }
#         </style>
#             """

hide_streamlit_style = """
            <style>
            .css-18e3th9 {
                    padding-top: 0rem;
                    padding-bottom: 10rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
               .css-1d391kg {
                    padding-top: 3.5rem;
                    padding-right: 1rem;
                    padding-bottom: 3.5rem;
                    padding-left: 1rem;
                }
        </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Configuration login/logout function
with open('Users Data/config.yaml') as file:
    config = yaml.safe_load(file)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Login Page
judul = st.markdown("<h1 style='text-align: center; color: #f94144;'>Mockup Analisis Teks Pemilu</h1>", unsafe_allow_html=True)
# subjudul = st.markdown("<h2 style='text-align: center; color: #ffffff;'>Sistem Evaluasi Dini Berbasis Anggaran dan Kinerja</h2>", unsafe_allow_html=True)
    
col1, col2, col3 = st.columns(3)
with col2:
    # Login form
    name, authentication_status, username = authenticator.login('Login', 'main')

if st.session_state["authentication_status"]:
    # st.write(f'Welcome *{st.session_state["name"]}*')
    judul.empty()
    # subjudul.empty()

    ## Read File
    df_berita = all_func.get_data_berita()
    df_tokoh = all_func.get_data_tokoh()
    st.session_state["df_berita"] = df_berita
    st.session_state["df_tokoh"] = df_tokoh

    # st.table(df_utama)

    if st.session_state["username"] == 'admin':
        # Sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title = 'MOCKUP ANALISIS',
                menu_icon = 'ui-radios',
                options = ['Beranda', 'News Portal', 'Social Media Portal', 'Statistics Portal (Sentiment)', 'Location Portal', 'Demography Portal', 'Emotion Portal', 'SNA', 'NER',  'Atur Profil'],
                icons = ['house-door', 'journal-album', 'bullseye', 'gear']
            )
    else:
        # Sidebar menu
        with st.sidebar:
            selected = option_menu(
                menu_title = 'SIDINIBAKERJA',
                menu_icon = 'ui-radios',
                options = ['Beranda', 'Pagu Anggaran', 'Target dan Realisasi', 'Capaian Kinerja/Output', 'Laporan Performa', 'Atur Profil'],
                icons = ['house-door', 'journal-album', 'journal-check', 'bullseye', 'clipboard-data', 'gear']
            )

    with st.sidebar:
        authenticator.logout('Logout', 'main')

    # Halaman Beranda
    if selected == 'Beranda':
        st.title('MOCKUP - ANALISIS TEKS PEMILU')

        st.markdown("""---""")

        st.warning(
                f"""
                Selamat datang **{st.session_state["name"]}**,

                **MOCKUP - ANALISIS TEKS PEMILU** merupakan mockup aplikasi analisis teks.

                Untuk pertanyaan atau masukan silakan hubungi **Admin** melalui
                [E-Mail](https://mail.google.com/) | [Twitter](https://twitter.com/) | [YouTube](https://www.youtube.com/c/).
                """
                )

    if selected == 'News Portal':
        tokoh.app()

    if selected == 'Atur Profil':
        st.title(selected)
        
        st.markdown("""---""")

        # Fungsi ADMIN
        colpro1, colpro2 = st.columns(2)
        with colpro1:
            # Ganti Password
            with st.expander("Ganti Password"):
                pass
                if authentication_status:
                    try:
                        if authenticator.reset_password(username, 'Ganti Password'):
                            st.success('Password berhasil diganti')
                            with open('Users Data/config.yaml', 'w') as file:
                                yaml.dump(config, file, default_flow_style=False)
                    except Exception as e:
                        st.error(e)

        
        with colpro2:
            if st.session_state["username"] == 'admin':
                # Tambah User baru
                with st.expander("Tambah User Baru"):
                    if authentication_status:
                        try:
                            if authenticator.register_user('Register user', preauthorization=False):
                                st.success('User registered successfully')
                                with open('Users Data/config.yaml', 'w') as file:
                                    yaml.dump(config, file, default_flow_style=False)
                        except Exception as e:
                            st.error(e)
         

elif st.session_state["authentication_status"] == False:
    with col2:
        st.error('Username/password salah atau tidak terdaftar')

elif st.session_state["authentication_status"] == None:
    with col2:
        st.warning('Silakan masukan username dan password')