from flask import Flask, request, jsonify
from flask_cors import CORS
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os
import joblib
import librosa

app = Flask(__name__)
CORS(app)

PASTA_AUDIOS = "audios_gravados"
os.makedirs(PASTA_AUDIOS, exist_ok=True)

def obter_proximo_nome_audio():
    """Garante a nomenclatura: audio1.wav, audio2.wav..."""
    arquivos = [f for f in os.listdir(PASTA_AUDIOS) if f.startswith('audio') and f.endswith('.wav')]
    return f"audio{len(arquivos) + 1}.wav"

@app.route('/api/capturar', methods=['POST'])
def capturar_audio():
    """Grava o áudio direto do hardware isolado"""
    nome_arquivo = obter_proximo_nome_audio()
    caminho = os.path.join(PASTA_AUDIOS, nome_arquivo)
    
    taxa_amostragem = 44100
    duracao = 10  
    
    try:
        audio_bruto = sd.rec(int(duracao * taxa_amostragem), samplerate=taxa_amostragem, channels=1, dtype='float32')
        sd.wait()
        audio_amplificado = np.clip(audio_bruto * 15.0, -1.0, 1.0) # Amplifica o som do pulmão
        write(caminho, taxa_amostragem, audio_amplificado)
        return jsonify({"status": "sucesso", "arquivo": nome_arquivo})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route('/api/analisar', methods=['POST'])
def analisar_audio():
    """Carrega a IA e compara o áudio recebido com o aprendizado"""
    arquivo_nome = request.json.get('arquivo')
    caminho = os.path.join(PASTA_AUDIOS, arquivo_nome)
    
    try:
        modelo = joblib.load('cerebro_pulmao.pkl')
        audio, sr = librosa.load(caminho, sr=22050)
        mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40).T, axis=0).reshape(1, -1)
        
        predicao = modelo.predict(mfccs)[0]
        probabilidade = np.max(modelo.predict_proba(mfccs)) * 100
        
        laudos = {
            0: "Pulmão Limpo (Padrão Vesicular Normal)",
            1: "Anomalia: Possível Sibilo detectado",
            2: "Anomalia: Possível Estertor detectado"
        }
        
        return jsonify({
            "diagnostico": laudos[predicao],
            "precisao": f"{probabilidade:.1f}%"
        })
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)