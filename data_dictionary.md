# 📚 Data Dictionary — Road2Work.id

Dokumen ini menjelaskan struktur data, skema kolom, dan keterkaitan antartabel yang digunakan dalam sistem Road2Work.id.

## 📂 Struktur Data (Tree View)

```text
data/
├── 01_raw/
│   ├── answer_dataset.csv               # Data jawaban kandidat
│   ├── competency_map.json              # Data jawaban kandidat
│   ├── evaluations_dataset.csv          # Data penilaian jawaban
│   ├── evidence_ladder_mapping.json     # Data penilaian jawaban
│   ├── question_seed.json               # Bank pertanyaan
│   ├── role_skill_matrix.csv            # Mapping Skill per Role
│   ├── role_skill_matrix.json           
│   ├── role_tree_dropdown.csv           # Hierarki Domain → Role
│   ├── role_tree_dropdown.json          # Hierarki Domain → Role
│   ├── scoring_rubric.json              # Aturan bobot penilaian
│   ├── skill_taxonomy.json              # Standarisasi Skill
│   ├── weakness_taxonomy.json           # Klasifikasi kelemahan
└── 02_interim/
    └── cleaned_answers_evaluation.csv   # Dataset hasil pembersihan pada notebook pengolahan data
└── 03_processed/
    └── test_df.csv                      # Dataset testing hasil olahan siap latih
    └── train_df.csv                     # Dataset pelatihan hasil olahan siap latih
    └── val_df.csv                       # Dataset validasi hasil olahan siap latih
```

## 🔗 Keterkaitan Antartabel
Dataset ini merupakan kumpulan *master data* dan *synthetic dataset* yang disusun sebagai fondasi pengembangan kecerdasan sistem Road2Work.id, yang terdiri dari:

* **Struktur Domain & Role:** `role_tree_dropdown` (Cascading menu Domain hingga Target Role) dan `role_skill_matrix` (Pemetaan *skill* dan bobot per *role*).
* **Taksonomi & Pemetaan:** `skill_taxonomy` (Standardisasi *skill*), `competency_map` (Target kompetensi per *role*), dan `weakness_taxonomy` (Klasifikasi kelemahan kandidat).
* **Logika Evaluasi & Rubrik:** `scoring_rubric` (Aturan bobot penilaian) dan `evidence_ladder_mapping` (Definisi level kedalaman bukti/STAR).
* **Konten & Data Wawancara:** `question_seed` (Bank pertanyaan), `answer_dataset` (Jawaban kandidat *dummy*), serta `evaluations_dataset` (Skor penilaian hasil simulasi).

## 🔗 Alur Pengolahan Data
Sistem ini menggunakan alur *pipeline* data terstruktur untuk memastikan dataset siap digunakan oleh modul AI:

1. **`data/01_raw/` (Master Data & Referensi)**
   Berisi data dasar (*source of truth*) mengenai struktur role, taksonomi skill, dan rubrik penilaian yang menjadi fondasi sistem.

2. **`data/02_interim/` (Data Pengayaan)**
   Hasil penggabungan dan pembersihan data dari *raw data*. Di sini, kita melakukan *feature engineering* untuk memperkaya informasi jawaban kandidat agar lebih siap untuk dianalisis model.

3. **`data/03_processed/` (Model Ready Data)**
   Dataset final yang sudah dibagi menjadi *train*, *val*, dan *test set*. Data di folder ini merupakan *input* utama bagi tim AI untuk proses pelatihan dan validasi model.

## 🛠 Tabel Data Dictionary

### Kategori 1: Master Data & Referensi (Induk)

#### `A. role_tree_dropdown.csv` & `role_tree_dropdown.json`
Tabel ini berfungsi sebagai *source of truth* untuk navigasi sistem, mendefinisikan hubungan hierarki dari domain makro hingga spesialisasi target role.

