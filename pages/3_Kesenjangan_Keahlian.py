import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.style import (inject_css, page_header, section, insight, warn,
                          dl_csv, PALETTE, PALETTE_VIZ, lyt)
from utils.loader import (skill_gap, hard_skills, taxonomy, jd)

inject_css()

BAR_H = 28
BAR_MIN = 300
def chart_h(n): return max(BAR_MIN, n * BAR_H + 80)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
    <b style='color:#FFE4E4;font-size:1rem;'>Dashboard Karir</b>
    <div style='font-size:0.72rem;color:#FFAAAA;margin-top:2px;'>Analisis Data Karir & Pasar Kerja</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.78rem;color:#FFAAAA;line-height:1.8;'>
    <b style='color:#FFE4E4;'>🔍 Kesenjangan Keahlian</b><br><br>
    Sumber: Analisis gap skill<br>lowongan vs resume kandidat<br><br>
    • Skill yang paling langka di pasar<br>
    • Skill yang sudah berlebih pada kandidat<br>
    • Kesenjangan hard skill vs soft skill
    </div>""", unsafe_allow_html=True)

with st.spinner("Memuat data analisis skill…"):
    df_gap  = skill_gap()
    hs      = hard_skills()

df_gap["Tipe"] = df_gap["skill"].apply(
    lambda s: "Hard Skill" if str(s).lower() in hs else "Soft Skill")

page_header("Kesenjangan Skill",
            "Perbandingan antara skill yang dibutuhkan oleh industri dengan skill yang "
            "dimiliki oleh kandidat — temukan peluang untuk mengisi celah yang paling bernilai.", "🔍")

shortage = (df_gap["gap_score"] > 0).sum()
surplus  = (df_gap["gap_score"] < 0).sum()

c1, c2, c3 = st.columns(3)
c1.metric("Total Skill Dianalisis",   f"{len(df_gap):,}",
          help="Jumlah skill unik yang ada di database lowongan dan resume")
c2.metric("Skill Langka di Pasar 🔴", f"{shortage:,}",
          help="Skill yang banyak dicari industri tapi sedikit kandidat yang memilikinya")
c3.metric("Skill Sudah Banyak 🔵",    f"{surplus:,}",
          help="Skill yang banyak dimiliki kandidat tapi permintaannya rendah di industri")
st.markdown("<hr>", unsafe_allow_html=True)

# ── SECTION 1 ─────────────────────────────────────────────────────
section("📊 Perbandingan Skill yang Dibutuhkan Industri vs yang Dimiliki Kandidat")
st.caption("Seberapa besar selisih antara apa yang dicari perusahaan dan apa yang dimiliki kandidat?")

with st.container(border=True):
    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f1:
        top_n = st.slider("Tampilkan berapa skill?", 10, 50, 20, key="g1_n")
    with c_f2:
        urutan = st.radio("Urutkan berdasarkan",
                          ["Paling Banyak Diminta","Paling Banyak Dimiliki","Selisih Terbesar"],
                          key="g1_sort")
    with c_f3:
        tipe = st.radio("Tipe skill", ["Semua","Hard Skill","Soft Skill"], key="g1_t")

    scol = {"Paling Banyak Diminta":"demand_pct",
            "Paling Banyak Dimiliki":"candidate_pct",
            "Selisih Terbesar":"gap_score"}[urutan]
    df_f = df_gap.copy()
    if tipe != "Semua":
        df_f = df_f[df_f["Tipe"] == tipe]
    df_f = df_f.sort_values(scol, ascending=False).head(top_n)

    df_melt = pd.melt(
        df_f[["skill","demand_pct","candidate_pct"]],
        id_vars="skill", value_vars=["demand_pct","candidate_pct"],
        var_name="Kategori", value_name="Persentase"
    )
    df_melt["Persentase"] = df_melt["Persentase"] * 100
    df_melt["Kategori"] = df_melt["Kategori"].map({
        "demand_pct":    "🏭 Dibutuhkan Industri",
        "candidate_pct": "👤 Dimiliki Kandidat"
    })
    fig = px.bar(df_melt, x="Persentase", y="skill",
                 color="Kategori", orientation="h", barmode="group",
                 color_discrete_map={"🏭 Dibutuhkan Industri":"#FF4B4B",
                                     "👤 Dimiliki Kandidat":"#118AB2"},
                 title="Skill: Dibutuhkan Industri vs Dimiliki Kandidat (%)",
                 labels={"skill":"","Persentase":"Persentase (%)"})
    fig.update_layout(**lyt(yaxis=dict(autorange="reversed"),
                             legend=dict(orientation="h", yanchor="bottom",
                                         y=1.02, xanchor="right", x=1)))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    <div style='background:#FFF5F5;border-left:3px solid #FF4B4B;padding:10px 14px;
    border-radius:0 8px 8px 0;font-size:0.83rem;color:#7F1D1D;margin-top:8px;'>
    📌 <b>Cara membaca:</b> Batang <b style='color:#FF4B4B;'>merah</b> = % lowongan yang
    mensyaratkan skill ini. Batang <b style='color:#118AB2;'>biru</b> = % kandidat yang
    sudah mencantumkannya di resume. Semakin jauh selisihnya, semakin besar nilai skill itu
    jika kamu kuasai sekarang.
    </div>""", unsafe_allow_html=True)
    dl_csv(df_f[["skill","demand_pct","candidate_pct","gap_score"]], "skill_perbandingan.csv")

