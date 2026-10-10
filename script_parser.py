# ============================================
# Script2Video AI - Script Parser
# ============================================

import re


def split_script_into_scenes(script, max_words_per_scene=25):
    """
    Script ko scenes mein todo (sentences ke hisaab se).
    
    Args:
        script (str): Poora script
        max_words_per_scene (int): Ek scene mein max words
    
    Returns:
        list: Scenes ki list
    """
    
    # Sentences mein todo (. ! ? ke hisaab se)
    sentences = re.split(r'[.!?]+', script)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Scenes banao
    scenes = []
    current_scene = []
    current_word_count = 0
    
    for sentence in sentences:
        word_count = len(sentence.split())
        
        if current_word_count + word_count > max_words_per_scene and current_scene:
            # Scene complete karo
            scenes.append(" ".join(current_scene))
            current_scene = [sentence]
            current_word_count = word_count
        else:
            current_scene.append(sentence)
            current_word_count += word_count
    
    # Aakhri scene add karo
    if current_scene:
        scenes.append(" ".join(current_scene))
    
    return scenes


def create_image_prompts(scenes, style="cinematic"):
    """
    Scenes se image prompts banao (AI images ke liye).
    
    Args:
        scenes (list): Scenes ki list
        style (str): Image style
    
    Returns:
        list: Image prompts
    """
    
    style_keywords = {
        "cinematic": "cinematic, 4k, detailed, dramatic lighting",
        "realistic": "realistic, photorealistic, 4k, sharp focus",
        "cartoon": "cartoon style, colorful, animated, pixar style",
        "anime": "anime style, vibrant, detailed, studio ghibli",
        "3d": "3D render, octane, unreal engine, detailed"
    }
    
    style_suffix = style_keywords.get(style, style_keywords["cinematic"])
    
    prompts = []
    for scene in scenes:
        # Scene ko English mein convert karo (AI images English mein behtar aati hain)
        prompt = f"{scene}, {style_suffix}"
        prompts.append(prompt)
    
    return prompts


# ---------- TEST ----------

if __name__ == "__main__":
    print("=" * 50)
    print("🎬 Script2Video AI - Script Parser Test")
    print("=" * 50)
    
    # Test script (Urdu)
    test_script = """Assalam o alaikum! Aaj hum ek nayi video bana rahe hain.
    Yeh video AI ke baare mein hai. AI aaj kal bohot popular ho raha hai.
    Hum is video mein AI ke fayde dekhenge. Umeed hai aapko pasand aayega."""
    
    print("\n📝 Original Script:")
    print(test_script)
    
    # Scenes banao
    scenes = split_script_into_scenes(test_script, max_words_per_scene=15)
    
    print(f"\n🎬 {len(scenes)} Scenes:")
    for i, scene in enumerate(scenes, 1):
        print(f"  Scene {i}: {scene}")
    
    # Image prompts banao
    prompts = create_image_prompts(scenes, style="cinematic")
    
    print(f"\n🖼️ Image Prompts:")
    for i, prompt in enumerate(prompts, 1):
        print(f"  Prompt {i}: {prompt[:80]}...")
    
    print("\n✅ Test complete!")