| Column | Description |
| :--- | :--- |
| `domain_id` | Identitas unik untuk Domain utama (e.g., `domain_information_technology`). |
| `domain_name` | Nama domain (e.g., Information & Technology). |
| `role_family_id` | Identitas unik untuk pengelompokan role (*Role Family*). |
| `role_family_name` | Nama kelompok role (e.g., Data & AI, Web Development). |
| `target_role_id` | Identitas unik untuk spesialisasi role yang dituju. |
| `target_role_name` | Nama role spesifik (e.g., Data Scientist, DevOps Engineer). |
| `competency_focus` | Ringkasan fokus kompetensi utama yang menjadi acuan penilaian dasar. |

#### B. role_tree_dropdown.csv` & `role_tree_dropdown.json`
Tabel ini mendefinisikan standar kompetensi teknis yang diharapkan untuk setiap spesialisasi *role*. Data ini menjadi fondasi bagi sistem dalam melakukan *role-fit analysis* dan menentukan ambang batas kelulusan (*guardrails*) untuk kandidat.

| Column | Description |
| :--- | :--- |
| `domain` | Domain utama (e.g., Information & Technology). |
| `role_family` | Kategori besar *role* (e.g., Data & AI, Web Development). |
| `target_role` | Nama spesifik *target role* (merujuk ke `target_role_name`). |
| `skill` | *Canonical skill* atau nama teknologi/metodologi yang diuji. |
| `importance` | Tingkat kepentingan (*high, medium, low*) untuk menentukan prioritas pertanyaan. |
| `weight` | Bobot numerik (0.0 - 1.0) yang digunakan sebagai variabel penentu skor akhir *role-fit*. |

**Catatan Implementasi:**
- Data ini digunakan untuk membangun *cascading dropdown* pada antarmuka pengguna, memastikan user memilih *role* yang valid sesuai dengan *domain* dan *family* yang tersedia.
- `competency_focus` bertindak sebagai *metadata* awal yang digunakan sistem untuk memfilter pertanyaan yang relevan di modul `question_seed`.

#### `C. skill_taxonomy.json`
File ini berfungsi sebagai mesin normalisasi untuk menyamakan berbagai variasi istilah teknis yang digunakan kandidat ke dalam satu nama standar (*canonical skill*). Sistem menggunakan pemetaan ini untuk melakukan ekstraksi entitas secara otomatis dari CV, profil, maupun jawaban interview.

| Column / Key | Description |
| :--- | :--- |
| `Domain Category` | Kategori domain utama (e.g., Data & AI, Web Development). |
| `Canonical Skill` | Nama standar yang digunakan dalam sistem sebagai *primary key* evaluasi. |
| `Aliases` | Daftar istilah/teknologi terkait yang dipetakan ke *canonical skill* yang sama. |

**Catatan Implementasi:**
- **Fungsi Normalisasi:** Ketika kandidat menyebutkan "k8s" dalam jawaban mereka, sistem akan otomatis mengenalinya sebagai `Kubernetes` dalam konteks `MLOps` atau `DevOps`.
- **Ekstraksi Data:** File ini digunakan oleh *Natural Language Processing (NLP) pipeline* untuk mengidentifikasi keberadaan *skill* tanpa harus mencocokkan teks secara kaku (*exact match*).
- **Skalabilitas:** Struktur ini memudahkan penambahan alias baru tanpa mengubah logika evaluasi inti, sehingga sistem dapat terus beradaptasi dengan perkembangan teknologi baru.

#### `D. competency_map.json`
Tabel ini berisi definisi kompetensi teknis per *target role* yang digunakan sebagai *ground truth* atau *guardrail* dalam proses *AI question generation* dan evaluasi jawaban. Dokumen ini memastikan bahwa setiap pertanyaan yang dihasilkan AI memiliki target kompetensi yang terukur dan selaras dengan standar industri (SFIA v9).