insight("Skill dengan batang merah jauh lebih panjang dari biru adalah skill yang paling langka "
        "dan paling bernilai di pasar saat ini. Menguasai skill-skill ini memberikan keunggulan "
        "kompetitif yang nyata, karena sedikit kandidat lain yang memilikinya. "
        "Ini adalah prioritas utama jika kamu ingin meningkatkan daya saing secara cepat.")

# ── SECTION 2 ─────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("📉 Skill yang Langka vs yang Sudah Berlebih di Pasar")
st.caption("Visualisasi dua arah: ke kanan berarti langka (banyak dicari, sedikit yang punya), ke kiri berarti berlebih (banyak yang punya, sedikit yang mencari).")

with st.container(border=True):
    c_f4, c_f5, c_f6 = st.columns(3)
    with c_f4:
        tampil  = st.radio("Tampilkan", ["Keduanya","Yang Langka","Yang Berlebih"],
                           key="g2_show")
    with c_f5:
        min_gap = st.slider("Minimal selisih", 0.0, 0.5, 0.05, step=0.01, key="g2_mg")
    with c_f6:
        min_dem = st.slider("Minimal permintaan", 0, 500, 50, key="g2_md")

    df_g = df_gap[(df_gap["gap_score"].abs() >= min_gap) &
                  (df_gap["demand_count"] >= min_dem)].copy()
    if tampil == "Yang Langka":     df_g = df_g[df_g["gap_score"] > 0]
    elif tampil == "Yang Berlebih": df_g = df_g[df_g["gap_score"] < 0]
    df_g = df_g.sort_values("gap_score", ascending=False).head(40)
    df_g["Status"] = df_g["gap_score"].apply(
        lambda v: "Langka — banyak dicari, sedikit yang punya" if v > 0
                  else "Berlebih — banyak yang punya, permintaan rendah")

    fig2 = px.bar(df_g, x="gap_score", y="skill", orientation="h",
                  color="Status",
                  color_discrete_map={
                      "Langka — banyak dicari, sedikit yang punya":"#FF4B4B",
                      "Berlebih — banyak yang punya, permintaan rendah":"#118AB2"},
                  hover_data={"demand_count":":.0f","candidate_count":":.0f",
                              "gap_score":":.3f","Status":False},
                  labels={"gap_score":"Skor Kesenjangan (+ = langka, − = berlebih)",
                          "skill":"","demand_count":"Dicari Industri",
                          "candidate_count":"Dimiliki Kandidat"},
                  title="Peta Kesenjangan Skill")
    fig2.add_vline(x=0, line_dash="dash", line_color="#9CA3AF",
                   annotation_text="Seimbang", annotation_position="top")
    fig2.update_layout(**lyt(yaxis=dict(autorange="reversed"),
                              legend=dict(orientation="h", yanchor="bottom",
                                          y=1.02, xanchor="right", x=1, font=dict(size=11))))
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("""
    <div style='background:#FFF5F5;border-left:3px solid #FF4B4B;padding:10px 14px;
    border-radius:0 8px 8px 0;font-size:0.83rem;color:#7F1D1D;margin-top:8px;'>
    📌 <b>Cara membaca:</b>
    <b style='color:#FF4B4B;'>Merah (ke kanan)</b> = skill langka, permintaan industri
    lebih tinggi dari jumlah kandidat yang punya.
    <b style='color:#118AB2;'>Biru (ke kiri)</b> = skill berlebih, banyak kandidat yang
    punya tapi perusahaan jarang mencarinya.
    </div>""", unsafe_allow_html=True)
    dl_csv(df_g[["skill","demand_count","candidate_count","gap_score"]], "skill_langka_berlebih.csv")

