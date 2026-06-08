# 🫁 Ausculta Pulmonar Digital: Sistema de Suporte à Decisão Clínica Suportado por IA

Este repositório contém a implementação de um Sistema de Suporte à Decisão Clínica (CDSS - *Clinical Decision Support System*). O projeto integra engenharia de hardware acústico customizado e algoritmos de aprendizado de máquina (Machine Learning) para a captação, processamento de sinais e inferência de anomalias em sons respiratórios (sibilos e estertores).

⚠️ **AVISO CLÍNICO INSTITUCIONAL:** Este software é um artefato computacional de triagem e segunda opinião técnica. Em conformidade com as normas de telemedicina, a ferramenta **não emite diagnósticos médicos autônomos**, devendo ser utilizada estritamente como apoio à decisão do profissional de saúde qualificado.

---

## 🛠️ Stack Tecnológico e Ferramentas

O ecossistema do projeto foi construído utilizando as seguintes tecnologias:

### Back-End e Processamento de Sinais
* **Linguagem:** Python 3.x
* **Framework Web:** Flask (com `flask-cors` para controle de origem transversal).
* **Processamento de Áudio:** `sounddevice` (captura em baixo nível via PortAudio) e `scipy.io.wavfile` (I/O de arquivos PCM WAV sem perdas).
* **Engenharia de Features:** `librosa` (extração de vetores MFCC - *Mel-Frequency Cepstral Coefficients*).
* **Machine Learning:** `scikit-learn` (classificador *Random Forest* para inferência não linear).
* **Segurança e Banco de Dados:** SQLite3 (banco relacional nativo) e `werkzeug.security` (funções de hash SHA-256 para criptografia de senhas).

### Front-End e Interface
* **Linguagens:** HTML5, CSS3 e Vanilla JavaScript (ES6+).
* **Visualização de Dados:** `WaveSurfer.js` (renderização de oscilogramas em canvas HTML).

### Engenharia de Hardware (Sensor de Captação)
* **Receptor Acústico:** Auscultador com campânula isolada e diafragma focado.
* **Transdutor:** Microfone omnidirecional Boya BY-M1.
* **Câmara Acústica:** Tubo polimérico (5cm) blindado com fita de autofusão de silicone, garantindo isolamento acústico contra ruídos externos e vazamentos de pressão atmosférica.

---

## ⚙️ Instalação e Configuração do Ambiente

Siga as diretrizes abaixo para provisionar o ambiente de desenvolvimento local via terminal (CLI).

**1. Clonagem do Repositório**
```bash
git clone [https://github.com/WagnerxOliveira/ausculta-pulmonar.git](https://github.com/WagnerxOliveira/ausculta-pulmonar.git)
cd ausculta-pulmonar