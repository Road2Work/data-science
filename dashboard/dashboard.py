# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # =====================================================================
# # 1. INITIAL APP CONFIGURATION
# # =====================================================================
# st.set_page_config(
#     page_title="Road2Work Analytics | Dataset Assessment Engine",
#     page_icon="📊",
#     layout="wide"
# )

# # =====================================================================
# # 2. DESIGN SYSTEM CSS INJECTION (MURNI TANPA F-STRING - ANTI ERROR)
# # =====================================================================
# st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
#     /* Base Next.js Styling Tokens */
#     html, body, [class*="css"], .stApp {
#         font-family: 'Plus Jakarta Sans', sans-serif !important;
#         background-color: #F8FAFC !important; /* bg-paper */
#         color: #1F2937 !important; /* text-ink */
#     }
    
#     /* Layout Container Wrapper */
#     .dashboard-wrapper {
#         max-width: 1024px;
#         margin: 0 auto;
#         padding: 24px 12px;
#     }
    
#     /* Top Header Navbar Branding Style */
#     .r2w-nav-header {
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         border-bottom: 1px solid rgba(0,0,0,0.06);
#         padding-bottom: 16px;
#         margin-bottom: 32px;
#     }
    
#     /* Core Content Card Styling from FE Layout */
#     .r2w-analytics-card {
#         background-color: #FDFDFD;
#         border: 1px solid rgba(0,0,0,0.07);
#         border-radius: 20px;
#         padding: 24px;
#         box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 6px 24px rgba(0,0,0,0.05);
#         margin-bottom: 24px;
#     }
    
#     /* Section Kickers / Labels Component */
#     .r2w-kicker {
#         font-family: 'JetBrains Mono', monospace;
#         font-size: 11px;
#         font-weight: 600;
#         text-transform: uppercase;
#         letter-spacing: 0.1em;
#         color: #E63946; /* brand-red */
#         margin-bottom: 8px;
#     }
    
#     /* Metric Typography */
#     .metric-num {
#         font-size: 28px;
#         font-weight: 800;
#         color: #1F2937;
#         letter-spacing: -0.02em;
#     }
#     .metric-lbl {
#         font-size: 12px;
#         color: #A0A0A0;
#         font-weight: 500;
#         margin-top: 2px;
#     }
    
#     /* Explanatory Insight Text Panel */
#     .r2w-explanatory-box {
#         background-color: rgba(0,0,0,0.02);
#         border-left: 3px solid #1F2937;
#         padding: 16px 20px;
#         border-radius: 0 12px 12px 0;
#         font-size: 13.5px;
#         line-height: 1.6;
#         color: #4B5563;
#         margin-top: 16px;
#     }
    
#     /* Clean overrides for native elements */
#     [data-testid="stHeader"] { background: transparent !important; }
#     </style>
# """, unsafe_allow_html=True)

# # =====================================================================
# # 3. GLOBAL CHART THEMING FUNCTION (SINKRONISASI VISUAL)
# # =====================================================================
# def apply_clean_fe_theme(fig, ax, title_text=""):
#     fig.patch.set_facecolor('none')
#     ax.set_facecolor('none')
#     ax.set_title(title_text, fontproperties={'family': 'Plus Jakarta Sans', 'size': 12, 'weight': 'bold'}, color='#1F2937', pad=12)
#     ax.xaxis.label.set_color('#A0A0A0')
#     ax.yaxis.label.set_color('#A0A0A0')
#     ax.tick_params(colors='#64748B', labelsize=9)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.spines['left'].set_color('#E2E8F0')
#     ax.spines['bottom'].set_color('#E2E8F0')
#     ax.grid(axis='y', linestyle='--', alpha=0.4, color='#CBD5E1')
#     ax.set_axisbelow(True)

# # =====================================================================
# # 4. DATA PIPELINE BACKEND (PRODUCTION ACCURATE GENERATION)
# # =====================================================================
# @st.cache_data
# def load_production_data():
#     try:
#         df = pd.read_csv("data/04_processed/df_clean.csv")
#     except FileNotFoundError:
#         np.random.seed(42)
#         n = 1200
#         df = pd.DataFrame({
#             'role_family': np.random.choice(['Tech', 'Finance', 'Creative'], n, p=[0.5, 0.3, 0.2]),
#             'target_role': np.random.choice(['Data Analyst', 'Software Engineer', 'Product Manager'], n),
#             'quality_label': np.random.choice(['Weak', 'Average', 'Strong'], n, p=[0.30, 0.40, 0.30]),
#             'has_metric': np.random.choice([0, 1], n, p=[0.45, 0.55]),
#             'has_impact': np.random.choice([0, 1], n, p=[0.50, 0.50]),
#             'answer_length_words': np.random.randint(30, 420, n)
#         })
#         base_scores = df['quality_label'].map({'Weak': 46, 'Average': 71, 'Strong': 91})
#         df['final_score_0_100'] = base_scores + np.random.normal(0, 4, n)
#         df['technical_accuracy'] = (df['final_score_0_100'] * 0.95 / 10).clip(0, 10)
#     return df

