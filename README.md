# 🚀 Road2Work.id — Data Science

Road2Work.id adalah platform kesiapan karir komprehensif yang dirancang untuk membantu *fresh graduate* dan pencari kerja mempersiapkan diri menghadapi wawancara kerja. Layanan backend ini bertindak sebagai *API gateway* utama dan pengelola logika bisnis, mengatur profil pengguna, sesi wawancara adaptif, analisis kecocokan peran (Role-Fit), dan analitik *dashboard* secara *real-time*.

## 🌟 Fitur Utama

* **End-to-End Data Pipeline:** Mengelola siklus data dari *gathering* dan *scraping* dataset relevan, melakukan *data wrangling*, hingga pembersihan dan validasi struktur data untuk memastikan kesiapan model.
* **Competency & Scoring Engine:** Mengimplementasikan logika evaluasi jawaban pelamar yang mengacu pada taksonomi kompetensi, rubrik penilaian, serta pemetaan *evidence ladder* untuk mendapatkan skor kecocokan yang terukur.
* **Feature Engineering & Insight Extraction:** Melakukan rekayasa fitur untuk meningkatkan informativitas data bagi model, serta mengekstrak komponen kunci seperti metrik (angka), konteks, dan dampak (*impact*) dari jawaban pelamar.
* **Interactive Analytics Dashboard:** Mengembangkan dasbor analitik berbasis Streamlit sebagai sarana visualisasi explanatory analysis. Akses dasbor di: [Road2Work.id Dashboard](https://road2work.streamlit.app/).
* **Model Readiness & Experimentation:** Menyiapkan infrastruktur data yang siap diproses oleh model, termasuk pembuatan *Data Dictionary* dan implementasi eksperimen A/B Testing menggunakan Python.
* **Technical Reporting:** Menyusun dokumentasi teknis komprehensif yang mencakup seluruh alur proyek, mulai dari *problem discovery* hingga hasil akhir proyek dalam format PDF.

## 📂 Struktur Folder & Data

```text
├── dashboard/
│   ├── dashboard.py                        # Skrip utama Streamlit
│   ├── icon.png                            # Favicon
│   └── logo.png                            # Logo navbar
├── data/
│   ├── 01_raw/
│   │   ├── answer_dataset.csv              # Data jawaban kandidat
│   │   ├── competency_map.json             # Pemetaan kompetensi target
│   │   ├── evaluations_dataset.csv         # Data penilaian jawaban
│   │   ├── evidence_ladder_mapping.json    # Definisi level Evidence Ladder
│   │   ├── question_seed.json              # Bank pertanyaan
│   │   ├── role_skill_matrix.csv           # Mapping Skill per Role
│   │   ├── role_skill_matrix.json          # Mapping Skill per Role
│   │   ├── role_tree_dropdown.csv          # Hierarki Domain → Role
│   │   ├── role_tree_dropdown.json         # Hierarki Domain → Role
│   │   ├── scoring_rubric.json             # Aturan bobot penilaian
│   │   ├── skill_taxonomy.json             # Standarisasi Skill
│   │   └── weakness_taxonomy.json          # Klasifikasi kelemahan
│   ├── 02_interim/
│   │   └── cleaned_answers_evaluation.csv  # Dataset hasil pembersihan pada notebook pengolahan data
│   └── 03_processed/
│       ├── test_df.csv                     # Dataset testing hasil olahan siap latih
│       ├── train_df.csv                    # Dataset pelatihan hasil olahan siap latih
│       └── val_df.csv                      # Dataset validasi hasil olahan siap latih
└── notebooks/
    └── notebook.ipynb                      # Notebook utama riset & EDA
```

### Struktur Utama
* `dashboard/`: Berisi kode sumber untuk *dashboard* analitik (Streamlit).
* `data/`: Penyimpanan data terstruktur.
* `notebooks/`: Area eksperimen, analisis eksploratif (EDA), dan pengembangan data untuk model.

### 1️⃣ Struktur Folder data/

#### 1.1. Isi folder`data/01_raw`
Berikut adalah daftar aset data yang digunakan, disusun berdasarkan urutan pengembangan dan ketergantungan antar-tabel:

| No | Nama File | Deskripsi |
| :--- | :--- | :--- |
| 1 | `role_tree_dropdown.csv/json` | Struktur cascading Domain → Role Family → Target Role. |
| 2 | `role_skill_matrix.csv/json` | Mapping target role ke *required skills*, *importance*, dan *weight*. |
| 3 | `skill_taxonomy.json` | *Canonical skill* dan alias untuk ekstraksi dari profil/jawaban. |
| 4 | `competency_map.json` | *Competency target* per *target role* sebagai *guardrail* AI. |
| 5 | `question_seed.json` | Seed pertanyaan *interview* per *role* dan kompetensi. |
| 6 | `weakness_taxonomy.json` | Daftar *weakness tags* dan *template clarification question*. |
| 7 | `scoring_rubric.json` | Bobot penilaian (*role relevance, STAR, evidence, technical accuracy, clarity, self-awareness*). |
| 8 | `evidence_ladder_mapping.json` | Definisi level *Evidence Ladder* 1-5. |
| 9 | `answer_dataset.csv` | Jawaban *user* dengan `sample_id` sebagai penghubung ke *seed* pertanyaan. |
| 10 | `evaluations_dataset.csv` | Penilaian (skor) dari jawaban yang diberikan pada `answer_dataset`. |

#### 1.2. Isi Folder `data/02_interim/`
Berisi data yang telah melewati proses *wrangling* dan *cleaning* awal.

| Nama File | Deskripsi |
| :--- | :--- |
| `cleaned_answers_evaluation.csv` | Hasil *merge* dari `answer_dataset.csv` dan `evaluations_dataset.csv` yang sudah melalui tahap cleaning data. |

#### 1.3. Isi Folder `data/03_processed/`
Berisi *split dataset* yang siap digunakan untuk melatih model AI. Data ini telah melalui tahap *feature engineering* dan pembagian porsi data.

| Nama File | Deskripsi |
| :--- | :--- |
| `train_df.csv` | *Training set* untuk proses pembelajaran model AI. |
| `val_df.csv` | *Validation set* untuk penyesuaian parameter dan evaluasi selama pelatihan. |
| `test_df.csv` | *Testing set* untuk pengujian performa akhir model sebelum diimplementasikan. |

### 2️⃣ Struktur Folder notebooks/
Area eksperimen, analisis, dan pengembangan model sebelum diimplementasikan ke dalam *pipeline* produksi.
* **`notebook.ipynb`**: *Notebook* utama untuk seluruh siklus hidup data:
    * **Data Wrangling:** *Gathering*, *Assessing*, dan *Cleaning* data.
    * **Exploratory Data Analysis (EDA):** Analisis statistik untuk mendapatkan *insight* bisnis.
    * **Feature Engineering:** Transformasi data menjadi fitur yang informatif bagi model.
    * **Visualization:** *Explanatory analysis* untuk menjawab pertanyaan bisnis.
    * **Data Splitting:** Pembagian dataset menjadi *train, val,* dan *test set*.
    * **A/B Testing:** Eksperimen statistik untuk memvalidasi efektivitas perubahan fitur/model.

### 3️⃣ Struktur Folder dashboard/
Berisi komponen utama untuk penyajian visualisasi analitik interaktif.
* **`dashboard.py`**: Skrip utama berbasis [Streamlit](https://streamlit.io/) yang memproses data hasil olahan menjadi dasbor analitik interaktif.
* **`icon.png`**: Aset visual yang digunakan sebagai *favicon* (ikon tab) pada *browser*.
* **`logo.png`**: Aset visual utama yang ditampilkan pada *navbar* dasbor sebagai elemen identitas *brand* Road2Work.

## 💻 Panduan Menjalankan Project (Getting Started)

Ikuti petunjuk di bawah ini untuk mengatur dan menjalankan layanan *Data Science* di komputer lokal Anda.

### Prasyarat (Prerequisites)

Pastikan Anda telah menginstal aplikasi berikut:
1. **Python** (v3.11 atau lebih baru)
2. **Git** untuk mengkloning repositori

### 1. Clone Repository

```bash
git clone https://github.com/Road2Work/data-science.git
cd data-science
```

### 2. Instalasi Dependencies

Instal semua *package* yang dibutuhkan menggunakan `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 3. Persiapan Data

Sebelum menjalankan dasbor, perlu dilakukan pemrosesan data mentah menjadi data yang siap dianalisis. Alur persiapan data dapat dijalankan melalui *notebook* utama:

1. Buka `notebooks/notebook.ipynb` menggunakan Jupyter Notebook atau VS Code.
2. Jalankan semua *cell* secara berurutan (*Run All*) untuk melakukan proses *data wrangling*, *cleaning*, dan *splitting* dataset.
3. Pastikan skrip telah berhasil membuat/memperbarui file-file di dalam folder `data/02_interim/` dan `data/03_processed/`.

### 5. Menjalankan Dashboard

Setelah data diproses melalui *notebook*, dasbor analitik dapat dijalankan untuk memvisualisasikan *insight* secara interaktif:

```bash
python -m streamlit run dashboard/dashboard.py
```

---
## 🤝 Kontribusi
Proyek ini masih terus dikembangkan. Jika Anda memiliki saran, masukan, atau ingin berkontribusi dalam perbaikan *pipeline* data maupun pengembangan fitur dasbor, jangan ragu untuk membuka *issue* atau melakukan *pull request*.

---
Dibuat dengan ❤️ untuk Road2Work.id