insight("Skill yang langka biasanya adalah teknologi baru atau kemampuan spesialis yang belum banyak "
        "diajarkan di kampus. Di sisi lain, skill yang sudah berlebih sering kali adalah kemampuan dasar "
        "yang sudah dimiliki hampir semua kandidat. Fokus belajar skill yang langka "
        "jauh lebih efisien untuk meningkatkan peluangmu.")

# ── SECTION 3 : Top Hard vs Soft Skill Gap ────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("⚖️ Skill Teknis vs Soft Skill: Mana yang Lebih Besar Kesenjangannya?")
st.caption("Membandingkan pola kesenjangan antara skill teknis (hard skill) dengan kemampuan interpersonal (soft skill).")

with st.container(border=True):
    col_hs, col_ss = st.columns(2, gap="large")
    n_each = 12

    df_hard = df_gap[df_gap["Tipe"]=="Hard Skill"].copy()
    df_soft = df_gap[df_gap["Tipe"]=="Soft Skill"].copy()

    with col_hs:
        st.markdown("**Top Hard Skill yang Paling Langka**")
        top_h = df_hard[df_hard["gap_score"]>0].sort_values("gap_score",ascending=False).head(n_each)
        fig_h = px.bar(top_h, x="gap_score", y="skill", orientation="h",
                       color="gap_score",
                       color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                       title="Skill Teknis Paling Langka",
                       labels={"skill":"","gap_score":"Skor Kesenjangan"})
        fig_h.update_layout(**lyt(coloraxis_showscale=False,
                                   yaxis=dict(autorange="reversed")))
        st.plotly_chart(fig_h, use_container_width=True)

    with col_ss:
        st.markdown("**Top Soft Skill yang Paling Langka**")
        top_s = df_soft[df_soft["gap_score"]>0].sort_values("gap_score",ascending=False).head(n_each)
        fig_s = px.bar(top_s, x="gap_score", y="skill", orientation="h",
                       color="gap_score",
                       color_continuous_scale=[[0,"#E8D5FF"],[1,"#8338EC"]],
                       title="Soft Skill Paling Langka",
                       labels={"skill":"","gap_score":"Skor Kesenjangan"})
        fig_s.update_layout(**lyt(coloraxis_showscale=False,
                                   yaxis=dict(autorange="reversed")))
        st.plotly_chart(fig_s, use_container_width=True)

insight("Kesenjangan terbesar di hard skill umumnya ada di bidang teknologi terbaru seperti cloud, "
        "machine learning, dan keamanan siber — area yang berkembang lebih cepat dari kemampuan "
        "institusi pendidikan untuk mengajarkannya. Sementara itu, soft skill yang langka biasanya "
        "adalah kemampuan kepemimpinan dan negosiasi yang membutuhkan jam terbang nyata. "
        "Keduanya sama-sama penting untuk membangun profil yang lengkap.")
