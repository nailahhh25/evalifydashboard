import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.style import (inject_css, page_header, section, insight, dl_csv,
                          PALETTE, lyt)
from utils.loader import (jd, postings, posting_industri, skill_domain_linkedin)

inject_css()

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
    <b style='color:#FFE4E4;font-size:1rem;'>Dashboard Karir</b>
    <div style='font-size:0.72rem;color:#FFAAAA;margin-top:2px;'>Analisis Data Karir & Pasar Kerja</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.78rem;color:#FFAAAA;line-height:1.8;'>
    <b style='color:#FFE4E4;'>🌐 Rekrutmen & Industri</b><br><br>
    Sumber: LinkedIn Job Postings 2023–2024<br><br>
    • Industri yang paling aktif membuka lowongan<br>
    • 35 kategori skill paling banyak diminta<br>
    • Level karir fresh grad hingga eksekutif<br>
    • Proporsi tipe kontrak pekerjaan
    </div>""", unsafe_allow_html=True)

BAR_H   = 28
BAR_MIN = 300
def chart_h(n): return max(BAR_MIN, n * BAR_H + 80)

with st.spinner("Menyiapkan data…"):
    df_jd   = jd()
    df_post = postings()
    df_ind  = posting_industri()
    df_skd  = skill_domain_linkedin()   # sudah berisi kolom: skill_name/skill_abr, Frekuensi, Tipe

# skill_demand langsung dari processed — sudah ada kolom Frekuensi dan Tipe
# Kolom nama skill: bisa 'skill_name' (processed) atau 'skill' (fallback)
SKILL_COL = "skill_name" if "skill_name" in df_skd.columns else "skill"
skill_demand = df_skd.rename(columns={SKILL_COL: "skill"}).copy()
# Pastikan kolom yang dibutuhkan ada
if "Frekuensi" not in skill_demand.columns and "count" in skill_demand.columns:
    skill_demand = skill_demand.rename(columns={"count": "Frekuensi"})

# Kolom industri: processed pakai 'industry_name'
IND_COL = "industry_name" if "industry_name" in df_ind.columns else "name"

page_header(
    "Rekrutmen & Industri",
    "Data dari 123.000+ lowongan kerja di LinkedIn — industri mana yang paling "
    "banyak membuka posisi, skill apa yang paling sering diminta, dan seberapa "
    "besar peluang untuk fresh graduate masuk ke pasar kerja.",
    "🌐"
)

c1, c2, c3 = st.columns(3)
c1.metric("Total Lowongan Tercatat", f"{len(df_post):,}",
          help="Jumlah postingan pekerjaan yang tersedia di dataset LinkedIn")
c2.metric("Jumlah Industri",         f"{df_ind[IND_COL].nunique():,}",
          help="Banyaknya industri berbeda yang membuka lowongan")

# title_clean ada di postings_clean; fallback ke title
title_col = "title_clean" if "title_clean" in df_post.columns else "title"
c3.metric("Jenis Posisi Pekerjaan",  f"{df_post[title_col].nunique():,}",
          help="Jumlah judul pekerjaan unik yang ditemukan di data")
st.markdown("<hr>", unsafe_allow_html=True)

# ── SECTION 1 ─────────────────────────────────────────────────────
section("📌 Industri & Bidang Keahlian yang Paling Banyak Dicari")

with st.container(border=True):
    st.markdown("**Industri yang Paling Banyak Membuka Lowongan**")
    st.caption("Industri mana yang paling aktif merekrut berdasarkan jumlah postingan lowongan.")
    MAX_IND = int(df_ind[IND_COL].nunique())
    top_i   = st.slider("Tampilkan berapa industri?", 5, min(MAX_IND, 35), 15, key="s1_topind")
    ic      = df_ind[IND_COL].value_counts().head(top_i).reset_index()
    ic.columns = ["Industri","Jumlah Lowongan"]
    fig2 = px.bar(ic, x="Jumlah Lowongan", y="Industri", orientation="h",
                  color="Jumlah Lowongan",
                  color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                  title=f"Top {top_i} Industri Paling Aktif Merekrut")
    fig2.update_layout(**lyt(coloraxis_showscale=False, height=chart_h(top_i)))
    fig2.update_yaxes(autorange="reversed", tickfont=dict(size=12))
    st.plotly_chart(fig2, use_container_width=True)
    dl_csv(ic, "industri_aktif.csv")

insight(
    "Bidang Kesehatan, IT, dan Retail mendominasi lowongan berdasarkan data terbaru. "
    "Ini mencerminkan tiga gelombang besar permintaan tenaga kerja pasca-pandemi: "
    "pemulihan layanan kesehatan, percepatan digitalisasi, dan bangkitnya perdagangan ritel. "
    "Bagi fresh graduate, ketiga sektor ini membuka peluang yang luas meski dengan tingkat "
    "persaingan yang berbeda-beda."
)

# ── SECTION 2 ─────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("🛠️ Skill yang Paling Sering Muncul di Lowongan Kerja")
st.caption("35 kategori skill LinkedIn berdasarkan frekuensi kemunculan di seluruh lowongan.")

with st.container(border=True):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        top_sk_n = st.slider("Tampilkan berapa skill?", 5, len(skill_demand), 15, key="s3_n")
    with col_f2:
        tipe_sk = st.radio("Filter tipe", ["Semua","Teknis & Spesialis","Bisnis & Manajerial"],
                           key="s3_t", horizontal=True)

    sk_f = skill_demand.copy()
    if tipe_sk != "Semua":
        sk_f = sk_f[sk_f["Tipe"] == tipe_sk]
    sk_top = sk_f.head(top_sk_n)

    fig5 = px.bar(sk_top, x="Frekuensi", y="skill", orientation="h",
                  color="Tipe",
                  color_discrete_map={"Teknis & Spesialis": PALETTE[0],
                                      "Bisnis & Manajerial": PALETTE[2]},
                  title=f"Top {top_sk_n} Skill Paling Sering Diminta di Lowongan",
                  labels={"skill":""})
    fig5.update_layout(**lyt(height=chart_h(top_sk_n)))
    fig5.update_yaxes(autorange="reversed", tickfont=dict(size=12))
    st.plotly_chart(fig5, use_container_width=True)
    dl_csv(sk_top, "skill_populer.csv")

insight(
    "Information Technology, Sales, dan Management mendominasi skill yang paling banyak dicari. "
    "Ini bukan berarti semua orang harus jadi programmer — tapi setiap bidang kini semakin "
    "membutuhkan pemahaman teknologi. Kandidat yang bisa menggabungkan keahlian teknis "
    "dengan kemampuan bisnis memiliki daya saing yang jauh lebih tinggi."
)

# ── SECTION 3 ─────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("👥 Peluang Berdasarkan Level Karir & Tipe Kontrak")
st.caption("Gambaran posisi apa yang paling banyak dibutuhkan dan bagaimana pola kontrak kerjanya.")

col_lv1, col_lv2 = st.columns(2, gap="large")

with col_lv1:
    with st.container(border=True):
        st.markdown("**Distribusi Level Karir yang Paling Dibutuhkan**")
        EXP_LABEL = {
            "Entry level":"Fresh Graduate / Junior","Mid-Senior level":"Senior",
            "Associate":"Associate","Director":"Direktur",
            "Internship":"Magang","Executive":"Eksekutif",
        }
        exp_cnt = (df_post["formatted_experience_level"].dropna()
                   .map(EXP_LABEL).fillna(df_post["formatted_experience_level"])
                   .value_counts().reset_index())
        exp_cnt.columns = ["Level Karir","Jumlah Lowongan"]
        exp_cnt["pct"]  = (exp_cnt["Jumlah Lowongan"]/exp_cnt["Jumlah Lowongan"].sum()*100).round(1)
        fig6 = px.bar(exp_cnt, x="Jumlah Lowongan", y="Level Karir",
                      orientation="h", color="Level Karir",
                      color_discrete_sequence=PALETTE,
                      text="pct", title="Distribusi Level Karir yang Dibutuhkan",
                      labels={"Level Karir":""})
        fig6.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig6.update_layout(**lyt(showlegend=False, height=chart_h(len(exp_cnt))))
        fig6.update_yaxes(autorange="reversed", tickfont=dict(size=12))
        st.plotly_chart(fig6, use_container_width=True)

with col_lv2:
    with st.container(border=True):
        st.markdown("**Proporsi Tipe Kontrak Pekerjaan**")
        WT_LABEL = {
            "Full-time":"Full-time","Part-time":"Part-time","Contract":"Kontrak",
            "Temporary":"Temporer","Internship":"Magang","Volunteer":"Sukarela","Other":"Lainnya"
        }
        wt_cnt = (df_post["formatted_work_type"].dropna()
                  .map(WT_LABEL).fillna(df_post["formatted_work_type"])
                  .value_counts().reset_index())
        wt_cnt.columns = ["Tipe Pekerjaan","Jumlah"]
        wt_cnt["pct"]  = (wt_cnt["Jumlah"]/wt_cnt["Jumlah"].sum()*100).round(1)
        fig7 = px.pie(wt_cnt, names="Tipe Pekerjaan", values="Jumlah",
                      hole=0.45, color_discrete_sequence=PALETTE,
                      title="Proporsi Tipe Kontrak Pekerjaan")
        fig7.update_traces(
            texttemplate="%{label}<br>%{percent:.1%}",
            textposition="outside", textfont_size=11, pull=[0.02]*len(wt_cnt))
        fig7.update_layout(**lyt(showlegend=True,
                                  legend=dict(orientation="v", x=1.02, y=0.5,
                                              bgcolor="rgba(0,0,0,0)", font=dict(size=11))))
        st.plotly_chart(fig7, use_container_width=True)

insight(
    "Sekitar 30% lowongan terbuka untuk level Fresh Graduate dan Junior, "
    "yang artinya tidak semua posisi mensyaratkan pengalaman bertahun-tahun. "
    "Mayoritas kontrak bersifat full-time, tapi lowongan magang juga cukup signifikan — "
    "ini bisa jadi pintu masuk yang baik untuk membangun portofolio sebelum melamar full-time."
)
