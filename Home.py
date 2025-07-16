import streamlit as st
import pandas as pd

# Sayfa yapılandırması
st.set_page_config(
    page_title="Kalp Yetmezliği Tahmin Platformu",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ana sayfa başlığı ve açıklaması
st.title("Kalp Yetmezliği Tahmin Platformu")

# Hoş geldiniz mesajı ve proje açıklaması
st.markdown("""
## 👋 Hoş Geldiniz!

Bu platform, kalp hastalığı verilerini analiz etmenize, görselleştirmenize ve tahminlerde bulunmanıza olanak tanır.

### 🔍 Bu platformda neler yapabilirsiniz?

- **Veri Keşfi**: Kalp hastalığı veri setini inceleyebilir ve temel istatistikleri görebilirsiniz.
- **Veri Görselleştirme**: Çeşitli grafiklerle veri setini analiz edebilirsiniz.
- **Tahmin Modeli**: Kendi sağlık verilerinizi girerek kalp hastalığı riskinizi tahmin edebilirsiniz.
- **Hakkında**: Proje ve veri seti hakkında detaylı bilgi alabilirsiniz.
""")

# Veri setini yükleme
@st.cache_data
def load_data():
    data = pd.read_csv('heart_cleaned.csv')
    return data

# Veri setini yükle
df = load_data()

# Hızlı erişim kartları
st.header("Hızlı Erişim")

# Üç sütunlu düzen
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 📊 Veri Görselleştirme
    Veri setini çeşitli grafiklerle analiz edin.
    
    [Görselleştirmeye Git](/Veri_Görselleştirme)
    """)

with col2:
    st.markdown("""
    ### 🔮 Tahmin Modeli
    Sağlık verilerinizi girerek kalp hastalığı riskinizi tahmin edin.
    
    [Tahmin Modeline Git](/Tahmin_Modeli)
    """)

with col3:
    st.markdown("""
    ### ℹ️ Hakkında
    Proje ve veri seti hakkında detaylı bilgi alın.
    
    [Hakkında Sayfasına Git](https://github.com/MuayyedAlibrahim.git)
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("© 2025 Kalp Hastalığı Analiz Platformu | Streamlit ile geliştirilmiştir.")
