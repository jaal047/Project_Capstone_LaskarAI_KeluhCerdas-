# Gunakan base image Python yang ringan
FROM python:3.11-slim

# Tetapkan direktori kerja di dalam container
WORKDIR /app

# Perbarui pip dan instal pustaka sistem yang mungkin diperlukan
RUN pip install --no-cache-dir --upgrade pip

# Salin file requirements terlebih dahulu untuk caching yang lebih baik
COPY requirements.txt requirements.txt

# Instal dependensi Python
RUN pip install --no-cache-dir -r requirements.txt

# Download data NLTK yang dibutuhkan oleh helper.py
RUN python -m nltk.downloader stopwords

# Salin semua file proyek ke dalam direktori kerja di container
COPY . .

# Beri tahu Docker bahwa aplikasi akan berjalan di port 7860 (port default HF Spaces)
EXPOSE 7860

# Perintah untuk menjalankan aplikasi Flask saat container dimulai
# Menggunakan host 0.0.0.0 agar dapat diakses dari luar container
CMD ["flask", "run", "--host=0.0.0.0", "--port=7860"]