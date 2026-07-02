import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.style  import (inject_css, page_header, section, insight, warn,
                           dl_csv, PALETTE, lyt, PULAU_MAP, WARNA_PULAU)
from utils.loader import (loker_indonesia, pengangguran_bps, ump_lengkap,
                           tpt_2026, upah_aktual, geojson)

inject_css()

BAR_H = 28; BAR_MIN = 300
def chart_h(n): return max(BAR_MIN, n * BAR_H + 80)

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
    <b style='color:#FFE4E4;font-size:1rem;'>Dashboard Karir</b>
    <div style='font-size:0.72rem;color:#FFAAAA;margin-top:2px;'>Analisis Data Karir & Pasar Kerja</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.78rem;color:#FFAAAA;line-height:1.8;'>
    <b style='color:#FFE4E4;'>📊 Pasar Kerja Indonesia</b><br><br>
    Sumber: BPS, UMP, Loker Indonesia<br><br>
    • Pengangguran per tingkat pendidikan<br>
    • Kota & industri dengan lowongan terbanyak<br>
    • Peta UMP & TPT per provinsi<br>
    • Tren upah minimum 2002–2026<br>
    • Estimasi gaji per bidang pekerjaan
    </div>""", unsafe_allow_html=True)

with st.spinner("Memuat data Indonesia…"):
    df_lkr  = loker_indonesia()
    df_bps  = pengangguran_bps()
    df_ump  = ump_lengkap()
    df_tpt  = tpt_2026()
    df_upah = upah_aktual()
    gj      = geojson()

EDU_URUTAN = ["Tidak Sekolah","Tidak Tamat SD","SD","SMP","SMA",
              "SMK","Diploma / D3","Universitas / S1+"]
EDU_TARGET = {"Diploma / D3","Universitas / S1+"}

page_header(
    "Pasar Kerja Indonesia",
    "Gambaran kondisi ketenagakerjaan nasional berdasarkan data BPS, lowongan kerja, "
    "dan upah minimum — untuk memahami konteks nyata pasar kerja di Indonesia.", "📊"
)

# ── Metric cards ──────────────────────────────────────────────────
bps24 = df_bps[df_bps["Tahun"]==2024]
sarjana_nganggur = int(bps24[bps24["Pendidikan"].isin(EDU_TARGET)]["Jumlah"].sum())

# TPT nasional dari tpt_clean: cari baris Indonesia atau rata-rata semua provinsi
tpt_nas = df_tpt[df_tpt["prov_raw"].str.upper().str.contains("INDONESIA|TOTAL", na=False)]["TPT_Feb2026"]
tpt_val = float(tpt_nas.values[0]) if len(tpt_nas) else round(df_tpt["TPT_Feb2026"].mean(), 2)

ump26   = df_ump[df_ump["Tahun"]==2026]
ump26_f = ump26[~ump26["Provinsi"].str.lower().str.contains("indonesia", na=False)]
ump_max = ump26_f.loc[ump26_f["UMP"].idxmax()] if len(ump26_f) else None

c1,c2,c3,c4 = st.columns(4)
c1.metric("Penganggur Diploma & S1+ (Feb 2024)",
          f"{sarjana_nganggur/1000:.0f} Ribu jiwa",
          delta="Target utama Evalify", delta_color="off")
c2.metric("Angka Pengangguran Nasional (Feb 2026)",
          f"{tpt_val:.2f}%")
c3.metric("UMP Tertinggi 2026",
          f"Rp {ump_max['UMP']/1e6:.2f} Juta/bln" if ump_max is not None else "—",
          delta=str(ump_max["Provinsi"]) if ump_max is not None else "")
c4.metric("Lowongan di Database Indonesia", f"{len(df_lkr):,}")

st.markdown("""
<div class='insight-box'>💡 <b>Mengapa ini penting?</b>
Lulusan Diploma dan Sarjana menyumbang jutaan penganggur setiap tahun —
padahal mereka memiliki pendidikan tinggi. Kesenjangan antara apa yang diajarkan
di kampus dengan apa yang dibutuhkan industri adalah masalah nyata yang Evalify
coba selesaikan.</div>
""", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ═══ SECTION 1: Kondisi Pengangguran ══════════════════════════════
section("📚 Kondisi Pengangguran Berdasarkan Tingkat Pendidikan")

col_bps1, col_bps2 = st.columns(2, gap="large")

with col_bps1:
    with st.container(border=True):
        st.markdown("**Jumlah Penganggur per Tingkat Pendidikan**")
        tahun_list = sorted(df_bps["Tahun"].unique(), reverse=True)
        sel_yr = st.selectbox("Pilih Tahun", tahun_list, index=0, key="i1_yr")
        df_c1  = df_bps[df_bps["Tahun"]==sel_yr].copy()
        df_c1["Pendidikan"] = pd.Categorical(df_c1["Pendidikan"],
                                             categories=EDU_URUTAN, ordered=True)
        df_c1 = df_c1.sort_values("Pendidikan")
        df_c1["Sorotan"] = df_c1["Pendidikan"].apply(
            lambda x: "🎓 Sarjana & Diploma" if x in EDU_TARGET else "Lainnya")
        fig1 = px.bar(df_c1, x="Pendidikan", y="Jumlah",
                      color="Sorotan",
                      color_discrete_map={"🎓 Sarjana & Diploma":"#FF4B4B","Lainnya":"#FFD6D6"},
                      text_auto=True,
                      title=f"Jumlah Penganggur per Pendidikan — {sel_yr}",
                      labels={"Jumlah":"Jumlah Penganggur (jiwa)","Pendidikan":""})
        fig1.update_traces(texttemplate="%{y:,.0f}", textposition="outside")
        fig1.update_layout(**lyt(xaxis_tickangle=-25, showlegend=True))
        st.plotly_chart(fig1, use_container_width=True)

with col_bps2:
    with st.container(border=True):
        st.markdown("**Tren Pengangguran 1986–2024**")
        edu_pilih = st.multiselect(
            "Pilih tingkat pendidikan", EDU_URUTAN,
            default=["SMA","Diploma / D3","Universitas / S1+"],
            key="i1_edu")
        df_c2 = df_bps[df_bps["Pendidikan"].isin(edu_pilih)] if edu_pilih else df_bps
        fig2  = px.line(df_c2, x="Tahun", y="Jumlah", color="Pendidikan",
                        markers=True, color_discrete_sequence=PALETTE,
                        title="Tren Pengangguran 1986–2024",
                        labels={"Jumlah":"Jumlah Penganggur","Pendidikan":""})
        fig2.add_vrect(x0=2020, x1=2021, fillcolor="#FEF3C7",
                       opacity=0.35, layer="below", line_width=0)
        fig2.add_annotation(x=2020.5,
                            y=df_c2["Jumlah"].max()*0.9 if len(df_c2) else 1,
                            text="Covid-19", font=dict(color="#92400E",size=11),
                            showarrow=False)
        fig2.update_xaxes(rangeslider_visible=False)
        fig2.update_layout(**lyt())
        st.plotly_chart(fig2, use_container_width=True)

# ═══ SECTION 2: Peta Lowongan ══════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
section("🗺️ Di Mana Lowongan Paling Banyak Tersedia?")

col_lk1, col_lk2 = st.columns(2, gap="large")

with col_lk1:
    with st.container(border=True):
        st.markdown("**Kota dengan Lowongan Terbanyak**")
        n_kota = st.slider("Tampilkan berapa kota?", 5, 20, 15, key="i2_k")
        kota   = df_lkr["location"].value_counts().head(n_kota).reset_index()
        kota.columns = ["Kota","Lowongan"]
        fig3 = px.bar(kota, x="Lowongan", y="Kota", orientation="h",
                      color="Lowongan",
                      color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                      title=f"Top {n_kota} Kota Lowongan Terbanyak",
                      labels={"Kota":""})
        fig3.update_layout(**lyt(coloraxis_showscale=False))
        fig3.update_yaxes(autorange="reversed")
        st.plotly_chart(fig3, use_container_width=True)
        dl_csv(kota, "kota_lowongan.csv")

with col_lk2:
    with st.container(border=True):
        st.markdown("**Industri yang Paling Banyak Merekrut di Indonesia**")
        n_ind = st.slider("Tampilkan berapa industri?", 5, 20, 15, key="i2_i")
        ind   = df_lkr["company_industry"].value_counts().head(n_ind).reset_index()
        ind.columns = ["Industri","Lowongan"]
        fig4 = px.bar(ind, x="Lowongan", y="Industri", orientation="h",
                      color="Lowongan",
                      color_continuous_scale=[[0,"#D5F5F0"],[1,"#06D6A0"]],
                      title=f"Top {n_ind} Industri Paling Aktif Merekrut",
                      labels={"Industri":""})
        fig4.update_layout(**lyt(coloraxis_showscale=False))
        fig4.update_yaxes(autorange="reversed")
        st.plotly_chart(fig4, use_container_width=True)
        dl_csv(ind, "industri_id.csv")

insight(
    "Jakarta Raya masih mendominasi jauh dengan lebih dari 8.000 lowongan, diikuti "
    "Jakarta Selatan, Tangerang, dan Jakarta Barat. Ini mencerminkan konsentrasi ekonomi "
    "yang masih sangat terpusat di Jabodetabek. Dari sisi industri, Manufaktur/Produksi "
    "dan Retail memimpin — menandakan bahwa sektor riil masih menjadi tulang punggung "
    "penyerapan tenaga kerja di Indonesia."
)

# ═══ SECTION 3: Peta Provinsi (TPT & UMP) ═════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
section("🗺️ Peta Pengangguran & Upah Minimum per Provinsi")

# TPT: pakai tpt_clean yang sudah bersih (38 provinsi, termasuk Papua baru)
df_tpt_prov = df_tpt[~df_tpt["prov_raw"].str.upper()
                     .str.contains("INDONESIA|TOTAL", na=False)].copy()
df_tpt_prov = df_tpt_prov[df_tpt_prov["TPT_Feb2026"].notna()]

tab_tpt, tab_ump = st.tabs(["📊 Peta Angka Pengangguran (TPT Feb 2026)",
                             "💰 Peta Upah Minimum Provinsi (UMP 2026)"])
fk = "properties.state"

with tab_tpt:
    if gj is None:
        warn("Koneksi internet dibutuhkan untuk menampilkan peta. Menampilkan tabel.")
        st.dataframe(
            df_tpt_prov[["Provinsi","TPT_Feb2026"]]
            .sort_values("TPT_Feb2026",ascending=False)
            .rename(columns={"TPT_Feb2026":"Angka Pengangguran (%)"}),
            use_container_width=True)
    else:
        try:
            sp = gj["features"][0]["properties"]
            if "state" not in sp: fk = "properties." + list(sp.keys())[0]
        except: pass
        fig5 = px.choropleth(df_tpt_prov, geojson=gj,
                             locations="Provinsi", featureidkey=fk,
                             color="TPT_Feb2026",
                             color_continuous_scale="RdYlGn_r",
                             hover_name="Provinsi",
                             hover_data={"TPT_Feb2026":":.2f","Provinsi":False},
                             labels={"TPT_Feb2026":"Pengangguran (%)"},
                             title="Tingkat Pengangguran per Provinsi — Februari 2026 (%)")
        fig5.update_geos(fitbounds="locations", visible=False)
        fig5.update_layout(**lyt(height=500))
        st.plotly_chart(fig5, use_container_width=True)

    # Tambah tabel ringkas top & bottom TPT
    col_hi, col_lo = st.columns(2)
    with col_hi:
        st.markdown("**5 Provinsi TPT Tertinggi**")
        st.dataframe(df_tpt_prov.sort_values("TPT_Feb2026",ascending=False)
                     .head(5)[["Provinsi","TPT_Feb2026"]]
                     .rename(columns={"TPT_Feb2026":"TPT (%)"}),
                     use_container_width=True, hide_index=True)
    with col_lo:
        st.markdown("**5 Provinsi TPT Terendah**")
        st.dataframe(df_tpt_prov.sort_values("TPT_Feb2026")
                     .head(5)[["Provinsi","TPT_Feb2026"]]
                     .rename(columns={"TPT_Feb2026":"TPT (%)"}),
                     use_container_width=True, hide_index=True)
    dl_csv(df_tpt_prov[["Provinsi","TPT_Feb2026"]], "tpt_2026.csv")

with tab_ump:
    ump26 = df_ump[(df_ump["Tahun"]==2026) &
                   (~df_ump["Provinsi"].str.lower().str.contains("indonesia", na=False))].copy()
    if gj is None:
        st.dataframe(ump26.sort_values("UMP",ascending=False)
                     .rename(columns={"UMP":"UMP 2026 (IDR)"}),
                     use_container_width=True)
    else:
        fig6 = px.choropleth(ump26, geojson=gj,
                             locations="Provinsi", featureidkey=fk,
                             color="UMP_Juta",
                             color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                             hover_name="Provinsi",
                             hover_data={"UMP_Juta":":.2f","Provinsi":False},
                             labels={"UMP_Juta":"UMP (Juta Rp)"},
                             title="Upah Minimum Provinsi 2026 (Juta Rupiah/Bulan)")
        fig6.update_geos(fitbounds="locations", visible=False)
        fig6.update_layout(**lyt(height=500))
        st.plotly_chart(fig6, use_container_width=True)
    dl_csv(ump26[["Provinsi","UMP","UMP_Juta"]], "ump_2026.csv")

# ═══ SECTION 4: Tren UMP ══════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
section("📈 Tren Kenaikan Upah Minimum Provinsi (2002–2026)")

with st.container(border=True):
    semua_prov = sorted(df_ump["Provinsi"].unique())
    default_pv = [p for p in ["DKI Jakarta","Jawa Barat","Jawa Timur","Banten","Jawa Tengah"]
                  if p in semua_prov]
    c_u1, c_u2 = st.columns([2,1])
    with c_u2:
        sel_prov = st.multiselect("Pilih Provinsi", semua_prov,
                                  default=default_pv, key="i4_prov")
        satuan   = st.radio("Satuan", ["Juta Rupiah","Rupiah"],
                            horizontal=True, key="i4_sat")
    with c_u1:
        df_uf = df_ump[df_ump["Provinsi"].isin(sel_prov)] if sel_prov else df_ump
        y_col = "UMP_Juta" if satuan=="Juta Rupiah" else "UMP"
        y_lbl = "UMP (Juta Rp/bulan)" if satuan=="Juta Rupiah" else "UMP (Rp/bulan)"
        fig7  = px.line(df_uf, x="Tahun", y=y_col, color="Provinsi",
                        markers=True, color_discrete_sequence=PALETTE,
                        title="Tren Upah Minimum Provinsi 2002–2026",
                        labels={y_col:y_lbl,"Provinsi":""})
        fig7.update_xaxes(rangeslider_visible=False)
        fig7.update_layout(**lyt())
        st.plotly_chart(fig7, use_container_width=True)
    dl_csv(df_uf[["Provinsi","Tahun","UMP"]], "tren_ump.csv")

# ═══ SECTION 5: Gaji per Jenis Pekerjaan ══════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
section("💼 Rentang Gaji Tiap Jenis Pekerjaan di Indonesia")

df_lkr_gaji = df_lkr[df_lkr["salary"].notna()].copy()

if len(df_lkr_gaji) == 0:
    st.info("Data gaji tidak tersedia pada dataset ini — kolom salary kosong setelah preprocessing.")
else:
    with st.container(border=True):
        c_g1, c_g2, c_g3 = st.columns(3)
        with c_g1:
            n_jf   = st.slider("Tampilkan berapa kategori?", 5, 20, 10, key="i6_n")
        with c_g2:
            lvl_opt = ["Semua"] + sorted(df_lkr_gaji["career_level"].dropna().unique())
            sel_lv  = st.selectbox("Level karir", lvl_opt, key="i6_lv")
        with c_g3:
            kota_opt = ["Semua"] + sorted(df_lkr_gaji["location"].dropna()
                                          .value_counts().head(15).index)
            sel_kt   = st.selectbox("Kota", kota_opt, key="i6_kt")

        df_gf = df_lkr_gaji.copy()
        if sel_lv != "Semua": df_gf = df_gf[df_gf["career_level"]==sel_lv]
        if sel_kt != "Semua": df_gf = df_gf[df_gf["location"]==sel_kt]

        agg_gf = (df_gf.groupby("fungsi_singkat")["salary"]
                  .agg(Terendah="min", Tengah="median", Tertinggi="max", Jumlah="count")
                  .reset_index()
                  .sort_values("Tengah", ascending=False)
                  .head(n_jf))
        agg_gf.columns = ["Jenis Pekerjaan","Terendah","Tengah","Tertinggi","Jumlah Data"]
        agg_gf["Tengah_Juta"] = (agg_gf["Tengah"]/1e6).round(1)

        fig9 = px.bar(agg_gf, x="Tengah_Juta", y="Jenis Pekerjaan",
                      orientation="h", color="Tengah_Juta",
                      color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                      hover_data={"Terendah":":,.0f","Tertinggi":":,.0f","Jumlah Data":True},
                      title=f"Median Gaji per Jenis Pekerjaan — Top {n_jf}",
                      labels={"Tengah_Juta":"Gaji Tengah (Juta Rp)","Jenis Pekerjaan":""})
        fig9.update_layout(**lyt(coloraxis_showscale=False))
        fig9.update_yaxes(autorange="reversed")
        st.plotly_chart(fig9, use_container_width=True)
        dl_csv(agg_gf, "gaji_per_pekerjaan.csv")

    insight(
        "Bidang Manufaktur, Perbankan/Keuangan, dan Konsulting secara konsisten "
        "menawarkan gaji tertinggi di pasar Indonesia. Bagi fresh graduate yang ingin "
        "masuk ke bidang ini, investasi dalam sertifikasi dan skill spesialis yang relevan "
        "bisa memberikan return yang signifikan sejak awal karir."
    )
