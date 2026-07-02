import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.style import (inject_css, page_header, section, insight, dl_csv,
                          PALETTE, PALETTE_VIZ, lyt)

inject_css()

with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:16px 0 8px;'>
    <b style='color:#FFE4E4;font-size:1rem;'>Dashboard Karir</b>
    <div style='font-size:0.72rem;color:#FFAAAA;margin-top:2px;'>Analisis Data Karir & Pasar Kerja</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    st.markdown("""<div style='font-size:0.78rem;color:#FFAAAA;line-height:1.8;'>
    <b style='color:#FFE4E4;'>🧬 Tren & Pola Pekerjaan</b><br><br>
    Sumber: 167.000+ deskripsi pekerjaan<br><br>
    • Posisi & bidang pekerjaan terbanyak<br>
    • Skill khas & perbandingan antar bidang<br>
    • Tangga karir: skill & pengalaman per level<br>
    • Eksplorasi domain spesialisasi
    </div>""", unsafe_allow_html=True)

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data",
                         "unique_job_role_descriptions_v5_structured_cache.csv")

BAR_H  = 28
BAR_MIN = 300
def chart_h(n): return max(BAR_MIN, n * BAR_H + 80)

@st.cache_data(show_spinner=False)
def load_cat():
    df = pd.read_csv(DATA_PATH)
    df["skill_count"] = df["job_required_skills"].dropna().str.split("|").apply(len)
    return df

FAMILY_LABEL = {
    "tech":"Teknologi","finance":"Keuangan","sales_marketing":"Sales & Marketing",
    "operations":"Operasional","general":"Umum","legal":"Hukum",
    "design":"Desain","health":"Kesehatan","education":"Pendidikan",
}
SENIORITY_ORDER = [
    "intern","trainee","apprentice","entry level","junior","associate",
    "mid level","intermediate","experienced","staff","senior","lead",
    "manager","senior manager","head","director","vice president","chief",
    "executive","principal",
]
LADDER_GROUP = {
    "intern":"Pemula","apprentice":"Pemula","trainee":"Pemula",
    "entry level":"Pemula","junior":"Pemula",
    "associate":"Menengah","intermediate":"Menengah","mid level":"Menengah",
    "staff":"Menengah","experienced":"Menengah",
    "senior":"Senior","lead":"Senior","principal":"Senior",
    "manager":"Manajer","senior manager":"Manajer",
    "head":"Manajer","director":"Manajer",
    "chief":"Eksekutif","vice president":"Eksekutif","executive":"Eksekutif",
}
GROUP_COLOR = {
    "Pemula":"#118AB2","Menengah":"#06D6A0","Senior":"#FFD166",
    "Manajer":"#FF8C42","Eksekutif":"#FF4B4B",
}
GROUP_ORDER  = ["Pemula","Menengah","Senior","Manajer","Eksekutif"]
GENERIC_SKILLS = {
    "documentation","communication","planning","teamwork","coordinating",
    "analytical thinking","problem solving","project execution","reporting",
    "operations","microsoft teams","training","management","execution","make",
}

try:
    with st.spinner("Memuat data…"):
        df = load_cat()
except FileNotFoundError:
    st.error("File deskripsi pekerjaan tidak ditemukan. Tambahkan "
             "`unique_job_role_descriptions_v5_structured_cache.csv` ke folder `data/`.")
    st.stop()

df["fam_label"]   = df["role_family"].map(FAMILY_LABEL).fillna(df["role_family"])
df["group_label"] = df["job_seniority_level"].map(LADDER_GROUP)
FAM_KEY_MAP = {v: k for k, v in FAMILY_LABEL.items()}
FAMILIES    = sorted(df["fam_label"].unique())

page_header("Tren & Pola Pekerjaan",
            "Gambaran lengkap dari 167.000+ deskripsi pekerjaan yang telah dianalisis — "
            "posisi apa yang paling banyak ada, skill apa yang khas tiap bidang, "
            "dan seperti apa jalur karir dari bawah hingga puncak.", "🧬")