| Column / Key | Description |
| :--- | :--- |
| `competency_id` | Identitas unik untuk setiap modul kompetensi. |
| `competency` | Nama kompetensi yang diuji. |
| `sfia_v9_reference` | Referensi standar industri (SFIA v9) untuk kalibrasi level keahlian (Level 3-4). |
| `description` | Deskripsi kualitatif mengenai tanggung jawab kompetensi tersebut. |
| `weight` | Bobot nilai dalam perhitungan skor akhir untuk *role* terkait. |
| `related_skills` | *Skill* teknis yang relevan dan menjadi prasyarat untuk kompetensi ini. |
| `expected_signals` | Daftar *key indicators* atau "sinyal" yang diharapkan muncul dalam jawaban kandidat untuk dianggap kompeten. |

**Catatan Implementasi:**
- **AI Question Generation:** Saat sistem membangkitkan pertanyaan interview, AI menggunakan `expected_signals` sebagai panduan untuk merumuskan pertanyaan yang menuntut kandidat untuk memberikan bukti nyata (*STAR method*).
- **Penilaian (Scoring):** Modul evaluasi menggunakan `weight` dan `expected_signals` sebagai rubrik perbandingan untuk memverifikasi apakah jawaban kandidat mengandung substansi yang diharapkan.
- **Guardrail:** Keberadaan `sfia_v9_reference` memastikan bahwa tingkat kesulitan pertanyaan yang dihasilkan oleh AI tetap konsisten dengan ekspektasi profesional di level yang ditentukan (misalnya, *Intermediate/Level 3*).

#### `E. question_seed.json`
File ini berfungsi sebagai basis data pertanyaan wawancara yang dikurasi. Setiap pertanyaan dirancang untuk memicu *expected signals* (sinyal kompetensi) yang selaras dengan `competency_map`. Struktur data ini memungkinkan sistem untuk menghasilkan alur wawancara yang adaptif berdasarkan *target role* dan *competency focus* kandidat.

| Column / Key | Description |
| :--- | :--- |
| `role_family` | Kategori *role* yang sesuai dengan hirarki organisasi. |
| `competency` | Kategori kompetensi yang diuji (merujuk pada `competency_map`). |
| `question_seed` | Teks pertanyaan wawancara yang bersifat terbuka. |
| `question_type` | Klasifikasi alur wawancara: `hr_basic`, `behavioral`, `technical`, atau `closing`. |
| `guardrail_signals` | Daftar *key indicators* (poin-poin kriteria) yang harus muncul dalam jawaban kandidat untuk dianggap memenuhi standar kompetensi. |

**Catatan Implementasi:**
- **Adaptivitas:** Sistem secara dinamis memilih pertanyaan dari *seed* ini berdasarkan `competency` yang belum diuji selama sesi berlangsung.
- **Validasi Evaluasi:** `guardrail_signals` berfungsi sebagai **rubrik evaluasi instan** bagi model AI untuk menilai kualitas jawaban kandidat saat itu juga.
- **Kualitas Wawancara:** Dengan menggunakan teknik *Behavioral Questions* (Situasi-Tindakan-Hasil), pertanyaan-pertanyaan ini memaksa kandidat untuk tidak hanya memberikan teori, tetapi juga memberikan bukti nyata (*STAR structure*) dari pengalaman mereka.

#### `F. weakness_taxonomy.json`
Tabel ini berisi taksonomi kelemahan jawaban kandidat yang digunakan oleh sistem untuk melakukan *diagnostik* otomatis. Jika jawaban kandidat dianggap kurang kuat (misalnya, kurang detail atau tidak terukur), sistem akan menggunakan *template* pertanyaan ini untuk memancing kandidat memberikan informasi tambahan (*clarification loop*).

| Column / Key | Description |
| :--- | :--- |
| `tag_name` | *Unique identifier* untuk jenis kelemahan jawaban. |
| `description` | Penjelasan logis mengapa jawaban tersebut dianggap belum memenuhi standar. |
| `clarification_type` | Kategori tipe klarifikasi (digunakan untuk memicu logika *AI follow-up questions*). |
| `template` | *Template* pertanyaan yang digunakan untuk meminta klarifikasi kepada kandidat. |

