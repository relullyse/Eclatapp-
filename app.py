import streamlit as st
import pandas as pd
from pyECLAT import ECLAT
from itertools import chain
from collections import defaultdict
import base64
import openpyxl

st.title('ECLAT SAYA NI PAK')

st.markdown("""
Ini merupakan aplikasi Teknik Asosiasi sederhana menggunakan Algoritma ECLAT
* **Data :** Data yang digunakan dibawah ini adalah contoh data. Jika ingin mencoba dengan data baru silahkan import manual.
""")



uploaded_file = st.file_uploader("Choose a file", type="xlsx")
if uploaded_file is not None:
    input_df = pd.read_excel(uploaded_file, engine='openpyxl')
else:
    input_df = pd.read_csv("coba_pendaftar.csv")
    
st.write(input_df)

st.sidebar.header('User Input Features')
st.sidebar.write("Masukkan nilai min supp dengan nilai maksimal", len(input_df))
min_supp = st.sidebar.number_input('Insert a number', 1, max_value=len(input_df), value=2)
min_comb = st.sidebar.slider('Pick a number of minimum combination', 1, len(input_df.columns), 2)
if min_comb == len(input_df.columns):
    max_comb = len(input_df.columns) 
else:
    max_comb = st.sidebar.slider('Pick a number of maximum combination', min_comb, len(input_df.columns))

df = input_df.copy()
df.columns = range(df.shape[1])

minimum_support = min_supp/len(input_df)

st.write('Minimum Support ',minimum_support)
st.write('minimum combination ',min_comb)
st.write('maximum combination ',max_comb)

#def eclat (df, minimum_support, min_comb, max_comb):
if st.button('Run'):
    eclat_instance = ECLAT(data=df, verbose=True)
    rule_indices, get_ECLAT_supports = eclat_instance.fit(min_support=minimum_support,
                                                            min_combination=min_comb,
                                                            max_combination=max_comb,
                                                            separator=' & ',
                                                            verbose=True)
    banyak_rule = len(get_ECLAT_supports)  
    if banyak_rule == 0:
        st.write('Tidak menghasilkan Rule dari aturan diatas')
    else:
        st.write('Menghasilkan Rule sebanyak', banyak_rule)
        new_dict = {}
        for key, value in rule_indices.items():
            new_dict[key] = len(value)
            
        dict_baru = defaultdict(list)
        for k, v in chain(get_ECLAT_supports.items(), new_dict.items()):
            dict_baru[k].append(v)
                
        hasil = pd.DataFrame.from_dict(dict_baru,orient='index', columns=['Nilai Support','Total Kemunculan'])
        hasil.reset_index(inplace=True)
        hasil = hasil.rename(columns = {'index':'Kombinasi Pilihan'})
            
        def filedownload(df):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
            href = f'<a href="data:file/csv;base64,{b64}" download="Hasil_kombinasi.csv">Download CSV File</a>'
            return href
            
        kolom_baru = hasil['Kombinasi Pilihan'].str.split('&', expand=True)
            
        panjang_kolom = len(kolom_baru.columns)
            
        if panjang_kolom == 1:
            hasil[['Prodi 1']] = hasil['Kombinasi Pilihan'].str.split('&', expand=True)
            st.write(hasil)
            st.markdown("""
            Silahkan download hasil tersebut untuk selanjutnya dapat dilakukan pengolahan lebih detail
            """)
            st.markdown(filedownload(hasil), unsafe_allow_html=True)
        elif panjang_kolom == 2:        
            hasil[['Prodi 1', 'Prodi 2']] = hasil['Kombinasi Pilihan'].str.split('&', expand=True)
            st.write(hasil)
            st.markdown("""
            Silahkan download hasil tersebut untuk selanjutnya dapat dilakukan pengolahan lebih detail
            """)
            st.markdown(filedownload(hasil), unsafe_allow_html=True)
        else:        
            hasil[['Prodi 1', 'Prodi 2','Prodi 3']] = hasil['Kombinasi Pilihan'].str.split('&', expand=True)
            st.write(hasil)
            st.markdown("""
            Silahkan download hasil tersebut untuk selanjutnya dapat dilakukan pengolahan lebih detail
            """) 
            st.markdown(filedownload(hasil), unsafe_allow_html=True)
            
#            return hasil

#hasil_kombinasi = eclat(df, minimum_support, min_comb, max_comb)
#hasil = pd.DataFrame(hasil_kombinasi)
#st.write(hasil_kombinasi)




#st.write(eclat(df, minimum_support, min_comb, max_comb))

#rules = get_ECLAT_supoorts

#st.write(rules)

#st.write(df)
#data = pd.read_csv("pilihan_pendaftar.csv")
#data
#def ahahah

