from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import joblib
import sqlite3
import librosa
import time

app = Flask(__name__)
CORS(app)

PASTA_AUDIOS = "audios_gravados"
os.makedirs(PASTA_AUDIOS, exist_ok=True)

# --- BANCO DE DADOS (SQLite) ---
def iniciar_banco():
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY, login TEXT UNIQUE, senha TEXT, perfil TEXT)''')
    # Cria usuários de teste apenas se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        senhas_seguras = [generate_password_hash("medico123"), generate_password_hash("enf123"), generate_password_hash("paciente123")]
        cursor.execute("INSERT INTO usuarios (login, senha, perfil) VALUES ('crm1234', ?, 'medico')", (senhas_seguras[0],))
        cursor.execute("INSERT INTO usuarios (login, senha, perfil) VALUES ('coren5678', ?, 'enfermeiro')", (senhas_seguras[1],))
        cursor.execute("INSERT INTO usuarios (login, senha, perfil) VALUES ('111.111.111-11', ?, 'paciente')", (senhas_seguras[2],))
        conn.commit()
    conn.close()

iniciar_banco()

# --- ROTAS DE API ---
@app.route('/api/login', methods=['POST'])
def login():
    dados = request.json
    conn = sqlite3.connect('hospital.db')
    cursor = conn.cursor()
    cursor.execute("SELECT senha, perfil FROM usuarios WHERE login=?", (dados['login'],))
    usuario = cursor.fetchone()
    conn.close()

    if usuario and check_password_hash(usuario[0], dados['senha']):
        return jsonify({"status": "sucesso", "perfil": usuario[1]})
    return jsonify({"status": "erro", "mensagem": "Credenciais inválidas"}), 401

@app.route('/api/capturar', methods=['POST'])
def capturar():
    arquivos = [f for f in os.listdir(PASTA_AUDIOS) if f.startswith('audio') and f.endswith('.wav')]
    nome_arquivo = f"audio{len(arquivos) + 1}.wav"
    caminho = os.path.join(PASTA_AUDIOS, nome_arquivo)
    
    try:
        audio_bruto = sd.rec(int(10 * 44100), samplerate=44100, channels=1, dtype='float32')
        sd.wait()
        write(caminho, 44100, np.clip(audio_bruto * 15.0, -1.0, 1.0))
        return jsonify({"status": "sucesso", "arquivo": nome_arquivo})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/api/analisar', methods=['POST'])
def analisar():
    arquivo_nome = request.json.get('arquivo')
    caminho = os.path.join(PASTA_AUDIOS, arquivo_nome)
    
    try:
        modelo = joblib.load('modelo_ia_pulmao.pkl')
        audio, sr = librosa.load(caminho, sr=22050)
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0).reshape(1, -1)
        
        predicao = modelo.predict(mfccs)[0]
        precisao = np.max(modelo.predict_proba(mfccs)) * 100
        
        laudos = {0: "Padrão Vesicular Normal", 1: "Sibilos (Possível Obstrução)", 2: "Estertores (Possível Secreção)"}
        return jsonify({"diagnostico": laudos[predicao], "precisao": f"{precisao:.1f}%"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)