**Catatan Implementasi:**
- ***Feedback Loop*:** Sistem tidak sekadar memberikan skor rendah, tetapi secara aktif membantu kandidat meningkatkan kualitas jawabannya melalui *clarification question*.
- **Integrasi Evaluasi:** `tag_name` ini akan disematkan pada dataset evaluasi (`evaluations_dataset.csv`), sehingga memungkinkan tim pengembang untuk memantau apakah tipe kelemahan tertentu lebih sering muncul pada *target role* atau *competency* tertentu.
- **Logika *Follow-up*:** `clarification_type` bertindak sebagai *trigger* agar AI menghasilkan pertanyaan lanjutan yang spesifik, relevan, dan tidak repetitif.

#### `G. scoring_rubric.json`
File ini adalah inti dari algoritma penilaian sistem. Ia menguraikan bobot penilaian untuk setiap dimensi kompetensi, mendefinisikan kriteria *quality label*, serta menentukan logika otomatis kapan sistem harus meminta klarifikasi tambahan kepada kandidat.

| Komponen Penilaian | Bobot (*Weight*) | Deskripsi Fokus |
| :--- | :--- | :--- |
| `role_relevance` | 25% | Relevansi pengalaman dengan target *role*. |
| `star_structure` | 20% | Kelengkapan metode STAR (*Situation, Task, Action, Result*). |
| `evidence_specificity` | 20% | Kedalaman bukti, *tools*, dan dampak nyata. |
| `technical_accuracy` | 15% | Ketepatan konsep teknis & *best practices*. |
| `communication_clarity` | 10% | Kejelasan artikulasi dan struktur jawaban. |
| `self_awareness` | 10% | Refleksi diri dan kapasitas belajar (*growth mindset*). |

#### Logika Evaluasi & Label Kualitas
Sistem mengonversi total skor (skala 0-100) menjadi *label* kualitatif untuk memudahkan HR/User memahami performa kandidat:

| Quality Label | Skor (0.0 - 1.0) | Kriteria Kualitatif |
| :--- | :--- | :--- |
| **Weak** | 0.00 – 0.49 | Jawaban kurang substansial atau tidak relevan. |
| **Average** | 0.50 – 0.74 | Jawaban cukup, namun kurang detail pada aspek teknis atau dampak. |
| **Strong** | 0.75 – 1.00 | Jawaban sangat baik, terstruktur (STAR), dan berdampak nyata. |

**Catatan Implementasi:**
- **Trigger Klarifikasi:** Sistem secara otomatis akan memicu pertanyaan klarifikasi (*follow-up*) jika ditemukan salah satu kondisi berikut: 
    1. `final_score` di bawah 0.75.
    2. `evidence_level` bernilai 3 atau kurang.
    3. Terdapat `weakness_tags` yang terdeteksi.
- **Batasan:** Untuk menjaga efisiensi durasi wawancara, sistem dibatasi maksimal **1 kali klarifikasi** per pertanyaan utama.

#### `H. evidence_ladder_mapping.json`
*Evidence Ladder* adalah kerangka kerja kualitatif yang digunakan sistem untuk memetakan tingkat kedalaman jawaban kandidat. Sistem menilai jawaban kandidat pada skala 1-5, di mana level yang lebih tinggi menunjukkan bukti kerja yang semakin spesifik, berdampak, dan terukur secara metrik.

| Level | Name | Description | Example |
| :--- | :--- | :--- | :--- |
| **1** | Claim | Klaim kemampuan tanpa konteks. | "Saya bisa membuat dashboard." |
| **2** | Skill | Menyebutkan *tools* tanpa konteks proyek. | "Saya menggunakan Excel dan Python." |
| **3** | Context | Penggunaan *tools* dalam konteks proyek spesifik. | "Saya membuat dashboard untuk data penjualan." |
| **4** | Impact | Menjelaskan kontribusi dan dampak positif. | "Dashboard membantu tim memahami tren produk." |
| **5** | Measurable Result | Hasil terukur secara kuantitatif/metrik. | "Waktu laporan berkurang dari 2 jam jadi 30 menit." |

