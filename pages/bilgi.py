import streamlit as st

st.set_page_config(page_title="Güneş Fırtınaları Bilgi", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #110022 0%, #000000 100%);
        color: #E0E0FF;
    }
    h1, h2, h3, h4 {
        background: -webkit-linear-gradient(45deg, #FF007A, #7928CA, #00D4FF) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        text-shadow: 0px 0px 15px rgba(121, 40, 202, 0.4);
    }
    .info-card {
        background: rgba(30,30,50,0.6);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #7928CA;
        margin-bottom: 20px;
    }
    .warning-card {
        background: rgba(255, 51, 51, 0.1);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #FF3333;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("Güneş Fırtınası Rehberi 🌌")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.header("1. Güneş Fırtınası Nedir?")
    st.write("Güneş fırtınaları, Güneş'in manyetik alanındaki düzensizlikler sonucu ortaya çıkan devasa enerji boşalmalarıdır. Bunları iki ana grupta inceleyebiliriz:")
    st.markdown("- **Güneş Parlamaları (Solar Flares):** Güneş atmosferindeki anlık ve çok şiddetli ışık patlamalarıdır. Işık hızıyla hareket ederler, yani Dünya'ya ulaşmaları sadece 8 dakika sürer.")
    st.markdown("- **Taçküre Kütle Atımları (CME):** Güneş'ten uzaya fırlatılan devasa plazma ve manyetik alan bulutlarıdır. Bunlar daha yavaştır; Dünya'ya ulaşmaları 1 ila 3 gün sürebilir.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.header("2. Dünya'ya Etkileri: Kozmik Bir Çarpışma")
    st.write("Dünya'nın kendi manyetik alanı (manyetosfer), bizi bu fırtınaların en kötü etkilerinden koruyan bir kalkan görevi görür. Ancak fırtına çok güçlüyse, bu kalkan 'esneyebilir' ve bazı sızıntılar yaşanabilir.")
    st.markdown("- Manyetik değişimler trafolarda aşırı yüklenmeye ve geniş çaplı elektrik kesintilerine neden olabilir.")
    st.markdown("- Elektronik devreler zarar görebilir. GPS sinyallerinde sapmalar yaşanabilir.")
    st.markdown("- Özellikle havacılıkta kullanılan kısa dalga radyo sinyalleri kesintiye uğrayabilir.")
    st.markdown("- Uzaydaki astronotlar veya yüksek irtifada uçan yolcular yüksek radyasyona maruz kalabilir.")
    st.subheader("Auroralar (Kutup Işıkları)")
    st.write("Güneş fırtınalarının en büyüleyici sonucu şüphesiz Kuzey ve Güney Işıkları'dır. Güneş'ten gelen yüklü parçacıklar atmosferimizdeki gazlarla çarpıştığında gökyüzünde yeşil, mor ve kırmızı dans eden ışıklar oluşturur. Fırtına ne kadar güçlüyse, bu ışıklar ekvatora o kadar yakın yerlerden görülebilir.")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.header("3. Güneş Döngüsü (Solar Cycle) Nedir?")
    st.write("Güneş, sabit ve durgun bir ateş topu değildir. Yaklaşık her 11 yılda bir tamamlanan bir hareketlilik döngüsüne sahiptir. Bu döngü sırasında Güneş'in yüzeyindeki lekeler, patlamalar ve radyasyon seviyesi önce artar, sonra azalır.")
    st.markdown("- **Güneş Minimumu:** Döngünün en sakin olduğu, neredeyse hiç güneş lekesinin görülmediği dönemdir.")
    st.markdown("- **Güneş Maksimumu:** Hareketliliğin tavan yaptığı, lekelerin çoğaldığı ve en güçlü fırtınaların yaşandığı dönemdir.")
    
    st.subheader("Neden 11 Yıl? (Manyetik Karışıklık)")
    st.write("Güneş, katı bir cisim olmadığı için (plazma halindedir) her yeri aynı hızla dönmez. Ekvator bölgesi, kutuplara göre daha hızlı döner. Bu duruma 'diferansiyel dönme' diyoruz. İşte olanlar tam olarak şudur:")
    st.markdown("1. Güneş'in manyetik alan çizgileri başlangıçta düzgündür.")
    st.markdown("2. Ekvator hızlı döndükçe bu çizgileri sürükler ve onları birbirine dolamaya, düğümlemeye başlar.")
    st.markdown("3. Bu düğümler yüzeye çıktığında Güneş Lekeleri oluşur.")
    st.markdown("4. Yaklaşık 11 yılın sonunda bu karışıklık o kadar artar ki, manyetik alan artık dayanamaz ve 'takla atar'.")
    st.write("Döngünün zirvesinde (Güneş Maksimumu), Güneş'in kuzey ve güney manyetik kutupları yer değiştirir. Yani Kuzey Kutbu Güney, Güney Kutbu ise Kuzey olur. Bu olay gerçekleştikten sonra manyetik alan çizgileri tekrar düzelmeye başlar ve Güneş yavaş yavaş sakinleşerek yeni bir döngüye hazırlanır.")
    
    st.info("**İlginç Bir Not:** Şu an (2024-2026 civarı), 25. Güneş Döngüsü'nün maksimum evresine oldukça yakınız. Bu yüzden son zamanlarda daha fazla kutup ışığı haberi ve GPS kesintisi uyarısı duyuyoruz.")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="warning-card">', unsafe_allow_html=True)
st.header("🚨 Güneş Fırtınası Öncesi ve Esnasında Yapılması Gerekenler:")
st.markdown("- **Elektronik Cihazları Koruyun:** Güçlü bir fırtına uyarısında, bilgisayarlar, televizyonlar ve hassas elektronik cihazların fişini prizden çekin. Voltaj dalgalanmaları cihazlara zarar verebilir.")
st.markdown("- **İletişim ve Güç Önlemleri:** Uydu iletişimi ve GPS sistemleri etkilenebileceğinden, acil durumlar için pilli radyo, el feneri, yedek piller ve güç bankaları (powerbank) bulundurun.")
st.markdown("- **Bilgi Takibi:** Resmi kurumların (AFAD, Meteoroloji vb.) uyarılarını radyo veya diğer iletişim araçlarından yakından takip edin.")
st.markdown("- **Yedekleme Yapın:** Önemli verilerinizi bulut sistemlerinde veya harici disklerde yedekleyin.")
st.markdown("- **Altyapı Kontrolü:** Eğer güneş paneli gibi bağımsız enerji sistemleriniz varsa, teknik koruma önlemlerini gözden geçirin.")
st.markdown('</div>', unsafe_allow_html=True)
