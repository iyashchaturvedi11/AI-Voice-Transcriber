# 🎙️ AI Voice Transcriber

**A beautiful, fast, and powerful voice-to-text web app** built with **Streamlit** and **OpenAI Whisper**.

Record your voice directly from the browser or upload an audio file and get instant, high-accuracy transcriptions with support for multiple languages and output formats.

![Demo](https://via.placeholder.com/800x400/1E3A8A/FFFFFF?text=AI+Voice+Transcriber+Demo)  
*(Add a GIF or screenshot here after deployment)*

---

## ✨ Features

- 🎤 **Live Voice Recording** — Record directly from your microphone
- 📁 **File Upload Support** — Works with mp3, wav, m4a, mp4, webm, etc.
- 🌍 **Multi-language Support** — Auto-detect + 9 popular languages (English, Hindi, French, Spanish, German, Arabic, Chinese, Japanese, Portuguese)
- 📄 **Multiple Output Formats** — Plain text, SRT, VTT, and Verbose JSON
- 🎛️ **Advanced Options** — Temperature control for creativity vs accuracy
- ⚡ **Fast & Clean UI** — Modern, responsive design with custom styling
- 📥 **Easy Download** — Download transcriptions instantly
- 🔐 **Secure API Key Handling** via `.env`

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Audio Recording**: streamlit-audiorecorder
- **Transcription**: OpenAI Whisper (`whisper-1`)
- **Backend**: Python 3
- **Environment**: dotenv

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-voice-transcriber.git
cd ai-voice-transcriber

 Set Up Environment Variables
Create a .env file in the root directory:
envOPENAI_API_KEY=sk-your-openai-api-key-here
Get your API key from OpenAI Platform


 Run the App
Bashstreamlit run app.py

📦 Installation (requirements.txt)
Create a requirements.txt file with the following content:
txtstreamlit
openai
python-dotenv
streamlit-audiorecorder
pydub
Note: pydub is required by streamlit-audiorecorder for audio handling.

🎯 How to Use

Record Voice Tab: Click "Start Recording" → Speak → "Stop Recording"
Upload File Tab: Drag & drop or select an audio file (max 25MB)
Configure Options in the sidebar:
Choose language (or Auto-detect)
Select output format (text, srt, vtt, verbose_json)
Adjust temperature

Click 🚀 Transcribe



🌟 Why This Project?

Clean and production-ready code
Excellent user experience
Supports both casual users and developers
Easy to extend (add translation, summarization, speaker diarization, etc.