**Catatan Implementasi:**
- **Analisis Kualitatif:** *Evidence Ladder* memungkinkan AI untuk membedakan antara kandidat yang hanya "berteori" (Level 1-2) dengan kandidat yang benar-benar "berpengalaman" (Level 4-5).
- **Trigger Level:** Kandidat dengan `evidence_level` ≤ 3 secara otomatis dianggap belum memberikan bukti yang kuat, sehingga sistem akan memicu *clarification loop* (menggunakan *template* dari `weakness_taxonomy`) untuk mendorong kandidat memberikan jawaban yang lebih detail.
- **Standar Evaluasi:** Level 5 adalah *gold standard* dalam penilaian sistem, yang mencerminkan pemahaman kandidat akan nilai bisnis dari pekerjaan teknis yang mereka lakukan.

#### `I. answer_dataset.csv`
Tabel ini merupakan kumpulan data jawaban kandidat hasil simulasi yang disusun untuk kebutuhan pengembangan model evaluasi. Dataset ini berisi variasi kualitas jawaban—mulai dari jawaban yang sangat terstruktur (*STAR-compliant*) hingga jawaban yang kurang informatif—untuk memberikan spektrum data yang luas bagi proses *training* dan *validation* model AI.

| Column | Description |
| :--- | :--- |
| `sample_id` | *Primary key* untuk setiap entri jawaban kandidat. |
| `domain`, `role_family`, `target_role` | Klasifikasi domain dan spesialisasi *role* kandidat. |
| `competency` | Kategori kompetensi yang diuji (merujuk ke `competency_map`). |
| `question` | Pertanyaan yang diajukan oleh sistem. |
| `answer` | Teks jawaban kandidat (raw input). |

**Catatan Implementasi:**
- **Variasi Kualitas Data:** Dataset ini sengaja dirancang untuk mencakup berbagai profil jawaban:
  - **High-Quality:** Jawaban yang memenuhi kriteria *Evidence Ladder* level 4-5 (detail, terukur, memiliki konteks).
  - **Low-Quality:** Jawaban yang bersifat ambigu, kurang struktur, atau tidak menjawab poin teknis (digunakan sebagai *negative samples* untuk melatih sistem agar mampu mendeteksi `weakness_tags`).
- **Penggunaan:** Data ini akan di-*merge* dengan `evaluations_dataset.csv` menggunakan `sample_id` untuk menciptakan label *ground truth* bagi model *Scoring Engine* dan *Clarification Trigger* kita.

#### `J. evaluations_dataset.csv`
Tabel ini berisi hasil penilaian (skor) yang dihasilkan oleh sistem terhadap jawaban kandidat dari `answer_dataset`. Dataset ini berfungsi sebagai *ground truth* untuk memvalidasi performa sistem penilaian otomatis, baik dalam memberikan skor numerik maupun menentukan label kualitas (*Weak, Average, Strong*).

| Column | Description |
| :--- | :--- |
| `sample_id` | *Foreign key* yang menghubungkan hasil penilaian dengan jawaban kandidat. |
| `role_relevance` ... `self_awareness` | Skor (0-100) per komponen berdasarkan `scoring_rubric`. |
| `evidence_level` | Level kedalaman bukti jawaban kandidat (skala 1-5). |
| `weakness_tags` | Daftar tag kelemahan yang ditemukan (dipisahkan titik koma). |
| `need_clarification` | *Boolean* (`True`/`False`) apakah sistem harus memicu pertanyaan tindak lanjut. |
| `clarification_type` | Kategori tipe klarifikasi yang direkomendasikan sistem. |
| `final_score_0_100` | Skor akhir terbobot (0-100). |
| `final_score_0_1` | Skor akhir ternormalisasi (0.0-1.0), digunakan sebagai target regresi untuk model evaluasi. |
| `quality_label` | Label kualitatif akhir (*Weak, Average, Strong*). |

