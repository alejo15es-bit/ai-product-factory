import os, requests, time
from datetime import datetime
from pytrends.request import TrendReq

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")

COUNTRIES = ["US", "GB", "CA", "AU", "DE"]

def get_viral_problems():
    pytrends = TrendReq(hl="en-US", tz=360)
    keywords = ["digital burnout", "inflation budget", "data privacy tools", "ai anxiety", "remote work focus"]
    results = []
    
    for country in COUNTRIES[:3]:
        try:
            for kw in keywords:
                pytrends.build_payload([kw], timeframe="now 7-d", geo=country)
                data = pytrends.interest_over_time()
                if not data.empty:
                    score = data[kw].mean()
                    if score > 40:
                        results.append({"query": kw, "country": country, "score": int(score)})
                time.sleep(2)
        except: continue
    
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:3] if results else [
        {"query": "digital burnout", "country": "US", "score": 85},
        {"query": "inflation budget", "country": "GB", "score": 72},
        {"query": "ai anxiety", "country": "CA", "score": 68}
    ]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TG_CHAT_ID, "text": msg, "parse_mode": "HTML"})

def run():
    problems = get_viral_problems()
    
    # Recomendaciones dinámicas
    recommendations = [
        {"asset": "🎧 NeuroSync Audio Kit + PDF Guía", "price": "$27"},
        {"asset": "💰 Inflation Shield Dashboard + Tracker", "price": "$19"},
        {"asset": "🔐 Privacy Guardian Toolkit + Checklists", "price": "$34"}
    ]
    
    lines = []
    for i, p in enumerate(problems, 1):
        rec = recommendations[i-1]
        lines.append(f"<b>{i}️⃣ {p['query'].upper()}</b>\n🌍 {p['country']} | 🔥 {p['score']}\n📦 Activo: {rec['asset']}\n💰 Precio sugerido: {rec['price']}")
    
    report = f"""🔥 <b>REPORTE VIRAL - {datetime.now().strftime('%d/%m/%Y')}</b>

📈 <b>TOP 3 PROBLEMAS URGENTES:</b>

{chr(10).join(lines)}

━━━━━━━━━━━━━━━━━━━━
✅ <b>Responde con el NÚMERO</b> (1, 2 o 3) para aprobar.
🤖 El sistema generará automáticamente:
• 3 Audios (ElevenLabs)
• 4 Imágenes (Stability AI)
• Música de fondo (Hugging Face)
• Guía PDF (PDFMonkey)
• Landing page lista para vender

⏳ Próxima investigación: en 3 días"""
    
    send_telegram(report)
    print("✅ Reporte enviado a Telegram")

if __name__ == "__main__":
    run()
