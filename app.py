import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import threading
from queue import Queue
from moviepy.video.io.VideoFileClip import VideoFileClip
import whisper

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

job_queue = Queue()
jobs = {}  # Track job status

def format_time(t):
    ms = int((t - int(t)) * 1000)
    s = int(t)
    h = s // 3600
    m = (s % 3600) // 60
    s = s % 60
    return f"{h:02}:{m:02}:{s:02},{ms:03}"
