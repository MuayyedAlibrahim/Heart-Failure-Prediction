import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Sayfa yapılandırması
st.set_page_config(
    page_title="Tanıtım - Kalp Yetmezliği Analiz Platformu",
    page_icon="ℹ️",
    layout="wide"
)

# Sayfa başlığı
st.title("ℹ️ Kalp Yetmezliği ve Risk Faktörleri Hakkında Bilgi")
st.markdown("Bu sayfada kalp hastalıkları, risk faktörleri ve korunma yöntemleri hakkında bilgiler bulabilirsiniz.")

# Ana içerik
tab1, tab2, tab3, tab4 = st.tabs(["Kalp Hastalıkları", "Risk Faktörleri", "Korunma Yöntemleri", "Veri Seti Hakkında"])

with tab1:
    st.header("Kalp Hastalıkları Nedir?")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **Kalp hastalığı**, kalbi ve kan damarlarını etkileyen çeşitli durumları kapsayan genel bir terimdir. 
        Kalp hastalıkları, dünya genelinde en yaygın ölüm nedenlerinden biridir.
        
        **Koroner Arter Hastalığı (KAH)**, kalp hastalıklarının en yaygın türüdür. 
        Kalbe kan sağlayan koroner arterlerin daralması veya tıkanması sonucu ortaya çıkar. 
        Bu durum, kalp kasına yeterli oksijen ve besin gitmemesine neden olur.
        
        **Kalp hastalığının belirtileri şunları içerebilir:**
        - Göğüs ağrısı veya rahatsızlığı (angina)
        - Nefes darlığı
        - Kalp çarpıntısı
        - Yorgunluk ve halsizlik
        - Baş dönmesi veya bayılma
        - Bacaklarda, ayak bileklerinde veya karında şişlik
        
        Kalp hastalığı tanısı için doktorlar genellikle şu testleri kullanır:
        - Elektrokardiyogram (EKG)
        - Ekokardiyogram
        - Stres testi
        - Koroner anjiyografi
        - Kan testleri
        """)
    
    with col2:
        st.image("https://www.acilcalisanlari.com/wp-content/uploads/2021/12/Kalp-Yetmezli%C4%9F-S%C4%B1n%C4%B1fland%C4%B1rma-Ventrik%C3%BCl-Yap%C4%B1s%C4%B1-2022.jpg", width=800)
        st.markdown("""
        **Kalp Hastalığı Türleri:**
        - Koroner Arter Hastalığı
        - Kalp Yetmezliği
        - Aritmi
        - Kalp Kapak Hastalıkları
        - Kardiyomiyopati
        - Doğumsal Kalp Hastalıkları
        - Perikardit
        """)

with tab2:
    st.header("Kalp Hastalığı Risk Faktörleri")
    
    st.markdown("""
    Kalp hastalığı risk faktörleri, değiştirilebilir ve değiştirilemez faktörler olarak ikiye ayrılır.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Değiştirilebilir Risk Faktörleri")
        st.markdown("""
        - **Yüksek Tansiyon:** Kan damarlarına ve kalbe zarar verir.
        - **Yüksek Kolesterol:** Damarlarda plak oluşumuna neden olur.
        - **Sigara Kullanımı:** Damar hasarına ve oksijen azalmasına yol açar.
        - **Diyabet:** Kan şekeri kontrolsüzlüğü damar hasarına neden olur.
        - **Obezite:** Kalp üzerinde ek stres oluşturur.
        - **Fiziksel Hareketsizlik:** Kalp sağlığını olumsuz etkiler.
        - **Sağlıksız Beslenme:** Yüksek yağ ve tuz tüketimi risk oluşturur.
        - **Aşırı Alkol Tüketimi:** Kalp kasına zarar verebilir.
        - **Stres:** Kan basıncını yükseltebilir ve diğer risk faktörlerini tetikleyebilir.
        """)
    
    with col2:
        st.subheader("Değiştirilemez Risk Faktörleri")
        st.markdown("""
        - **Yaş:** Risk 45 yaş üstü erkeklerde ve 55 yaş üstü kadınlarda artar.
        - **Cinsiyet:** Erkekler genellikle daha yüksek risk altındadır.
        - **Aile Öyküsü:** Ailede kalp hastalığı öyküsü riski artırır.
        - **Etnik Köken:** Bazı etnik gruplar daha yüksek risk altındadır.
        """)
    
    # Risk faktörleri grafiği
    st.subheader("Risk Faktörlerinin Kalp Hastalığı Üzerindeki Etkisi")
    
    # Örnek veri
    risk_factors = ['Yüksek Tansiyon', 'Yüksek Kolesterol', 'Sigara', 'Diyabet', 'Obezite', 'Hareketsizlik']
    risk_impact = [75, 70, 65, 60, 55, 50]  # Örnek etki yüzdeleri
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(risk_factors, risk_impact, color=sns.color_palette("Blues_r"))
    ax.set_xlabel('Kalp Hastalığı Riskine Etkisi (%)')
    ax.set_xlim(0, 100)
    
    # Değerleri çubukların üzerine ekleme
    for i, v in enumerate(risk_impact):
        ax.text(v + 1, i, f"{v}%", va='center')
    
    st.pyplot(fig)
    
    st.markdown("""
    **Not:** Yukarıdaki grafik, risk faktörlerinin kalp hastalığı üzerindeki tahmini etkisini göstermektedir. 
    Gerçek etki, kişiden kişiye ve diğer faktörlerin varlığına göre değişebilir.
    """)