c1, c2 = st.columns(2)
c1.metric("Total Peran Pekerjaan", f"{len(df):,}")
c2.metric("Bidang Pekerjaan",      f"{df['role_family'].nunique()}")
st.markdown("<hr>", unsafe_allow_html=True)

# ── SECTION 1 ─────────────────────────────────────────────────────
section("📌 Posisi & Bidang Pekerjaan yang Paling Banyak Ada")

col_L, col_R = st.columns(2, gap="large")

with col_L:
    with st.container(border=True):
        st.markdown("**Posisi Pekerjaan yang Paling Banyak Tersedia**")
        st.caption("Judul pekerjaan yang paling sering muncul di seluruh dataset deskripsi pekerjaan.")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            tn_role = st.slider("Top posisi", 10, 30, 15, key="c1_role")
        with col_f2:
            dom_opts = sorted(df["job_domain"].dropna().str.split("|").explode().str.strip().unique())
            sel_dom  = st.multiselect("Filter domain", dom_opts,
                                      placeholder="Semua domain", key="c1_dom")
        df_cf = df.copy()
        if sel_dom:
            df_cf = df[df["job_domain"].apply(
                lambda x: any(d in str(x).split("|") for d in sel_dom) if pd.notna(x) else False)]
        rc = df_cf["job_role"].value_counts().head(tn_role).reset_index()
        rc.columns = ["Posisi","Jumlah"]
        fig_rc = px.bar(rc, x="Jumlah", y="Posisi", orientation="h",
                        color="Jumlah",
                        color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                        title=f"Top {tn_role} Posisi Pekerjaan Terbanyak",
                        labels={"Posisi":""})
        fig_rc.update_layout(**lyt(coloraxis_showscale=False, height=chart_h(tn_role)))
        fig_rc.update_yaxes(autorange="reversed", tickfont=dict(size=11))
        st.plotly_chart(fig_rc, use_container_width=True)

with col_R:
    with st.container(border=True):
        st.markdown("**Komposisi Bidang Pekerjaan**")
        st.caption("Pengelompokan semua peran ke dalam bidang fungsi utama.")
        rf = df["fam_label"].value_counts().reset_index()
        rf.columns = ["Bidang","Jumlah Peran"]
        rf["Persen"] = (rf["Jumlah Peran"]/rf["Jumlah Peran"].sum()*100).round(1)
        fig_rf = px.bar(rf, x="Jumlah Peran", y="Bidang", orientation="h",
                        color="Jumlah Peran",
                        color_continuous_scale=[[0,"#D5F5F0"],[1,"#06D6A0"]],
                        text="Persen", title="Komposisi Bidang Pekerjaan",
                        labels={"Bidang":""})
        fig_rf.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
        fig_rf.update_layout(**lyt(coloraxis_showscale=False, height=chart_h(len(rf))))
        fig_rf.update_yaxes(autorange="reversed", tickfont=dict(size=12))
        st.plotly_chart(fig_rf, use_container_width=True)

insight("Bidang Operasional dan Teknologi mendominasi dataset dengan jumlah variasi pekerjaan terbanyak. "
        "Kedua bidang ini memiliki spektrum peran paling luas, mulai dari level pemula hingga eksekutif, "
        "dan membuka peluang yang cukup merata bagi kandidat dari berbagai latar belakang.")

# ── SECTION 2 ─────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("🎯 Skill yang Paling Khas di Tiap Bidang Pekerjaan")
st.caption("Pilih bidang untuk melihat skill yang paling dibutuhkan. "
           "Skill generik seperti 'communication' dan 'teamwork' sudah dikecualikan "
           "agar yang tampil adalah skill pembeda yang benar-benar spesifik.")

sel_fam = st.selectbox("Pilih bidang pekerjaan", FAMILIES, key="sec2_fam")
fam_key = FAM_KEY_MAP.get(sel_fam, sel_fam)
df_fam  = df[df["role_family"] == fam_key]