**Catatan Implementasi:**
- **Analisis Kinerja:** Kolom `weakness_tags` digunakan oleh sistem untuk mengidentifikasi pola kesalahan umum yang dilakukan kandidat pada *role* tertentu, yang kemudian dapat diumpankan kembali ke dalam modul *competency_map* untuk peningkatan kualitas pertanyaan.
- **Validasi Model:** `final_score_0_1` dan `quality_label` digunakan sebagai label target dalam proses *supervised learning* untuk meningkatkan akurasi *Scoring Engine* sistem agar semakin mendekati penilaian manusia (*Human-in-the-loop validation*).
- **Relasi:** Tabel ini dirancang untuk di-*merge* dengan `answer_dataset` menggunakan `sample_id` sebelum dilakukan visualisasi pada dasbor `Candidate Performance`.
---
### Kategori 2: Data Pengayaan (Interim)
#### `A. cleaned_answers_evaluation.csv`
Dataset ini merupakan hasil penggabungan (*merge*) antara `answer_dataset.csv` dan `evaluations_dataset.csv` yang telah melalui proses pembersihan dan pengayaan fitur (*feature engineering*) di dalam *notebook* pengolahan data. Dataset ini dirancang untuk mempermudah analisis korelasi antara konten jawaban kandidat dengan metrik performa mereka.

| Column | Description |
| :--- | :--- |
| `sample_id` | *Primary key* dari data transaksional. |
| `role_family` ... `answer` | Data dasar hasil input kandidat. |
| `role_relevance` ... `quality_label` | Hasil penilaian model evaluasi. |
| `answer_length_words` | Total jumlah kata dalam jawaban. |
| `has_context` ... `has_data_processing` | **Feature Flags:** *Boolean* (0 atau 1) yang menunjukkan keberadaan elemen spesifik dalam jawaban (misal: `has_tools`, `has_impact`, `has_model_evaluation`). |
| `filler_word_count` | Jumlah kata pengisi (*filler words*) seperti "em", "eh", "anu", untuk mengukur tingkat kepercayaan diri/kelancaran komunikasi. |

**Catatan Implementasi:**
- **Feature Engineering:** Penambahan kolom *boolean flag* bertujuan untuk mempermudah model dalam mengidentifikasi pola jawaban kandidat secara kuantitatif (misalnya: apakah kandidat yang menyebutkan `has_tools` memiliki `final_score` yang lebih tinggi?).
- **Analisis Kualitas:** Kolom `filler_word_count` memberikan dimensi baru bagi sistem untuk mendeteksi tingkat keraguan atau kurangnya persiapan kandidat saat menjawab pertanyaan teknis.
- **Tujuan:** Data di folder ini merupakan *staging area* sebelum data dipisahkan menjadi *split* pelatihan untuk tim AI.

