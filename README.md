# 💬 KeluhCerdas - Sistem Prioritisasi Keluhan Publik Berbasis AI

**KeluhCerdas** adalah sebuah sistem berbasis kecerdasan buatan (AI) yang dirancang untuk membantu instansi pemerintah dalam memprioritaskan keluhan masyarakat secara efisien dan objektif. Sistem ini menganalisis isi keluhan menggunakan pemrosesan bahasa alami untuk mendeteksi topik dan emosi, lalu menghitung skor prioritas menggunakan metode Multi-Criteria Decision Making (VIKOR). Hasilnya disajikan melalui dashboard visual yang interaktif.

---

## 🚀 Fitur Utama

- 📌 **Analisis Topik Otomatis** dengan NLP dan Keyword Extraction
- 😡 **Deteksi Emosi Keluhan** berbasis model klasifikasi TensorFlow
- 🧮 **Skoring Prioritas** menggunakan metode VIKOR
- 📊 **Dashboard Interaktif** berbasis Flask + Bootstrap
- 🔍 **Filter & Visualisasi** keluhan berdasarkan emosi, topik, instansi, status

---

## 🧠 Teknologi yang Digunakan

- Python 3.11
- TensorFlow / Keras
- Pandas, NumPy, Scikit-learn
- Flask (Backend)
- Bootstrap 5 (Frontend)
- Matplotlib, Seaborn, Plotly
- VIKOR (Multi-Criteria Decision Making)
- Excel / CSV Input (Sementara)

---

## 📂 Struktur Proyek

```
Project_Capstone_LaskarAI_KeluhCerdas/
│
├── Backend/                  # Backend Flask + Dashboard UI
│   ├── app.py                # Main Flask app
│   ├── static/               # Img
│   ├── templates/            # HTML Template Files
│   ├── data/                 # Dataset (Excel)
│   ├── Model/                    # Notebook & Model Files
│       ├── indobert_lstm_tfjs
│           ├── group1-shard1of1.bin        # Model Deteksi Emosi
│           ├── model.json
│       ├── indobert_lstm_model.keras       # Model Klasifikasi Topik      
│       └── indobert_lstm_model.tflite
│
├── README.md
└── requirements.txt
```

---

## 📥 Instalasi & Menjalankan Proyek

1. **Clone repositori ini**
```bash
git clone https://github.com/jaal047/Project_Capstone_LaskarAI_KeluhCerdas-.git
cd KeluhCerdas/Backend
```

2. **Aktifkan Python 3.11 dan install dependensi**
```bash
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

3. **Jalankan Flask App**
```bash
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
```

---

## 📊 Contoh Tampilan Dashboard

![Contoh Dashboard](https://via.placeholder.com/800x400.png?text=Screenshot+Dashboard+KeluhCerdas)

---

## 🎯 Tujuan Proyek

Proyek ini dikembangkan sebagai bagian dari Capstone Project pada program pelatihan Machine Learning untuk membantu:

- Pemerintah dalam **mengelola keluhan publik** secara adil dan efisien.
- Masyarakat dalam mendapatkan **respon yang lebih cepat** terhadap keluhan kritis.
- Mengintegrasikan AI dalam praktik pelayanan publik yang nyata.

---

## 🧑‍💻 Tim Pengembang

- [Rijal Akhdan](https://github.com/jaal047) – Project Lead
- Mohammad Sihabudin Al Qurtubi 
- Muhammad Naufal Ilman
- M Mahfudl Awaludin

---