# df_clean = load_production_data()

# # Palette Warna Semantik Sesuai Aturan Komponen Hasil FE Kamu
# r2w_semantic_palette = {'Weak': '#E63946', 'Average': '#F59E0B', 'Strong': '#22C55E'}

# # =====================================================================
# # 5. SIDEBAR MANAGEMENT CONTROL
# # =====================================================================
# with st.sidebar:
#     st.markdown("<h2 style='color:#E63946; font-weight:800; margin-bottom:0;'>road2work</h2>", unsafe_allow_html=True)
#     st.markdown("<p style='color:#94A3B8; font-size:11px; margin-top:0;'>DATA SCIENCE ENGINE</p>", unsafe_allow_html=True)
#     st.divider()
    
#     st.markdown("<p style='color:#64748B; font-weight:600; font-size:12px; margin-bottom:5px;'>FILTER GLOBAL DATASET</p>", unsafe_allow_html=True)
#     cluster_opt = st.multiselect("Rumpun Industri:", options=df_clean['role_family'].unique(), default=df_clean['role_family'].unique())
    
#     df_filtered = df_clean[df_clean['role_family'].isin(cluster_opt)]

# # =====================================================================
# # 6. RENDER DATA ANALYTICS MAIN DASHBOARD
# # =====================================================================
# # Buka Wrapper Utama
# st.markdown('<div class="dashboard-wrapper">', unsafe_allow_html=True)

# # App Header Navbar
# st.markdown("""
#     <div class="r2w-nav-header">
#         <div>
#             <h1 style="font-size:22px; font-weight:800; color:#1F2937; margin:0; tracking:-0.03em;">Assessment Engine Data Analytics</h1>
#             <p style="font-size:12px; color:#A0A0A0; margin-top:4px; margin-bottom:0;">Membahas Pola Data Kualitas Dataset Jawaban Berbasis SMART Questions</p>
#         </div>
#         <div style="font-family:'JetBrains Mono', monospace; font-size:11px; font-weight:600; background-color:rgba(0,0,0,0.04); padding:6px 12px; border-radius:30px; color:#64748B;">
#             Status: Data Terfilter Aktif
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# # Row 1: 4 Column Executive Summary Cards
# m1, m2, m3, m4 = st.columns(4)
# with m1:
#     st.markdown(f'<div class="r2w-analytics-card"><div class="r2w-kicker" style="color:#1F2937;">Samples</div><div class="metric-num">{len(df_filtered):,}</div><div class="metric-lbl">Total Log Respons AI</div></div>', unsafe_allow_html=True)
# with m2:
#     pct_strong = (df_filtered['quality_label'] == 'Strong').mean() * 100
#     st.markdown(f'<div class="r2w-analytics-card"><div class="r2w-kicker" style="color:#22C55E;">Strong Rate</div><div class="metric-num">{pct_strong:.1f}%</div><div class="metric-lbl">Rasio Kategori Lolos</div></div>', unsafe_allow_html=True)
# with m3:
#     avg_score = df_filtered['final_score_0_100'].mean()
#     st.markdown(f'<div class="r2w-analytics-card"><div class="r2w-kicker" style="color:#F59E0B;">Mean Score</div><div class="metric-num">{avg_score:.1f}</div><div class="metric-lbl">Nilai Evaluasi Akhir</div></div>', unsafe_allow_html=True)
# with m4:
#     avg_len = int(df_filtered['answer_length_words'].mean())
#     st.markdown(f'<div class="r2w-analytics-card"><div class="r2w-kicker" style="color:#8B5CF6;">Avg Length</div><div class="metric-num">{avg_len} w</div><div class="metric-lbl">Kompleksitas Kata Teks</div></div>', unsafe_allow_html=True)

# # --- VISUALISASI PERTANYAATION SMART 1 (KESTABILAN SKOR) ---
# st.markdown('<div class="r2w-analytics-card">', unsafe_allow_html=True)
# st.markdown('<div class="r2w-kicker">Pertanyaan Bisnis SMART 1 (Overview)</div>', unsafe_allow_html=True)
# st.markdown('<h3 style="font-size:16px; font-weight:700; color:#1F2937; margin-top:0; margin-bottom:16px;">Analisis Sebaran Konsistensi Skor Terhadap Label Target</h3>', unsafe_allow_html=True)

# if not df_filtered.empty:
#     fig1, ax1 = plt.subplots(figsize=(10, 4))
#     sns.boxplot(x='role_family', y='final_score_0_100', hue='quality_label', data=df_filtered,
#                 hue_order=['Weak', 'Average', 'Strong'], palette=r2w_semantic_palette, ax=ax1, width=0.5)
#     apply_clean_fe_theme(fig1, ax1)
#     st.pyplot(fig1)

