from flask import Flask, render_template, request
from datetime import date

app = Flask(__name__)

# Dummy Data contoh untuk dashboard
dummy_dashboard = {
    "total_reports": 150,
    "in_process": 60,
    "high_priority": 25,
    "new_reports": 10,
    "resolved_reports": 55,
    "pending_reports": 35
}

# Dummy data untuk leaderboard
dummy_leaderboard = {
    "top_topics": [
        {"topic": "Sampah", "count": 40},
        {"topic": "Lalu Lintas", "count": 30},
        {"topic": "Penerangan Jalan", "count": 20}
    ],
    "top_instansi": [
        {"instansi": "Dinas Kebersihan", "count": 50},
        {"instansi": "Dinas Perhubungan", "count": 35},
        {"instansi": "Dinas Penerangan", "count": 25}
    ],
    "complaints": [
        {"id": 1, "keluhan": "Jalan berlubang di depan rumah", "instansi": "Dinas PU", "status": "Pending"},
        {"id": 2, "keluhan": "Lampu jalan mati di RT 05", "instansi": "Dinas Penerangan", "status": "Diproses"},
        {"id": 3, "keluhan": "Sampah menumpuk di pasar", "instansi": "Dinas Kebersihan", "status": "Selesai"}
    ],
    "wordcloud_words": [
        {"text": "Sampah", "weight": 40},
        {"text": "Jalan", "weight": 35},
        {"text": "Lampu", "weight": 25},
        {"text": "Macet", "weight": 15},
        {"text": "Air", "weight": 10}
    ]
}

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', data=dummy_dashboard)

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html', data=dummy_leaderboard)

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')
    if request.method == 'POST':
        # Untuk sekarang dummy dulu, nanti bisa disambung ke backend model
        keluhan = request.form.get('keluhan')
        instansi = request.form.get('instansi')
        tanggal_keluhan = request.form.get('tanggal_keluhan')
        kecamatan = request.form.get('kecamatan')
        kelurahan = request.form.get('kelurahan')
        # Bisa proses disini
