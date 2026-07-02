# utils/loader.py  —  semua fungsi loading & preprocessing data
# ⚡ Diperbarui: pakai file processed/ untuk semua data yang sudah dipreproses

import ast, json, os, re
import numpy as np
import pandas as pd
import requests
import streamlit as st

from utils.style import PROVINSI_NORM, KATEGORI_CV_RULES

DIR  = "data"
PROC = "data/processed"

def _p(f):  return os.path.join(DIR,  f)
def _pp(f): return os.path.join(PROC, f)

def _lfs(fp):
    try:
        with open(fp,"rb") as f: return b"git-lfs.github.com" in f.read(200)
    except: return True

def _prov(name):
    s = str(name).strip()
    return PROVINSI_NORM.get(s, PROVINSI_NORM.get(s.upper(), s))

# ─── Tab 1: Rekrutmen & Industri ────────────────────────────────────

@st.cache_data(show_spinner=False)
def jd():
    """Job descriptions — pakai preprocessed jika tersedia."""
    fp = _pp("jd_preprocessed.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        # skills_list sudah string repr list di kolom skills_list
        df["skills_list"] = df["skills_list"].apply(
            lambda x: ast.literal_eval(x) if pd.notna(x) else [])
        return df
    # fallback ke file asli
    df = pd.read_csv(_p("jd_cleaned.csv"))
    df["title_clean"] = df["title_clean"].str.strip().str.lower()
    df["skills_list"] = df["job_skills"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else [])
    return df

@st.cache_data(show_spinner=False)
def postings():
    """LinkedIn postings — pakai processed jika tersedia."""
    fp = _pp("postings_clean.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df["listed_dt"] = pd.to_datetime(df["listed_dt"], errors="coerce")
        return df
    # fallback ke file asli
    cols = ["job_id","title","formatted_experience_level",
            "formatted_work_type","listed_time","normalized_salary",
            "location","remote_allowed"]
    df = pd.read_csv(_p("postings.csv"), usecols=cols, low_memory=False)
    df["listed_dt"] = pd.to_datetime(df["listed_time"], unit="ms", errors="coerce")
    df["Bulan"]    = df["listed_dt"].dt.to_period("M").astype(str)
    df["Kuartal"]  = df["listed_dt"].dt.to_period("Q").astype(str)
    return df

@st.cache_data(show_spinner=False)
def posting_industri():
    """Postings sudah di-join dengan industri — pakai processed."""
    fp = _pp("postings_industri_clean.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df["listed_dt"] = pd.to_datetime(df.get("listed_dt",""), errors="coerce")
        return df
    # fallback: merge manual
    p   = postings()
    ji  = pd.read_csv(_p("job_industries.csv"))
    ind = pd.read_csv(_p("industries.csv"))
    return p.merge(ji, on="job_id").merge(ind, on="industry_id")

@st.cache_data(show_spinner=False)
def skill_domain_linkedin():
    """35 kategori skill LinkedIn — pakai processed yang sudah ada Tipe."""
    fp = _pp("skill_demand_linkedin_clean.csv")
    if os.path.exists(fp):
        return pd.read_csv(fp)
    # fallback: merge job_skills + skills
    js = pd.read_csv(_p("job_skills.csv"))
    sm = pd.read_csv(_p("skills.csv"))
    return js.merge(sm, on="skill_abr")

@st.cache_data(show_spinner=False)
def catalog():
    fp = _p("unique_job_role_descriptions_v5_structured_cache.csv")
    if not os.path.exists(fp) or _lfs(fp): return None
    return pd.read_csv(fp)

def explode_pipe(df, col):
    return (df[col].dropna().str.split("|").explode()
            .str.strip().loc[lambda s: s!=""])

# ─── Tab 2: Skill Gap ────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def skill_gap():
    return pd.read_csv(_p("skill_gap_analysis.csv"))

@st.cache_data(show_spinner=False)
def hard_skills():
    hs = set()
    for fn in ["hardskills.txt","skills_index_final.csv"]:
        fp = _p(fn)
        if not os.path.exists(fp): continue
        if fn.endswith(".txt"):
            with open(fp) as f:
                for l in f:
                    t = l.strip().lower()
                    if t: hs.add(t)
        else:
            for s in pd.read_csv(fp)["Skill"].dropna():
                hs.add(str(s).lower())
    return hs

@st.cache_data(show_spinner=False)
def taxonomy():
    with open(_p("taxonomy.json")) as f: return json.load(f)

@st.cache_data(show_spinner=False)
def gap_domain():
    tax     = taxonomy()
    domains = tax["cv_taxonomy"]["domain_keywords"]
    teks_jd = " ".join(jd()["text_combined"].dropna()).lower()
    teks_kd = " ".join(kamus_skill()["skill"].dropna()).lower() \
              if os.path.exists(_p("validated_skill_dictionary.csv")) else ""
    rows = []
    for d in domains:
        dm = teks_jd.count(d.lower())
        sp = teks_kd.count(d.lower())
        rows.append({"Domain":d,"Dibutuhkan Industri":dm,
                     "Dimiliki Kandidat":sp,"Selisih":dm-sp})
    df = pd.DataFrame(rows)
    return df[df["Dibutuhkan Industri"]>0].sort_values("Selisih",ascending=False)

def kamus_skill():
    fp = _p("validated_skill_dictionary.csv")
    if os.path.exists(fp): return pd.read_csv(fp)
    return pd.DataFrame(columns=["skill"])

# ─── Tab 3: Pasar Kerja Indonesia ────────────────────────────────

@st.cache_data(show_spinner=False)
def loker_indonesia():
    """Lowongan kerja Indonesia — pakai processed."""
    fp = _pp("loker_indonesia_clean.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
        if "fungsi_singkat" not in df.columns:
            df["fungsi_singkat"] = df["job_function"].str.split(",").str[0].str.strip().fillna("Lainnya")
        return df
    # fallback
    df = pd.read_csv(_p("Job_Description_and_Salary_in_Indonesia.csv"), sep="|", low_memory=False)
    df["salary"] = pd.to_numeric(df["salary"], errors="coerce")
    df = df[(df["salary"].isna()) | ((df["salary"]>=500_000)&(df["salary"]<=500_000_000))]
    df["fungsi_singkat"] = df["job_function"].str.split(",").str[0].str.strip().fillna("Lainnya")
    return df

@st.cache_data(show_spinner=False)
def pengangguran_bps():
    """BPS pengangguran — pakai processed clean."""
    fp = _pp("bps_pengangguran_clean.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        # Gunakan data Februari saja jika ada kolom Periode
        if "Periode" in df.columns:
            df_feb = df[df["Periode"]=="Februari"]
            # Untuk tahun sebelum 2005 data hanya tahunan
            df_thn = df[df["Periode"]=="Tahunan"]
            df = pd.concat([df_thn, df_feb], ignore_index=True)
            # Jika satu tahun punya keduanya, prioritaskan Februari
            df = df.sort_values("Periode").drop_duplicates(
                subset=["Tahun","Pendidikan"], keep="last")
        return df[["Tahun","Pendidikan","Jumlah"]]
    # fallback: parse manual
    fp2 = _p("pengangguran_bps_1986_2024.csv")
    raw = pd.read_csv(fp2, header=None, skiprows=2, low_memory=False)
    mask = pd.to_numeric(raw.iloc[:,0], errors="coerce").notna()
    edu  = raw[mask].reset_index(drop=True).iloc[:8]
    levels = edu.iloc[:,1].tolist()
    MAP = {"Tidak/belum pernah sekolah":"Tidak Sekolah","Tidak/belum tamat SD":"Tidak Tamat SD",
           "SD":"SD","SLTP":"SMP","SLTA Umum/SMU":"SMA","SLTA Kejuruan/SMK":"SMK",
           "Akademi/Diploma":"Diploma / D3","Universitas":"Universitas / S1+"}
    rows = []
    for off,yr in enumerate(range(1986,2005)):
        c = 2+off
        for i,lv in enumerate(levels):
            v=edu.iloc[i,c]
            if pd.notna(v):
                try: rows.append({"Tahun":yr,"Pendidikan":MAP.get(lv,lv),"Jumlah":float(v)})
                except: pass
    for yo in range(20):
        yr=2005+yo; c=21+yo*2
        for i,lv in enumerate(levels):
            try:
                v=edu.iloc[i,c]
                if pd.notna(v): rows.append({"Tahun":yr,"Pendidikan":MAP.get(lv,lv),"Jumlah":float(v)})
            except: pass
    return pd.DataFrame(rows)

@st.cache_data(show_spinner=False)
def ump_lengkap():
    """UMP 2002-2026 semua provinsi — pakai processed."""
    fp = _pp("ump_lengkap_clean.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df["UMP"]     = pd.to_numeric(df["UMP"],     errors="coerce")
        df["UMP_Juta"]= pd.to_numeric(df["UMP_Juta"],errors="coerce")
        return df
    # fallback manual
    h = pd.read_csv(_p("ump_df.csv"))
    h["prov"] = h["provinsi"].apply(_prov)
    fp26 = _p("ump_2026.csv")
    d26 = pd.read_csv(fp26, header=None, skiprows=2, names=["provinsi","ump"])
    d26 = d26[pd.to_numeric(d26["ump"],errors="coerce").notna()].copy()
    d26["ump"]   = pd.to_numeric(d26["ump"],errors="coerce")
    d26 = d26[d26["ump"]>1_000_000].copy()
    d26["tahun"] = 2026
    d26["prov"]  = d26["provinsi"].apply(_prov)
    out = pd.concat([h[["prov","tahun","ump"]], d26[["prov","tahun","ump"]]], ignore_index=True)
    out.columns = ["Provinsi","Tahun","UMP"]
    out["UMP_Juta"] = (out["UMP"]/1e6).round(2)
    return out

@st.cache_data(show_spinner=False)
def ump_pivot():
    """UMP pivot tahun × provinsi (Juta Rp) — pakai processed."""
    fp = _pp("ump_pivot_clean.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df = df.set_index("Tahun")
        return df.ffill()
    # fallback: pivot dari ump_lengkap
    df = ump_lengkap()
    pv = df.pivot_table(index="Tahun", columns="Provinsi", values="UMP_Juta")
    return pv.ffill()

@st.cache_data(show_spinner=False)
def tpt_2026():
    """TPT Februari 2026 per provinsi — pakai processed."""
    fp = _pp("tpt_clean.csv")
    if os.path.exists(fp):
        return pd.read_csv(fp)
    # fallback
    fp2 = _p("tpt_provinsi_2026.csv")
    df = pd.read_csv(fp2, header=None, skiprows=3,
                     names=["prov_raw","TPT_Feb2026","Agustus","Tahunan"])
    df["TPT_Feb2026"] = pd.to_numeric(df["TPT_Feb2026"], errors="coerce")
    df = df[df["TPT_Feb2026"].notna()].copy()
    df["Provinsi"] = df["prov_raw"].apply(_prov)
    return df

@st.cache_data(show_spinner=False)
def upah_aktual():
    """Upah aktual BPS — pakai processed."""
    fp = _pp("upah_aktual_clean.csv")
    if os.path.exists(fp):
        df = pd.read_csv(fp)
        df["Provinsi"] = df["Provinsi"].apply(_prov)
        return df
    # fallback
    df = pd.read_csv(_p("upah_df.csv"))
    df["upah_bulanan"] = df["upah"]*8*22
    df["Provinsi"] = df["provinsi"].apply(_prov)
    return df

@st.cache_data(show_spinner=False, ttl=3600)
def geojson():
    url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson"
    try:
        r = requests.get(url, timeout=15)
        if r.status_code==200: return r.json()
    except: pass
    return None

# ─── Tab 4: Profil Kandidat ──────────────────────────────────────

@st.cache_data(show_spinner=False)
def ner_stats():
    fp = _p("Entity_Recognition_in_Resumes.json")
    if not os.path.exists(fp): return {"per_resume":[],"skill_freq":{},"edu_levels":[],
                                        "exp_years":[],"cv_categories":[],"total":0}
    with open(fp) as f: data = json.load(f)
    per_resume, sf, df_dict, el, ey = [], {}, {}, [], []
    for item in data:
        txt = item["text"]; anns = item["annotations"]
        sk,ds,ed,ex,ct = [],[],[],[],[]
        for a in anns:
            if len(a)!=3: continue
            s,e,lb = a
            try: sp=txt[int(s):int(e)].strip()
            except: continue
            if not sp: continue
            if lb=="SKILL":
                sk.append(sp.lower()); sf[sp.lower()]=sf.get(sp.lower(),0)+1
            elif lb=="DESIGNATION":
                ds.append(sp.lower()); df_dict[sp.lower()]=df_dict.get(sp.lower(),0)+1
            elif lb=="EDUCATION":  ed.append(sp)
            elif lb=="EXPERIENCE": ex.append(sp); y=_parse_exp(sp); ey.append(y) if y else None
            elif lb=="CERTIFICATION": ct.append(sp.lower())
        el.append(_klasif_edu(ed))
        per_resume.append({"skill_count":len(sk),"skills":sk,"designations":ds,
                           "educations":ed,"experiences":ex,"certifications":ct})
    cv_cats = [_klasif_desig(r["designations"]) for r in per_resume]
    return {"per_resume":per_resume,"skill_freq":sf,"edu_levels":el,
            "exp_years":ey,"cv_categories":cv_cats,"total":len(per_resume)}

def _parse_exp(txt):
    t=str(txt).lower()
    m=re.search(r"(\d+\.?\d*)\s*month",t)
    if m: return float(m.group(1))/12
    m=re.search(r"(\d+\.?\d*)\s*(?:year|yr)",t)
    if m: return float(m.group(1))
    return None

def _klasif_edu(spans):
    t=" ".join(str(s) for s in spans).lower()
    if any(x in t for x in ["phd","ph.d","doctor","s3"]):            return "PhD / S3"
    if any(x in t for x in ["master","s2","m.sc","m.tech","mba","mca"]): return "S2 / Master"
    if any(x in t for x in ["bachelor","b.e","b.tech","b.sc","degree","s1","engineering"]): return "S1 / Sarjana"
    if any(x in t for x in ["diploma","d3","d4","polytechnic"]):     return "Diploma / D3"
    if any(x in t for x in ["high school","sma","12th","slta"]):     return "SMA / Sederajat"
    return "Lainnya"

def _klasif_desig(desig_list):
    t=" ".join(desig_list).lower()
    for kws,cat in KATEGORI_CV_RULES:
        if any(kw in t for kw in kws): return cat
    return "Lainnya"
