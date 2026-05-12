import os, requests, time

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
GH_TOKEN = os.getenv("GH_PAT")  # El token que creamos en el paso 1
GH_REPO = os.getenv("GH_REPO")  # Ej: alejo15es-bit/ai-product-factory
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

def get_updates(offset):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/getUpdates?offset={offset}&timeout=30"
    try:
        return requests.get(url).json()
    except:
        return {"ok": False}

def trigger_generation(problem_name):
    print(f"🚀 Activando generación para: {problem_name}")
    # URL para activar el workflow de generación
    url = f"https://api.github.com/repos/{GH_REPO}/actions/workflows/generate.yml/dispatches"
    headers = {"Authorization": f"token {GH_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    # Envía el problema como variable
    payload = {"ref": "main", "inputs": {"problem": problem_name}}
    
    resp = requests.post(url, headers=headers, json=payload)
    if resp.status_code == 204:
        print("✅ ¡Orden enviada a GitHub!")
    else:
        print(f"❌ Error activando GitHub: {resp.status_code}")

def listen():
    print("👂 Escuchando Telegram... (Responde con 1, 2 o 3 al bot)")
    offset = 0
    while True:
        data = get_updates(offset)
        if data.get("ok") and data.get("result"):
            for update in data["result"]:
                msg = update.get("message", {})
                text = msg.get("text", "").strip()
                chat_id = str(msg.get("chat", {}).get("id"))
                
                # Si es tu chat y respondes 1, 2 o 3
                if chat_id == str(TG_CHAT_ID) and text in ["1", "2", "3"]:
                    problems_map = {
                        "1": "Digital Burnout", 
                        "2": "Inflation Budget", 
                        "3": "AI Anxiety"
                    }
                    chosen_name = problems_map[text]
                    
                    # Confirmar en Telegram
                    requests.post(f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
                        json={"chat_id": chat_id, "text": f"✅ <b>Aprobado:</b> {chosen_name}\n⏳ Generando activos... (Espera 5 min)"})
                    
                    trigger_generation(chosen_name)
                    
                    offset = update["update_id"] + 1
                    break # Salir para esperar el siguiente
        time.sleep(2)

if __name__ == "__main__":
    # Variables de entorno locales para prueba
    # En Windows: set TG_BOT_TOKEN=...
    # En Linux/Mac: export TG_BOT_TOKEN=...
    listen()
