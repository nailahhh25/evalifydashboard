import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import streamlit as st

st.set_page_config(
    page_title="Dashboard Karir",
    layout="wide",
    initial_sidebar_state="expanded",
)

pg = st.navigation([
    st.Page("pages/0_Beranda.py",                 title="Beranda",               icon="🏠"),
    st.Page("pages/1_Rekrutmen_&_Industri.py",    title="Rekrutmen & Industri",  icon="🌐"),
    st.Page("pages/2_Tren_&_Pola_Pekerjaan.py",   title="Tren & Pola Pekerjaan", icon="🧬"),
    st.Page("pages/3_Kesenjangan_Keahlian.py",    title="Kesenjangan Keahlian",  icon="🔍"),
    st.Page("pages/4_Pasar_Kerja_Indonesia.py",   title="Pasar Kerja Indonesia", icon="📊"),
    st.Page("pages/5_Prediksi_Time_Series.py",    title="Prediksi Time Series",  icon="🔮"),
])
pg.run()
