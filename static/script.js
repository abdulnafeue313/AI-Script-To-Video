// ============================================
// Script2Video AI - Frontend Logic
// ============================================

let selectedVoice = "ai";
let uploadedVoicePath = "";
let selectedVideoSource = "ai";
let uploadedVideoPaths = [];

// Character counter
document.getElementById("script").addEventListener("input", function() {
    document.getElementById("charCount").textContent = 
        this.value.length + " characters";
});

// Voice option select karo
function selectVoice(type) {
    selectedVoice = type;
    
    document.getElementById("voiceAI").classList.remove("active");
    document.getElementById("voiceUpload").classList.remove("active");
    
    if (type === "ai") {
        document.getElementById("voiceAI").classList.add("active");
        document.getElementById("uploadArea").style.display = "none";
    } else {
        document.getElementById("voiceUpload").classList.add("active");
        document.getElementById("uploadArea").style.display = "block";
    }
}

// Video source select karo
function selectVideoSource(type) {
    selectedVideoSource = type;
    
    document.getElementById("videoAI").classList.remove("active");
    document.getElementById("videoUpload").classList.remove("active");
    
    if (type === "ai") {
        document.getElementById("videoAI").classList.add("active");
        document.getElementById("videoUploadArea").style.display = "none";
    } else {
        document.getElementById("videoUpload").classList.add("active");
        document.getElementById("videoUploadArea").style.display = "block";
    }
}

// Voice upload karo
function uploadVoice() {
    const fileInput = document.getElementById("voiceFile");
    const file = fileInput.files[0];
    
    if (!file) return;
    
    const formData = new FormData();
    formData.append("voice_file", file);
    
    document.getElementById("uploadText").textContent = "⏳ Upload ho rahi hai...";
    document.getElementById("uploadStatus").textContent = "";
    
    fetch("/upload_voice", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadedVoicePath = data.voice_path;
            document.getElementById("uploadText").textContent = "✅ " + file.name;
            document.getElementById("uploadStatus").textContent = 
                "Voice ready! Ab video generate karo.";
        } else {
            document.getElementById("uploadText").textContent = "❌ Upload fail";
            document.getElementById("uploadStatus").textContent = data.message;
        }
    })
    .catch(error => {
        document.getElementById("uploadText").textContent = "❌ Error";
        document.getElementById("uploadStatus").textContent = error.message;
    });
}

// Videos upload karo
function uploadVideo() {
    const fileInput = document.getElementById("videoFile");
    const files = fileInput.files;
    
    if (files.length === 0) return;
    
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("video_files", files[i]);
    }
    
    document.getElementById("videoUploadText").textContent = "⏳ Upload ho rahi hain...";
    document.getElementById("videoUploadStatus").textContent = "";
    
    fetch("/upload_videos", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            uploadedVideoPaths = data.video_paths;
            document.getElementById("videoUploadText").textContent = 
                "✅ " + files.length + " videos upload ho gayi";
            document.getElementById("videoUploadStatus").textContent = 
                "Ab video generate karo.";
        } else {
            document.getElementById("videoUploadText").textContent = "❌ Upload fail";
            document.getElementById("videoUploadStatus").textContent = data.message;
        }
    })
    .catch(error => {
        document.getElementById("videoUploadText").textContent = "❌ Error";
        document.getElementById("videoUploadStatus").textContent = error.message;
    });
}

// Video generate karo
function generateVideo() {
    const script = document.getElementById("script").value.trim();
    const language = document.getElementById("language").value;
    const style = document.getElementById("style").value;
    const videoName = document.getElementById("videoName").value.trim() || "video.mp4";

    if (!script) {
        showStatus("error", "❌ Pehle script likho!");
        return;
    }

    if (script.length < 10) {
        showStatus("error", "❌ Script bohot chhota hai!");
        return;
    }

    if (selectedVoice === "upload" && !uploadedVoicePath) {
        showStatus("error", "❌ Pehle voice upload karo!");
        return;
    }

    if (selectedVideoSource === "upload" && uploadedVideoPaths.length === 0) {
        showStatus("error", "❌ Pehle videos upload karo!");
        return;
    }

    const btn = document.getElementById("generateBtn");
    btn.disabled = true;
    btn.textContent = "⏳ Video ban rahi hai...";

    showStatus("loading", "⏳ Video ban rahi hai... (1-2 minute lag sakte hain)");
    document.getElementById("videoResult").style.display = "none";

    // Route choose karo
    let url = "/generate";
    let body = {
        script: script,
        language: language,
        style: style,
        video_name: videoName,
        voice_source: selectedVoice,
        video_source: selectedVideoSource
    };

    if (selectedVoice === "upload") {
        url = "/generate_with_voice";
        body = {
            script: script,
            style: style,
            video_name: videoName,
            voice_path: uploadedVoicePath,
            video_source: selectedVideoSource,
            video_paths: uploadedVideoPaths
        };
    }

    fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showStatus("success", "✅ " + data.message);
            
            const videoPlayer = document.getElementById("videoPlayer");
            videoPlayer.src = data.video_path;
            
            document.getElementById("downloadLink").href = data.video_path;
            document.getElementById("downloadLink").download = videoName;
            
            document.getElementById("videoResult").style.display = "block";
        } else {
            showStatus("error", "❌ " + data.message);
        }
    })
    .catch(error => {
        showStatus("error", "❌ Server error: " + error.message);
    })
    .finally(() => {
        btn.disabled = false;
        btn.textContent = "✨ Generate Luxury Video";
    });
}

// Status dikhao
function showStatus(type, message) {
    const status = document.getElementById("status");
    status.className = "status " + type;
    status.textContent = message;
}