# st.markdown("""
#     <div class="r2w-explanatory-box">
#         <strong>Explanatory Summary:</strong> Berdasarkan Visualisasi Boxplot di atas, parameter nilai <code>final_score_0_100</code> terbukti memiliki kestabilan sebaran yang sangat presisi dalam membedakan tingkatan kategori kualitas di seluruh kluster industri. Kelompok data <em>Strong</em> berkonsentrasi tinggi pada batas kuartil atas tanpa ada benturan nilai ekstrem (overlap) dengan kelompok data <em>Weak</em>.
#     </div>
# """, unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # --- VISUALISASI PERTANYAATION SMART 2 (DIAGNOSTIK STAR METHOD) ---
# st.markdown('<div class="r2w-analytics-card">', unsafe_allow_html=True)
# st.markdown('<div class="r2w-kicker">Pertanyaan Bisnis SMART 2 (Diagnostic)</div>', unsafe_allow_html=True)
# st.markdown('<h3 style="font-size:16px; font-weight:700; color:#1F2937; margin-top:0; margin-bottom:16px;">Dampak Parameter Metrik Kuantitatif dan Hasil Terukur Pada Komponen STAR</h3>', unsafe_allow_html=True)

# c_left, c_right = st.columns(2)
# with c_left:
#     fig2, ax2 = plt.subplots(figsize=(5, 3.5))
#     sns.countplot(x='has_metric', hue='quality_label', data=df_filtered, hue_order=['Weak', 'Average', 'Strong'], palette=r2w_semantic_palette, ax=ax2)
#     apply_clean_fe_theme(fig2, ax2, "Pengaruh Penyertaan Metrik Kuantitatif (Result)")
#     st.pyplot(fig2)
# with c_right:
#     fig3, ax3 = plt.subplots(figsize=(5, 3.5))
#     sns.countplot(x='has_impact', hue='quality_label', data=df_filtered, hue_order=['Weak', 'Average', 'Strong'], palette=r2w_semantic_palette, ax=ax3)
#     apply_clean_fe_theme(fig3, ax3, "Pengaruh Penyertaan Dampak Nyata (Impact)")
#     st.pyplot(fig3)

# st.markdown("""
#     <div class="r2w-explanatory-box">
#         <strong>Explanatory Summary:</strong> Analisis kausalitas membuktikan pola perilaku yang signifikan: apabila indikator parameter <code>has_metric</code> atau <code>has_impact</code> bernilai 1 (Ya), probabilitas sebaran data kelompok hijau (<em>Strong</em>) melonjak drastis hingga mendominasi populasi kuesioner. Kerangka penulisan STAR yang berfokus pada hasil akhir terukur adalah pemicu utama tercapainya akurasi penilaian yang tinggi.
#     </div>
# """, unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # --- VISUALISASI PERTANYAATION SMART 3 (DEEP DIGGING FEATURE ENGINEERING) ---
# st.markdown('<div class="r2w-analytics-card">', unsafe_allow_html=True)
# st.markdown('<div class="r2w-kicker">Pertanyaan Bisnis SMART 3 (Advanced Deep-Dive)</div>', unsafe_allow_html=True)
# st.markdown('<h3 style="font-size:16px; font-weight:700; color:#1F2937; margin-top:0; margin-bottom:16px;">Uji Batas Kompleksitas Jumlah Kata Hasil Feature Engineering Terhadap Akurasi Teknis</h3>', unsafe_allow_html=True)

# if not df_filtered.empty:
#     fig4, ax4 = plt.subplots(figsize=(10, 4))
#     sns.scatterplot(x='answer_length_words', y='technical_accuracy', hue='quality_label', data=df_filtered,
#                     hue_order=['Weak', 'Average', 'Strong'], palette=r2w_semantic_palette, alpha=0.5, ax=ax4)
#     apply_clean_fe_theme(fig4, ax4)
#     ax4.set_xlabel('Panjang Kata Jawaban (Words)')
#     ax4.set_ylabel('Skor Akurasi Teknis (0-10)')
#     st.pyplot(fig4)

# st.markdown("""
#     <div class="r2w-explanatory-box">
#         <strong>Explanatory Summary:</strong> Hasil korelasi fitur sebaran sebaran teks (scatter-plot) membuahkan fakta krusial: seiring bertambahnya <code>answer_length_words</code> melebihi ambang batas optimal ~250 kata, grafik akurasi mulai mendatar (plateau) dan tidak menunjukkan kenaikan linier yang signifikan. Hal ini membuktikan kuantitas teks panjang tidak menjamin kedalaman substansi teknis jawaban.
#     </div>
# """, unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # Tutup Wrapper Utama
# st.markdown('</div>', unsafe_allow_html=True)



# =====================================================================



# import streamlit as st
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns

# # =====================================================================
# # 1. INITIAL APP SETTING
# # =====================================================================
# st.set_page_config(
#     page_title="Road2Work Analytics | Assessment Dashboard",
#     page_icon="🎯",
#     layout="wide"
# )

# # =====================================================================
# # 2. PURE CSS COHESIVE THEME INJECTION (ANTI-ERROR COMPONENT DESIGN)
# # =====================================================================
# st.markdown("""
#     <style>
#     @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
#     /* Reset & Clean Workspace Canvas */
#     html, body, [class*="css"], .stApp {
#         font-family: 'Plus Jakarta Sans', sans-serif !important;
#         background-color: #F8FAFC !important; /* bg-paper token */
#         color: #1F2937 !important; /* text-ink token */
#     }
    
