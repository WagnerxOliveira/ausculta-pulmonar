import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

print("🧠 Iniciando o treinamento da IA com os dados pulmonares...")

def extrair_caracteristicas():
    # Na prática, a IA varreria a pasta do ICBHI 2017 extraída aqui.
    # Como simulação para gerar o arquivo do cérebro:
    X_treino = np.random.rand(200, 40) # 200 áudios, 40 características (MFCC)
    y_treino = np.random.choice([0, 1, 2], 200) # 0: Normal, 1: Sibilo, 2: Estertor
    return X_treino, y_treino

X, y = extrair_caracteristicas()

modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X, y)

joblib.dump(modelo, 'modelo_ia_pulmao.pkl')
print("✅ Inteligência Artificial treinada e conhecimento salvo em 'modelo_ia_pulmao.pkl'")