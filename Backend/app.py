from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import date, datetime
import os, json
import numpy as np
import pandas as pd
import ast
import calendar
from wordcloud import WordCloud
from helper import predict_emotion,keyword, load_tflite_model

app = Flask(__name__)

@app.route('/')
@app.route('/dashboard')
def dashboard():
    base_path = os.path.join('data')
    dash_df = pd.read_excel(os.path.join(base_path, 'dataset_dash.xlsx'))
    emosi_df = pd.read_excel(os.path.join(base_path, 'vikor_fix.xlsx'))

    # Info utama
    total_keluhan = dash_df.shape[0]
    topik_terbanyak = dash_df['Topik'].value_counts().idxmax()
    instansi_terbanyak = dash_df['Instansi'].value_counts().idxmax()

    # Keluhan belum selesai
    keluhan_belum_selesai = emosi_df[emosi_df['status'] != 'selesai']
    keluhan_belum_selesai = keluhan_belum_selesai.shape[0]

    # Data emosi
    emosi_dist = emosi_df['emosi'].value_counts()
    emosi_values = emosi_dist.values.tolist()

    # Data keluhan bulanan dengan sorting berdasarkan tanggal
    # Buat kolom untuk menampung data bulanan dan kelompokkan berdasarkan bulan dan tahun
    dash_df['tanggal_keluhan'] = pd.to_datetime(dash_df['tanggal_keluhan']).dt.normalize()
    dash_df['month'] = dash_df['tanggal_keluhan'].dt.month.astype(int)
    dash_df['year'] = dash_df['tanggal_keluhan'].dt.year.astype(int)
    
    # Kelompokkan berdasarkan bulan dan tahun
    keluhan_bulanan = dash_df.groupby(['year', 'month']).size().reset_index()
    keluhan_bulanan.columns = ['year', 'month', 'count']
    
    # Urutkan berdasarkan tahun dan bulan
    keluhan_bulanan = keluhan_bulanan.sort_values(['year', 'month'])
    
    # Format label bulan-tahun untuk tampilan
    keluhan_bulanan['bulan_nama'] = keluhan_bulanan.apply(
        lambda row: f"{calendar.month_abbr[int(row['month'])]} {int(row['year'])}",
        axis=1
    )

    keluhan_bulanan_labels = keluhan_bulanan['bulan_nama'].tolist()
    keluhan_bulanan_values = keluhan_bulanan['count'].tolist()

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

    return render_template(
        'dashboard.html',
        total_keluhan=total_keluhan,
        topik_terbanyak=topik_terbanyak,
        instansi_terbanyak=instansi_terbanyak,
        keluhan_belum_selesai=keluhan_belum_selesai,
        emosi_labels=emosi_dist.index.tolist(),
        emosi_values=emosi_values,
        keluhan_bulanan_labels=keluhan_bulanan_labels,
        keluhan_bulanan_values=keluhan_bulanan_values,
        wordcloud_image='wordcloud.png',           
        top_topik        = top_topik.itertuples(index=False),
        top_instansi     = top_instansi.itertuples(index=False),
    )

@app.route('/ubah_status', methods=['POST'])
def ubah_status():
    keluhan_id = int(request.form['id'])

    base_path = os.path.join('data')
    file_path = os.path.join(base_path, 'vikor_fix.xlsx')
    df = pd.read_excel(file_path)

    # Update status menjadi 'selesai'
    df.loc[df['id'] == keluhan_id, 'status'] = 'selesai'

    # Simpan kembali
    df.to_excel(file_path, index=False)

    return redirect(url_for('leaderboard'))