with st.container(border=True):
    n_sk = st.slider("Tampilkan berapa skill?", 8, 25, 15, key="sec2_n")
    skills_exploded = df_fam["job_required_skills"].dropna().str.split("|").explode().str.strip()
    all_skills = skills_exploded.value_counts().reset_index()
    all_skills.columns = ["Skill","Frekuensi"]
    unique_skills = all_skills[~all_skills["Skill"].isin(GENERIC_SKILLS)].head(n_sk)
    fig_us = px.bar(unique_skills, x="Frekuensi", y="Skill", orientation="h",
                    color="Frekuensi",
                    color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                    title=f"Skill Paling Dibutuhkan di Bidang {sel_fam}",
                    labels={"Skill":""})
    fig_us.update_layout(**lyt(coloraxis_showscale=False, height=chart_h(n_sk)))
    fig_us.update_yaxes(autorange="reversed", tickfont=dict(size=12))
    st.plotly_chart(fig_us, use_container_width=True)

# ── SECTION 3 ─────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("🔀 Perbandingan Skill Antar Bidang Pekerjaan")
st.caption("Pilih beberapa bidang. Lingkaran yang lebih besar dan lebih gelap = skill itu lebih sering "
           "diminta di bidang tersebut. Skill yang muncul di banyak bidang sekaligus = skill paling versatile.")

sel_fams  = st.multiselect("Pilih bidang (2–4)", FAMILIES,
                            default=["Teknologi","Keuangan","Sales & Marketing"],
                            key="sec3_fams")
n_compare = st.slider("Top skill per bidang", 5, 12, 8, key="sec3_n")

if len(sel_fams) < 2:
    st.warning("Pilih minimal 2 bidang.")
else:
    skill_rows = []
    for fl in sel_fams:
        fk = FAM_KEY_MAP.get(fl, fl)
        s  = (df[df["role_family"] == fk]["job_required_skills"]
               .dropna().str.split("|").explode().str.strip())
        top = s.value_counts().reset_index()
        top.columns = ["Skill","Frekuensi"]
        top = top[~top["Skill"].isin(GENERIC_SKILLS)].head(n_compare).copy()
        top["Bidang"] = fl
        skill_rows.append(top)

    df_cmp = pd.concat(skill_rows, ignore_index=True)
    pivot  = df_cmp.pivot_table(index="Skill", columns="Bidang",
                                 values="Frekuensi", fill_value=0)
    pivot["_total"] = pivot.sum(axis=1)
    pivot = (pivot.sort_values("_total", ascending=False)
             .drop(columns="_total").head(n_compare * 2))

    with st.container(border=True):
        fig_heat = px.imshow(
            pivot,
            color_continuous_scale=[[0,"#FFF5F5"],[0.3,"#FF8C42"],[1,"#FF4B4B"]],
            aspect="auto",
            title="Seberapa Sering Skill Ini Diminta per Bidang?",
            labels={"color":"Frekuensi","x":"Bidang","y":"Skill"},
            text_auto=True
        )
        fig_heat.update_layout(**lyt(
            height=max(300, len(pivot)*28),
            coloraxis_colorbar=dict(title="Frekuensi"),
            xaxis_side="bottom"
        ))
        st.plotly_chart(fig_heat, use_container_width=True)
        st.markdown("""
        <div style='background:#FFF5F5;border-left:3px solid #FF4B4B;padding:10px 14px;
        border-radius:0 8px 8px 0;font-size:0.83rem;color:#7F1D1D;margin-top:6px;'>
        📌 <b>Cara membaca:</b> Semakin merah, semakin sering skill itu diminta di bidang tersebut.
        Baris yang merah di banyak kolom sekaligus = skill lintas bidang yang paling berharga untuk dikuasai.
        </div>""", unsafe_allow_html=True)
insight("Skill seperti database, analisis keuangan, dan pemasaran digital muncul di lebih dari satu bidang. "
        "Skill semacam ini membuat profilmu lebih fleksibel — kamu tidak terkunci di satu jalur karir saja. "
        "Di sisi lain, skill yang sangat spesifik di satu bidang menunjukkan kedalaman keahlian "
        "yang justru bisa membedakanmu dari kandidat lain.")

# ── SECTION 4 ─────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("🪜 Tangga Karir: Makin Tinggi Level, Makin Banyak yang Dibutuhkan")
st.caption("Rata-rata jumlah skill dan tahun pengalaman yang dibutuhkan di setiap jenjang, "
           "dari magang hingga eksekutif.")

