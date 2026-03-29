from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
import json

# 1. Uygulamamızı ve Mimariyi Başlatıyoruz
app = FastAPI(title="CAOA - Bilişsel Geçit Prototipi", version="1.0")

# DİKKAT: GROQ API ANAHTARINI BURAYA YAPIŞTIRACAKSIN
client = Groq(api_key="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")

# 2. Gelen Veri Formatını Tanımlıyoruz
class DisasterReport(BaseModel):
    ihbar_metni: str

# 3. Nabız Kontrolü
@app.get("/")
def read_root():
    return {"Sistem Durumu": "Aktif", "Mimari": "Bilişsel Geçit Çalışıyor (Groq/Llama3)"}

# 4. GERÇEK BİLİŞSEL GEÇİT (Cognitive Gateway)
@app.post("/analyze-disaster")
def analyze_disaster(report: DisasterReport):
    
    # Yapay zekaya kim olduğunu ve ne yapması gerektiğini söylüyoruz (Prompt Engineering)
    system_prompt = """
    Sen bir Afet Yönetimi Bilişsel Yönlendiricisisin (Cognitive Router).
    Gelen kaotik ihbar metnini analiz et ve alt sistemlere (Agent'lara) görev atamak için SADECE aşağıdaki JSON formatında çıktı ver. Başka hiçbir sohbet veya açıklama yazma.
    Format:
    {
      "orijinal_ihbar": "...",
      "analiz_durumu": "Basarili",
      "kategoriler": ["Arama_Kurtarma", "Medikal", "Yangin", "Lojistik"],
      "oncelik_seviyesi": "DUSUK|ORTA|YUKSEK|KRITIK",
      "yonlendirilecek_ajanlar": [
         {"ajan": "Lojistik_Ajani", "gorev": "Ajanin yapmasi gereken spesifik gorev"},
         {"ajan": "Saglik_Ajani", "gorev": "Ajanin yapmasi gereken spesifik gorev"}
      ]
    }
    """
    
    try:
        # Groq API'sine (Llama 3 modeline) bağlanıp veriyi işliyoruz
        response = client.chat.completions.create(
           model="llama-3.1-8b-instant", # Açık kaynaklı, bedava ve şimşek hızında model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": report.ihbar_metni}
            ],
            response_format={"type": "json_object"} # Kesinlikle JSON vermesini zorluyoruz
        )
        
        # Gelen metni sistemin okuyabileceği JSON objesine çeviriyoruz
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        return {"Hata": str(e), "Mesaj": "Bilişsel Geçit çöktü. Groq API anahtarını kontrol et."}