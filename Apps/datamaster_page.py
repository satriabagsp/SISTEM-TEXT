import streamlit as st
import pandas as pd
import all_func
from deta import Deta
import io

def app():

    st.title("Kelola Data Master")
    # st.markdown(f'<h1 style="color:#fe9028;font-size:42px;">Kelola Data Master</h1>', unsafe_allow_html=True)

    col_data1, col_data2 = st.columns(2)

    with col_data1:
        # FROM DETA
        deta = Deta("c0n2zvpx_fmuHGnBH9sZT4JnDscVCjZ9nbwUukFhp")
        drive = deta.Drive("sidinibakerja")
        all_files = drive.list().get("names")

        # Print list data
        st.write('Berikut daftar data anggaran yang telah tersimpan di database. Silakan tambah data anggaran bulan terbaru atau hapus data anggaran yang sudah ada pada isian di samping.')
        for filename in all_files:
            st.write(f'- {filename}')

    with col_data2:
        st.subheader('Tambah Data Anggaran')
        # Form Bulan File
        bulan_file = st.selectbox(
            'Pilih bulan anggaran',
            ('JANUARI', 'FEBRUARI', 'MARET', 'APRIL', 'MEI', 'JUNI', 'JULI', 'AGUSTUS', 'SEPTEMBER', 'OKTOBER', 'NOVEMBER', 'DESEMBER'))

        # Form Tahun File
        tahun_file = st.selectbox(
            'Pilih bulan anggaran',
            ('2019', '2020', '2021', '2022', '2023'))

        # Form upload file
        pilih_file = st.file_uploader("Pilih file")

        if pilih_file is not None:
            bytesData = pilih_file.getvalue()
            
            # Set nama file yang akan diupload
            nama_file_upload = f'LK {bulan_file} {tahun_file}.xlsx'
            st.write(f'File {pilih_file.name} akan diupload dengan nama: {nama_file_upload}')

            # Upload file ke DETA
            uploadFile = st.button('Upload File')
            if uploadFile:
                with st.spinner('Silakan tunggu...'):
                    drive.put(nama_file_upload, io.BytesIO(bytesData))

                    # Update data json
                    all_func.update_data()

                    st.success(f'File berhasil diupload. Silakan refresh halaman.')

        st.subheader('')
        st.subheader('Hapus Data Anggaran')

        hapusData = st.multiselect('Silakan pilih data yang ingin dihapus',all_files)

        st.write('Mohon periksa kembali data yang akan dihapus karena proses ini tidak dapat dikembalikan. Data yang akan dihapus:', hapusData)

        # Hapus file dari DETA
        hapusFile = st.button('Hapus File')
        if hapusFile:
            with st.spinner('Silakan tunggu...'):
                result = drive.delete_many(hapusData)

                # Update data json
                all_func.update_data()

                st.success(f'Proses penghapusan berhasil. Silakan refresh halaman.')
                st.write("File berhasil dihapus:", result.get("deleted"))
                st.write("File gagal dihapus:", result.get("failed"))

                