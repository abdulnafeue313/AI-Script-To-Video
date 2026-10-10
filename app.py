# ============================================
# Script2Video AI - Flask Web Server
# ============================================

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import config
from video_generator import create_animated_video


app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB max


# ---------- ROUTES ----------

@app.route("/")
def home():
    """Main page."""
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    """Video generate karo (AI images + AI voice)."""
    try:
        data = request.json
        script = data.get("script", "").strip()
        language = data.get("language", "ur")
        style = data.get("style", "cinematic")
        video_name = data.get("video_name", "video.mp4")
        voice_source = data.get("voice_source", "ai")
        video_source = data.get("video_source", "ai")
        
        if not script:
            return jsonify({"success": False, "message": "Script khali hai!"})
        
        if len(script) < 10:
            return jsonify({"success": False, "message": "Script bohot chhota hai!"})
        
        output_path = f"output/{video_name}"
        
        print(f"\n🎬 Video generate: {video_name}")
        print(f"🎙️ Voice: {voice_source} | 📹 Video: {video_source}")
        
        create_animated_video(
            script=script,
            language=language,
            output_path=output_path,
            style=style,
            width=1920,
            height=1080,
            api_key=config.POLLINATIONS_API_KEY,
            voice_source=voice_source
        )
        
        return jsonify({
            "success": True,
            "message": "Video ready!",
            "video_path": f"/output/{video_name}"
        })
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"})


@app.route("/upload_voice", methods=["POST"])
def upload_voice():
    """User ki voice upload karo."""
    try:
        if "voice_file" not in request.files:
            return jsonify({"success": False, "message": "Koi file nahi mili!"})
        
        file = request.files["voice_file"]
        
        if file.filename == "":
            return jsonify({"success": False, "message": "File khali hai!"})
        
        allowed = {"mp3", "wav", "m4a", "ogg"}
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        
        if ext not in allowed:
            return jsonify({"success": False, "message": f"Sirf {', '.join(allowed)} allowed hain!"})
        
        os.makedirs("uploads", exist_ok=True)
        upload_path = f"uploads/user_voice.{ext}"
        file.save(upload_path)
        
        print(f"✅ Voice upload: {upload_path}")
        
        return jsonify({
            "success": True,
            "message": "Voice upload ho gayi!",
            "voice_path": upload_path
        })
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"})


@app.route("/upload_videos", methods=["POST"])
def upload_videos():
    """User ki videos upload karo."""
    try:
        if "video_files" not in request.files:
            return jsonify({"success": False, "message": "Koi file nahi mili!"})
        
        files = request.files.getlist("video_files")
        allowed = {"mp4", "mov", "avi", "mkv"}
        saved_paths = []
        
        os.makedirs("uploads/videos", exist_ok=True)
        
        for file in files:
            if file.filename == "":
                continue
            
            ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
            
            if ext not in allowed:
                continue
            
            save_path = f"uploads/videos/{file.filename}"
            file.save(save_path)
            saved_paths.append(save_path)
            print(f"✅ Video upload: {save_path}")
        
        if not saved_paths:
            return jsonify({"success": False, "message": "Koi valid video nahi mili!"})
        
        return jsonify({
            "success": True,
            "message": f"{len(saved_paths)} videos upload ho gayi!",
            "video_paths": saved_paths
        })
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"})


@app.route("/generate_with_voice", methods=["POST"])
def generate_with_voice():
    """Video generate karo uploaded voice ke saath."""
    try:
        data = request.json
        script = data.get("script", "").strip()
        style = data.get("style", "cinematic")
        video_name = data.get("video_name", "video.mp4")
        voice_path = data.get("voice_path", "")
        video_source = data.get("video_source", "ai")
        video_paths = data.get("video_paths", [])
        
        if not script:
            return jsonify({"success": False, "message": "Script khali hai!"})
        
        if not voice_path or not os.path.exists(voice_path):
            return jsonify({"success": False, "message": "Voice file nahi mili!"})
        
        output_path = f"output/{video_name}"
        
        print(f"\n🎬 Video generate (uploaded voice)")
        
        create_animated_video(
            script=script,
            language="ur",
            output_path=output_path,
            style=style,
            width=1920,
            height=1080,
            api_key=config.POLLINATIONS_API_KEY,
            voice_source="upload",
            uploaded_voice_path=voice_path
        )
        
        return jsonify({
            "success": True,
            "message": "Video ready!",
            "video_path": f"/output/{video_name}"
        })
    
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})


@app.route("/output/<path:filename>")
def download_video(filename):
    """Video download karo."""
    return send_from_directory("output", filename)


# ---------- RUN ----------

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("uploads/videos", exist_ok=True)
    
    print("\n" + "=" * 50)
    print("🎬 Script2Video AI - Web Server")
    print("=" * 50)
    print("🌐 Browser mein kholo: http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)