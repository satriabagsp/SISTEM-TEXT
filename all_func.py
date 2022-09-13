import pandas as pd
from glob import glob
from datetime import datetime, date
from deta import Deta
import io
import xlrd
import mysql.connector as mysql
import re
import string
# xlrd.xlsx.ensure_elementtree_imported(False, None)
# xlrd.xlsx.Element_has_iter = True

# def get_data_berita():
#     # read mysql
#     mydb = mysql.connect(host = "localhost", user = "root", passwd = "", database = "berita")
#     hasil_scrap = pd.read_sql('SELECT url_berita, sumber, katakunci, aspek, tanggal, judul_berita, konten_clean, sentimen_judul, sentimen_berita \
#                     FROM hasil_scrap', mydb)

#     return hasil_scrap

# def get_data_tokoh():
#     # read mysql
#     mydb = mysql.connect(host = "localhost", user = "root", passwd = "", database = "berita")
#     tokoh_berita = pd.read_sql('SELECT * \
#                     FROM tokoh_berita', mydb)

#     return tokoh_berita

def get_data_berita():
    hasil_scrap = pd.read_csv('Data/hasil_scrap.csv', sep = ';',  encoding='iso-8859-1', error_bad_lines=False, engine='python')

    return hasil_scrap

def get_data_tokoh():
    tokoh_berita = pd.read_csv('Data/tokoh_berita.csv', sep = ';',  encoding='iso-8859-1', error_bad_lines=False, engine='python')

    return tokoh_berita

def wordcloud(teks):
    df_stopwords = pd.read_csv('Data/stopwords_tambahan.csv', sep = ';')
    teks = str(teks)

    # Membuat tulisan non kapital
    teks = teks.lower()

    # Menghapus newline, contoh: “\n”.
    teks = teks.replace('\n',' ')
    teks = teks.replace('\t',' ')
    teks = teks.replace('-',' ')
    teks = teks.replace('/',' ')
    teks = teks.replace(',',' ')
    teks = teks.replace('.',' ')
    teks = teks.replace('  ',' ')

    # Penghapusan karakter Unicode yang berada diluar jangkauan ASCII.
    teks = re.sub(r'http\S+', ' ', teks)

    # Menghapus karakter Unicode yang berada diluar jangkauan ASCII.
    teks = re.sub(r'[^\x00-\x7F]+',' ', teks)

    # Menghapus alamat URL yang terdapat pada teks
    teks = re.sub(r'http\S+', ' ', teks)

    # Menghapus mention yang ada pada teks -> @blabla
    teks = re.sub(r'@[A-Za-z0-9_]+', ' ', teks)

    # Menghapus hashtag yang ada pada teks -> #blabla
    teks = re.sub(r'#[A-Za-z0-9_]+', ' ', teks)

    # Menghapus angka yang ada pada teks
    # teks = re.sub(r'\b\d+\b', '', teks)
    # teks = re.sub(r'[0-9]', '', teks)

    # Menghapus tanda baca yang terdapat pada teks
    teks = teks.translate(str.maketrans('','',string.punctuation))

    # Menghilangkan stopwords atau kata-kata yang kurang bernilai
    text_id_filtered = []
    list_tambahan = df_stopwords.stopwords.to_list()
    token_teks = teks.split()
    for w in token_teks:
        if w not in list_tambahan:
            # w = stemmer.stem(w)
            text_id_filtered.append(w)
    teks = ' '.join(text_id_filtered)

    return teks

