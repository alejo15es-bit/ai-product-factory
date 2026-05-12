import os, requests, json, base64, time

# APIs
ELEVEN_KEY = os.getenv("ELEVENLABS_API_KEY")
STABILITY_KEY = os.getenv("STABILITY_API_KEY")
PDFMONKEY_KEY = os.getenv("PDFMONKEY_API_KEY")
HF_KEY = os.getenv("HF_API_KEY")

PROBLEM = os.getenv("PROBLEM", "Digital Burnout")
os.makedirs("assets", exist_ok=True)

def gen_audio():
    print("🎙️ Generando audios con ElevenLabs...")
    scripts = [
        f"Welcome to NeuroSync. This 15-minute session targets {PROBLEM}. Breathe in 4, hold 7, exhale 8. Release the noise. Reclaim your focus.",
        f"Work Focus Protocol for {PROBLEM}. Single-tasking mode activated. Spotlight on one goal. Breathe steadily. Depth over speed.",
        f"Evening Detox for {PROBLEM}. Disconnect to reconnect. Screens off. Nervous system downshifting. Rest is productive."
    ]
    voice_id = "21m00Tcm4TlvDq8ikWAM"
    for i, txt in enumerate(scripts, 1):
        resp = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
            headers={"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json"},
            json={"text": txt, "model_id": "eleven_monolingual_v1"})
        if resp.status_code == 200:
            with open(f"assets/audio_{i}.mp3", "wb") as f: f.write(resp.content)
            print(f"✅ audio_{i}.mp3")

def gen_images():
    print("🎨 Generando imágenes con Stability AI...")
    prompts = [
        f"Professional wellness product cover for {PROBLEM}, calming gradient, abstract neural visualization, 4k",
        "Peaceful morning workspace, soft light, zen atmosphere, minimalist",
        "Focused professional at clean desk, natural lighting, productivity vibe",
        "Cozy evening relaxation, warm sunset tones, digital detox concept"
    ]
    names = ["cover", "session1", "session2", "session3"]
    for name, prompt in zip(names, prompts):
        resp = requests.post("https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
            headers={"Authorization": f"Bearer {STABILITY_KEY}", "Content-Type": "application/json"},
            json={"text_prompts": [{"text": prompt}], "cfg_scale": 7, "height": 1024, "width": 1024, "samples": 1, "steps": 30})
        if resp.status_code == 200:
            img_b64 = resp.json()["artifacts"][0]["base64"]
            with open(f"assets/{name}.png", "wb") as f: f.write(base64.b64decode(img_b64))
            print(f"✅ {name}.png")

def gen_music():
    print("🎵 Generando música con Hugging Face (MusicGen)...")
    url = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    headers = {"Authorization": f"Bearer {HF_KEY}"}
    moods = ["calm ambient meditation", "focused productivity electronic", "relaxing evening sleep"]
    for i, mood in enumerate(moods, 1):
        resp = requests.post(url, headers=headers, json={"inputs": mood, "parameters": {"duration": 15}}, timeout=60)
        if resp.status_code == 200:
            with open(f"assets/music_{i}.mp3", "wb") as f: f.write(resp.content)
            print(f"✅ music_{i}.mp3")

def gen_pdf():
    print("📄 Generando PDF con PDFMonkey...")
    html = f"""<html><body style="font-family:sans-serif;line-height:1.6;max-width:700px;margin:40px auto">
    <h1 style="color:#4F46E5">NeuroSync: {PROBLEM} Protocol</h1>
    <div style="background:#F3F4F6;padding:15px;border-radius:8px;margin:15px 0">
    <strong>🧠 Phase 1:</strong> Nervous System Reset (4-7-8 Breath)<br>
    <strong>🎯 Phase 2:</strong> Attention Anchoring<br>
    <strong>🌙 Phase 3:</strong> Digital Sunset Protocol</div>
    <p>Science-backed steps to overcome {PROBLEM} in 15 minutes daily.</p>
    <div style="text-align:center;margin-top:40px;color:#6B7280">© 2026 NeuroSync AI Kit</div>
    </body></html>"""
    resp = requests.post("https://api.pdfmonkey.io/v1/documents",
        headers={"Authorization": f"Bearer {PDFMONKEY_KEY}", "Content-Type": "application/json"},
        json={"document": {"template": {"body": html}, "payload": {"title": PROBLEM}}})
    if resp.status_code in [200, 201]:
        pdf_url = resp.json().get("pdf_url") or resp.json().get("url")
        pdf_resp = requests.get(pdf_url)
        with open("assets/guide.pdf", "wb") as f: f.write(pdf_resp.content)
        print("✅ guide.pdf")

def run():
    print(f"🚀 Iniciando generación para: {PROBLEM}")
    gen_audio()
    gen_images()
    gen_music()
    gen_pdf()
    print("✅ Todos los assets generados en /assets")

if __name__ == "__main__":
    run()
