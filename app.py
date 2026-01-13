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

def generate_srt(result):
    srt = ""
    idx = 1
    for segment in result["segments"]:
        words = segment.get("words", [])
        chunk = []
        for w in words:
            chunk.append(w)
            if len(chunk) == 7:
                srt += f"{idx}\n"
                srt += f"{format_time(chunk[0]['start'])} --> {format_time(chunk[-1]['end'])}\n"
                srt += " ".join(x["word"] for x in chunk) + "\n\n"
                idx += 1
                chunk = []
        if chunk:
            srt += f"{idx}\n"
            srt += f"{format_time(chunk[0]['start'])} --> {format_time(chunk[-1]['end'])}\n"
            srt += " ".join(x["word"] for x in chunk) + "\n\n"
            idx += 1
    return srt

def worker():
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    print("Whisper model loaded successfully!")

    while True:
        job = job_queue.get()
        job_id = job["id"]
        jobs[job_id]["status"] = "processing"

        try:
            videopath = job["video"]
            audiopath = os.path.splitext(videopath)[0] + ".wav"
            outputpath = job["output"]

            print(f"Processing job {job_id}...")

            # Extract audio
            video = VideoFileClip(videopath)
            video.audio.write_audiofile(audiopath, fps=16000, logger=None)
            video.close()

            # Transcribe
            result = model.transcribe(audiopath, word_timestamps=True)
            srt = generate_srt(result)

            # Save to file
            with open(outputpath, "w", encoding="utf-8") as f:
                f.write(srt)

            jobs[job_id]["status"] = "done"
            jobs[job_id]["srt"] = srt

            print(f"Job {job_id} completed successfully!")

            # Cleanup temporary files
            try:
                os.remove(videopath)
                os.remove(audiopath)
            except:
                pass

        except Exception as e:
            print(f"Worker error for job {job_id}: {e}")
            jobs[job_id]["status"] = "error"
            jobs[job_id]["error"] = str(e)

        finally:
            job_queue.task_done()


threading.Thread(target=worker, daemon=True).start()

@app.route("/upload", methods=['POST'])
def upload():
    print("Upload request received")
    
    if "video" not in request.files:
        print("No video file in request")
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    
    if file.filename == '':
        print("Empty filename")
        return jsonify({"error": "No file selected"}), 400

    job_id = str(uuid.uuid4())
    print(f"Created job ID: {job_id}")

    videopath = os.path.join(UPLOAD_DIR, f"{job_id}.mp4")
    outputpath = os.path.join(UPLOAD_DIR, f"{job_id}.srt")

    file.save(videopath)
    print(f"Video saved to: {videopath}")

    job = {"id": job_id, "video": videopath, "output": outputpath}
    jobs[job_id] = {"status": "queued", "output": outputpath}
    job_queue.put(job)
    
    print(f"Job {job_id} queued successfully")

    return jsonify({
        "message": "Video queued for processing",
        "job_id": job_id
    }), 200

@app.route("/result/<job_id>")
def result(job_id):
    print(f"Status check for job: {job_id}")
    
    if job_id not in jobs:
        print(f"Job {job_id} not found")
        return jsonify({"status": "error", "error": "Invalid job ID"}), 404

    job_status = jobs[job_id]["status"]
    print(f"Job {job_id} status: {job_status}")

    if job_status == "queued":
        queue_list = list(job_queue.queue)
        pos = next((i for i, j in enumerate(queue_list) if j["id"] == job_id), None)
        position = (pos + 1) if pos is not None else 0
        return jsonify({
            "status": "queued",
            "position": position,
            "message": f"Waiting in queue (Position: {position})"
        }), 200

    elif job_status == "processing":
        return jsonify({
            "status": "processing",
            "message": "Processing your video..."
        }), 200

    elif job_status == "done":
        print(f"Job {job_id} completed, returning SRT")
        return jsonify({
            "status": "done",
            "srt": jobs[job_id]["srt"],
            "message": "Captions generated successfully!"
        }), 200

    elif job_status == "error":
        return jsonify({
            "status": "error",
            "error": jobs[job_id].get("error", "Unknown error occurred")
        }), 200

    return jsonify({"status": "unknown"}), 200

if __name__ == "__main__":
    print("Starting Caption Generator Server...")
    print("Server will run on http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
