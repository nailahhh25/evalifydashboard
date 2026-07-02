# utils/style.py
import streamlit as st

PRIMARY   = "#FF4B4B"
SECONDARY = "#FF6B6B"
SUCCESS   = "#21BA45"
WARNING   = "#F59E0B"
DANGER    = "#EF4444"
GRAY      = "#6B7280"
LIGHT_BG  = "#FFF5F5"

PALETTE = [
    "#FF4B4B","#FF8C42","#FFD166","#06D6A0",
    "#118AB2","#073B4C","#EF476F","#8338EC",
    "#FB5607","#3A86FF"
]

# Netral abu-abu untuk chart struktural (katalog AI)
PALETTE_VIZ = [
    "#374151","#6B7280","#9CA3AF","#4B5563","#1F2937",
    "#64748B","#475569","#94A3B8","#D1D5DB","#CBD5E1"
]

LABEL_WARNA = {"Good Fit":"#21BA45","Potential Fit":"#F59E0B","No Fit":"#EF4444"}

BOBOT_SCORING = {
    "Kecocokan Skill":0.35,"Kecocokan Tools":0.15,"Kecocokan Domain":0.15,
    "Kecocokan Pengalaman":0.10,"Kecocokan Pendidikan":0.08,
    "Kecocokan Proyek":0.07,"Kecocokan Level Jabatan":0.05,
    "Sertifikasi":0.03,"Tanggung Jawab":0.02,
}
WARNA_BOBOT = {
    "Kecocokan Skill":"#FF4B4B","Kecocokan Tools":"#06D6A0",
    "Kecocokan Domain":"#118AB2","Kecocokan Pengalaman":"#8338EC",
    "Kecocokan Pendidikan":"#F59E0B","Kecocokan Proyek":"#FB5607",
    "Kecocokan Level Jabatan":"#EF476F","Sertifikasi":"#9CA3AF",
    "Tanggung Jawab":"#073B4C",
}

PROVINSI_NORM = {
    "ACEH":"Aceh","SUMATERA UTARA":"Sumatera Utara","SUMATERA BARAT":"Sumatera Barat",
    "SUMATERA SELATAN":"Sumatera Selatan","RIAU":"Riau","JAMBI":"Jambi",
    "BENGKULU":"Bengkulu","LAMPUNG":"Lampung",
    "KEP. BANGKA BELITUNG":"Kepulauan Bangka Belitung",
    "KEPULAUAN BANGKA BELITUNG":"Kepulauan Bangka Belitung",
    "KEP. RIAU":"Kepulauan Riau","KEPULAUAN RIAU":"Kepulauan Riau",
    "DKI JAKARTA":"DKI Jakarta","Dki Jakarta":"DKI Jakarta",
    "JAWA BARAT":"Jawa Barat","JAWA TENGAH":"Jawa Tengah",
    "DI YOGYAKARTA":"DI Yogyakarta","D.I YOGYAKARTA":"DI Yogyakarta",
    "Di Yogyakarta":"DI Yogyakarta","JAWA TIMUR":"Jawa Timur",
    "BANTEN":"Banten","BALI":"Bali",
    "NUSA TENGGARA BARAT":"Nusa Tenggara Barat","NUSA TENGGARA TIMUR":"Nusa Tenggara Timur",
    "KALIMANTAN BARAT":"Kalimantan Barat","KALIMANTAN TENGAH":"Kalimantan Tengah",
    "KALIMANTAN SELATAN":"Kalimantan Selatan","KALIMANTAN TIMUR":"Kalimantan Timur",
    "KALIMANTAN UTARA":"Kalimantan Utara","SULAWESI UTARA":"Sulawesi Utara",
    "SULAWESI TENGAH":"Sulawesi Tengah","SULAWESI SELATAN":"Sulawesi Selatan",
    "SULAWESI TENGGARA":"Sulawesi Tenggara","GORONTALO":"Gorontalo",
    "SULAWESI BARAT":"Sulawesi Barat","MALUKU":"Maluku","MALUKU UTARA":"Maluku Utara",
    "PAPUA BARAT":"Papua Barat","PAPUA":"Papua",
    "Kep. Bangka Belitung":"Kepulauan Bangka Belitung","Kep. Riau":"Kepulauan Riau",
}

PULAU_MAP = {p:"Jawa" for p in ["DKI Jakarta","Jawa Barat","Jawa Tengah","DI Yogyakarta","Jawa Timur","Banten"]}
PULAU_MAP.update({p:"Sumatera" for p in ["Aceh","Sumatera Utara","Sumatera Barat","Riau","Jambi","Sumatera Selatan","Bengkulu","Lampung","Kepulauan Bangka Belitung","Kepulauan Riau"]})
PULAU_MAP.update({p:"Kalimantan" for p in ["Kalimantan Barat","Kalimantan Tengah","Kalimantan Selatan","Kalimantan Timur","Kalimantan Utara"]})
PULAU_MAP.update({p:"Sulawesi" for p in ["Sulawesi Utara","Sulawesi Tengah","Sulawesi Selatan","Sulawesi Tenggara","Gorontalo","Sulawesi Barat"]})
PULAU_MAP.update({p:"Bali & Nusa Tenggara" for p in ["Bali","Nusa Tenggara Barat","Nusa Tenggara Timur"]})
PULAU_MAP.update({p:"Maluku & Papua" for p in ["Maluku","Maluku Utara","Papua Barat","Papua"]})
WARNA_PULAU = {
    "Jawa":"#FF4B4B","Sumatera":"#06D6A0","Kalimantan":"#F59E0B",
    "Sulawesi":"#118AB2","Bali & Nusa Tenggara":"#EF476F","Maluku & Papua":"#8338EC"
}