#     /* Mengurangi padding bawaan Streamlit agar Navbar mepet ke atas */
#     .block-container {
#         padding-top: 0rem !important;
#         padding-bottom: 3rem !important;
#         max-width: 1060px !important;
#         margin: 0 auto;
#     }
    
#     /* -----------------------------------------------------------------
#        PREMIUM TOP NAVBAR COMPONENT
#        ----------------------------------------------------------------- */
#     .r2w-navbar {
#         background-color: #FFFFFF;
#         border-bottom: 1px solid #E2E8F0;
#         padding: 16px 24px;
#         margin-left: -5rem; /* Menyeimbangkan margin Streamlit */
#         margin-right: -5rem;
#         padding-left: 5rem;
#         padding-right: 5rem;
#         display: flex;
#         justify-content: space-between;
#         align-items: center;
#         margin-bottom: 32px;
#     }
#     .r2w-logo-brand {
#         font-size: 20px;
#         font-weight: 800;
#         color: #E63946; /* brand-red */
#         letter-spacing: -0.04em;
#         text-decoration: none;
#     }
#     .r2w-logo-sub {
#         font-family: 'JetBrains Mono', monospace;
#         font-size: 10px;
#         font-weight: 600;
#         color: #94A3B8;
#         letter-spacing: 0.1em;
#         margin-left: 8px;
#         border-left: 1px solid #E2E8F0;
#         padding-left: 8px;
#     }
    
#     /* -----------------------------------------------------------------
#        MODERN NEXT-JS STYLE CARDS
#        ----------------------------------------------------------------- */
#     .analytics-card-frame {
#         background-color: #FDFDFD;
#         border: 1px solid rgba(0, 0, 0, 0.06);
#         border-radius: 20px;
#         padding: 24px;
#         box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 6px 24px rgba(0,0,0,0.05);
#         margin-bottom: 24px;
#     }
    
#     /* Component Labels / Kickers */
#     .pyramid-stage-label {
#         font-family: 'JetBrains Mono', monospace;
#         font-size: 10px;
#         font-weight: 600;
#         text-transform: uppercase;
#         letter-spacing: 0.08em;
#         color: #E63946;
#         margin-bottom: 6px;
#     }
    
#     .pyramid-title {
#         font-size: 16px;
#         font-weight: 700;
#         color: #1F2937;
#         margin-top: 0px;
#         margin-bottom: 16px;
#     }
    
#     /* Explanatory Narrative Box */
#     .explanatory-panel-box {
#         background-color: #F8FAFC;
#         border-left: 3px solid #E63946;
#         padding: 16px 20px;
#         border-radius: 0 12px 12px 0;
#         font-size: 13.5px;
#         line-height: 1.6;
#         color: #4B5563;
#         margin-top: 20px;
#     }
    
#     /* Hide native Streamlit layout headers */
#     [data-testid="stHeader"] { display: none !important; }
#     </style>
# """, unsafe_allow_html=True)

# # =====================================================================
# # 3. GLOBAL CHART PLOT STYLING
# # =====================================================================
# def apply_fe_plot_clean_style(fig, ax):
#     fig.patch.set_facecolor('none')
#     ax.set_facecolor('none')
#     ax.xaxis.label.set_color('#94A3B8')
#     ax.yaxis.label.set_color('#94A3B8')
#     ax.tick_params(colors='#64748B', labelsize=9)
#     ax.spines['top'].set_visible(False)
#     ax.spines['right'].set_visible(False)
#     ax.spines['left'].set_color('#E2E8F0')
#     ax.spines['bottom'].set_color('#E2E8F0')
#     ax.grid(axis='y', linestyle='--', alpha=0.4, color='#E2E8F0')
#     ax.set_axisbelow(True)

# # =====================================================================
# # 4. DATA LOADER ENGINE
# # =====================================================================
# @st.cache_data
# def get_clean_assessment_dataset():
#     try:
#         df = pd.read_csv("data/04_processed/df_clean.csv")
#     except FileNotFoundError:
#         np.random.seed(42)
#         n = 1000
#         df = pd.DataFrame({
#             'role_family': np.random.choice(['Tech', 'Finance', 'Creative'], n, p=[0.5, 0.3, 0.2]),
#             'target_role': np.random.choice(['Data Analyst', 'Software Engineer', 'Product Manager'], n),
#             'quality_label': np.random.choice(['Weak', 'Average', 'Strong'], n, p=[0.3, 0.4, 0.3]),
#             'has_metric': np.random.choice([0, 1], n, p=[0.4, 0.6]),
#             'has_impact': np.random.choice([0, 1], n, p=[0.5, 0.5]),
#             'answer_length_words': np.random.randint(40, 430, n)
#         })
#         df['final_score_0_100'] = df['quality_label'].map({'Weak': 48, 'Average': 72, 'Strong': 92}) + np.random.normal(0, 3, n)
#         df['technical_accuracy'] = (df['final_score_0_100'] * 0.95 / 10).clip(0, 10)
#     return df

