# ============================================
# Script2Video AI - Video Generator with Voice Options
# ============================================

from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
import os
import config
from voice_generator import generate_voice, use_uploaded_voice, get_voice_duration
from image_generator import generate_ai_image
from script_parser import split_script_into_scenes, create_image_prompts


def create_animated_clip(image_path, duration, animation="zoom_in"):
    """Image ko animated clip banao."""
    clip = ImageClip(image_path).set_duration(duration)
    
    if animation == "zoom_in":
        clip = clip.resize(lambda t: 1 + 0.15 * (t / duration))
    elif animation == "zoom_out":
        clip = clip.resize(lambda t: 1.15 - 0.15 * (t / duration))
    elif animation == "pan_left":
        clip = clip.set_position(lambda t: (100 - 200 * (t / duration), 'center'))
    elif animation == "pan_right":
        clip = clip.set_position(lambda t: (-100 + 200 * (t / duration), 'center'))
    
    return clip


def create_animated_video(script, language="ur", output_path="output/video.mp4",
                          style="cinematic", width=1920, height=1080, api_key=None,
                          voice_source="ai", uploaded_voice_path=None):
    """
    Script se animated video banao (voice options ke saath).
    
    Args:
        voice_source (str): "ai" (gTTS) ya "upload" (user ki voice)
        uploaded_voice_path (str): Uploaded voice file (agar voice_source="upload")
    """
    
    print("\n" + "=" * 50)
    print("🎬 Script2Video AI - Animated Video Generator")
    print("=" * 50)
    
    # Folders
    os.makedirs("output", exist_ok=True)
    os.makedirs("temp", exist_ok=True)
    os.makedirs("output/scenes", exist_ok=True)
    
    # Step 1: Voice banao (AI ya Upload)
    print(f"\n📍 Step 1: Voice ({'AI' if voice_source == 'ai' else 'Uploaded'})")
    voice_path = "temp/voice.mp3"
    
    if voice_source == "upload" and uploaded_voice_path:
        use_uploaded_voice(uploaded_voice_path, voice_path)
    else:
        generate_voice(script, language, voice_path)
    
    duration = get_voice_duration(voice_path)
    print(f"📊 Total video duration: {duration:.2f} seconds")
    
    # Step 2: Scenes
    print("\n📍 Step 2: Script ko scenes mein toda ja raha hai...")
    scenes = split_script_into_scenes(script, max_words_per_scene=15)
    print(f"🎬 {len(scenes)} scenes bane")
    
    # Step 3: AI images
    print("\n📍 Step 3: AI images generate ho rahi hain...")
    prompts = create_image_prompts(scenes, style=style)
    
    image_paths = []
    for i, prompt in enumerate(prompts, 1):
        print(f"\n📸 Image {i}/{len(prompts)}")
        img_path = f"output/scenes/scene_{i}.jpg"
        image_path = generate_ai_image(
            prompt=prompt, output_path=img_path,
            width=width, height=height, api_key=api_key
        )
        if image_path:
            image_paths.append(image_path)
    
    # Step 4: Animation
    print("\n📍 Step 4: Animation add ho rahi hai...")
    scene_duration = duration / len(image_paths)
    animations = ["zoom_in", "zoom_out", "pan_left", "pan_right", "static"]
    
    clips = []
    for i, img_path in enumerate(image_paths):
        animation = animations[i % len(animations)]
        print(f"  Scene {i+1}: {animation}")
        clip = create_animated_clip(img_path, scene_duration, animation)
        clips.append(clip)
    
    # Step 5: Video jodo
    print("\n📍 Step 5: Video ban raha hai...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    audio_clip = AudioFileClip(voice_path)
    final_video = final_video.set_audio(audio_clip)
    
    # Save
    print("💾 Video save ho raha hai...")
    final_video.write_videofile(
        output_path, fps=24,
        codec="libx264", audio_codec="aac",
        audio_bitrate="192k",
        verbose=False, logger=None,
        temp_audiofile="temp/temp_audio.m4a",
        remove_temp=True
    )
    
    # Cleanup
    final_video.close()
    audio_clip.close()
    for clip in clips:
        clip.close()
    
    print(f"\n✅ Video ready: {output_path}")
    return output_path


# ---------- TEST ----------

if __name__ == "__main__":
    test_script = """Assalam o alaikum! Aaj hum ek nayi video bana rahe hain.
    Yeh video AI ke baare mein hai. AI aaj kal bohot popular ho raha hai."""
    
    API_KEY = getattr(config, "POLLINATIONS_API_KEY", None)
    
    video_path = create_animated_video(
        script=test_script,
        language="ur",
        output_path="output/animated_video.mp4",
        style="cinematic",
        width=1920, height=1080,
        api_key=API_KEY,
        voice_source="ai"
    )
    
    print("\n✅ Test complete!")