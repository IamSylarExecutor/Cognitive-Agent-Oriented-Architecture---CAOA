import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="CAOA Afet Yönetim Paneli", layout="wide")

# Başlık ve Açıklama
st.title("🚨 CAOA - Bilişsel Afet Komuta Merkezi")
st.markdown("""
Bu sistem, sahadan gelen kaotik ihbarları geleneksel yöntemlerle değil, **Bilişsel Geçit (Cognitive Gateway)** mimarisiyle işler. 
Llama-3.1 yapay zekası, ihbarı saniyenin onda biri sürede anlamsal olarak analiz edip, doğru otonom ajanlara yönlendirir.
""")
st.divider()

# Kullanıcı Girdisi Alanı
ihbar = st.text_area("Afet İhbarını Giriniz (Simülasyon):", height=150, 
                     placeholder="Örn: Atatürk mahallesi 3. sokakta bina çöktü, içeride mahsur kalanlar var, doğalgaz kokusu alıyoruz!")

# Gönderim Butonu
if st.button("İhbarı Bilişsel Ağda İşle", type="primary"):
    if ihbar:
        with st.spinner("Bilişsel Geçit ihbarı analiz ediyor ve ajanları görevlendiriyor..."):
            try:
                # Arka planda çalışan kendi FastAPI (main.py) sunucumuza veri gönderiyoruz
                response = requests.post("http://127.0.0.1:8000/analyze-disaster", json={"ihbar_metni": ihbar})
                
                if response.status_code == 200:
                    veri = response.json()
                    
                    st.success("✅ Bilişsel Yönlendirme Başarılı! Ekipler (Ajanlar) Atandı.")
                    
                    # Verileri 3 Kolon Halinde Şık Bir Şekilde Gösterme
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("⚠️ Öncelik Seviyesi")
                        # Önceliğe göre renk atama
                        if veri.get("oncelik_seviyesi") == "KRITIK":
                            st.error("🔴 " + veri.get("oncelik_seviyesi", "Bilinmiyor"))
                        elif veri.get("oncelik_seviyesi") == "YUKSEK":
                            st.warning("🟠 " + veri.get("oncelik_seviyesi", "Bilinmiyor"))
                        else:
                            st.info("🟡 " + veri.get("oncelik_seviyesi", "Bilinmiyor"))

                    with col2:
                        st.subheader("📋 Tespit Edilen Kategoriler")
                        for kat in veri.get("kategoriler", []):
                            st.success(kat)

                    with col3:
                        st.subheader("🤖 Otonom Ajan Görevlendirmeleri")
                        for ajan in veri.get("yonlendirilecek_ajanlar", []):
                            st.info(f"**{ajan.get('ajan')}**: {ajan.get('gorev')}")
                    
                    st.divider()
                    st.write("Sistemin (Cognitive Gateway) Ürettiği Ham Veri (Jüri Kanıtı):")
                    st.json(veri)
                    
                else:
                    st.error(f"Backend'e ulaşılamadı. Hata Kodu: {response.status_code}. İlk terminalde Uvicorn (main.py) çalışıyor mu?")
            except Exception as e:
                st.error(f"Sistem Hatası. Lütfen FastAPI sunucusunun açık olduğundan emin olun. Detay: {e}")
    else:
        st.warning("Lütfen sisteme işlenmesi için bir ihbar metni girin.")