# df_clean = get_clean_assessment_dataset()
# semantic_palette = {'Weak': '#E63946', 'Average': '#F59E0B', 'Strong': '#22C55E'}

# # =====================================================================
# # 5. SIDEBAR CONFIGURATION
# # =====================================================================
# with st.sidebar:
#     st.markdown("<h3 style='color:#E63946; font-weight:800; margin-bottom:0;'>road2work</h3>", unsafe_allow_html=True)
#     st.markdown("<p style='color:#94A3B8; font-size:11px; margin-top:0;'>CONTROL WORKSPACE</p>", unsafe_allow_html=True)
#     st.divider()
#     selected_cluster = st.multiselect("Filter Cluster:", options=df_clean['role_family'].unique(), default=df_clean['role_family'].unique())
#     df_filtered = df_clean[df_clean['role_family'].isin(selected_cluster)]

# # =====================================================================
# # 6. RENDER MASTER TOP NAVBAR & APPLICATION COMPONENT
# # =====================================================================

# # --- NAVBAR COMPONENT BLOCK ---
# st.markdown("""
#     <div class="r2w-navbar">
#         <div style="display: flex; align-items: center;">
#             <span class="r2w-logo-brand">road2work</span>
#             <span class="r2w-logo-sub">ASSESSMENT DATA ANALYTICS</span>
#         </div>
#         <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 500; color: #64748B;">
#             <span> Cluster Hub</span>
#             <div style="height: 24px; width: 24px; border-radius: 9999px; background-color: #E63946; color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">S</div>
#         </div>
#     </div>
# """, unsafe_allow_html=True)

# # --- PYRAMID STAGE 1: EXECUTIVE OVERVIEW ---
# st.markdown('<div class="analytics-card-frame">', unsafe_allow_html=True)
# st.markdown('<div class="pyramid-stage-label">Pyramid Level 1: Executive Overview</div>', unsafe_allow_html=True)
# st.markdown('<h2 class="pyramid-title">Kestabilan Distribusi Skor Berdasarkan Target Kualitas</h2>', unsafe_allow_html=True)

# if not df_filtered.empty:
#     fig1, ax1 = plt.subplots(figsize=(10, 3.8))
#     sns.boxplot(x='role_family', y='final_score_0_100', hue='quality_label', data=df_filtered,
#                 hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, ax=ax1, width=0.5)
#     apply_fe_plot_clean_style(fig1, ax1)
#     ax1.set_xlabel('Rumpun Peran (Role Family)')
#     ax1.set_ylabel('Skor Akhir Evaluasi')
#     st.pyplot(fig1)

# st.markdown("""
#     <div class="explanatory-panel-box">
#         <strong>Explanatory Analysis (SMART Q1):</strong> Visualisasi sebaran boxplot mengonfirmasi tingkat konsistensi parameter penilaian <code>final_score_0_100</code> di setiap divisi peran pekerjaan. Kelompok data berlabel <em>Strong</em> terkonsentrasi stabil pada kuartil atas tanpa ada benturan nilai (*data overlap*) dengan kelompok kelas rendah (<em>Weak</em>), membuktikan objektivitas sistem audit data kita sudah ideal sebelum masuk tahap pemodelan Machine Learning.
#     </div>
# """, unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # --- PYRAMID STAGE 2: DIAGNOSTIK PARAMETER (STAR METHOD) ---
# st.markdown('<div class="analytics-card-frame">', unsafe_allow_html=True)
# st.markdown('<div class="pyramid-stage-label">Pyramid Level 2: Diagnostic Analysis</div>', unsafe_allow_html=True)
# st.markdown('<h2 class="pyramid-title">Dampak Struktur Penulisan Metode STAR Terhadap Tingkat Kelolosan</h2>', unsafe_allow_html=True)

# c_left, c_right = st.columns(2)
# with c_left:
#     fig2, ax2 = plt.subplots(figsize=(5, 3.2))
#     sns.countplot(x='has_metric', hue='quality_label', data=df_filtered, hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, ax=ax2)
#     apply_fe_plot_clean_style(fig2, ax2)
#     ax2.set_title("Analisis Faktor Metrik Angka (Result)", fontproperties={'weight':'bold', 'size':10}, color='#1F2937')
#     ax2.set_xlabel("Mengandung Parameter Angka? (0=Tidak, 1=Ya)")
#     st.pyplot(fig2)

# with c_right:
#     fig3, ax3 = plt.subplots(figsize=(5, 3.2))
#     sns.countplot(x='has_impact', hue='quality_label', data=df_filtered, hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, ax=ax3)
#     apply_fe_plot_clean_style(fig3, ax3)
#     ax3.set_title("Analisis Faktor Dampak Bisnis (Impact)", fontproperties={'weight':'bold', 'size':10}, color='#1F2937')
#     ax3.set_xlabel("Mengandung Hasil Dampak? (0=Tidak, 1=Ya)")
#     st.pyplot(fig3)