@app.route('/leaderboard')
def leaderboard():
    base_path = os.path.join('data')
    final_df  = pd.read_excel(os.path.join(base_path, 'vikor_fix.xlsx'))

     # Filter hanya data yang belum selesai
    df_pending = final_df[final_df['status'] != 'selesai']
    df_pending['keyword'] = df_pending['keyword'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

    # ----- Hitung VIKOR -----
    f_emosi_plus  = df_pending['new_emosi'].max()
    f_emosi_min   = df_pending['new_emosi'].min()
    f_ranking_plus= df_pending['new_keyword'].max()
    f_ranking_min = df_pending['new_keyword'].min()

    emosi_denom  = f_emosi_plus - f_emosi_min
    ranking_denom = f_ranking_plus - f_ranking_min

    df_pending['normalisasi_emosi'] = (f_emosi_plus - df_pending['new_emosi']) / (emosi_denom if emosi_denom != 0 else 1)
    df_pending['normalisasi_ranking'] = (f_ranking_plus - df_pending['new_keyword']) / (ranking_denom if ranking_denom != 0 else 1)

    df_pending['normalisasi_bobot_emosi']   = 0.5 * df_pending['normalisasi_emosi']
    df_pending['normalisasi_bobot_ranking'] = 0.5 * df_pending['normalisasi_ranking']

    df_pending['ultility'] = df_pending['normalisasi_bobot_emosi'] + df_pending['normalisasi_bobot_ranking']
    df_pending['regret']   = df_pending[['normalisasi_bobot_emosi', 'normalisasi_bobot_ranking']].max(axis=1)

    s_plus = df_pending['ultility'].max()
    s_min  = df_pending['ultility'].min()
    r_plus = df_pending['regret'].max()
    r_min  = df_pending['regret'].min()

    df_pending['vikor'] = 0.5 * ((df_pending['ultility'] - s_min) / (s_plus - s_min)) + \
                          0.5 * ((df_pending['regret']   - r_min) / (r_plus - r_min))

    df_pending['rank'] = df_pending['vikor'].rank(ascending=True).astype(int)

    # ----- Keluhan prioritas (10 skor vikor tertinggi) -------------------
    prioritas_df = df_pending.sort_values(by='vikor', ascending=True).head(10)

    # ----- Render ke template -------------------------------------------
    return render_template(
        'leaderboard.html',
        keluhan_prioritas = prioritas_df
    )

@app.route('/form', methods=['GET', 'POST'])
def form():
    # Load dataframes
    base_path = os.path.join('data')
    instansi_df = pd.read_csv(os.path.join(base_path, 'mediacenter_instansi_202311220929.csv'), sep=';')
    kecamatan_df = pd.read_csv(os.path.join(base_path, 'mediacenter_kecamatan_202311220929.csv'), sep=';')
    kelurahan_df = pd.read_csv(os.path.join(base_path, 'mediacenter_kelurahan_202311220929.csv'), sep=';')
    topik_df = pd.read_csv(os.path.join(base_path, 'mediacenter_topik_202311230834.csv'), sep=';')
    # Join antar dataframe agar dapatkan nama kecamatan pada kelurahan
    kecamatan_dict = kecamatan_df.set_index('id')['name'].to_dict()
    kelurahan_df['kecamatan_name'] = kelurahan_df['kecamatan_id'].map(kecamatan_dict)

    # Buat mapping: kecamatan_name -> list of kelurahan names
    kelurahan_map = kelurahan_df.groupby('kecamatan_name')['name'].apply(list).to_dict()

    dash_df = pd.read_excel(os.path.join(base_path, 'dataset_dash.xlsx'))
    if dash_df.empty or 'id' not in dash_df.columns:
        new_id = 1
    else:
        # Ambil ID terakhir dan tambah 1
        last_id = dash_df['id'].max()
        if pd.isna(last_id):
            new_id = 1
        else:
            new_id = int(last_id) + 1

    message = None
    if request.method == 'POST':
        # Form
        keluhan = request.form.get('keluhan')
        instansi = request.form.get('instansi')
        tanggal_keluhan = request.form.get('tanggal_keluhan')
        kecamatan = request.form.get('kecamatan')
        kelurahan = request.form.get('kelurahan')
        topik = request.form.get('topik')
        tanggal_hanya = datetime.strptime(tanggal_keluhan, '%Y-%m-%d')
        waktu_sekarang = datetime.now().time()
        tanggal_lengkap = datetime.combine(tanggal_hanya, waktu_sekarang) 
        tanggal_formatted = tanggal_lengkap.strftime('%Y-%m-%d %H:%M:%S.%f')
        
        # Prediksi emosi dan ekstrak keyword
        interpreter = load_tflite_model()
        emosi = predict_emotion(keluhan, interpreter)
        keywords, ranked_keywords = keyword(keluhan)
        emotion_mapping = {
            'anger': 3,
            'fear': 2,
            'sadness': 1
        }
        new_emosi = emotion_mapping.get(emosi, emosi)

        # Buat dictionary data baru
        new_data = {
            'id': new_id,
            'keluhan': keluhan,
            'instansi': instansi,
            'tanggal_keluhan': tanggal_formatted,
            'kecamatan': kecamatan,
            'kelurahan': kelurahan,
            'topik': topik,
            'emosi': emosi,
            'new_emosi': new_emosi,
            'new_keyword': ranked_keywords,
            'keyword': keywords,
            'status': 'belum_selesai'
        }
        new_data_for_dash = {
            'id': new_id,
            'keluhan': keluhan,
            'tanggal_keluhan': tanggal_formatted,
            'Topik': topik,      
            'Instansi': instansi
        }

        # Simpan ke final_dataset.xlsx
        # Cek apakah file sudah ada, jika tidak buat baru
        dataset_path = os.path.join('data', 'vikor_fix.xlsx')
        full_dataset_path = os.path.join('data', 'dataset_dash.xlsx')
        if not os.path.exists(dataset_path):
            df = pd.DataFrame([new_data])
        else:
            df = pd.read_excel(dataset_path)
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            dt = pd.read_excel(full_dataset_path)
            dt_n = pd.DataFrame([new_data_for_dash])
            dt = pd.concat([dt,dt_n], ignore_index=True)
        df.to_excel(dataset_path, index=False)
        dt.to_excel(full_dataset_path, index=False)

        message = "✅ Keluhan berhasil disimpan!"

    # Pass dataframes to the template
    return render_template('form.html', instansi=instansi_df, 
                           kecamatan=kecamatan_df, kelurahan=kelurahan_df, 
                           topik=topik_df, kelurahan_map=json.dumps(kelurahan_map), message=message)