with tab3:
    st.header("Kalp Hastalığından Korunma Yöntemleri")
    
    st.markdown("""
    Kalp hastalığı riskini azaltmak için yaşam tarzı değişiklikleri ve düzenli sağlık kontrolleri önemlidir.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Beslenme Önerileri")
        st.markdown("""
        - Meyve ve sebzelerden zengin beslenin
        - Tam tahıllı ürünleri tercih edin
        - Yağsız protein kaynakları tüketin
        - Doymuş ve trans yağları sınırlayın
        - Tuz tüketimini azaltın
        - Şeker tüketimini sınırlayın
        - Porsiyon kontrolüne dikkat edin
        """)
    
    with col2:
        st.subheader("Fiziksel Aktivite")
        st.markdown("""
        - Haftada en az 150 dakika orta yoğunlukta aerobik aktivite yapın
        - Haftada en az 2 gün kas güçlendirici aktiviteler yapın
        - Uzun süre oturmaktan kaçının
        - Günlük aktivitenizi artırın (merdiven kullanma, yürüyüş vb.)
        - Kendinize uygun bir egzersiz programı belirleyin
        - Düzenli olarak egzersiz yapın
        """)
    
    with col3:
        st.subheader("Diğer Öneriler")
        st.markdown("""
        - Sigara kullanmayın, kullanıyorsanız bırakın
        - Alkol tüketimini sınırlayın
        - Stresi yönetmeyi öğrenin
        - Düzenli sağlık kontrollerinizi yaptırın
        - Tansiyon, kolesterol ve kan şekeri seviyelerinizi kontrol altında tutun
        - Yeterli uyku alın
        - Kilonuzu sağlıklı bir aralıkta tutun
        """)
    
    # Korunma yöntemleri etkinliği
    st.subheader("Korunma Yöntemlerinin Etkinliği")
    
    # Örnek veri
    prevention_methods = [
        'Düzenli Egzersiz', 'Sağlıklı Beslenme', 'Sigarayı Bırakma', 
        'Tansiyon Kontrolü', 'Kolesterol Kontrolü', 'Stres Yönetimi'
    ]
    effectiveness = [85, 80, 90, 75, 70, 60]  # Örnek etkinlik yüzdeleri
    
    # Pasta grafiği
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Renk paleti
    colors = sns.color_palette('Blues', len(prevention_methods))
    
    # Pasta dilimlerini oluşturma
    wedges, texts, autotexts = ax.pie(
        effectiveness, 
        labels=prevention_methods,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1}
    )
    
    # Pasta grafiğini çembere dönüştürme
    ax.axis('equal')
    
    # Metin özelliklerini ayarlama
    plt.setp(autotexts, size=10, weight='bold')
    plt.setp(texts, size=10)
    
    st.pyplot(fig)
    
    st.markdown("""
    **Not:** Yukarıdaki grafik, korunma yöntemlerinin kalp hastalığı riskini azaltmadaki tahmini etkinliğini göstermektedir. 
    En etkili korunma, tüm yöntemlerin birlikte uygulanmasıyla sağlanır.
    """)

with tab4:
    st.header("Veri Seti Hakkında Bilgi")
    
    st.markdown("""
    Bu uygulamada kullanılan veri seti, kalp hastalığı teşhisi için çeşitli klinik parametreleri içermektedir.
    """)
    
    # Veri setini yükleme
    @st.cache_data
    def load_data():
        data = pd.read_csv('c:\\Users\\somef\\OneDrive\\Desktop\\uygulama\\heart_cleaned.csv')
        return data
    
    df = load_data()
    
    # Veri seti özellikleri açıklaması
    st.subheader("Veri Seti Özellikleri")
    
    feature_descriptions = pd.DataFrame({
        'Özellik': [
            'Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS',
            'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope', 'HeartDisease'
        ],
        'Açıklama': [
            'Hastanın yaşı (yıl)',
            'Hastanın cinsiyeti (M: Erkek, F: Kadın)',
            'Göğüs ağrısı tipi (TA: Tipik Angina, ATA: Atipik Angina, NAP: Non-Anginal Ağrı, ASY: Asemptomatik)',
            'İstirahat kan basıncı (mm Hg)',
            'Serum kolesterol (mg/dl)',
            'Açlık kan şekeri > 120 mg/dl (1: Evet, 0: Hayır)',
            'İstirahat elektrokardiyogram sonuçları (Normal, ST: ST-T dalga anormalliği, LVH: Sol ventrikül hipertrofisi)',
            'Maksimum kalp hızı',
            'Egzersiz kaynaklı angina (Y: Evet, N: Hayır)',
            'Oldpeak = ST depresyonu (egzersizle indüklenen ST depresyonu, dinlenmeye göre)',
            'ST eğiminin eğimi (Up: Yukarı, Flat: Düz, Down: Aşağı)',
            'Kalp hastalığı çıktısı (1: Kalp hastalığı var, 0: Normal)'
        ]
    })
    
    st.table(feature_descriptions)
    
    # Veri seti istatistikleri
    st.subheader("Veri Seti İstatistikleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Toplam Örnek Sayısı:** {len(df)}")
        st.write(f"**Kalp Hastalığı Olan Hasta Sayısı:** {df['KalpHastalığı'].sum()}")
        st.write(f"**Kalp Hastalığı Olmayan Hasta Sayısı:** {len(df) - df['KalpHastalığı'].sum()}")
        
        # Cinsiyet dağılımı
        gender_counts = df['Cinsiyet'].value_counts()
        st.write(f"**Erkek Hasta Sayısı:** {gender_counts.get(1, 0)}")
        st.write(f"**Kadın Hasta Sayısı:** {gender_counts.get(0, 0)}")
    
    with col2:
        # Yaş istatistikleri
        st.write(f"**Ortalama Yaş:** {df['Yaş'].mean():.1f} yıl")
        st.write(f"**Minimum Yaş:** {df['Yaş'].min()} yıl")
        st.write(f"**Maksimum Yaş:** {df['Yaş'].max()} yıl")
        
        # Göğüs ağrısı tipi dağılımı
        chest_pain_counts = df['GöğüsAğrısıTürü'].value_counts()
        st.write("**Göğüs Ağrısı Tipi Dağılımı:**")
        for pain_type, count in chest_pain_counts.items():
            st.write(f"- {pain_type}: {count} hasta")
    
    # Veri seti görselleştirmeleri
    st.subheader("Veri Seti Görselleştirmeleri")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Yaş dağılımı
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(data=df, x='Yaş', hue='KalpHastalığı', multiple='stack', bins=20, ax=ax)
        ax.set_title('Yaş Dağılımı ve Kalp Hastalığı İlişkisi')
        ax.set_xlabel('Yaş')
        ax.set_ylabel('Hasta Sayısı')
        ax.legend(['Normal', 'Kalp Hastalığı'])
        st.pyplot(fig)
    
    with col2:
        # Cinsiyet ve kalp hastalığı ilişkisi
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.countplot(data=df, x='Cinsiyet', hue='KalpHastalığı', ax=ax)
        ax.set_title('Cinsiyet ve Kalp Hastalığı İlişkisi')
        ax.set_xlabel('Cinsiyet')
        ax.set_ylabel('Hasta Sayısı')
        ax.set_xticklabels(['Kadın', 'Erkek'])
        ax.legend(['Normal', 'Kalp Hastalığı'])
        st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("© 2025 Kalp Hastalığı Analiz Platformu | Streamlit ile geliştirilmiştir.")