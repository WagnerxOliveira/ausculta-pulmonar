# 🫁 Ausculta Pulmonar Inteligente (IA & Telemedicina)

Sistema de Suporte à Decisão Clínica (CDSS) com hardware customizado e Inteligência Artificial para análise de sons pulmonares.

⚠️ **Aviso:** Este projeto é uma ferramenta auxiliar. Não substitui o diagnóstico de um médico qualificado.

---

## 🛠️ Especificações de Hardware
- **Auscultador:** Campânula isolada (fechada) e diafragma ativo focado na pele.
- **Sensor:** Microfone Boya BY-M1 encapsulado na câmara acústica.
- **Isolamento Acústico:** Mangueira de 5cm vedada nas extremidades com fita de autofusão e fita isolante para bloquear ruídos e vazamentos de ar externos.

---

## 💻 Arquitetura do Software

### 1. Base de Dados (Dataset)
Para o treinamento da Inteligência Artificial (Machine Learning), utilizamos o padrão ouro em pesquisa respiratória: o **ICBHI 2017 Respiratory Sound Database**.
* **Sobre o Dataset:** Contém centenas de gravações clínicas reais com marcações exatas de anomalias como sibilos e estertores.
* **Link para Download:** [Baixar ICBHI 2017 via Kaggle](https://www.kaggle.com/datasets/vbookshelf/respiratory-sound-database)

### 2. Back-End (A "Ponte" do Sistema)
O servidor foi desenvolvido em **Python** utilizando o microframework **Flask**. O script principal (`app.py`) atua como o "garçom" do sistema: ele gerencia a captação física do microfone Boya, salva os arquivos `.wav` localmente, valida as requisições de CPF e roda o modelo de Machine Learning para retornar o laudo ao Front-End.

**Como instalar e rodar no VS Code:**
1. Abra o terminal integrado do VS Code (`Ctrl` + `'`).
2. Certifique-se de estar na pasta raiz do projeto (`ausculta_pulmonar`).
3. Instale todas as bibliotecas e dependências matemáticas necessárias executando o comando abaixo:
   ```bash
   pip install flask flask-cors sounddevice scipy numpy joblib librosa scikit-learn