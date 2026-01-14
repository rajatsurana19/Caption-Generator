<!-- badges (Build / PyPI / License) -->
[![Python](https://img.shields.io/badge/python-%3E%3D3.8-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-v2.x-green)](https://flask.palletsprojects.com/)


# Caption-Generator

**Caption-Generator** is a lightweight web application that uses OpenAI’s **Whisper** speech-to-text model to generate captions (transcriptions) from uploaded media  video, etc. The project features a simple **Flask** API backend and a minimal **HTML/CSS/JS** frontend interface for uploading files and viewing captions.

This is ideal for building quick speech recognition tools, subtitling helpers, or integrating Whisper into existing apps.

---

## 🧠 What the Project Does

Caption-Generator lets users upload audio/video files and returns accurate captions using the Whisper model. On the backend, a Flask server loads Whisper and processes uploads. The frontend provides a simple upload form and displays [generated text].

**Key Capabilities**
- Upload media files via a browser form
- Transcribe contents using Whisper
- Display captions on the frontend
- Simple and extensible architecture

---

## ✨ Why This Project Is Useful

This project is useful for developers who want:
- A **ready-to-use Whisper package** in Python + Flask
- A base for adding features like subtitle export, language selection, or streaming transcription

Typical benefits:
- Works out of the box with Whisper’s models
- Easy to customize and extend
- Demonstrates full stack integration

---

## 🚀 Getting Started

These instructions will get you a local copy up and running.

### 💾 Prerequisites

Make sure you have:

```bash
python >= 3.8
git
ffmpeg
```

## 📦 Installation

### Clone the repository
```bash
git clone https://github.com/rajatsurana19/Caption-generator.git
cd Caption-generator
```

## Create & activate a Python virtual environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```
## Install dependencies
```bash
pip install -r requirements.txt
```

## 🖥 Backend (Flask)

### Start the Flask server:
```bash
export FLASK_APP=app.py
flask run
```

## 🔗 Connect with Me

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rajatsurana19)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rajat-surana/)