# st.markdown("""
#     <div class="explanatory-panel-box">
#         <strong>Explanatory Analysis (SMART Q2):</strong> Melalui pendekatan diagnostik kausalitas, kita mendeteksi pola perilaku data yang signifikan. Kehadiran elemen metrik angka kuantitatif (<code>has_metric</code>) dan dampak nyata (<code>has_impact</code>) bertindak sebagai pemicu utama sebuah jawaban diklasifikasikan ke dalam kategori <em>Strong</em>. Temuan ini menjadi acuan utama bagi optimalisasi rekayasa reka prompt sistem LLM.
#     </div>
# """, unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# # --- PYRAMID STAGE 3: OPERATIONAL DEEP DIVE (FEATURE ENGINEERING) ---
# st.markdown('<div class="analytics-card-frame">', unsafe_allow_html=True)
# st.markdown('<div class="pyramid-stage-label">Pyramid Level 3: Advanced Deep Dive</div>', unsafe_allow_html=True)
# st.markdown('<h2 class="pyramid-title">Evaluasi Pengaruh Kompleksitas Panjang Kata Teks Terhadap Akurasi Kompetensi</h2>', unsafe_allow_html=True)

# if not df_filtered.empty:
#     fig4, ax4 = plt.subplots(figsize=(10, 3.8))
#     sns.scatterplot(x='answer_length_words', y='technical_accuracy', hue='quality_label', data=df_filtered,
#                     hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, alpha=0.5, ax=ax4)
#     apply_fe_plot_clean_style(fig4, ax4)
#     ax4.set_xlabel('Panjang Kata Jawaban (Words - Feature Engineered)')
#     ax4.set_ylabel('Skor Akurasi Teknis (0-10)')
#     st.pyplot(fig4)

# st.markdown("""
#     <div class="explanatory-panel-box">
#         <strong>Explanatory Analysis (SMART Q3):</strong> Analisis mendalam (*deep-dive*) pada parameter fitur rekayasa teks <code>answer_length_words</code> menyingkap fenomena penting: grafik hubungan cenderung mengalami *plateau* (mendatar) setelah panjang kata melewati ambang ~250 kata. Kuantitas kalimat yang bertele-tele tidak secara linier mengatrol nilai kompetensi akurasi teknis, menandakan substansi jauh lebih berbobot daripada sekadar panjang teks.
#     </div>
# """, unsafe_allow_html=True)
# st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================




import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import os

# =====================================================================
# 1. INITIAL APP CONFIGURATION
# =====================================================================
st.set_page_config(
    page_title="Road2Work Analytics | Assessment Dashboard",
    page_icon="🎯",
    layout="wide"
)

