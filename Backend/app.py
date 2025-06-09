
from flask import Flask, render_template, request
from datetime import date, datetime
import os
import pandas as pd
import pandas as pd
from wordcloud import WordCloud

app = Flask(__name__)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    base_path = os.path.join('data')
    dash_df = pd.read_excel(os.path.join(base_path, 'dataset_dash.xlsx'))
    emosi_df = pd.read_excel(os.path.join(base_path, 'final_dataset.xlsx'))

    # Info utama
    total_keluhan = dash_df.shape[0]
    topik_terbanyak = dash_df['Topik'].value_counts().idxmax()
    instansi_terbanyak = dash_df['Instansi'].value_counts().idxmax()

    # Proses tanggal
    dash_df['tanggal_keluhan'] = pd.to_datetime(dash_df['tanggal_keluhan']).dt.normalize()
    today = pd.to_datetime(datetime.today().date())
    keluhan_hari_ini = dash_df[dash_df['tanggal_keluhan'] == today].shape[0]

    # Data keluhan harian (last 7 days)
    start_date = today - pd.Timedelta(days=6)
    last_7_days_df = dash_df[(dash_df['tanggal_keluhan'] >= start_date) & (dash_df['tanggal_keluhan'] <= today)].copy()

    last_7_days_df['nama_hari'] = last_7_days_df['tanggal_keluhan'].dt.day_name()
    hari_en_to_id = {
        'Monday': 'Senin',
        'Tuesday': 'Selasa',
        'Wednesday': 'Rabu',
        'Thursday': 'Kamis',
        'Friday': 'Jumat',
        'Saturday': 'Sabtu',
        'Sunday': 'Minggu'
    }
    last_7_days_df['nama_hari'] = last_7_days_df['nama_hari'].map(hari_en_to_id)
    hari_urut = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    keluhan_per_hari = last_7_days_df.groupby('nama_hari').size().reindex(hari_urut, fill_value=0)
    keluhan_harian_labels = keluhan_per_hari.index.tolist()
    keluhan_harian_values = keluhan_per_hari.values.tolist()

    # Data emosi
    emosi_dist = emosi_df['emosi'].value_counts()
    emosi_values = emosi_dist.values.tolist()

    # Data keluhan bulanan dengan sorting berdasarkan tanggal
    # Buat kolom untuk menampung data bulanan dan kelompokkan berdasarkan bulan dan tahun
    dash_df['year'] = dash_df['tanggal_keluhan'].dt.year
    dash_df['month'] = dash_df['tanggal_keluhan'].dt.month
    
    # Kelompokkan berdasarkan bulan dan tahun
    keluhan_bulanan = dash_df.groupby(['year', 'month']).size().reset_index()
    keluhan_bulanan.columns = ['year', 'month', 'count']
    
    # Urutkan berdasarkan tahun dan bulan
    keluhan_bulanan = keluhan_bulanan.sort_values(['year', 'month'])
    
    # Format label bulan-tahun untuk tampilan
    import calendar
    keluhan_bulanan['bulan_nama'] = keluhan_bulanan.apply(
        lambda row: f"{calendar.month_abbr[row['month']]} {row['year']}",
        axis=1
    )
    keluhan_bulanan_labels = keluhan_bulanan['bulan_nama'].tolist()
    keluhan_bulanan_values = keluhan_bulanan['count'].tolist()

    return render_template(
        'dashboard.html',
        total_keluhan=total_keluhan,
        topik_terbanyak=topik_terbanyak,
        instansi_terbanyak=instansi_terbanyak,
        keluhan_hari_ini=keluhan_hari_ini,
        keluhan_harian_labels=keluhan_harian_labels,
        keluhan_harian_values=keluhan_harian_values,
        emosi_labels=emosi_dist.index.tolist(),
        emosi_values=emosi_values,
        keluhan_bulanan_labels=keluhan_bulanan_labels,
        keluhan_bulanan_values=keluhan_bulanan_values
    )


@app.route('/leaderboard')
def leaderboard():
    base_path = os.path.join('data')
    dash_df   = pd.read_excel(os.path.join(base_path, 'dataset_dash.xlsx'))
    final_df  = pd.read_excel(os.path.join(base_path, 'final_dataset.xlsx'))

    # ----- Top 5 Topik & Instansi ---------------------------------------
    top_topik     = dash_df['Topik'].value_counts().head(5).reset_index()
    top_topik.columns = ['Topik', 'Jumlah']

    top_instansi  = dash_df['Instansi'].value_counts().head(5).reset_index()
    top_instansi.columns = ['Instansi', 'Jumlah']

    # ----- Word-cloud ----------------------------------------------------
    text_wc = ' '.join(dash_df['keluhan'].dropna().astype(str))
    wc_img  = WordCloud(width=800, height=400, background_color="white").generate(text_wc)

    wc_path = os.path.join('static', 'wordcloud.png')
    os.makedirs(os.path.dirname(wc_path), exist_ok=True)
    wc_img.to_file(wc_path)          # simpan ⇒ static/wordcloud.png

    # ----- Keluhan prioritas (10 skor vikor tertinggi) -------------------
    prioritas_df = final_df.sort_values(by='vikor', ascending=False).head(10)
    gabung = pd.merge(
        prioritas_df,
        dash_df[['id', 'keluhan', 'Topik', 'Instansi']],
        left_index=True, right_index=True
    )

    # ----- Render ke template -------------------------------------------
    return render_template(
        'leaderboard.html',
        wordcloud_image='wordcloud.png',           # <<<<<<  baru
        top_topik        = top_topik.itertuples(index=False),
        top_instansi     = top_instansi.itertuples(index=False),
        keluhan_prioritas= gabung.itertuples(index=False)
    )

@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        # Untuk sekarang dummy dulu, nanti bisa disambung ke backend model
        keluhan = request.form.get('keluhan')
        instansi = request.form.get('instansi')
        tanggal_keluhan = request.form.get('tanggal_keluhan')
        kecamatan = request.form.get('kecamatan')
        kelurahan = request.form.get('kelurahan')
        # Proses data di sini sesuai kebutuhan
        # ...
        return "Form submitted!"  # Sementara response sederhana

    return render_template('form.html')
