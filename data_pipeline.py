import requests
import pandas as pd
from datetime import datetime

def get_real_space_weather():
    # NOAA L1 Gerçek Zamanlı API URL'leri
    plasma_url = "https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json"
    mag_url = "https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json"
    
    try:
        # 1. Plazma Verisini Çek (Hız, Yoğunluk, Sıcaklık)
        plasma_res = requests.get(plasma_url)
        plasma_data = plasma_res.json()
        df_plasma = pd.DataFrame(plasma_data[1:], columns=plasma_data[0])
        
        # 2. Manyetometre Verisini Çek (Bz bileşeni)
        mag_res = requests.get(mag_url)
        mag_data = mag_res.json()
        df_mag = pd.DataFrame(mag_data[1:], columns=mag_data[0])
        
        # HATA ÖNLEYİCİ: API bazen boş (None) veri gönderir. 
        # Boş satırları atlayıp en temiz ve en güncel veriyi alıyoruz.
        df_plasma = df_plasma.dropna()
        df_mag = df_mag.dropna()
        
        latest_plasma = df_plasma.iloc[-1]
        latest_mag = df_mag.iloc[-1]
        
        # Verileri ayrıştır (bz yerine bz_gsm kullandık)
        current_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "speed_km_s": float(latest_plasma['speed']),
            "density_p_cc": float(latest_plasma['density']),
            "temperature_k": float(latest_plasma['temperature']),
            "bz_nt": float(latest_mag['bz_gsm'])  # <-- Hatanın düzeltildiği yer
        }
        
        return current_data

    except Exception as e:
        print(f"HATA: Veri çekilemedi. Detay: {e}")
        return None

if __name__ == "__main__":
    print("📡 NOAA L1 Uydusuna bağlanılıyor...")
    live_data = get_real_space_weather()
    
    if live_data:
        print("\n✅ BAĞLANTI BAŞARILI! Gelen Canlı Veri:")
        print(f"Zaman: {live_data['timestamp']}")
        print(f"Güneş Rüzgarı Hızı: {live_data['speed_km_s']} km/s")
        print(f"Plazma Yoğunluğu: {live_data['density_p_cc']} p/cc")
        print(f"Manyetik Alan (Bz): {live_data['bz_nt']} nT")