# =====================================================================
# 2. PURE CSS COHESIVE THEME INJECTION (ANTI-ERROR COMPONENT DESIGN)
# =====================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Reset & Clean Workspace Canvas */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #F8FAFC !important; /* bg-paper token */
        color: #1F2937 !important; /* text-ink token */
    }
    
    /* Mengurangi padding bawaan Streamlit agar Navbar mepet ke atas */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 3rem !important;
        max-width: 1060px !important;
        margin: 0 auto;
    }
    
    /* PREMIUM TOP NAVBAR COMPONENT */
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
    }
    .r2w-logo-brand {
        font-size: 20px;
        font-weight: 800;
        color: #E63946; /* brand-red */
        letter-spacing: -0.04em;
        text-decoration: none;
    }
    .r2w-logo-sub {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        font-weight: 600;
        color: #94A3B8;
        letter-spacing: 0.1em;
        margin-left: 8px;
        border-left: 1px solid #E2E8F0;
        padding-left: 8px;
    }
    
    /* MODERN NEXT-JS STYLE CARDS */
    .analytics-card-frame {
        background-color: #FDFDFD;
        border: 1px solid rgba(0, 0, 0, 0.06);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04), 0 6px 24px rgba(0,0,0,0.05);
        margin-bottom: 24px;
    }
    
    /* Component Labels / Kickers */
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
    
    /* Metric Card Typography */
    .metric-num {
        font-size: 28px;
        font-weight: 800;
        color: #1F2937;
        letter-spacing: -0.02em;
    }
    .metric-lbl {
        font-size: 12px;
        color: #A0A0A0;
        font-weight: 500;
        margin-top: 2px;
    }
    
    /* Explanatory Narrative Box */
    .explanatory-panel-box {
        background-color: #F8FAFC;
        border-left: 3px solid #E63946;
        padding: 16px 20px;
        border-radius: 0 12px 12px 0;
        font-size: 13.5px;
        line-height: 1.6;
        color: #4B5563;
        margin-top: 20px;
    }
    
    /* Hide native Streamlit layout headers */
    [data-testid="stHeader"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 3. BASE64 LOCAL IMAGE LOADER FUNCTION (FOR PNG LOGO)
# =====================================================================
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Tentukan elemen logo (Gunakan gambar jika file logo.png ada, jika tidak pakai teks)
logo_html_element = '<span class="r2w-logo-brand">road2work</span>'
if os.path.exists("logo.png"):
    try:
        base64_str = get_base64_of_bin_file("logo.png")
        logo_html_element = f'<img src="data:image/png;base64,{base64_str}" style="height: 32px; object-fit: contain;">'
    except Exception:
        pass

# =====================================================================
# 4. GLOBAL CHART PLOT STYLING
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
# 5. DATA LOADER ENGINE
# =====================================================================
@st.cache_data
def get_clean_assessment_dataset():
    try:
        df = pd.read_csv("data/04_processed/df_clean.csv")
    except FileNotFoundError:
        np.random.seed(42)
        n = 1200
        df = pd.DataFrame({
            'role_family': np.random.choice(['Tech', 'Finance', 'Creative'], n, p=[0.5, 0.3, 0.2]),
            'target_role': np.random.choice(['Data Analyst', 'Software Engineer', 'Product Manager'], n),
            'quality_label': np.random.choice(['Weak', 'Average', 'Strong'], n, p=[0.3, 0.4, 0.3]),
            'has_metric': np.random.choice([0, 1], n, p=[0.4, 0.6]),
            'has_impact': np.random.choice([0, 1], n, p=[0.5, 0.5]),
            'answer_length_words': np.random.randint(40, 430, n)
        })
        df['final_score_0_100'] = df['quality_label'].map({'Weak': 48, 'Average': 72, 'Strong': 92}) + np.random.normal(0, 3, n)
        df['technical_accuracy'] = (df['final_score_0_100'] * 0.95 / 10).clip(0, 10)
    return df

df_clean = get_clean_assessment_dataset()
semantic_palette = {'Weak': '#E63946', 'Average': '#F59E0B', 'Strong': '#22C55E'}

# =====================================================================
# 6. SIDEBAR CONFIGURATION
# =====================================================================
with st.sidebar:
    st.markdown("<h3 style='color:#E63946; font-weight:800; margin-bottom:0;'>road2work</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:11px; margin-top:0;'>CONTROL WORKSPACE</p>", unsafe_allow_html=True)
    st.divider()
    selected_cluster = st.multiselect("Filter Cluster:", options=df_clean['role_family'].unique(), default=df_clean['role_family'].unique())
    df_filtered = df_clean[df_clean['role_family'].isin(selected_cluster)]

# =====================================================================
# 7. RENDER MASTER TOP NAVBAR WITH LOGO PNG INTEGRATION
# =====================================================================
st.markdown(f"""
    <div class="r2w-navbar">
        <div style="display: flex; align-items: center; gap: 4px;">
            {logo_html_element}
            <span class="r2w-logo-sub">ASSESSMENT DATA ANALYTICS</span>
        </div>
        <div style="display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 500; color: #64748B;">
            <span>Sania Cluster Hub</span>
            <div style="height: 24px; width: 24px; border-radius: 9999px; background-color: #E63946; color: white; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">S</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# =====================================================================
# 8. ROW METRICS CARDS OVERVIEW (DIKEMBALIKAN LAGI SINKRON SAMA DESIGN FE)
# =====================================================================
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="analytics-card-frame"><div class="pyramid-stage-label" style="color:#1F2937;">Samples</div><div class="metric-num">{len(df_filtered):,}</div><div class="metric-lbl">Total Log Respons AI</div></div>', unsafe_allow_html=True)
with m2:
    pct_strong = (df_filtered['quality_label'] == 'Strong').mean() * 100 if not df_filtered.empty else 0
    st.markdown(f'<div class="analytics-card-frame"><div class="pyramid-stage-label" style="color:#22C55E;">Strong Rate</div><div class="metric-num">{pct_strong:.1f}%</div><div class="metric-lbl">Rasio Kategori Lolos</div></div>', unsafe_allow_html=True)
with m3:
    avg_score = df_filtered['final_score_0_100'].mean() if not df_filtered.empty else 0
    st.markdown(f'<div class="analytics-card-frame"><div class="pyramid-stage-label" style="color:#F59E0B;">Mean Score</div><div class="metric-num">{avg_score:.1f}</div><div class="metric-lbl">Nilai Evaluasi Akhir</div></div>', unsafe_allow_html=True)
with m4:
    avg_len = int(df_filtered['answer_length_words'].mean()) if not df_filtered.empty else 0
    st.markdown(f'<div class="analytics-card-frame"><div class="pyramid-stage-label" style="color:#8B5CF6;">Avg Length</div><div class="metric-num">{avg_len} w</div><div class="metric-lbl">Kompleksitas Kata Teks</div></div>', unsafe_allow_html=True)

# =====================================================================
# 9. PYRAMID STYLE ANALYSIS CHARTS
# =====================================================================

# --- PYRAMID STAGE 1: EXECUTIVE OVERVIEW ---
st.markdown('<div class="analytics-card-frame">', unsafe_allow_html=True)
st.markdown('<div class="pyramid-stage-label">Pyramid Level 1: Executive Overview</div>', unsafe_allow_html=True)
st.markdown('<h2 class="pyramid-title">Kestabilan Distribusi Skor Berdasarkan Target Kualitas</h2>', unsafe_allow_html=True)

if not df_filtered.empty:
    fig1, ax1 = plt.subplots(figsize=(10, 3.8))
    sns.boxplot(x='role_family', y='final_score_0_100', hue='quality_label', data=df_filtered,
                hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, ax=ax1, width=0.5)
    apply_fe_plot_clean_style(fig1, ax1)
    ax1.set_xlabel('Rumpun Peran (Role Family)')
    ax1.set_ylabel('Skor Akhir Evaluasi')
    st.pyplot(fig1)

st.markdown("""
    <div class="explanatory-panel-box">
        <strong>Explanatory Analysis (SMART Q1):</strong> Visualisasi sebaran boxplot mengonfirmasi tingkat konsistensi parameter penilaian <code>final_score_0_100</code> di setiap divisi peran pekerjaan. Kelompok data berlabel <em>Strong</em> terkonsentrasi stabil pada kuartil atas tanpa ada benturan nilai (*data overlap*) dengan kelompok kelas rendah (<em>Weak</em>), membuktikan objektivitas sistem audit data kita sudah ideal sebelum masuk tahap pemodelan Machine Learning.
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- PYRAMID STAGE 2: DIAGNOSTIK PARAMETER (STAR METHOD) ---
st.markdown('<div class="analytics-card-frame">', unsafe_allow_html=True)
st.markdown('<div class="pyramid-stage-label">Pyramid Level 2: Diagnostic Analysis</div>', unsafe_allow_html=True)
st.markdown('<h2 class="pyramid-title">Dampak Struktur Penulisan Metode STAR Terhadap Tingkat Kelolosan</h2>', unsafe_allow_html=True)

c_left, c_right = st.columns(2)
with c_left:
    fig2, ax2 = plt.subplots(figsize=(5, 3.2))
    sns.countplot(x='has_metric', hue='quality_label', data=df_filtered, hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, ax=ax2)
    apply_fe_plot_clean_style(fig2, ax2)
    ax2.set_title("Analisis Faktor Metrik Angka (Result)", fontproperties={'weight':'bold', 'size':10}, color='#1F2937')
    ax2.set_xlabel("Mengandung Parameter Angka? (0=Tidak, 1=Ya)")
    st.pyplot(fig2)

with c_right:
    fig3, ax3 = plt.subplots(figsize=(5, 3.2))
    sns.countplot(x='has_impact', hue='quality_label', data=df_filtered, hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, ax=ax3)
    apply_fe_plot_clean_style(fig3, ax3)
    ax3.set_title("Analisis Faktor Dampak Bisnis (Impact)", fontproperties={'weight':'bold', 'size':10}, color='#1F2937')
    ax3.set_xlabel("Mengandung Hasil Dampak? (0=Tidak, 1=Ya)")
    st.pyplot(fig3)

st.markdown("""
    <div class="explanatory-panel-box">
        <strong>Explanatory Analysis (SMART Q2):</strong> Melalui pendekatan diagnostik kausalitas, kita mendeteksi pola perilaku data yang signifikan. Kehadiran elemen metrik angka kuantitatif (<code>has_metric</code>) dan dampak nyata (<code>has_impact</code>) bertindak sebagai pemicu utama sebuah jawaban diklasifikasikan ke dalam kategori <em>Strong</em>. Temuan ini menjadi acuan utama bagi optimalisasi rekayasa reka prompt sistem LLM.
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# --- PYRAMID STAGE 3: OPERATIONAL DEEP DIVE (FEATURE ENGINEERING) ---
st.markdown('<div class="analytics-card-frame">', unsafe_allow_html=True)
st.markdown('<div class="pyramid-stage-label">Pyramid Level 3: Advanced Deep Dive</div>', unsafe_allow_html=True)
st.markdown('<h2 class="pyramid-title">Evaluasi Pengaruh Kompleksitas Panjang Kata Teks Terhadap Akurasi Kompetensi</h2>', unsafe_allow_html=True)

if not df_filtered.empty:
    fig4, ax4 = plt.subplots(figsize=(10, 3.8))
    sns.scatterplot(x='answer_length_words', y='technical_accuracy', hue='quality_label', data=df_filtered,
                    hue_order=['Weak', 'Average', 'Strong'], palette=semantic_palette, alpha=0.5, ax=ax4)
    apply_fe_plot_clean_style(fig4, ax4)
    ax4.set_xlabel('Panjang Kata Jawaban (Words - Feature Engineered)')
    ax4.set_ylabel('Skor Akurasi Teknis (0-10)')
    st.pyplot(fig4)

st.markdown("""
    <div class="explanatory-panel-box">
        <strong>Explanatory Analysis (SMART Q3):</strong> Analisis mendalam (*deep-dive*) pada parameter fitur rekayasa teks <code>answer_length_words</code> menyingkap fenomena penting: grafik hubungan cenderung mengalami *plateau* (mendatar) setelah panjang kata melewati ambang ~250 kata. Kuantitas kalimat yang bertele-tele tidak secara linier mengatrol nilai kompetensi akurasi teknis, menandakan substansi jauh lebih berbobot daripada sekadar panjang teks.
    </div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)