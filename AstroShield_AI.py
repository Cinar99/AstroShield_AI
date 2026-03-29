import streamlit as st
import plotly.graph_objects as go
import requests
import folium
from streamlit_folium import st_folium
from data_pipeline import get_real_space_weather
from ai_model import predict_storm

# 1. Sayfa Ayarları ve CSS
st.set_page_config(page_title="AstroShield Komuta Merkezi", layout="wide")
st.markdown("""
<style>
    /* Global background and text */
    .stApp {
        background: radial-gradient(circle at top right, #110022 0%, #000000 100%);
        color: #E0E0FF;
    }
    
    /* Headers with glowing gradient */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #FF007A, #7928CA, #00D4FF) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-shadow: 0px 0px 15px rgba(121, 40, 202, 0.4);
    }
    
    /* Existing Risk classes with added glow */
    .risk-safe { font-size: 35px; font-weight: bold; color: #00FFAA; text-shadow: 0px 0px 15px rgba(0,255,170,0.6); }
    .risk-danger { font-size: 35px; font-weight: bold; color: #FF3333; animation: blinker 1s linear infinite; text-shadow: 0px 0px 20px rgba(255,51,51,0.8); }
    @keyframes blinker { 50% { opacity: 0.2; } }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] {
        font-size: 40px !important;
        color: #00D4FF !important;
        text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.6);
    }
    div[data-testid="stMetricLabel"] {
        font-size: 18px !important;
        color: #FFAA00 !important;
        font-weight: bold;
    }

    /* Tabs Styling */
    button[data-baseweb="tab"] {
        background-color: #1a1a2e !important;
        color: #00d4ff !important;
        border-top: 2px solid #7928ca !important;
        border-radius: 8px 8px 0 0 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #7928ca !important;
        color: white !important;
        box-shadow: 0px -5px 15px rgba(121, 40, 202, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# SİSTEM DEĞİŞKENLERİ (Telegram Spam'i Engellemek İçin)
if "alert_sent" not in st.session_state:
    st.session_state.alert_sent = False

# TELEGRAM BOT AYARLARI (Kendi bilgilerinizi buraya girin)
TELEGRAM_TOKEN = "8553394485:AAH2C2U7ECGsrELWUA28s45IzNjmUjHXpVQ"
TELEGRAM_CHAT_ID = "8608987993"

def send_telegram_alert(impact_time):
    # Eğer token girilmişse ve daha önce mesaj atılmamışsa çalışır
    if TELEGRAM_TOKEN == "8553394485:AAH2C2U7ECGsrELWUA28s45IzNjmUjHXpVQ" and not st.session_state.alert_sent:
        message = f"🚨 [ASTROSHIELD ACİL DURUM KODU: KIRMIZI]\n\nL1 noktasında güçlü bir jeomanyetik şok tespit edildi! Dünya'ya çarpmasına tahmini {impact_time} dakika kaldı.\n\nTUA Kritik Altyapı Koruma Protokolleri devreye alındı. Lütfen http://localhost:8501/ adresinden ne yapabileceğinize bakın."
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            requests.post(url, json=payload)
            st.session_state.alert_sent = True # Mesaj gitti, bir daha atma
        except Exception as e:
            pass

# YAN MENÜ: JÜRİ SİMÜLASYON KONTROLÜ
# st.sidebar.image(["sun1.jpg", "sun2.jpg"], use_container_width=True)
st.sidebar.title("Kontrol Paneli")
st.sidebar.markdown("---")
demo_mode = st.sidebar.checkbox("🚨 Kriz Simülasyonunu Başlat")


if not demo_mode:
    st.session_state.alert_sent = False # Simülasyon kapanınca alarm sistemini sıfırla

st.title("🛡️ AstroShield AI: Otonom Uzay Havası Erken Uyarı Sistemi")
st.markdown("Dünya Yörüngesi (L1 Noktası) Gerçek Zamanlı Telemetri ve Karar Destek Paneli")
st.markdown("---")

# 2. Veri Çekme (Canlı veya Simülasyon)
if demo_mode:
    speed = 850.0
    density = 25.0
    temp = 350000.0
    bz = -15.0  # Kritik fırtına eşiği
    st.error("DİKKAT: SİSTEM ŞU AN SİMÜLASYON (KRİZ) MODUNDA ÇALIŞIYOR!")
else:
    live_data = get_real_space_weather()
    if live_data:
        speed = live_data['speed_km_s']
        density = live_data['density_p_cc']
        temp = live_data['temperature_k']
        bz = live_data['bz_nt']
    else:
        st.error("API Bağlantı Hatası!")
        st.stop()

# 3. AI Tahminini Al
risk_status = predict_storm(speed, density, temp, bz)
is_storm = "FIRTINA" in risk_status

# 4. Üst Göstergeler (Metrikler)
col1, col2, col3 = st.columns(3)
impact_minutes = 0

with col1:
    st.markdown("### 📡 Canlı Telemetri (L1)")
    st.write(f"**Güneş Rüzgarı Hızı:** {speed} km/s")
    st.write(f"**Manyetik Alan (Bz):** {bz} nT")
    st.write(f"**Plazma Yoğunluğu:** {density} p/cc")
    
with col3:
    st.markdown("### ⏱️ Çarpma Süresi")
    if speed > 0:
        impact_minutes = int((1500000 / speed) / 60)
        st.metric(label="Tahmini Altın Saat", value=f"{impact_minutes} Dakika")

with col2:
    st.markdown("### 🧠 AI Karar Destek")
    if is_storm == True:
        st.markdown(f'<p class="risk-danger">🚨 {risk_status}</p>', unsafe_allow_html=True)
        st.warning("Kritik Altyapı Uyarı Protokolü Devrede!")
        send_telegram_alert(impact_minutes) # Alarmı Tetikle!
    elif is_storm != demo_mode:
        st.markdown(f'<p class="risk-danger">🚨 {risk_status}</p>', unsafe_allow_html=True)
        st.warning("Kritik Altyapı Uyarı Protokolü Devrede!")
        send_telegram_alert(impact_minutes) 
    else:
        st.markdown(f'<p class="risk-safe">✅ {risk_status}</p>', unsafe_allow_html=True)
        st.success("Tüm sistemler normal çalışma düzeninde.")

st.markdown("---")

# 5. TÜRKİYE KRİTİK ALTYAPI HARİTASI & HIZ MONİTÖRÜ
col_map, col_gauge = st.columns([2, 1])

with col_map:
    st.subheader("🗺️ Türkiye Kritik Altyapı Risk Haritası")
    # Haritayı oluştur (Merkez: Türkiye)
    m = folium.Map(location=[39.0, 35.0], zoom_start=5, tiles="CartoDB dark_matter") # Karanlık Uzay Teması
    
    # Duruma göre renkleri belirle
    if is_storm != demo_mode:
        marker_color = "red"
    else:
        marker_color = "green"

    if is_storm != demo_mode:
        status_text = "RİSKLİ (Fırtına Bekleniyor)"
    else:
        status_text = "GÜVENLİ"
    
    # 1. İstanbul Havalimanı
    folium.Marker(
        [41.25, 28.74],
        popup=f"<b>İstanbul Havalimanı</b><br>Durum: {status_text}<br>Risk: GNSS Sapması & Rota İhlali",
        icon=folium.Icon(color=marker_color, icon="plane", prefix='fa')
    ).add_to(m)
    
    # 2. Keban Barajı (Enerji)
    folium.Marker(
        [38.79, 38.74],
        popup=f"<b>Keban Barajı Şebekesi</b><br>Durum: {status_text}<br>Risk: GIC (Aşırı Yüklenme)",
        icon=folium.Icon(color=marker_color, icon="bolt", prefix='fa')
    ).add_to(m)
    
    # 3. TÜRKSAT Gölbaşı Yer İstasyonu
    folium.Marker(
        [39.80, 32.80],
        popup=f"<b>TÜRKSAT Gölbaşı</b><br>Durum: {status_text}<br>Risk: HF Radyo Kesintisi",
        icon=folium.Icon(color=marker_color, icon="satellite", prefix='fa')
    ).add_to(m)

    # 4. Antalya Havalimanı
    folium.Marker(
        [36.90, 30.78],
        popup=f"<b>Antalya Havalimanı</b><br>Durum: {status_text}<br>Risk: GNSS Sapması & Rota İhlali",
        icon=folium.Icon(color=marker_color, icon="plane", prefix='fa')
    ).add_to(m)

    # 5. İzmir Havalimanı
    folium.Marker(
        [38.29, 27.16],
        popup=f"<b>İzmir Havalimanı</b><br>Durum: {status_text}<br>Risk: GNSS Sapması & Rota İhlali",
        icon=folium.Icon(color=marker_color, icon="plane", prefix='fa')
    ).add_to(m)

    # 6. Zonguldak Eren Enerji Santrali
    folium.Marker(
        [41.45, 32.10],
        popup=f"<b>Zonguldak Eren Enerji Santrali</b><br>Durum: {status_text}<br>Risk: GIC (Aşırı Yüklenme)",
        icon=folium.Icon(color=marker_color, icon="bolt", prefix='fa')
    ).add_to(m)

    # 7. Hunutlu Termik Santrali
    folium.Marker(
        [36.60, 35.90],
        popup=f"<b>Hunutlu Termik Santral</b><br>Durum: {status_text}<br>Risk: GIC (Aşırı Yüklenme)",
        icon=folium.Icon(color=marker_color, icon="bolt", prefix='fa')
    ).add_to(m)

    # 8. Cenal Termik Santrali
    folium.Marker(
        [40.45, 27.18],
        popup=f"<b>Cenal Termik Santral</b><br>Durum: {status_text}<br>Risk: GIC (Aşırı Yüklenme)",
        icon=folium.Icon(color=marker_color, icon="bolt", prefix='fa')
    ).add_to(m)
    
    # Haritayı ekrana bas
    st_folium(m, width=700, height=400)

with col_gauge:
    st.subheader("Güneş Rüzgarı Hızı")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=speed,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
                        'axis': {
                'range': [0, 1000],
                'tickmode': 'array',
                'tickvals': [0, 250, 500, 750, 1000],
                'ticktext': ['0', '250', '500', '750', '1000']
            },
            'bar': {'color': "red" if is_storm else "#00FFAA"},
            'bgcolor': "black",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 450], 'color': "rgba(0, 255, 0, 0.3)"},
                {'range': [450, 600], 'color': "rgba(255, 255, 0, 0.3)"},
                {'range': [600, 1000], 'color': "rgba(255, 0, 0, 0.5)"}
            ]
        }
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        font={'color': '#00D4FF'}
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# 6. LLM Sektörel Acil Eylem Raporu
st.subheader("🤖 Otonom LLM Kriz Yönetim Protokolü")
if is_storm != demo_mode:
    st.error("AstroShield LLM: Kp=8 Seviyesinde Jeomanyetik Fırtına algılandı. Sektörel acil durum bültenleri oluşturuluyor...")
    tab1, tab2, tab3 = st.tabs(["⚡ Enerji Şebekeleri", "✈️ Havacılık", "📡 Haberleşme ve Uydu"])
    with tab1:
        st.markdown("**[KIRMIZI KOD]** GIC seviyelerinde kritik artış. Keban-İstanbul hattındaki transformatörleri soğutmaya alın ve santrallerdeki elektrik yükünü azaltın.")
    with tab2:
        st.markdown("**[TURUNCU KOD]** GNSS/GPS sinyal kaybı riski. İstanbul Havalimanı, İzmir Havalimanı ve Antalya Havalimanı aletli iniş (ILS) sistemlerine öncelik vermeli.")
    with tab3:
        st.markdown("**[SARI KOD]** HF iletişim kararması. TÜRKSAT uyduları otonom 'Safe-Mode' yönelimine geçmelidir.")
else:
    st.info("AstroShield LLM: Güneş aktivitesi normal. Operasyonel değişiklik gerekmiyor.")