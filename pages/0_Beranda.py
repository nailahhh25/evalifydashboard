import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
from utils.style import inject_css, PALETTE

inject_css()

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
        <b style='color:#FFE4E4;font-size:1rem;'>Dashboard Karir</b>
        <div style='font-size:0.72rem;color:#FFAAAA;margin-top:2px;'>Analisis Data Karir & Pasar Kerja</div>
    </div>""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────────
st.markdown("""
<div style='background:linear-gradient(135deg,#FF4B4B 0%,#FF8C42 60%,#FFD166 100%);
border-radius:20px;padding:48px 40px;color:white;margin-bottom:32px;'>
  <h1 style='color:white;font-size:2.4rem;font-weight:800;margin:0 0 14px;line-height:1.2;'>
    Data Nyata di Balik<br>Kebutuhan Industri & Peluang Karir</h1>
  <p style='color:rgba(255,255,255,0.88);font-size:1.05rem;margin:0;max-width:660px;'>
    Menyajikan hasil analisis data lowongan pekerjaan untuk membantu memahami kebutuhan industri,
    kompetensi yang dibutuhkan, serta perkembangan peluang karier di berbagai bidang.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Cards navigasi (5 halaman) ─────────────────────────────────────
pages = [
    ("🌐", "Rekrutmen & Industri",
     "Tren dari 123.000+ lowongan LinkedIn: industri paling aktif, skill paling banyak diminta, level karir yang dibutuhkan, dan tipe kontrak yang ditawarkan.",
     "#FF4B4B"),
    ("🧬", "Tren & Pola Pekerjaan",
     "Analisis 167.000+ deskripsi pekerjaan: posisi terpopuler, skill khas tiap bidang, perbandingan lintas bidang, dan jalur karir dari pemula hingga eksekutif.",
     "#FF8C42"),
    ("🔍", "Kesenjangan Keahlian",
     "Perbandingan skill yang dibutuhkan industri vs yang dimiliki kandidat — mana yang langka, mana yang sudah berlebih, dan di mana celah terbesar.",
     "#8338EC"),
    ("📊", "Pasar Kerja Indonesia",
     "Kondisi ketenagakerjaan: sebaran lowongan per kota, peta upah minimum provinsi, tren pengangguran berdasarkan pendidikan, dan estimasi kisaran gaji.",
     "#118AB2"),
    ("🔮", "Prediksi Time Series",
     "Forecasting deep learning (LSTM, Stacked LSTM, Bi-LSTM) pada data BPS 1986–2024: prediksi penganggur sarjana, UMP per provinsi, dan analisis ACF/PACF.",
     "#8338EC"),
]

# Baris pertama 4 card, baris kedua 1 card di tengah
cols1 = st.columns(4, gap="medium")
for col, (icon, title, desc, color) in zip(cols1, pages[:4]):
    with col:
        st.markdown(f"""
        <div style='background:white;border:1px solid #FFD6D6;border-radius:16px;
        padding:22px 18px;min-height:200px;box-shadow:0 2px 8px rgba(255,75,75,0.08);
        border-top:4px solid {color};display:flex;flex-direction:column;'>
          <div style='font-size:1.7rem;margin-bottom:8px;'>{icon}</div>
          <div style='font-weight:700;color:#111827;font-size:0.9rem;margin-bottom:8px;'>{title}</div>
          <div style='color:#6B7280;font-size:0.8rem;line-height:1.6;flex:1;'>{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Card ke-5 (Prediksi Time Series) — full width dengan style berbeda sebagai "fitur baru"
icon5, title5, desc5, color5 = pages[4]
st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(131,56,236,0.08) 0%,rgba(131,56,236,0.03) 100%);
border:1px solid rgba(131,56,236,0.3);border-radius:16px;padding:24px 28px;
border-left:4px solid {color5};display:flex;align-items:center;gap:20px;'>
  <div style='font-size:2.4rem;flex-shrink:0;'>{icon5}</div>
  <div style='flex:1;'>
    <div style='display:flex;align-items:center;gap:10px;margin-bottom:6px;'>
      <span style='font-weight:700;color:#111827;font-size:0.95rem;'>{title5}</span>
      <span style='background:{color5};color:white;font-size:0.68rem;font-weight:700;
                   padding:2px 8px;border-radius:20px;letter-spacing:0.5px;'>BARU</span>
    </div>
    <div style='color:#6B7280;font-size:0.83rem;line-height:1.6;'>{desc5}</div>
  </div>
  <div style='font-size:0.78rem;color:{color5};font-weight:600;flex-shrink:0;'>→ Buka halaman</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='background:#FFF5F5;border:1px solid #FFD6D6;border-radius:12px;
padding:16px 20px;display:flex;align-items:center;gap:12px;'>
  <span style='font-size:1.4rem;'>👈</span>
  <div>
    <div style='font-weight:600;color:#111827;font-size:0.9rem;'>Mulai Eksplorasi</div>
    <div style='color:#6B7280;font-size:0.82rem;margin-top:2px;'>
      Pilih halaman melalui menu navigasi di sidebar kiri.</div>
  </div>
</div>""", unsafe_allow_html=True)

# ── Konteks & Relevansi ────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### Mengapa Data Ini Penting?")

st.markdown("""
<div style='background:white;border:1px solid #FFD6D6;border-radius:16px;
padding:28px 32px;margin-bottom:20px;line-height:1.85;color:#374151;font-size:0.95rem;'>
  Sebagian besar kandidat masuk ke pasar kerja dengan gambaran yang tidak lengkap —
  tidak tahu skill apa yang benar-benar paling banyak dicari, tidak tahu seberapa tinggi
  standar yang ditetapkan industri, dan tidak tahu di mana posisi mereka dibandingkan
  ribuan kandidat lain.<br><br>
  Dashboard ini hadir untuk mengisi kekosongan itu. Data dari ratusan ribu lowongan,
  deskripsi pekerjaan, dan kondisi pasar kerja dianalisis dan disajikan dalam bentuk
  yang mudah dipahami — <b>agar setiap keputusan karir bisa didasarkan pada fakta,
  bukan perkiraan.</b>
</div>
""", unsafe_allow_html=True)

konteks = [
    ("📊", "Apa yang sebenarnya dicari industri?",
     "Dari ratusan ribu lowongan kerja, kita bisa melihat pola yang konsisten: skill apa yang paling sering muncul, industri mana yang paling aktif, dan level karir apa yang paling banyak dibutuhkan.",
     "🌐 Rekrutmen & Industri"),
    ("🧩", "Pekerjaan itu seperti apa sebenarnya?",
     "167.000+ deskripsi pekerjaan dianalisis untuk mengungkap pola nyata: apa skill khas tiap bidang, berapa pengalaman yang biasanya diminta, dan bagaimana jalur karir dari satu level ke level berikutnya.",
     "🧬 Tren & Pola Pekerjaan"),
    ("⚖️", "Di mana celah terbesar antara kandidat dan industri?",
     "Membandingkan skill yang dicari perusahaan dengan skill yang dimiliki kandidat mengungkap gap yang nyata — dan gap inilah yang sering menjadi penyebab utama kandidat tidak lolos seleksi.",
     "🔍 Kesenjangan Keahlian"),
    ("🗺️", "Bagaimana kondisi pasar kerja nyata di Indonesia?",
     "Data BPS, UMP, dan ribuan lowongan lokal memberikan gambaran realistis: gaji yang wajar, kota dengan peluang terbanyak, dan tren ketenagakerjaan per provinsi.",
     "📊 Pasar Kerja Indonesia"),
    ("🔮", "Ke mana arah pasar kerja ke depan?",
     "Model LSTM, Stacked LSTM, dan Bidirectional LSTM memproyeksikan tren pengangguran sarjana dan UMP per provinsi — lengkap dengan analisis statistik ACF, PACF, dan dekomposisi time series.",
     "🔮 Prediksi Time Series"),
]

cols2 = st.columns(5, gap="small")
for col, (icon, judul, isi, halaman) in zip(cols2, konteks):
    with col:
        st.markdown(f"""
        <div style='background:#FFF5F5;border:1px solid #FFD6D6;border-radius:14px;
        padding:20px 18px;height:100%;display:flex;flex-direction:column;'>
          <div style='font-size:1.5rem;margin-bottom:8px;'>{icon}</div>
          <div style='font-weight:700;color:#991B1B;font-size:0.88rem;margin-bottom:8px;'>{judul}</div>
          <div style='color:#374151;font-size:0.8rem;line-height:1.6;flex:1;margin-bottom:10px;'>{isi}</div>
          <div style='font-size:0.73rem;color:#FF8C42;font-weight:600;'>→ {halaman}</div>
        </div>""", unsafe_allow_html=True)

# ── Sumber data ────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("### Sumber Data")
st.caption("Dataset yang digunakan di tiap halaman.")

sumber = [
    ("Rekrutmen & Industri 🌐",
     "LinkedIn Job Postings 2023–2024 (~123rb lowongan), LinkedIn Job Industries & Skills, LinkedIn Salaries"),
    ("Tren & Pola Pekerjaan 🧬",
     "Job Role Descriptions — 167.000+ deskripsi pekerjaan yang dianalisis dan distrukturkan menggunakan AI"),
    ("Kesenjangan Keahlian 🔍",
     "Skill Gap Analysis — hasil perbandingan antara skill di lowongan vs skill yang tercantum di resume kandidat"),
    ("Pasar Kerja Indonesia 📊",
     "Job Salary Indonesia (~34.700 lowongan), BPS Pengangguran 1986–2024, UMP Provinsi 2002–2026, TPT Provinsi Feb 2026"),
    ("Prediksi Time Series 🔮",
     "BPS Sakernas 1986–2024 (pengangguran per tingkat pendidikan), BPS UMP 2002–2026 per provinsi — model: LSTM, Stacked LSTM, Bi-LSTM Multivariate"),
]

cols3 = st.columns(5, gap="small")
for col, (nama, isi) in zip(cols3, sumber):
    with col:
        st.markdown(f"""
        <div style='background:#FFF5F5;border:1px solid #FFD6D6;border-radius:12px;
        padding:14px 16px;height:100%;'>
          <div style='font-weight:700;font-size:0.85rem;color:#111827;margin-bottom:6px;'>{nama}</div>
          <div style='font-size:0.78rem;color:#6B7280;line-height:1.6;'>{isi}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""<p style='text-align:center;color:#9CA3AF;font-size:0.78rem;margin-top:28px;'>
Capstone Project · Coding Camp 2026</p>""", unsafe_allow_html=True)
