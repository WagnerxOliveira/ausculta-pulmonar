# 🫁 Ausculta Pulmonar Inteligente (IA & Telemedicina)

Sistema de Suporte à Decisão Clínica (CDSS) com hardware customizado e Inteligência Artificial para análise de sons pulmonares.

⚠️ **Aviso:** Este projeto é uma ferramenta auxiliar. Não substitui o diagnóstico de um médico qualificado.

## 🛠️ Especificações de Hardware
- **Auscultador:** Campânula isolada (fechada) e diafragma ativo.
- **Sensor:** Microfone Boya BY-M1 encapsulado.
- **Isolamento Acústico:** Mangueira de 5cm vedada nas extremidades com fita de autofusão para bloquear ruídos externos.

## 💻 Arquitetura do Software
- **Front-End:** Interface HTML/JS com controle de acesso por perfis (Médico, Enfermeiro, Paciente). Visualização de ondas sonoras via WaveSurfer.js.
- **Back-End (API):** Flask (Python) responsável pela captação física do áudio e gerenciamento de arquivos.
- **Machine Learning (ML):** Modelo treinado com o dataset ICBHI 2017 utilizando extração de características MFCC (Mel-Frequency Cepstral Coefficients) para classificação de anomalias respiratórias.