| Nama Kolom | Deskripsi |
| :--- | :--- |
| `sample_id` | ID unik untuk setiap sampel jawaban (Primary Key). |
| `role_family` | Kategori besar *role* yang dilamar kandidat. |
| `target_role` | Nama spesifik *target role* yang dilamar. |
| `competency` | Kategori kompetensi yang diuji dalam pertanyaan tersebut. |
| `question` | Teks lengkap pertanyaan interview yang diberikan. |
| `answer` | Teks jawaban mentah dari kandidat. |
| `role_relevance` | Skor (0-100) relevansi pengalaman dengan *role*. |
| `star_structure` | Skor (0-100) kelengkapan alur STAR (*Situation, Task, Action, Result*). |
| `evidence_specificity` | Skor (0-100) kedalaman bukti, *tools*, dan detail kontribusi. |
| `technical_accuracy` | Skor (0-100) ketepatan konsep teknis dan *best practice*. |
| `communication_clarity` | Skor (0-100) kejelasan, keruntutan, dan artikulasi kandidat. |
| `self_awareness` | Skor (0-100) kemampuan refleksi dan *growth mindset*. |
| `evidence_level` | Level 1-5 pada *Evidence Ladder* (dari Klaim hingga *Measurable Result*). |
| `weakness_tags` | *List* tanda kelemahan jawaban (dipisahkan `;`). |
| `need_clarification` | Status apakah sistem perlu meminta pertanyaan klarifikasi tambahan. |
| `clarification_type` | Kategori jenis klarifikasi yang dibutuhkan (misal: *impact, metric*). |
| `final_score_0_100` | Total skor akhir (0-100) yang sudah terbobot. |
| `final_score_0_1` | Skor akhir ternormalisasi (0.0-1.0), target regresi model AI. |
| `quality_label` | Kategori label akhir: *Weak, Average,* atau *Strong*. |
| `answer_length_words`| Total panjang kata dalam jawaban kandidat. |
| `has_context` | Flag (0/1): Apakah jawaban mengandung konteks masalah/situasi. |
| `has_contribution` | Flag (0/1): Apakah jawaban menjelaskan peran personal kandidat. |
| `has_tools` | Flag (0/1): Apakah jawaban menyebutkan *tools* atau teknologi spesifik. |
| `has_impact` | Flag (0/1): Apakah jawaban menyebutkan dampak/hasil kerja. |
| `has_metric` | Flag (0/1): Apakah jawaban menyertakan angka/metrik terukur. |
| `has_technical_detail`| Flag (0/1): Apakah jawaban mengandung detail teknis mendalam. |
| `has_self_awareness` | Flag (0/1): Apakah jawaban menunjukkan proses refleksi diri. |
| `filler_word_count` | Jumlah kata *filler* (eh, anu, hmm) sebagai indikator keraguan. |
| `has_testing_coverage`| Flag (0/1): Indikator spesifik kompetensi *Software Tester*. |
| `has_deployment` | Flag (0/1): Indikator spesifik kompetensi *DevOps/Deployment*. |
| `has_mobile_platform` | Flag (0/1): Indikator spesifik kompetensi *Mobile Development*. |
| `has_security_awareness`| Flag (0/1): Indikator spesifik kompetensi *Security*. |
| `has_backend_architecture`| Flag (0/1): Indikator spesifik kompetensi *Backend Architecture*. |
| `has_model_evaluation` | Flag (0/1): Indikator spesifik kompetensi *AI/ML Model Evaluation*. |
| `has_data_processing` | Flag (0/1): Indikator spesifik kompetensi *Data Processing/ETL*. |
---
### Kategori 3: Data Pelatihan Model (Processed)

#### Dataset Folder: `data/03_processed/`
Folder ini berisi dataset final yang telah diproses, dibersihkan, dan dibagi (*split*) menjadi tiga bagian untuk kebutuhan *training*, *validation*, dan *testing* model AI. Dataset ini siap digunakan langsung oleh tim AI untuk membangun dan menguji *Scoring Engine* serta modul deteksi kelemahan jawaban.

| File Name | Description |
| :--- | :--- |
| `train_df.csv` | Dataset pelatihan (70%) untuk melatih model mempelajari pola evaluasi jawaban kandidat. |
| `val_df.csv` | Dataset validasi (15%) untuk menyetel *hyperparameter* dan memantau *overfitting* selama pelatihan. |
| `test_df.csv` | Dataset pengujian (15%) sebagai data *hold-out* untuk evaluasi akhir performa model. |

**Catatan Implementasi:**
- **Rasio Pembagian (*Data Split Ratio*):** Data dibagi dengan proporsi **70% Training, 15% Validation, dan 15% Testing**. Rasio ini dipilih untuk memastikan model memiliki cukup data untuk mempelajari pola (`train`), namun tetap memiliki porsi yang cukup untuk validasi berkala (`val`) dan pengujian final yang objektif (`test`).
- **Konsistensi:** Dataset ini merupakan turunan langsung dari `cleaned_answers_evaluation.csv` di folder `02_interim`.