KATEGORI_CV_RULES = [
    (["data scientist","data analyst","data engineer","machine learning","ml engineer","ai engineer","analytics"],"Data Science"),
    (["web developer","frontend","backend","fullstack","full stack","react","angular","django","flask","nodejs"],"Web Dev"),
    (["software engineer","software developer","programmer","application developer","mobile developer","android","ios"],"Software Eng"),
    (["devops","cloud engineer","sre","site reliability","kubernetes","docker","aws engineer"],"DevOps/Cloud"),
    (["hr","human resource","recruiter","talent acquisition","hrd"],"HR"),
    (["marketing","digital marketing","seo","sem","content","brand","growth"],"Marketing"),
    (["finance","financial","accounting","accountant","auditor","tax"],"Finance"),
    (["sales","business development","account manager","account executive"],"Sales"),
    (["project manager","program manager","scrum master","agile"],"Project Mgmt"),
    (["product manager","product owner","ux","ui designer","product designer","graphic designer"],"Product & Design"),
    (["network engineer","system admin","sysadmin","it support","security engineer","cybersecurity"],"IT & Infrastruktur"),
]

LAYOUT = dict(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=12, color="#374151"),
    margin=dict(l=8, r=8, t=40, b=8),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Inter"),
    legend=dict(bgcolor="rgba(0,0,0,0)"),
)

def lyt(**kw):
    d = LAYOUT.copy(); d.update(kw); return d


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

[data-testid="metric-container"] {
    background: white;
    border: 1px solid #FFD6D6;
    border-radius: 14px;
    padding: 18px 22px;
    box-shadow: 0 1px 4px rgba(255,75,75,0.08);
}
[data-testid="metric-container"] label {
    font-size: 0.72rem; color: #9CA3AF;
    font-weight: 600; letter-spacing: 0.05em;
    text-transform: uppercase;
}
[data-testid="stMetricValue"] { font-size: 1.65rem !important; font-weight: 700; color: #111827; }
[data-testid="stMetricDelta"] { font-size: 0.8rem !important; }

[data-testid="stSidebar"] { background-color: #1A0A0A; }
[data-testid="stSidebar"] * { color: #FFE4E4 !important; }
[data-testid="stSidebarNav"] a { border-radius: 8px; margin: 2px 0; }
[data-testid="stSidebarNav"] a:hover { background: rgba(255,75,75,0.15); }
[data-testid="stSidebarNav"] a[aria-selected="true"] { background: rgba(255,75,75,0.35); font-weight: 600; }

.page-header {
    background: linear-gradient(135deg, #FF4B4B 0%, #FF8C42 100%);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 24px; color: white;
}
.page-header h1 { color: white; margin: 0 0 6px; font-size: 1.7rem; font-weight: 700; }
.page-header p  { color: rgba(255,255,255,0.88); margin: 0; font-size: 0.95rem; }

.section-title {
    font-size: 1.05rem; font-weight: 700; color: #111827;
    border-left: 4px solid #FF4B4B; padding-left: 10px;
    margin: 24px 0 12px;
}

.insight-box {
    background: #FFF5F5; border-left: 4px solid #FF4B4B;
    padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 10px 0;
    font-size: 0.88rem; color: #7F1D1D;
}
.insight-box b { color: #991B1B; }

.warn-box {
    background: #FFFBEB; border-left: 4px solid #F59E0B;
    padding: 12px 16px; border-radius: 0 10px 10px 0; margin: 10px 0;
    font-size: 0.88rem; color: #92400E;
}

hr { border-color: #FFE4E4; margin: 20px 0; }

[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 14px !important; border-color: #FFD6D6 !important;
    box-shadow: 0 1px 4px rgba(255,75,75,0.05);
}
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)

def page_header(title: str, desc: str, icon: str = ""):
    st.markdown(
        f'<div class="page-header"><h1>{icon} {title}</h1><p>{desc}</p></div>',
        unsafe_allow_html=True)

def section(title: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def insight(text: str):
    st.markdown(f'<div class="insight-box">💡 <b>Insight:</b> {text}</div>', unsafe_allow_html=True)

def warn(text: str):
    st.markdown(f'<div class="warn-box">⚠️ {text}</div>', unsafe_allow_html=True)

def dl_csv(df, fname, label="⬇ Unduh Data"):
    st.download_button(label, df.to_csv(index=False).encode(),
                       fname, "text/csv", key=f"dl_{fname}_{id(df)}")
