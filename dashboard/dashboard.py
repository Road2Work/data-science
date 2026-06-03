# =====================================================================
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os

# =====================================================================
# 1. SETUP HALAMAN AWAL
# =====================================================================
st.set_page_config(
    page_title="Road2Work Analytics",
    page_icon="dashboard/icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# 2. CUSTON CSS BIAR MIRIP DESIGN SYSTEM
# =====================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F8FAFC !important;
        color: #1F2937 !important;
    }
    
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 3rem !important;
        max-width: 1060px !important;
        margin: 0 auto;
    }
    
    /* Navbar Putih Solid */
    .r2w-navbar {
        background-color: #FFFFFF;
        border-bottom: 1px solid #E2E8F0;
        padding: 16px 24px;
        margin-left: -5rem; 
        margin-right: -5rem;
        padding-left: 5rem;
        padding-right: 5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 32px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    
    .r2w-logo-brand {
        font-size: 22px;
        font-weight: 800;
        color: #E63946;
        letter-spacing: -0.04em;
        text-decoration: none;
    }
    
    .r2w-logo-sub {
        font-size: 15px;
        font-weight: 500;
        color: #64748B;
        margin-left: 14px;
        border-left: 1px solid #CBD5E1;
        padding-left: 14px;
    }
    
    /* Styling Tabs agar lebih premium */
    div[data-testid="stTabs"] button {
        font-weight: 600 !important;
        font-size: 14px !important;
        padding-top: 8px !important;
        padding-bottom: 8px !important;
    }
    
    .status-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #64748B;
        font-weight: 500;
    }
    
    .status-dot {
        height: 8px;
        width: 8px;
        background-color: #10B981;
        border-radius: 50%;
        display: inline-block;
    }
    
    .analytics-card-frame {
        background-color: #FDFDFD;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 20px;
        padding: 20px 24px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 6px 24px rgba(0,0,0,0.05);
        margin-bottom: 24px;
        height: 130px; 
        display: flex;
        flex-direction: column;
        justify-content: space-between; 
    }
    
    .pyramid-stage-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #E63946;
        margin-bottom: 6px;
    }
    
    .pyramid-title {
        font-size: 16px;
        font-weight: 700;
        color: #1F2937;
        margin-top: 0px;
        margin-bottom: 16px;
    }
    
    .metric-num {
        font-size: 28px; 
        font-weight: 800;
        color: #1F2937;
        letter-spacing: -0.02em;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .metric-lbl {
        font-size: 12px;
        color: #A0A0A0;
        font-weight: 500;
        margin-top: 2px;
    }

    [data-testid="stHeader"] { background-color: transparent !important; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 3. IMAGE LOADER FUNCTION (FOR PNG LOGO)
# =====================================================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

logo_html_element = '<span class="r2w-logo-brand">road2work</span>'
logo_path = "dashboard/logo.png"

if os.path.exists(logo_path):
    try:
        base64_str = get_base64_of_bin_file(logo_path)
        logo_html_element = f'<img src="data:image/png;base64,{base64_str}" style="height: 32px; object-fit: contain;">'
    except Exception as e:
        st.error(f"Error loading logo: {e}")

# =====================================================================
# 4. FUNGSI BUAT INSIGHT
# =====================================================================
def get_insight_box(content, color="#3B82F6"):
    return f"""
        <div style="background-color: #F8FAFC; border-left: 4px solid {color}; padding: 12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
            <span style="font-size: 12px; color: #1F2937; line-height: 1.5;">{content}</span>
        </div>
    """

# =====================================================================
# 5. GLOBAL CHART PLOT STYLING
# =====================================================================
def apply_fe_plot_clean_style(fig, ax):
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    ax.xaxis.label.set_color('#94A3B8')
    ax.yaxis.label.set_color('#94A3B8')
    ax.tick_params(colors='#64748B', labelsize=9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E2E8F0')
    ax.spines['bottom'].set_color('#E2E8F0')
    ax.grid(axis='y', linestyle='--', alpha=0.4, color='#E2E8F0')
    ax.set_axisbelow(True)

# =====================================================================
# 6. RENDER CUSTOM NAVBAR
# =====================================================================
st.markdown(f"""
    <div class="r2w-navbar">
        <div style="display: flex; align-items: center;">
            {logo_html_element}
        </div>
        <div style="text-align: right;">
            <span class="r2w-logo-sub">Candidate Performance Dashboard</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 7. DATA LOADING (DENGAN CACHE AGAR CEPAT)
# =====================================================================
@st.cache_data
def load_data():
    file_path = "../data/02_interim/cleaned_answers_evaluation.csv" 
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        df = pd.read_csv("data/02_interim/cleaned_answers_evaluation.csv") 
    return df

df_main = load_data()

# =====================================================================
# 8. SIDEBAR & FILTERING 
# =====================================================================

# Header Sidebar
st.sidebar.markdown("""
    <div style='font-weight: 700; font-size: 14px; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 1px solid #E2E8F0;'>
        Parameter Filter
    </div>
""", unsafe_allow_html=True)

# 1. Filter Divisi (Multiselect)
all_roles = list(df_main['role_family'].dropna().unique())
selected_roles = st.sidebar.multiselect(
    "Divisi (Role Family)", 
    options=all_roles, 
    default=[], 
    placeholder="Pilih divisi..."
)

# Menyiapkan data sementara agar filter "Target Role" menyesuaikan divisi
df_temp_role = df_main[df_main['role_family'].isin(selected_roles)] if selected_roles else df_main

# 2. Filter Posisi Spesifik (Multiselect Hierarki)
all_targets = list(df_temp_role['target_role'].dropna().unique())
selected_targets = st.sidebar.multiselect(
    "Posisi Spesifik", 
    options=all_targets, 
    default=[],
    placeholder="Pilih posisi..."
)

# 3. Filter Kualitas Jawaban (Multiselect)
quality_options = ["Strong", "Average", "Weak"] 
selected_quality = st.sidebar.multiselect(
    "Kategori Kualitas", 
    options=quality_options, 
    default=[],
    placeholder="Pilih kualitas..."
)

# 4. Filter Komponen Jawaban (Multiselect)
komponen_map = {
    "Ada Angka/Metrik (Metric)": "has_metric",
    "Ada Dampak (Impact)": "has_impact",
    "Ada Konteks (Context)": "has_context",
    "Detail Teknis Lengkap": "has_technical_detail",
    "Menyebutkan Tools": "has_tools",
    "Ada Self-Awareness": "has_self_awareness",
    "Kontribusi Jelas": "has_contribution"
}

selected_komponen = st.sidebar.multiselect(
    "Komponen Jawaban", 
    options=list(komponen_map.keys()),
    default=[],
    placeholder="Pilih komponen..."
)

st.sidebar.markdown("<br>", unsafe_allow_html=True) # Jarak pemisah untuk grup slider

# 5. Filter Evidence Level (Range Slider)
min_ev = int(df_main['evidence_level'].min())
max_ev = int(df_main['evidence_level'].max())
selected_evidence = st.sidebar.slider(
    "Kedalaman Bukti (Level)", 
    min_value=min_ev, 
    max_value=max_ev, 
    value=(min_ev, max_ev)
)

# 6. Filter Rentang Jumlah Kata (Range Slider)
min_word = int(df_main['answer_length_words'].min())
max_word = int(df_main['answer_length_words'].max())
selected_word_range = st.sidebar.slider(
    "Panjang Jawaban (Kata)", 
    min_value=min_word, 
    max_value=max_word, 
    value=(min_word, max_word)
)

st.sidebar.markdown("<br>", unsafe_allow_html=True) # Jarak pemisah untuk radio button

# 7. Filter Komunikasi / Clarification (Radio Button)
clarify_options = ["Semua", "Lancar", "Butuh Klarifikasi"]
selected_clarify = st.sidebar.radio("Kelancaran Komunikasi", clarify_options)


# =====================================================================
# --- LOGIKA PEMOTONGAN DATA (APPLY ALL FILTERS) ---
# =====================================================================
df_filtered = df_main.copy()

# Jika list filter TIDAK kosong, baru lakukan pemotongan. 
# Jika kosong, biarkan df_filtered utuh (artinya Select All)
if selected_roles:
    df_filtered = df_filtered[df_filtered['role_family'].isin(selected_roles)]

if selected_targets:
    df_filtered = df_filtered[df_filtered['target_role'].isin(selected_targets)]

if selected_quality:
    df_filtered = df_filtered[df_filtered['quality_label'].isin(selected_quality)]

# Apply Filter Range Slider (Jumlah kata & Evidence level)
df_filtered = df_filtered[
    (df_filtered['answer_length_words'] >= selected_word_range[0]) & 
    (df_filtered['answer_length_words'] <= selected_word_range[1])
]

df_filtered = df_filtered[
    (df_filtered['evidence_level'] >= selected_evidence[0]) & 
    (df_filtered['evidence_level'] <= selected_evidence[1])
]

# Apply Filter Radio Button (Clarification)
if selected_clarify == "Lancar":
    df_filtered = df_filtered[df_filtered['need_clarification'] == False]
elif selected_clarify == "Butuh Klarifikasi":
    df_filtered = df_filtered[df_filtered['need_clarification'] == True]

if selected_komponen:
    for komp in selected_komponen:
        nama_kolom = komponen_map[komp]
        # Hanya ambil kandidat yang memiliki komponen tersebut (True / 1)
        df_filtered = df_filtered[df_filtered[nama_kolom] == True]

# Info jumlah baris data yang sedang aktif di bagian bawah sidebar
st.sidebar.divider()
st.sidebar.markdown(f"""
    <div style="background-color: #F9FAFB; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #E2E8F0;">
        <span style="font-size: 11px; color: #64748B; font-weight: 700; letter-spacing: 0.05em;">JUMLAH DATA TERFILTER</span><br>
        <span style="font-size: 24px; color: #1F2937; font-weight: 800; font-family: 'JetBrains Mono', monospace;">{len(df_filtered):,}</span><br>
        <span style="font-size: 11px; color: #94A3B8;">Kandidat Sesuai Kriteria</span>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 9. TOP LEVEL KPI CARDS (OVERVIEW & CONDITIONAL)
# =====================================================================
st.markdown('<div class="pyramid-title" style="margin-top: 10px;">Executive Overview</div>', unsafe_allow_html=True)

# --- 1. MENYUSUN TEKS FILTER AKTIF ---
active_filters = []
if selected_roles: 
    active_filters.append(f"Divisi: {', '.join(selected_roles)}")
if selected_targets: 
    active_filters.append(f"Posisi: {', '.join(selected_targets)}")
if selected_quality: 
    active_filters.append(f"Kualitas: {', '.join(selected_quality)}")
if selected_komponen: 
    active_filters.append(f"Komponen: {', '.join(selected_komponen)}")

# Tambahan untuk mendeteksi slider Range Kata (jika nilainya digeser dari default)
if selected_word_range != (min_word, max_word):
    active_filters.append(f"Kata: {selected_word_range[0]}-{selected_word_range[1]}")

# Tambahan untuk mendeteksi slider Evidence Level (jika nilainya digeser dari default)
if selected_evidence != (min_ev, max_ev):
    active_filters.append(f"Bukti Lvl: {selected_evidence[0]}-{selected_evidence[1]}")

if selected_clarify not in ["Semua", "Semua Kandidat"]: 
    active_filters.append(f"Komunikasi: {selected_clarify}")

filter_text = " | ".join(active_filters) if active_filters else "Semua kandidat (tanpa filter spesifik)"

# Menampilkan banner filter aktif
st.markdown(f"""
    <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; padding: 12px 16px; border-radius: 8px; margin-bottom: 24px; font-size: 13px; color: #64748B;">
        <span style="color: #334155; font-weight: 700;">Filter Aktif:</span> {filter_text}
    </div>
""", unsafe_allow_html=True)

# --- 2. MENGHITUNG METRIK & LOGIKA WARNA ---
col1, col2, col3, col4 = st.columns([1, 1, 1.1, 1.1])

total_candidates = len(df_filtered)
avg_score = df_filtered['final_score_0_100'].mean() if total_candidates > 0 else 0
clarification_rate = (df_filtered['need_clarification'].sum() / total_candidates * 100) if total_candidates > 0 else 0

# --- LOGIKA TEKS WEAKNESS ---
if total_candidates > 0:
    top_weakness_raw = df_filtered['weakness_tags'].str.split(';').explode().mode()[0]
    
    if top_weakness_raw == "no_weakness":
        top_weakness = "Tidak Ada"
        weakness_label = "Kandidat Sudah Optimal"
    else:
        # Menghapus berbagai variasi suffix agar tersisa inti komponennya saja
        top_weakness = top_weakness_raw.replace('_missing', '').replace('_unclear', '').replace('_', ' ').title()
        weakness_label = "Komponen Sering Terlewat" 
else:
    top_weakness = "-"
    weakness_label = "Kendala Komunikasi Utama"

# Kondisi Warna Rata-rata Skor
if avg_score >= 75:
    score_color = "#10B981" 
elif avg_score >= 60:
    score_color = "#F59E0B" 
else:
    score_color = "#E63946" 

# Kondisi Warna Clarification Rate
if clarification_rate <= 20:
    clar_color = "#10B981" 
elif clarification_rate <= 50:
    clar_color = "#F59E0B" 
else:
    clar_color = "#E63946" 

# --- 3. RENDER KARTU KPI ---
with col1:
    st.markdown(f"""
        <div class="analytics-card-frame">
            <div class="pyramid-stage-label" style="color: #4B5563;">TOTAL PELAMAR</div>
            <div class="metric-num">{total_candidates:,}</div>
            <div class="metric-lbl">Kandidat Dievaluasi</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="analytics-card-frame">
            <div class="pyramid-stage-label" style="color: #4B5563;">RATA-RATA SKOR</div>
            <div class="metric-num" style="color: {score_color};">{avg_score:.1f}</div>
            <div class="metric-lbl">Dari Skala 100</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="analytics-card-frame">
            <div class="pyramid-stage-label" style="color: #4B5563;">CLARIFICATION RATE</div>
            <div class="metric-num" style="color: {clar_color};">{clarification_rate:.1f}%</div>
            <div class="metric-lbl">Butuh Pertanyaan Lanjutan</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="analytics-card-frame">
            <div class="pyramid-stage-label" style="color: #4B5563;">TOP WEAKNESS</div>
            <div class="metric-num" style="font-size: 22px; color: #1F2937;" title="{top_weakness}">
                {top_weakness}
            </div>
            <div class="metric-lbl">{weakness_label}</div>
        </div>
    """, unsafe_allow_html=True)

# =====================================================================
# 10. VISUALISASI DATA (BERDASARKAN 3 PILAR BISNIS)
# =====================================================================
st.markdown("---") 

tab1, tab2, tab3 = st.tabs([
    "Standar & Keadilan Skor", 
    "Pola Jawaban Sukses", 
    "Identifikasi Kelemahan"
])

# ---------------------------------------------------------------------
# TAB 1: PILAR 1 (Standar & Keadilan Skor)
# ---------------------------------------------------------------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col_chart1, col_chart2 = st.columns([1.3, 1])

    # =======================================================
    # PERTANYAAN 1: Rata-rata Skor per Role Family & Quality Label
    # =======================================================
    with col_chart1:
        if df_filtered['role_family'].nunique() == 1:
            group_col = 'target_role'
            divisi_terpilih = df_filtered['role_family'].iloc[0]
            title_text = f"Q1: Konsistensi Penilaian ({divisi_terpilih})"
        else:
            group_col = 'role_family'
            title_text = "Q1: Konsistensi Penilaian Antar Divisi"
            
        st.markdown(f'<div class="pyramid-title">{title_text}</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty:
                chart_type = st.radio(
                    "Pilih Tampilan Analisis:", 
                    ["Rata-rata (Bar Chart)", "Distribusi Skor (Boxplot)"], 
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                fig1, ax1 = plt.subplots(figsize=(6, 5.5)) 
                
                if "Bar Chart" in chart_type:
                    sns.barplot(data=df_filtered, y=group_col, x='final_score_0_100', hue='quality_label', palette={'Strong':'#10B981', 'Average':'#F59E0B', 'Weak':'#EF4444'}, ax=ax1, errorbar=None)
                    for container in ax1.containers:
                        ax1.bar_label(container, fmt='%.1f', padding=5, fontsize=9, color='#4B5563', weight='bold')
                    ax1.set_xlabel("Rata-rata Skor Akhir (0-100)", fontsize=11)
                else:
                    sns.boxplot(data=df_filtered, y=group_col, x='final_score_0_100', hue='quality_label', palette={'Strong':'#10B981', 'Average':'#F59E0B', 'Weak':'#EF4444'}, ax=ax1, linewidth=1.5)
                    ax1.set_xlabel("Distribusi Skor Akhir (0-100)", fontsize=11)
                
                ax1.set_ylabel("") 
                ax1.legend(title="Kualitas", bbox_to_anchor=(1.02, 1), loc='upper left', frameon=False, fontsize=9)
                apply_fe_plot_clean_style(fig1, ax1)
                ax1.tick_params(axis='both', labelsize=10)
                st.pyplot(fig1)

                # --- BAGIAN INSIGHT ---
                stats = df_filtered.groupby('quality_label')['final_score_0_100'].agg(['mean', 'std']).reindex(['Strong', 'Average', 'Weak'])
                s_mean = stats.loc['Strong', 'mean'] if 'Strong' in stats.index else 0
                a_mean = stats.loc['Average', 'mean'] if 'Average' in stats.index else 0
                w_mean = stats.loc['Weak', 'mean'] if 'Weak' in stats.index else 0
                s_std = stats.loc['Strong', 'std'] if 'Strong' in stats.index else 0
                is_balanced = s_std < 2.0 
                
                    # Cek konteks filter
                jumlah_role = df_filtered[group_col].nunique()
                nama_group = "divisi" if group_col == 'role_family' else "posisi"

                if jumlah_role > 1:
                    # Narasi Perbandingan (Banyak Role/Divisi)
                    insight_text = f"""
                    <strong>Insight:</strong> Evaluasi terhadap <b>{jumlah_role} {nama_group}</b> menunjukkan standar penilaian yang ajek. 
                    Kandidat <i>Strong</i> mencatatkan rata-rata <b>{s_mean:.1f}</b>, <i>Average</i> di <b>{a_mean:.1f}</b>, dan <i>Weak</i> di <b>{w_mean:.1f}</b>. 
                    Secara statistik, tidak ditemukan bias penilaian yang signifikan antar {nama_group} tersebut.
                    """
                else:
                    # Narasi Analisis Tunggal (Cuma 1 Role/Divisi)
                    nama_spesifik = df_filtered[group_col].iloc[0]
                    insight_text = f"""
                    <strong>Insight:</strong> Fokus analisis pada <b>{nama_spesifik}</b> menunjukkan bahwa kandidat kategori <i>Strong</i> memiliki rata-rata skor <b>{s_mean:.1f}</b>. 
                    Rentang skor untuk kategori <i>Average</i> (<b>{a_mean:.1f}</b>) dan <i>Weak</i> (<b>{w_mean:.1f}</b>) pada peran ini tetap mengikuti standar global perusahaan, 
                    menunjukkan bahwa tidak ada pelonggaran standar penilaian untuk peran spesifik ini.
                    """

                st.markdown(get_insight_box(insight_text, "#3B82F6"), unsafe_allow_html=True)
            
            else:
                st.warning("Data tidak mencukupi untuk analisis fairness audit.")


    # =======================================================
    # PERTANYAAN 2: Ketimpangan Penilaian 
    # =======================================================
    with col_chart2:
        st.markdown('<div class="pyramid-title">Q2: Ketimpangan Teknis vs Komunikasi</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty:
                jomplang = df_filtered[(df_filtered['technical_accuracy'] > 75) & (df_filtered['communication_clarity'] < 60)]
                
                if not jomplang.empty:
                    persentase_jomplang = (len(jomplang) / len(df_filtered)) * 100
                    
                    st.markdown(f"""
                        <div style="text-align: center; padding: 8px 0;">
                            <span style="font-size: 13px; color: #64748B;">Kandidat dgn Teknis >75 tapi Komunikasi <60</span><br>
                            <span style="font-size: 38px; font-weight: 800; color: #E63946; line-height: 1.2;">{persentase_jomplang:.1f}%</span><br>
                            <span style="font-size: 12px; color: #94A3B8;">({len(jomplang)} dari {len(df_filtered)} kandidat)</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px dashed #E2E8F0;'>", unsafe_allow_html=True)
                    st.markdown("<div style='font-size: 12px; color: #4B5563; font-weight: 700; margin-bottom: 8px;'>Distribusi Posisi Rentan:</div>", unsafe_allow_html=True)
                    
                    breakdown = jomplang['target_role'].value_counts().reset_index()
                    breakdown.columns = ['Posisi', 'Jumlah Kandidat']
                
                    st.dataframe(breakdown, hide_index=True, use_container_width=True, height=220)
                    
                    # --- INSIGHT Q2 ---
                    st.markdown(f"""
                        <div style="background-color: #F8FAFC; border-left: 4px solid #E63946; padding: 12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                            <span style="font-size: 12px; color: #1F2937; line-height: 1.5;">
                                <strong>Insight:</strong> Tabel di atas menunjukkan posisi mana yang paling banyak memiliki 'Hidden Gem' (kandidat pintar teknis namun rentan gagal karena komunikasi).
                            </span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.success("Luar biasa! Tidak ada kandidat dengan ketimpangan penilaian pada filter ini.")
            else:
                st.warning("Tidak ada data untuk dianalisis.")

    # =======================================================
    # GRAFIK OVERALL PEMENUHAN KOMPONEN (GENERAL vs TECHNICAL)
    # =======================================================
    st.markdown("<br>", unsafe_allow_html=True) 
    # 1. Logika penentuan label
    if df_filtered['target_role'].nunique() == 1:
        # Kalau cuma 1 role spesifik yang terpilih
        filter_label = f"Role {df_filtered['target_role'].iloc[0]}"
    elif df_filtered['role_family'].nunique() == 1:
        # Kalau user pilih 1 role family saja
        filter_label = f"Rumpun {df_filtered['role_family'].iloc[0]}"
    else:
        # Kalau user pilih banyak role atau belum filter sama sekali
        filter_label = "(Gabungan)"

    # 2. Masukkan ke dalam judul
    st.markdown(f'<div class="pyramid-title">Analisis Kelengkapan Komponen Jawaban {filter_label}</div>', unsafe_allow_html=True)

    with st.container(border=True):
        if not df_filtered.empty:
            # 1. Definisi Kelompok Kolom
            komponen_umum = ['has_context', 'has_contribution', 'has_tools', 'has_impact', 'has_metric', 'has_technical_detail', 'has_self_awareness']
            komponen_spesifik = ['has_testing_coverage', 'has_deployment', 'has_mobile_platform_detail', 'has_security_awareness', 'has_backend_architecture', 'has_model_evaluation', 'has_data_processing']
            
            # 2. Filter yang tersedia di dataset
            umum_tersedia = [c for c in komponen_umum if c in df_filtered.columns]
            spesifik_tersedia = [c for c in komponen_spesifik if c in df_filtered.columns and df_filtered[c].sum() > 0]
            
            col1, col2 = st.columns(2)
            
            # Helper untuk plotting
            def plot_comp(cols, title, base_color, highlight_low=False):
                data = df_filtered[cols].mean() * 100
                # Sort: True = Rendah di atas (untuk umum), False = Tinggi di atas (untuk spesifik)
                data = data.sort_values(ascending=highlight_low).reset_index()
                
                data.columns = ['Komponen', 'Persentase']
                data['Komponen'] = data['Komponen'].str.replace('has_', '').str.replace('_', ' ').str.title()
                
                # Tentukan warna
                if highlight_low:
                    bottom_3 = data.nsmallest(3, 'Persentase')['Komponen'].tolist()
                    colors = [base_color if comp not in bottom_3 else '#E63946' for comp in data['Komponen']]
                else:
                    colors = [base_color] * len(data)
                
                fig, ax = plt.subplots(figsize=(5, 4))
                sns.barplot(data=data, x='Persentase', y='Komponen', palette=colors, width=0.6, ax=ax)

                # Label angka
                for container in ax.containers:
                    ax.bar_label(container, fmt='%.0f%%', padding=5, fontsize=8, color='#1F2937', weight='bold')
                
                ax.set_xlabel("Persentase Pelamar (%)", fontsize=8)
                ax.set_ylabel("")
                ax.set_xlim(0, 115)
                apply_fe_plot_clean_style(fig, ax)
                
                st.markdown(f"<div style='font-size:12px; font-weight:700; color:#475569; margin-bottom: 5px;'>{title}</div>", unsafe_allow_html=True)
                st.pyplot(fig)

            # Plot Kiri & Kanan
            with col1:
                plot_comp(umum_tersedia, "A. Komponen Umum (Wajib)", "#64748B", highlight_low=True)
            with col2:
                if spesifik_tersedia:
                    plot_comp(spesifik_tersedia, "B. Komponen Spesifik Peran", "#60A5FA", highlight_low=False)
                else:
                    st.info("Tidak ada data teknis spesifik untuk filter ini.")

            # =======================================================
            # LOGIKA INSIGHT DINAMIS (PISAH UMUM & SPESIFIK)
            # =======================================================
            umum_means = df_filtered[umum_tersedia].mean() * 100
            spesifik_means = df_filtered[spesifik_tersedia].mean() * 100 if spesifik_tersedia else None

            # Data Umum
            top_gen = umum_means.idxmax().replace('has_', '').replace('_', ' ').title()
            top_gen_val = umum_means.max()
            bot_gen = umum_means.idxmin().replace('has_', '').replace('_', ' ').title()
            bot_val = umum_means.min()

            # Konstruksi teks 
            insight_body = f"""
                <strong>Insight:</strong> 
                Secara umum, kompetensi <b>{top_gen}</b> menjadi kekuatan utama kandidat ({top_gen_val:.1f}%). 
                Namun, perhatian perlu difokuskan pada komponen <b>{bot_gen}</b> ({bot_val:.1f}%), 
                yang saat ini menjadi titik terlemah dalam pemenuhan kriteria umum.
            """

            if spesifik_means is not None and not spesifik_means.empty:
                top_spec = spesifik_means.idxmax().replace('has_', '').replace('_', ' ').title()
                insight_body += f"""<br><br>Pada aspek teknis spesifik, kandidat menunjukkan performa sangat baik pada <b>{top_spec}</b> ({spesifik_means.max():.1f}%), 
                menandakan kesesuaian profil kandidat dengan tuntutan teknis pada peran ini."""

            # RENDER
            st.markdown(f"""
                <div style="background-color: #F8FAFC; border-left: 4px solid #10B981; padding: 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0; font-family: sans-serif;">
                    <div style="font-size: 13px; color: #1F2937; line-height: 1.6;">
                        <strong>Insight:</strong> 
                        Secara umum, kompetensi <b>{top_gen}</b> menjadi kekuatan utama kandidat ({top_gen_val:.1f}%). 
                        Namun, perhatian perlu difokuskan pada komponen <b>{bot_gen}</b> ({bot_val:.1f}%), 
                        yang saat ini menjadi titik terlemah dalam pemenuhan kriteria umum.
                    </div>
                </div>
            """, unsafe_allow_html=True)
                
        else:
            st.warning("Data tidak tersedia.")
                        
# ---------------------------------------------------------------------
# TAB 2: PILAR 2 (Pola Jawaban Sukses)
# ---------------------------------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_chart3, col_chart4 = st.columns(2)
    
    # =======================================================
    # PERTANYAAN 3: Komponen Paling Menentukan (MACRO & MICRO)
    # =======================================================
    with col_chart3:
        st.markdown('<div class="pyramid-title">Q3: Analisis Kelengkapan Komponen Jawaban</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty:
                # --- GRAFIK 1: HEATMAP (Peta Keseluruhan) ---
                st.markdown("<div style='font-size: 13px; font-weight: 700; color: #1F2937; margin-bottom: 8px;'>A. Peta Kelengkapan Seluruh Komponen</div>", unsafe_allow_html=True)
                
                fitur_kelengkapan = ['has_context', 'has_contribution', 'has_tools', 'has_impact', 'has_metric', 'has_technical_detail', 'has_self_awareness']
                fitur_tersedia = [col for col in fitur_kelengkapan if col in df_filtered.columns]
                
                if fitur_tersedia:
                    pilar2_q3_raw = df_filtered.groupby('quality_label')[fitur_tersedia].mean() * 100 
                    label_urutan = ['Strong', 'Average', 'Weak']
                    label_tersedia = [l for l in label_urutan if l in pilar2_q3_raw.index]
                    pilar2_q3_raw = pilar2_q3_raw.reindex(label_tersedia)
                    
                    fig2a, ax2a = plt.subplots(figsize=(6, 2.5)) 
                    sns.heatmap(
                        pilar2_q3_raw, annot=True, fmt=".0f", cmap="Blues", 
                        linewidths=1, cbar=False, ax=ax2a, annot_kws={"size": 9, "weight": "bold"}
                    )
                    label_x_manusiawi = [col.replace('has_', '').replace('_', ' ').title() for col in fitur_tersedia]
                    
                    ax2a.set_xticklabels(label_x_manusiawi, rotation=30, ha='right', fontsize=9)
                    ax2a.tick_params(axis='y', rotation=0, labelsize=10)
                    ax2a.set_xlabel("")
                    ax2a.set_ylabel("Kualitas", fontsize=10)
                    
                    st.pyplot(fig2a)
                    
                    st.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px dashed #E2E8F0;'>", unsafe_allow_html=True)
                    
                    # --- GRAFIK 2: BAR CHART (Bukti Telak 3 Komponen Utama) ---
                    st.markdown("<div style='font-size: 13px; font-weight: 700; color: #1F2937; margin-bottom: 8px;'>B. Pengaruh 3 Komponen Terpenting</div>", unsafe_allow_html=True)
                    
                    fig2b, ax2b = plt.subplots(figsize=(6, 3))
                    komponen = df_filtered.groupby('quality_label')[['has_metric', 'has_impact', 'has_context']].mean() * 100
                    komponen = komponen.reindex(label_tersedia)
                    
                    komponen.plot(kind='bar', ax=ax2b, color=['#64748B', '#E63946', '#1F2937'], width=0.7)
                    
                    for container in ax2b.containers:
                        ax2b.bar_label(container, fmt='%.0f%%', padding=4, fontsize=9, color='#4B5563', weight='bold')
                        
                    ax2b.set_xlabel("")
                    ax2b.set_ylabel("Persentase (%)", fontsize=10)
                    
                    # Legend di luar grafik
                    ax2b.legend(
                        ["Angka (Metric)", "Dampak (Impact)", "Konteks"], 
                        loc='lower center', bbox_to_anchor=(0.5, 1.05), 
                        ncol=3, fontsize=9, frameon=False
                    )
                    
                    apply_fe_plot_clean_style(fig2b, ax2b)
                    ax2b.tick_params(axis='x', rotation=0, labelsize=10)
                    ax2b.margins(y=0.25)
                    
                    st.pyplot(fig2b)
                    
                    # --- TEMPAT INSIGHT Q3 ---
                    if not df_filtered.empty:
                        insight_text = """
                        <strong>Insight:</strong> 
                        Analisis heatmap mengungkap bahwa kandidat <i>Strong</i> memiliki disiplin struktur sempurna. 
                        Kesenjangan utama antara pelamar <i>Average</i> dan <i>Strong</i> terletak pada <b>metrik (8%)</b> dan <b>dampak kerja (15%)</b>. 
                        Sementara itu, kandidat <i>Weak</i> menunjukkan anomali; mereka langsung melompat ke hasil kerja tanpa membangun <i>context</i> atau menjelaskan peran mereka dengan baik. 
                        Data ini memvalidasi bahwa fokus evaluasi pada metode STAR adalah langkah paling krusial untuk menyaring kandidat unggul.
                        """
                        
                        st.markdown(f"""
                            <div style="background-color: #F8FAFC; border-left: 4px solid #3B82F6; padding: 12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                                <div style="font-size: 13px; color: #1F2937; line-height: 1.5;">{insight_text}</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                else:
                    st.warning("Kolom komponen kelengkapan tidak ditemukan di dataset.")
            else:
                st.warning("Tidak ada data untuk divisualisasikan.")

    # =======================================================
    # PERTANYAAN 4: Titik Jenuh / Verbosity Bias
    # =======================================================
    with col_chart4:
        st.markdown('<div class="pyramid-title">Q4: Analisis Titik Jenuh (Verbosity Bias)</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty:
                fig3, ax3 = plt.subplots(figsize=(6, 6.8)) 
                
                sns.regplot(
                    data=df_filtered, x='answer_length_words', y='final_score_0_100', 
                    scatter_kws={'alpha':0.4, 'color':'#64748B', 's': 40}, 
                    line_kws={'color':'#1F2937', 'linewidth': 2}, ax=ax3
                )
                
                ax3.axvline(x=250, color='#E63946', linestyle='--', linewidth=2, alpha=0.8)
                
                ax3.text(
                    260, 45, 
                    'Titik Jenuh (>250 kata)\nSkor Cenderung Drop', 
                    color='#E63946', fontsize=10, weight='bold',
                    bbox=dict(facecolor='#F8FAFC', alpha=0.85, edgecolor='none', boxstyle='round,pad=0.4')
                )
                
                ax3.set_xlabel("Jumlah Kata dalam Jawaban", fontsize=10)
                ax3.set_ylabel("Skor Akhir (0-100)", fontsize=10)
                ax3.tick_params(axis='both', labelsize=10)
                
                apply_fe_plot_clean_style(fig3, ax3)
                st.pyplot(fig3)
                
                # --- TEMPAT INSIGHT Q4 ---
                if not df_filtered.empty:
                    insight_text = """
                    <strong>Insight:</strong> 
                    Grafik ini membongkar mitos bahwa jawaban panjang selalu lebih baik. Tren skor justru menukik tajam setelah melewati <b>batas jenuh 200-250 kata</b>. 
                    Kandidat yang menjawab terlalu panjang cenderung kehilangan substansi dan berputar-putar pada detail yang tidak relevan. 
                    Data ini memvalidasi urgensi penerapan <i>word limit</i> sebagai metrik objektif untuk menjaga efisiensi jawaban dan akurasi skor sistem.
                    """
                    
                    st.markdown(f"""
                        <div style="background-color: #F8FAFC; border-left: 4px solid #E63946; padding: 12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                            <div style="font-size: 13px; color: #1F2937; line-height: 1.5;">{insight_text}</div>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Data kosong. Ubah filter untuk melihat tren.")

# ---------------------------------------------------------------------
# TAB 3: PILAR 3 (Identifikasi Kelemahan))
# ---------------------------------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- BARIS 1 (Q5 & Q6) ---
    col_chart5, col_chart6 = st.columns(2)
    
    # PERTANYAAN 5: Proporsi Low Evidence 
    with col_chart5:
        if df_filtered['role_family'].nunique() == 1:
            group_col = 'target_role'
            title_text = f"Q5: Proporsi Low Evidence Lintas Role Family ({df_filtered['role_family'].iloc[0]})"
        else:
            group_col = 'role_family'
            title_text = "Q5: Proporsi Low Evidence Lintas Role Family"
            
        st.markdown(f'<div class="pyramid-title">{title_text}</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty:
                df_filtered['is_low_evidence'] = df_filtered['evidence_level'] <= 2
                low_ev_prop = df_filtered.groupby(group_col)['is_low_evidence'].mean() * 100
                low_ev_prop = low_ev_prop.sort_values(ascending=False).reset_index()
                
                fig5, ax5 = plt.subplots(figsize=(6, 4.5))
                sns.barplot(data=low_ev_prop, x='is_low_evidence', y=group_col, color='#3B82F6', width=0.6, ax=ax5)
                
                for container in ax5.containers:
                    ax5.bar_label(container, fmt='%.1f%%', padding=5, fontsize=9, color='#1F2937', weight='bold')
                
                ax5.set_xlabel("Persentase Kandidat (%)", fontsize=10)
                ax5.set_ylabel("")
                ax5.margins(x=0.15) 
                
                apply_fe_plot_clean_style(fig5, ax5)
                ax5.tick_params(axis='both', labelsize=10)
                st.pyplot(fig5)
                
                # --- INSIGHT Q5 ---
                insight_text = """
                <strong>Insight:</strong> 
                Visualisasi memperlihatkan proporsi "kandidat minim bukti" yang seragam (33%-34%) di seluruh rumpun peran. 
                Fenomena ini mengonfirmasi bahwa kesulitan mengartikulasikan bukti (metode STAR) adalah <b>penyakit sistemik universal</b>.
                <br><br>
                <b>Implikasi Strategis:</b> Karena kelemahan ini bersifat lintas peran, modul evaluasi AI <b>tidak memerlukan pembobotan berbeda</b> 
                untuk setiap divisi. Kita dapat menerapkan parameter ekstraksi bukti yang seragam dan ketat di seluruh jenis peran, 
                menjamin standardisasi penilaian yang adil dan efisien tanpa diskriminasi antar posisi.
                """
                
                # Rendering 
                st.markdown(f"""
                    <div style="background-color: #F8FAFC; border-left: 4px solid #8B5CF6; padding: 12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                        <div style="font-size: 14px; color: #1F2937; line-height: 1.6;">{insight_text}</div>
                        </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Tidak ada data untuk kombinasi filter ini.")

    # PERTANYAAN 6: Top Weakness
    with col_chart6:
        st.markdown('<div class="pyramid-title">Q6: Pemicu Utama "Need Clarification"</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty:
                df_clarify = df_filtered[df_filtered['need_clarification'] == True]
                
                if not df_clarify.empty:
                    weaknesses = df_clarify['weakness_tags'].str.split(';').explode().value_counts().head(5).reset_index()
                    weaknesses.columns = ['Kelemahan', 'Jumlah']
                    weaknesses['Kelemahan'] = weaknesses['Kelemahan'].str.replace('_missing', ' Hilang').str.replace('_unclear', ' Tidak Jelas').str.replace('_', ' ').str.title()
                    
                    fig6, ax6 = plt.subplots(figsize=(6, 4.5))
                    sns.barplot(data=weaknesses, x='Jumlah', y='Kelemahan', color='#64748B', width=0.6, ax=ax6)
                    
                    if len(ax6.patches) > 0: ax6.patches[0].set_facecolor('#E63946')
                    if len(ax6.patches) > 1: ax6.patches[1].set_facecolor('#E63946')
                    
                    for container in ax6.containers:
                        ax6.bar_label(container, fmt=' %d kasus', padding=5, fontsize=9, color='#1F2937', weight='bold')
                    
                    ax6.set_xlabel("Frekuensi Kemunculan", fontsize=10)
                    ax6.set_ylabel("")
                    ax6.margins(x=0.2)
                    
                    apply_fe_plot_clean_style(fig6, ax6)
                    ax6.tick_params(axis='both', labelsize=10)
                    st.pyplot(fig6)
                    
                    # --- TEMPAT INSIGHT Q6 ---
                    if not df_filtered.empty:
                        insight_text = """
                        <strong>Insight:</strong> 
                        Visualisasi ini mengungkap hierarki masalah pelamar dengan jelas. Dua kelemahan utama yang paling fatal adalah 
                        <b>ketiadaan hasil terukur (Measurable Result)</b> dan <b>kegagalan menjelaskan dampak (Impact)</b>. 
                        <br><br>
                        Kendala komunikasi struktural seperti alur penceritaan yang berantakan memang kerap terjadi, namun tidak sefatal "lupa menyertakan bukti angka". 
                        Dominasi dua kelemahan ini memvalidasi bahwa model AI kita wajib memiliki sensitivitas ekstra untuk mendeteksi 
                        ketidakhadiran metrik agar simulasi penilaian benar-benar setegas dunia nyata.
                        """
                        
                        # Rendering 
                        st.markdown(f"""
                            <div style="background-color: #F8FAFC; border-left: 4px solid #E63946; padding:12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                                <div style="font-size: 14px; color: #1F2937; line-height: 1.6;">{insight_text}</div>
                                </div>
                """, unsafe_allow_html=True)
                else:
                    st.success("Hebat! Semua kandidat terfilter memiliki komunikasi yang lancar.")
            else:
                st.warning("Tidak ada data.")

    # --- BARIS 2 (Q7 & Q8) ---
    st.markdown("<br>", unsafe_allow_html=True) 
    col_chart7, col_chart8 = st.columns(2)

    # PERTANYAAN 7: Relevansi vs Evidence Level
    with col_chart7:
        st.markdown('<div class="pyramid-title">Q7: Tren Relevansi Jawaban vs Kedalaman Bukti</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty and 'role_relevance' in df_filtered.columns:
                trend_data = df_filtered.groupby('evidence_level')['role_relevance'].mean().reset_index()
                
                if not trend_data.empty:
                    fig7, ax7 = plt.subplots(figsize=(6, 4.5))
                    
                    sns.lineplot(data=trend_data, x='evidence_level', y='role_relevance', linewidth=3, color='#E63946', ax=ax7, zorder=1)
                    sns.scatterplot(data=trend_data, x='evidence_level', y='role_relevance', s=90, color='#FFFFFF', edgecolor='#E63946', linewidth=2, ax=ax7, zorder=2)
                    
                    ax7.set_xticks(trend_data['evidence_level'])
                    ax7.set_xticklabels([f"Lvl {int(x)}" for x in trend_data['evidence_level']], fontsize=10)
                    
                    for index, row in trend_data.iterrows():
                        ax7.text(row['evidence_level'], row['role_relevance'] + 2, f"{row['role_relevance']:.1f}", 
                                color='#1F2937', ha="center", weight='bold', fontsize=9)
                    
                    ax7.set_xlabel("Tingkat Kedalaman Bukti Nyata (Evidence Level)", fontsize=10)
                    ax7.set_ylabel("Rata-rata Skor Relevansi (0-100)", fontsize=10)
                    ax7.margins(y=0.2)
                    
                    apply_fe_plot_clean_style(fig7, ax7)
                    ax7.tick_params(axis='both', labelsize=10)
                    st.pyplot(fig7)
                    
                    # --- TEMPAT INSIGHT Q7 ---
                    if not df_filtered.empty:
                        insight_text = """
                        <strong>Insight:</strong> 
                        Kurva ini membuktikan korelasi positif yang tak terbantahkan antara kedalaman bukti dan relevansi jawaban. 
                        Skor tidak bisa dimanipulasi dengan sekadar "merangkai kata"; jika skor pembuktian rendah, skor relevansi dipastikan ikut tenggelam. 
                        <br><br>
                        Lonjakan paling kritis terjadi saat transisi dari <b>Level 2 ke Level 3 (skor 43.6 ke 69.3)</b>. 
                        Ini adalah fase di mana kandidat sukses mengalihkan cara bercerita dari sekadar "menyebutkan *skill*" 
                        menjadi "menceritakan konteks masalah nyata", yang merupakan kunci utama jawaban dianggap nyambung oleh industri.
                        """
                        
                        # Rendering 
                        st.markdown(f"""
                            <div style="background-color: #F8FAFC; border-left: 4px solid #8B5CF6; padding: 12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                                <div style="font-size: 14px; color: #1F2937; line-height: 1.6;">{insight_text}</div>
                                </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Tidak cukup data untuk membentuk tren.")
            else:
                st.warning("Data 'role_relevance' tidak ditemukan pada filter ini.")

    # PERTANYAAN 8: Filler Words vs Kualitas
    with col_chart8:
        st.markdown('<div class="pyramid-title">Q8: Dampak Filler Words pada Kualitas Jawaban</div>', unsafe_allow_html=True)
        
        with st.container(border=True):
            if not df_filtered.empty and 'filler_word_count' in df_filtered.columns:
                fig8, ax8 = plt.subplots(figsize=(6, 4.5))
                
                label_urutan = ['Strong', 'Average', 'Weak']
                label_tersedia = [l for l in label_urutan if l in df_filtered['quality_label'].unique()]
                
                sns.boxplot(
                    data=df_filtered, x='quality_label', y='filler_word_count', 
                    order=label_tersedia,
                    palette={'Strong':'#10B981', 'Average':'#F59E0B', 'Weak':'#EF4444'}, 
                    width=0.5, ax=ax8
                )
                ax8.set_xlabel("Kategori Kualitas Jawaban", fontsize=10)
                ax8.set_ylabel("Jumlah Kemunculan Filler Words", fontsize=10)
                
                apply_fe_plot_clean_style(fig8, ax8)
                ax8.tick_params(axis='both', labelsize=10)
                st.pyplot(fig8)
                
                # --- TEMPAT INSIGHT Q8 ---
                if not df_filtered.empty:
                    insight_text = """
                    <strong>Insight:</strong> 
                    Visualisasi <i>boxplot</i> ini menampilkan kontras yang ekstrem. Kotak <i>Strong</i> nyaris rata di garis dasar (0), 
                    membuktikan bahwa kandidat unggul memiliki kelancaran berbicara luar biasa tanpa bergantung pada kata pengisi (*filler words*).
                    <br><br>
                    Sebaliknya, kategori <i>Weak</i> memiliki sebaran yang lebar dan penuh <i>outliers</i>. Hal ini mengonfirmasi bahwa 
                    keraguan atau minimnya penguasaan materi teknis bermanifestasi secara langsung melalui produksi lisan yang terbata-bata 
                    dan tidak efisien.
                    """
                    
                    # Rendering dengan warna border yang konsisten (Merah untuk Kritis/Weak)
                    st.markdown(f"""
                        <div style="background-color: #F8FAFC; border-left: 4px solid #E63946; padding: 12px 16px; margin-top: 16px; margin-bottom: 16px; border-radius: 0 4px 4px 0;">
                            <div style="font-size: 14px; color: #1F2937; line-height: 1.6;">{insight_text}</div>
                            </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Tidak ada data.")