LADDER_SEQ = [s for s in SENIORITY_ORDER if s in df["job_seniority_level"].unique()]
df_ladder  = df[df["job_seniority_level"].isin(LADDER_SEQ)].copy()
df_ladder["group_label"] = df_ladder["job_seniority_level"].map(LADDER_GROUP)

agg = df_ladder.groupby("job_seniority_level").agg(
    avg_skills=("skill_count","mean"),
    avg_exp=("job_required_years_experience","mean"),
    jumlah=("job_role","count"),
).reset_index()
agg["job_seniority_level"] = pd.Categorical(
    agg["job_seniority_level"], categories=LADDER_SEQ, ordered=True)
agg = agg.sort_values("job_seniority_level")
agg["group"]      = agg["job_seniority_level"].map(LADDER_GROUP)
agg["avg_skills"] = agg["avg_skills"].round(1)
agg["avg_exp"]    = agg["avg_exp"].round(1)
# Label untuk display (Title Case)
agg["level_label"] = agg["job_seniority_level"].astype(str).str.title()

with st.container(border=True):
    col_l, col_r = st.columns(2, gap="large")

    H_TANGGA = max(520, len(LADDER_SEQ) * 27 + 80)

    with col_l:
        st.markdown("**Rata-rata Jumlah Skill yang Dibutuhkan per Level**")
        # Gunakan lollipop / dot chart untuk lebih visual
        fig_sk = go.Figure()
        for grp in GROUP_ORDER:
            sub = agg[agg["group"] == grp]
            if sub.empty: continue
            color = GROUP_COLOR[grp]
            # Garis dari 0 ke nilai
            for _, row in sub.iterrows():
                fig_sk.add_shape(
                    type="line",
                    x0=0, x1=row["avg_skills"],
                    y0=row["level_label"], y1=row["level_label"],
                    line=dict(color=color, width=2.5)
                )
            fig_sk.add_trace(go.Scatter(
                x=sub["avg_skills"], y=sub["level_label"],
                mode="markers+text",
                name=grp,
                marker=dict(size=14, color=color,
                            line=dict(width=2, color="white")),
                text=sub["avg_skills"].astype(str),
                textposition="middle right",
                textfont=dict(size=11, color="#374151"),
                hovertemplate=f"<b>{grp}</b><br>%{{y}}<br>Rata-rata skill: %{{x:.1f}}<extra></extra>",
            ))
        fig_sk.update_layout(**lyt(
            title="Rata-rata Skill per Level",
            height=H_TANGGA,
            showlegend=True,
            legend=dict(orientation="h", y=1.06, x=0, font=dict(size=11)),
            xaxis=dict(title="Rata-rata Jumlah Skill", tickfont=dict(size=11),
                       range=[0, agg["avg_skills"].max() * 1.3]),
            yaxis=dict(title="", categoryorder="array",
                       categoryarray=agg["level_label"].tolist()[::-1],
                       tickfont=dict(size=12)),
            margin=dict(l=10, r=60, t=50, b=10),
        ))
        st.plotly_chart(fig_sk, use_container_width=True)

    with col_r:
        st.markdown("**Rata-rata Pengalaman yang Dibutuhkan per Level (Tahun)**")
        agg_exp = agg[agg["avg_exp"] > 0].copy()
        fig_exp = go.Figure()
        for grp in GROUP_ORDER:
            sub = agg_exp[agg_exp["group"] == grp]
            if sub.empty: continue
            color = GROUP_COLOR[grp]
            for _, row in sub.iterrows():
                fig_exp.add_shape(
                    type="line",
                    x0=0, x1=row["avg_exp"],
                    y0=row["level_label"], y1=row["level_label"],
                    line=dict(color=color, width=2.5)
                )
            fig_exp.add_trace(go.Scatter(
                x=sub["avg_exp"], y=sub["level_label"],
                mode="markers+text",
                name=grp,
                marker=dict(size=14, color=color,
                            line=dict(width=2, color="white")),
                text=sub["avg_exp"].apply(lambda v: f"{v:.1f} thn"),
                textposition="middle right",
                textfont=dict(size=11, color="#374151"),
                hovertemplate=f"<b>{grp}</b><br>%{{y}}<br>Pengalaman: %{{x:.1f}} tahun<extra></extra>",
            ))
        fig_exp.update_layout(**lyt(
            title="Rata-rata Pengalaman per Level",
            height=H_TANGGA,
            showlegend=True,
            legend=dict(orientation="h", y=1.06, x=0, font=dict(size=11)),
            xaxis=dict(title="Tahun Pengalaman", tickfont=dict(size=11),
                       range=[0, agg_exp["avg_exp"].max() * 1.35]),
            yaxis=dict(title="", categoryorder="array",
                       categoryarray=agg["level_label"].tolist()[::-1],
                       tickfont=dict(size=12)),
            margin=dict(l=10, r=80, t=50, b=10),
        ))
        st.plotly_chart(fig_exp, use_container_width=True)

