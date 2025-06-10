import demoji
import re
import pandas as pd
import numpy as np
import nltk
import keras
from transformers import BertTokenizer, TFBertModel
import tensorflow as tf
from string import punctuation
from keybert import KeyBERT
from nltk.corpus import stopwords
from sentence_transformers import SentenceTransformer
import os
import warnings
warnings.filterwarnings("ignore")

# --- Configuration & Global Variables ---
MAX_LENGTH = 128
base_path = os.path.join('data')
model_path = os.path.join('Model')

# --- Helper: Download NLTK data ---
nltk.download('stopwords')

# --- Load Resources ---
alay_dict = pd.read_csv(os.path.join(base_path, 'kamus_alay.csv'), names=['alay', 'normal'], encoding='latin-1')
alay_dict_map = dict(zip(alay_dict['alay'], alay_dict['normal']))
stop_words = set(stopwords.words('indonesian'))
tokenizer = BertTokenizer.from_pretrained("indobenchmark/indobert-large-p1")
bert_model = TFBertModel.from_pretrained("indobenchmark/indobert-large-p1")
lstm_model = keras.models.load_model(os.path.join(model_path, 'indobert_lstm_model.keras'))

# --- Preprocessing Functions ---
def process_text(text):
    # Baca kamus CSV ke dalam DataFrame
    global alay_dict_map
    text = str(text) # Convert Object to str
    text = text.lower() # Lowercase text
    text = re.sub(r'\d+', '', text) # Remove number
    text = text.replace('\\n\\n\\n', ' ')
    text = text.replace('\\n\\n', ' ')
    text = text.replace('\\n', ' ')
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE) # Remove link
    text = re.sub(f"[{re.escape(punctuation)}]", " ", text) # Remove punctuation
    text = demoji.replace(text, "") # Remove emoji
    text = " ".join(text.split()) # Remove extra spaces, tabs, and new lines
    text = text.split()
    text = [alay_dict_map[word] if word in alay_dict_map else word for word in text]
    text = ' '.join(text)

    return text

# --- Emotion Prediction ---
def load_tflite_model(tflite_path="Model/indobert_lstm_model.tflite"):
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    return interpreter

def predict_emotion(text, interpreter):
    cleaned = process_text(text)
    tokens = tokenizer(cleaned, return_tensors="tf", padding='max_length', truncation=True, max_length=128)

    # Ambil seluruh token embeddings (bukan hanya CLS token)
    outputs = bert_model(**tokens)
    embeddings = outputs.last_hidden_state  # shape (1, 128, 1024)

    input_data = embeddings.numpy().astype(np.float32)  # sesuai shape TFLite
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])

    label = np.argmax(output, axis=1)[0]
    emotions = ['anger', 'fear', 'sadness']
    return emotions[label]

# --- Keyword Extraction & Ranking ---
# Load rank keyword
df_rank_keyword = pd.read_excel(os.path.join(base_path, 'Keyword_KeyBERT.xlsx'))
df_rank_keyword['keyword'] = df_rank_keyword['keyword'].apply(process_text)
df_rank_keyword['new_rank'] = df_rank_keyword['rank'].max() - df_rank_keyword['rank'] + 1

def rank_keywords(row):
    total_ranking = 0
    total_keyword = 0
    for keyword in row:
        frekuensi_rank = df_rank_keyword.loc[df_rank_keyword['keyword'] == keyword]
        if not frekuensi_rank.empty:
            total_ranking += frekuensi_rank['new_rank'].values[0]
            total_keyword += 1
    if total_keyword > 0:
        return total_ranking / total_keyword
    else:
        return 0

def keyword(text):
    # Model Keyword
    sentence_model = SentenceTransformer("denaya/indoSBERT-large", trust_remote_code=True)

    # Buat objek KeyBERT
    kw_model = KeyBERT(model=sentence_model)

    # Proses Keyword
    stop_words = set(stopwords.words('indonesian'))
    text = text.split()
    text = [w for w in text if not w in stop_words]
    text = ' '.join(text)
    text = process_text(text)
    keywords = kw_model.extract_keywords(text, top_n=5)
    keyword = [keyword for keyword, _ in keywords]
    rank = rank_keywords(keyword)
    
    return keyword, rank
