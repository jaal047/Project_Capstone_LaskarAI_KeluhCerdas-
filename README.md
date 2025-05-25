# 💬 KeluhCerdas: Klasifikasi Emosi dan Prioritas Keluhan Publik Berbasis IndoBERT

**KeluhCerdas** adalah sistem kecerdasan buatan berbasis **Natural Language Processing (NLP)** dengan model klasifikasi emosi berbasis **IndoBERT**. Aplikasi ini dirancang untuk memahami isi emosional dari keluhan masyarakat, mengekstraksi informasi penting, dan menentukan tingkat urgensinya. Dengan KeluhCerdas, instansi pemerintah dapat merespons aduan publik secara **lebih cepat, tepat, dan empatik**.

---

## 📌 Daftar Isi

* [Latar Belakang](#latar-belakang)
* [Rumusan Masalah](#rumusan-masalah)
* [Tujuan](#tujuan)
* [Lingkup Proyek](#lingkup-proyek)
* [Metodologi](#metodologi)
* [Teknologi yang Digunakan](#teknologi-yang-digunakan)
* [Potensi Risiko atau Masalah](#potensi-risiko-atau-masalah)

---

## 🧠 Latar Belakang

Instansi publik di Indonesia menerima ribuan keluhan dari masyarakat setiap harinya. Namun, tidak semua keluhan memiliki tingkat urgensi yang sama. Beberapa mengandung emosi kuat seperti kemarahan atau kesedihan, sementara yang lain bersifat netral. Dengan teknologi NLP dan model **IndoBERT** yang sudah dioptimasi untuk Bahasa Indonesia, KeluhCerdas mampu mengidentifikasi emosi serta menilai prioritas keluhan secara otomatis.

---

## ❓ Rumusan Masalah

* Bagaimana mengklasifikasikan emosi dalam keluhan masyarakat berbahasa Indonesia secara akurat?
* Bagaimana mengekstraksi kata kunci penting dari keluhan?
* Bagaimana menentukan prioritas penanganan keluhan berdasarkan konten dan emosinya?

---

## 🌟 Tujuan

* Membangun sistem klasifikasi emosi menggunakan **IndoBERT**.
* Mengembangkan fitur ekstraksi kata kunci dari teks keluhan.
* Menentukan prioritas penanganan keluhan menggunakan metode **MCDM (AHP + VIKOR)**.

---

## 🧱 Lingkup Proyek

✅ Termasuk:

* Pengumpulan dan pelabelan data keluhan publik
* Pelatihan model IndoBERT untuk klasifikasi emosi
* Ekstraksi kata kunci menggunakan KeyBERT atau TextRank
* Perankingan urgensi keluhan dengan AHP + VIKOR
* Pembuatan antarmuka pengguna dan backend API

🚫 Tidak termasuk:

* Speech-to-text untuk keluhan suara
* Sentiment analysis lanjutan
* Integrasi real-time dengan platform pengaduan publik

---

## 🧪 Metodologi

1. **Data Collection & Labeling**

   * Emosi yang dilabeli: *Marah*, *Sedih*, *Netral*, *Senang*.

2. **Preprocessing**

   * Case folding, tokenisasi, stopword removal, dan normalisasi teks.

3. **Modeling**

   * Fine-tuning **IndoBERT** dan **IndoBERTweet**.
   * Evaluasi: akurasi, precision, recall, F1-score.

4. **Keyword Extraction**

   * Menggunakan metode **TF-IDF** dan **YAKE!**.

5. **Prioritas Keluhan (MCDM)**

   * **AHP** untuk menentukan bobot kriteria (emosi, keyword, panjang teks).
   * **VIKOR** untuk menyusun peringkat urgensi berdasarkan bobot tersebut.

6. **Deployment**

   * API klasifikasi menggunakan **Flask**.
   * Frontend web antarmuka pengguna.
   * Database penyimpanan dengan **MySQL**.

---

## 🛠 Teknologi yang Digunakan

| Tools/Library             | Fungsi                                     |
| ------------------------- | ------------------------------------------ |
| Python                    | Bahasa pemrograman utama                   |
| IndoBERT, IndoBERTweet    | Model pre-trained untuk Bahasa Indonesia   |
| Hugging Face Transformers | Fine-tuning model IndoBERT                 |
| Scikit-learn              | Preprocessing dan evaluasi                 |
| Flask                     | Backend REST API                           |
| YAKE / TF-IDF             | Ekstraksi kata kunci                       |
| AHP, VIKOR                | Pengambilan keputusan multikriteria (MCDM) |
| HTML, CSS, JS             | Frontend sederhana                         |
| MySQL                     | Database keluhan                           |


---


## ⚠️ Potensi Risiko atau Masalah

| Risiko                                    | Solusi atau Mitigasi                                         |
| ----------------------------------------- | ------------------------------------------------------------ |
| Data emosi tidak seimbang                 | Resampling dan augmentasi data                               |
| Ambiguitas dalam labeling emosi           | Gunakan guideline labeling dan diskusi tim                   |
| Kompleksitas integrasi                    | Modul sistem dibuat terpisah dan terdokumentasi dengan baik  |
| Kriteria AHP bersifat subjektif           | Validasi bobot dengan pakar atau metode pairwise consistency |