insight("Level Senior dan Lead adalah titik kritis dalam tangga karir — di sinilah tuntutan "
        "skill dan pengalaman melonjak paling signifikan. Rata-rata dibutuhkan 4–5 tahun pengalaman "
        "untuk mencapai level ini. Artinya, investasi dalam skill yang tepat sejak awal karir "
        "sangat menentukan seberapa cepat kamu bisa naik ke jenjang berikutnya.")

# ── SECTION 5 ─────────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
section("🌐 Eksplorasi Domain Spesialisasi")
st.caption("Pilih satu domain spesialisasi pekerjaan untuk melihat peran apa saja yang ada "
           "dan sebaran level jabatannya.")

top_domains = (df["job_domain"].dropna().str.split("|").explode()
               .str.strip().value_counts().head(25).index.tolist())
sel_domain  = st.selectbox("Pilih Domain", top_domains, key="dom_sel")

df_dom = df[df["job_domain"].fillna("").str.contains(sel_domain, regex=False)].copy()
df_dom["group_label"] = df_dom["job_seniority_level"].map(LADDER_GROUP)

col_d1, col_d2 = st.columns(2, gap="large")

with col_d1:
    with st.container(border=True):
        st.markdown(f"**Posisi yang Ada di Domain '{sel_domain.title()}'**")
        rc2 = df_dom["role_group"].value_counts().head(15).reset_index()
        rc2.columns = ["Peran","Jumlah"]
        fig_d1 = px.bar(rc2, x="Jumlah", y="Peran", orientation="h",
                        color="Jumlah",
                        color_continuous_scale=[[0,"#FFD6D6"],[1,"#FF4B4B"]],
                        title=f"Top 15 Peran di Domain {sel_domain.title()}",
                        labels={"Peran":""})
        fig_d1.update_layout(**lyt(coloraxis_showscale=False, height=chart_h(15)))
        fig_d1.update_yaxes(autorange="reversed", tickfont=dict(size=11))
        st.plotly_chart(fig_d1, use_container_width=True)

with col_d2:
    with st.container(border=True):
        st.markdown(f"**Sebaran Level Jabatan di Domain '{sel_domain.title()}'**")
        lv2 = df_dom["group_label"].dropna().value_counts().reset_index()
        lv2.columns = ["Level","Jumlah"]
        lv2["Level"] = pd.Categorical(lv2["Level"], categories=GROUP_ORDER, ordered=True)
        lv2 = lv2.sort_values("Level")
        fig_d2 = px.bar(lv2, x="Level", y="Jumlah",
                        color="Level", color_discrete_map=GROUP_COLOR,
                        title=f"Level Jabatan di Domain {sel_domain.title()}",
                        text="Jumlah", labels={"Level":""})
        fig_d2.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_d2.update_layout(**lyt(showlegend=False))
        st.plotly_chart(fig_d2, use_container_width=True)

st.markdown("""<p style='text-align:center;color:#9CA3AF;font-size:0.78rem;margin-top:32px;'>
Sumber: 167.000+ deskripsi pekerjaan yang distrukturisasi menggunakan AI</p>""",
            unsafe_allow_html=True)
