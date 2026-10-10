# ============================================
# Script2Video AI - AI Image Generator (Pollinations)
# ============================================

from PIL import Image, ImageDraw
import os
import requests
import config


def generate_ai_image(prompt, output_path, width=1920, height=1080, 
                      model="flux", api_key=None):
    """
    Pollinations.ai se AI image generate karo.
    
    Args:
        prompt (str): Image ka description
        output_path (str): Kahan save karna hai
        width (int): Image width
        height (int): Image height
        model (str): "flux", "turbo", "zimage"
        api_key (str): Pollinations API key (optional)
    
    Returns:
        str: Image file ka path
    """
    
    # URL encode karo
    from urllib.parse import quote
    encoded_prompt = quote(prompt)
    
    # Naya URL (gen.pollinations.ai)
    url = f"https://gen.pollinations.ai/image/{encoded_prompt}"
    
    # Parameters
    params = {
        "width": width,
        "height": height,
        "model": model,
        "nologo": "true",
        "enhance": "true"
    }
    
    # API key ho toh add karo
    if api_key:
        params["key"] = api_key
    
    try:
        print(f"🎨 AI image generate ho rahi hai: {prompt[:50]}...")
        
        # Image download karo
        response = requests.get(url, params=params, timeout=120)
        response.raise_for_status()
        
        # Folder banao
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Image save karo
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        print(f"✅ AI image ready: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ AI image generate nahi hui: {e}")
        
        # Fallback: Gradient image banao
        print("⚠️ Fallback: Gradient image bana raha hoon...")
        return create_gradient_image(
            width, height,
            (30, 30, 60), (80, 30, 100),
            output_path
        )


def create_gradient_image(width, height, color1, color2, output_path):
    """
    Fallback: Gradient background banao.
    """
    img = Image.new("RGB", (width, height), color1)
    draw = ImageDraw.Draw(img)
    
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    print(f"✅ Gradient image ready: {output_path}")
    return output_path


def generate_scene_images(scenes, output_folder="output/scenes", 
                           width=1920, height=1080, api_key=None):
    """
    Multiple scenes ke liye images generate karo.
    """
    os.makedirs(output_folder, exist_ok=True)
    image_paths = []
    
    print(f"\n🎬 {len(scenes)} images generate ho rahi hain...")
    
    for i, prompt in enumerate(scenes, 1):
        print(f"\n📸 Image {i}/{len(scenes)}")
        output_path = f"{output_folder}/scene_{i}.jpg"
        
        image_path = generate_ai_image(
            prompt=prompt,
            output_path=output_path,
            width=width,
            height=height,
            api_key=api_key
        )
        
        if image_path:
            image_paths.append(image_path)
    
    print(f"\n✅ {len(image_paths)} images ready!")
    return image_paths


# ---------- TEST ----------

if __name__ == "__main__":
    print("=" * 50)
    print("🎬 Script2Video AI - AI Image Generator Test")
    print("=" * 50)
    
    # API key config se lo
    API_KEY = getattr(config, "POLLINATIONS_API_KEY", None)
    
    if API_KEY:
        print(f"🔑 API key mil gayi: {API_KEY[:10]}...")
    else:
        print("⚠️ API key nahi mili — fallback use hoga")
    
    # Test 1: Single AI image
    generate_ai_image(
        prompt="a beautiful sunset over mountains, cinematic, 4k",
        output_path="output/test_ai_image.jpg",
        width=1920,
        height=1080,
        api_key=API_KEY
    )
    
    # Test 2: Multiple scenes
    test_scenes = [
        "a beautiful sunset over mountains, cinematic",
        "a busy city street at night, neon lights",
        "a peaceful forest with sunlight, 4k"
    ]
    
    generate_scene_images(
        scenes=test_scenes,
        output_folder="output/test_scenes",
        api_key=API_KEY
    )
    
    print("\n✅ Test complete!")