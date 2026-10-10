# ============================================
# Script2Video AI - Voice Generator (gTTS + Upload)
# ============================================

from gtts import gTTS
import os
import shutil
import config


def generate_voice(text, language="ur", output_path="output/voice.mp3"):
    """
    Text ko AI voice mein convert karo (gTTS).
    """
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    lang_map = {
        "ur": "ur", "en": "en", "hi": "hi",
        "urdu": "ur", "english": "en", "hindi": "hi"
    }
    lang_code = lang_map.get(language.lower(), "ur")
    
    try:
        print(f"🎙️ AI Voice generate ho rahi hai ({lang_code})...")
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(output_path)
        print(f"✅ AI Voice ready: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ Voice generate nahi hui: {e}")
        return None


def use_uploaded_voice(uploaded_file_path, output_path="temp/voice.mp3"):
    """
    User ki uploaded voice use karo.
    
    Args:
        uploaded_file_path (str): Uploaded MP3/WAV file ka path
        output_path (str): Kahan copy karni hai
    
    Returns:
        str: Voice file ka path
    """
    
    try:
        print(f"🎙️ Uploaded voice use ho rahi hai...")
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # File copy karo
        shutil.copy(uploaded_file_path, output_path)
        
        print(f"✅ Uploaded voice ready: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ Uploaded voice use nahi hui: {e}")
        return None


def get_voice_duration(mp3_path):
    """
    MP3 file ki duration (seconds) nikalo.
    """
    try:
        from moviepy.editor import AudioFileClip
        audio = AudioFileClip(mp3_path)
        duration = audio.duration
        audio.close()
        return duration
    except Exception as e:
        print(f"⚠️ Duration nahi mili: {e}")
        return 0


# ---------- TEST ----------

if __name__ == "__main__":
    print("=" * 50)
    print("🎬 Script2Video AI - Voice Generator Test")
    print("=" * 50)
    
    # AI Voice test
    urdu_text = "Assalam o alaikum! Yeh Script2Video AI ka test hai."
    urdu_file = generate_voice(urdu_text, "ur", "output/test_urdu.mp3")
    
    if urdu_file:
        duration = get_voice_duration(urdu_file)
        print(f"📊 Duration: {duration:.2f} seconds")
    print("\n✅ Test complete!")