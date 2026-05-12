import os, requests, json, time

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
GH_TOKEN = os.getenv("GH_PAT")  # Token personal de GitHub con repo scope
GH_REPO = os.getenv("GH_REPO")  # ej: alejo15es-bit/neurosync-product

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
    return requests.get(url).json()

def trigger_generation(problem_name):
    url = f"https://api.github.com/repos/{GH_REPO}/actions/workflows/generate.yml/dispatches"
    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"ref": "main", "inputs": {"problem": problem_name}}
    resp = requests.post(url, headers=headers, json=payload)
    print(f"🚀 Generación activada para: {problem_name} | Status: {resp.status_code}")

def listen():
    print("👂 Escuchando respuestas en Telegram...")
    offset = 0
    while True:
        try:
            data = get_updates(offset)
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    msg = update.get("message", {})
                    text = msg.get("text", "").strip()
                    chat_id = msg.get("chat", {}).get("id")
                    
                    if text in ["1", "2", "3"] and str(chat_id) == str(os.getenv("TG_CHAT_ID")):
                        problems_map = {"1": "Digital Burnout", "2": "Inflation Budget", "3": "AI Anxiety"}
                        chosen = problems_map[text]
                        
                        # Notificar aprobación
                        requests.post(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
                            json={"chat_id": chat_id, "text": f"✅ <b>Aprobado:</b> {chosen}\n⏳ Generando activos con IA... (3-5 min)"})
                        
                        trigger_generation(chosen)
                        offset = update["update_id"] + 1
                        break
            time.sleep(2)
        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    listen()
