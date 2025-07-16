import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Sayfa yapılandırması
st.set_page_config(
    page_title="Veri Görselleştirme - Kalp Hastalığı Analiz Platformu",
    page_icon="📊",
    layout="wide"
)

# Sayfa başlığı
st.title("📊 Veri Görselleştirme")
st.markdown("Bu sayfada kalp hastalığı veri setini çeşitli grafiklerle analiz edebilirsiniz.")

# Veri setini yükleme
@st.cache_data
def load_data():
    data = pd.read_csv('heart_cleaned.csv')
    return data

df = load_data()

# Sidebar oluşturma
st.sidebar.header("Görselleştirme Seçenekleri")

# Görselleştirme kategorileri
visualization_category = st.sidebar.radio(
    "Görselleştirme Kategorisi Seçin",
    ["Demografik Analizler", "Sağlık Parametreleri", "İlişki Analizleri"]
)

# Demografik Analizler
if visualization_category == "Demografik Analizler":
    st.header("Demografik Analizler")
    
    # Alt kategori seçimi
    demographic_option = st.selectbox(
        "Görselleştirme Türü Seçin",
        ["Yaş Dağılımı", "Cinsiyet Dağılımı", "Yaş ve Cinsiyet İlişkisi"]
    )
    
    if demographic_option == "Yaş Dağılımı":
        st.subheader("Yaş Dağılımı ve Kalp Hastalığı İlişkisi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='Yaş', bins=20, kde=True, ax=ax)
            ax.set_title("Yaş Dağılımı")
            ax.set_xlabel("Yaş")
            ax.set_ylabel("Frekans")
            st.pyplot(fig)
        
        with col2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='Yaş', hue='KalpHastalığı', bins=20, kde=True, ax=ax)
            ax.set_title("Yaş Dağılımı ve Kalp Hastalığı İlişkisi")
            ax.set_xlabel("Yaş")
            ax.set_ylabel("Frekans")
            st.pyplot(fig)
        
        # Yaş gruplarına göre analiz
        st.subheader("Yaş Gruplarına Göre Kalp Hastalığı Oranı")
        
        # Yaş grupları oluşturma
        df_temp = df.copy()
        df_temp['AgeGroup'] = pd.cut(df_temp['Yaş'], bins=[20, 30, 40, 50, 60, 70, 80], labels=['20-30', '30-40', '40-50', '50-60', '60-70', '70-80'])
        
        # Yaş gruplarına göre kalp hastalığı oranı
        age_group_heart_disease = df_temp.groupby('AgeGroup')['KalpHastalığı'].mean() * 100
        
        fig, ax = plt.subplots(figsize=(10, 6))
        age_group_heart_disease.plot(kind='bar', ax=ax, color='coral')
        ax.set_title("Yaş Gruplarına Göre Kalp Hastalığı Oranı (%)")
        ax.set_xlabel("Yaş Grubu")
        ax.set_ylabel("Kalp Hastalığı Oranı (%)")
        ax.set_ylim(0, 100)
        
        # Değerleri çubukların üzerine ekleme
        for i, v in enumerate(age_group_heart_disease):
            ax.text(i, v + 2, f"{v:.1f}%", ha='center')
            
        st.pyplot(fig)
        
        # Yaş istatistikleri
        st.subheader("Yaş İstatistikleri")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Ortalama Yaş", f"{df['Yaş'].mean():.1f}")
        
        with col2:
            st.metric("Minimum Yaş", int(df['Yaş'].min()))
        
        with col3:
            st.metric("Maksimum Yaş", int(df['Yaş'].max()))
    
    elif demographic_option == "Cinsiyet Dağılımı":
        st.subheader("Cinsiyet Dağılımı ve Kalp Hastalığı İlişkisi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Veri çerçevesinin bir kopyasını oluştur
            df_gender = df.copy()
            
            # Sayısal değerler yerine metin değerlerini kullan
            df_gender['Cinsiyet_Label'] = df_gender['Cinsiyet'].map({1: 'Erkek', 0: 'Kadın'})
                
            # Cinsiyet dağılımı
            gender_count = df_gender['Cinsiyet_Label'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(gender_count, labels=gender_count.index, autopct='%1.1f%%', startangle=90, colors=['#66b3ff', '#ff9999'])
            ax.set_title("Cinsiyet Dağılımı")
            st.pyplot(fig)
            
            # Cinsiyet sayıları
            for gender, count in gender_count.items():
                st.write(f"**{gender}:** {count} kişi ({count/len(df_gender)*100:.1f}%)")
        
        with col2:
            # Cinsiyet ve kalp hastalığı ilişkisi
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.countplot(data=df_gender, x='Cinsiyet_Label', hue='KalpHastalığı', ax=ax)
            ax.set_title("Cinsiyet ve Kalp Hastalığı İlişkisi")
            ax.set_xlabel("Cinsiyet")
            ax.set_ylabel("Kişi Sayısı")
            st.pyplot(fig)
        
        # Cinsiyet bazında kalp hastalığı oranları
        st.subheader("Cinsiyet Bazında Kalp Hastalığı Oranları")
        
        gender_heart_disease = df_gender.groupby(['Cinsiyet_Label', 'KalpHastalığı']).size().unstack()
        gender_heart_disease_percent = gender_heart_disease.div(gender_heart_disease.sum(axis=1), axis=0) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Cinsiyet Bazında Kalp Hastalığı Sayıları")
            st.dataframe(gender_heart_disease)
        
        with col2:
            st.write("Cinsiyet Bazında Kalp Hastalığı Oranları (%)")
            st.dataframe(gender_heart_disease_percent.round(1))
        
        # Cinsiyet bazında kalp hastalığı oranları grafiği
        fig, ax = plt.subplots(figsize=(10, 6))
        gender_heart_disease_percent[1].plot(kind='bar', ax=ax, color='coral')
        ax.set_title("Cinsiyet Bazında Kalp Hastalığı Oranı (%)")
        ax.set_xlabel("Cinsiyet")
        ax.set_ylabel("Kalp Hastalığı Oranı (%)")
        ax.set_ylim(0, 100)
        
        # Değerleri çubukların üzerine ekleme
        for i, v in enumerate(gender_heart_disease_percent[1]):
            ax.text(i, v + 2, f"{v:.1f}%", ha='center')
            
        st.pyplot(fig)
    
    elif demographic_option == "Yaş ve Cinsiyet İlişkisi":
        st.subheader("Yaş ve Cinsiyet İlişkisi")
        
        # Veri hazırlama
        df_temp = df.copy()
        df_temp['Cinsiyet_Label'] = df_temp['Cinsiyet'].map({1: 'Erkek', 0: 'Kadın'})
        
        # Cinsiyete göre yaş dağılımı
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_temp, x='Cinsiyet_Label', y='Yaş', ax=ax)
        ax.set_title("Cinsiyete Göre Yaş Dağılımı")
        ax.set_xlabel("Cinsiyet")
        ax.set_ylabel("Yaş")
        st.pyplot(fig)
        
        # Cinsiyete ve kalp hastalığına göre yaş dağılımı
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(data=df_temp, x='Cinsiyet_Label', y='Yaş', hue='KalpHastalığı', ax=ax)
        ax.set_title("Cinsiyete ve Kalp Hastalığına Göre Yaş Dağılımı")
        ax.set_xlabel("Cinsiyet")
        ax.set_ylabel("Yaş")
        st.pyplot(fig)
        
        # Yaş grupları ve cinsiyet dağılımı
        st.subheader("Yaş Grupları ve Cinsiyet Dağılımı")
        
        # Yaş grupları oluşturma
        df_temp['AgeGroup'] = pd.cut(df_temp['Yaş'], bins=[20, 30, 40, 50, 60, 70, 80], labels=['20-30', '30-40', '40-50', '50-60', '60-70', '70-80'])
        
        # Yaş grupları ve cinsiyet dağılımı
        age_gender_distribution = pd.crosstab(df_temp['AgeGroup'], df_temp['Cinsiyet_Label'])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        age_gender_distribution.plot(kind='bar', ax=ax)
        ax.set_title("Yaş Grupları ve Cinsiyet Dağılımı")
        ax.set_xlabel("Yaş Grubu")
        ax.set_ylabel("Kişi Sayısı")
        st.pyplot(fig)

# Sağlık Parametreleri
elif visualization_category == "Sağlık Parametreleri":
    st.header("Sağlık Parametreleri Analizleri")
    
    # Alt kategori seçimi
    health_param_option = st.selectbox(
        "Görselleştirme Türü Seçin",
        ["Göğüs Ağrısı Tipi", "Kolesterol ve Kan Basıncı", "Kalp Hızı ve Egzersiz Angina", "ST Eğimi ve Oldpeak"]
    )
    
    if health_param_option == "Göğüs Ağrısı Tipi":
        st.subheader("Göğüs Ağrısı Tipi Analizi")
        
        # Göğüs ağrısı tipi açıklaması
        st.markdown("""
       **Göğüs Ağrısı Tipleri:**
       - **0**: Asemptomatik (ASY)  
       Hasta göğüs ağrısı hissetmiyor ancak kalp hastalığı belirtileri testlerde ortaya çıkabilir.
       - **1**: Atipik Angina (ATA)  
       Göğüs ağrısı mevcut ama klasik anjina belirtilerine tam olarak uymuyor, kalp dışı nedenler de olabilir.
       - **2**: Non-Anginal Ağrı (NAP)  
       Göğüs ağrısı var ancak kalp ile ilgili değil; genellikle kas, mide gibi başka kaynaklardan kaynaklanır.
       - **3**: Tipik Angina (TA)  
       Fiziksel aktiviteyle artan, dinlenmeyle azalan klasik göğüs ağrısı; kalp hastalığı ile yüksek oranda ilişkilidir.
       """)
        
        # Veri çerçevesinin bir kopyasını oluştur
        df_chest_pain = df.copy()
        
        # Sayısal değerler yerine metin değerlerini kullan
        chest_pain_mapping = {0: 'ASY', 1: 'ATA', 2: 'NAP', 3: 'TA'}
        df_chest_pain['GöğüsAğrısı_Label'] = df_chest_pain['GöğüsAğrısıTürü'].map(chest_pain_mapping)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Göğüs ağrısı tipi dağılımı
            chest_pain_count = df_chest_pain['GöğüsAğrısı_Label'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(chest_pain_count, labels=chest_pain_count.index, autopct='%1.1f%%', startangle=90, 
                  colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'])
            ax.set_title("Göğüs Ağrısı Tipi Dağılımı")
            st.pyplot(fig)
        
        with col2:
            # Göğüs ağrısı tipi ve kalp hastalığı ilişkisi
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.countplot(data=df_chest_pain, x='GöğüsAğrısı_Label', hue='KalpHastalığı', ax=ax)
            ax.set_title("Göğüs Ağrısı Tipi ve Kalp Hastalığı İlişkisi")
            ax.set_xlabel("Göğüs Ağrısı Tipi")
            ax.set_ylabel("Kişi Sayısı")
            st.pyplot(fig)
        
        # Göğüs ağrısı tipine göre kalp hastalığı oranı
        st.subheader("Göğüs Ağrısı Tipine Göre Kalp Hastalığı Oranı")
        
        chest_pain_heart_disease = df_chest_pain.groupby(['GöğüsAğrısı_Label', 'KalpHastalığı']).size().unstack()
        chest_pain_heart_disease_percent = chest_pain_heart_disease.div(chest_pain_heart_disease.sum(axis=1), axis=0) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("Göğüs Ağrısı Tipine Göre Kalp Hastalığı Sayıları")
            st.dataframe(chest_pain_heart_disease)
        
        with col2:
            st.write("Göğüs Ağrısı Tipine Göre Kalp Hastalığı Oranları (%)")
            st.dataframe(chest_pain_heart_disease_percent.round(1))
        
        # Göğüs ağrısı tipine göre kalp hastalığı oranı grafiği
        fig, ax = plt.subplots(figsize=(10, 6))
        chest_pain_heart_disease_percent[1].plot(kind='bar', ax=ax, color='coral')
        ax.set_title("Göğüs Ağrısı Tipine Göre Kalp Hastalığı Oranı (%)")
        ax.set_xlabel("Göğüs Ağrısı Tipi")
        ax.set_ylabel("Kalp Hastalığı Oranı (%)")
        ax.set_ylim(0, 100)
        
        # Değerleri çubukların üzerine ekleme
        for i, v in enumerate(chest_pain_heart_disease_percent[1]):
            ax.text(i, v + 2, f"{v:.1f}%", ha='center')
            
        st.pyplot(fig)
    
    elif health_param_option == "Kolesterol ve Kan Basıncı":
        st.subheader("Kolesterol ve Kan Basıncı Analizi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Kolesterol dağılımı
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='Kolesterol', bins=20, kde=True, ax=ax)
            ax.set_title("Kolesterol Dağılımı")
            ax.set_xlabel("Kolesterol (mg/dl)")
            ax.set_ylabel("Frekans")
            st.pyplot(fig)
            
            # Kolesterol istatistikleri
            st.write(f"**Ortalama Kolesterol:** {df['Kolesterol'].mean():.1f} mg/dl")
            st.write(f"**Minimum Kolesterol:** {df['Kolesterol'].min()} mg/dl")
            st.write(f"**Maksimum Kolesterol:** {df['Kolesterol'].max()} mg/dl")
        
        with col2:
            # Kan basıncı dağılımı
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='İstirahatKanBasıncı', bins=20, kde=True, ax=ax)
            ax.set_title("İstirahat Kan Basıncı Dağılımı")
            ax.set_xlabel("İstirahat Kan Basıncı (mm Hg)")
            ax.set_ylabel("Frekans")
            st.pyplot(fig)
            
            # Kan basıncı istatistikleri
            st.write(f"**Ortalama Kan Basıncı:** {df['İstirahatKanBasıncı'].mean():.1f} mm Hg")
            st.write(f"**Minimum Kan Basıncı:** {df['İstirahatKanBasıncı'].min()} mm Hg")
            st.write(f"**Maksimum Kan Basıncı:** {df['İstirahatKanBasıncı'].max()} mm Hg")
        
        # Kolesterol ve kan basıncı ilişkisi
        st.subheader("Kolesterol ve Kan Basıncı İlişkisi")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='Kolesterol', y='İstirahatKanBasıncı', hue='KalpHastalığı', ax=ax)
        ax.set_title("Kolesterol ve Kan Basıncı İlişkisi")
        ax.set_xlabel("Kolesterol (mg/dl)")
        ax.set_ylabel("İstirahat Kan Basıncı (mm Hg)")
        st.pyplot(fig)
    
    elif health_param_option == "Kalp Hızı ve Egzersiz Angina":
        st.subheader("Kalp Hızı ve Egzersiz Angina Analizi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Maksimum kalp hızı dağılımı
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='MaksimumKalpHızı', bins=20, kde=True, ax=ax)
            ax.set_title("Maksimum Kalp Hızı Dağılımı")
            ax.set_xlabel("Maksimum Kalp Hızı")
            ax.set_ylabel("Frekans")
            st.pyplot(fig)
            
            # Maksimum kalp hızı istatistikleri
            st.write(f"**Ortalama Maksimum Kalp Hızı:** {df['MaksimumKalpHızı'].mean():.1f}")
            st.write(f"**Minimum Maksimum Kalp Hızı:** {df['MaksimumKalpHızı'].min()}")
            st.write(f"**Maksimum Maksimum Kalp Hızı:** {df['MaksimumKalpHızı'].max()}")
        
        with col2:
            # Egzersiz angina dağılımı
            df_temp = df.copy()
            df_temp['EgzersizAngina_Label'] = df_temp['EgzersizAnginası'].map({1: 'Evet', 0: 'Hayır'})
            
            exercise_angina_count = df_temp['EgzersizAngina_Label'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(exercise_angina_count, labels=exercise_angina_count.index, autopct='%1.1f%%', startangle=90, 
                  colors=['#99ff99', '#ff9999'])
            ax.set_title("Egzersiz Angina Dağılımı")
            st.pyplot(fig)
            
            # Egzersiz angina sayıları
            for angina, count in exercise_angina_count.items():
                st.write(f"**{angina}:** {count} kişi ({count/len(df)*100:.1f}%)")
        
        # Yaş ve maksimum kalp hızı ilişkisi
        st.subheader("Yaş ve Maksimum Kalp Hızı İlişkisi")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=df, x='Yaş', y='MaksimumKalpHızı', hue='KalpHastalığı', ax=ax)
        ax.set_title("Yaş ve Maksimum Kalp Hızı İlişkisi")
        ax.set_xlabel("Yaş")
        ax.set_ylabel("Maksimum Kalp Hızı")
        st.pyplot(fig)
    
    elif health_param_option == "ST Eğimi ve Oldpeak":
        st.subheader("ST Eğimi ve Oldpeak Analizi")
        
        # ST Eğimi açıklaması
        st.markdown("""
        **ST Eğimi (ST_Slope):**
        - **0**: Aşağı eğimli (Down)  
        Egzersiz sırasında ST segmenti aşağı doğru eğim gösteriyor. Bu durum genellikle kalp kasına yeterince oksijen gitmediğini (iskemi) gösterir ve **kalp hastalığı riski yüksektir**.
        - **1**: Düz (Flat)  
        ST segmenti egzersiz sırasında düz kalır. Bu da anormal bir durum olabilir ve **kalp hastalığına işaret edebilir**.
        - **2**: Yukarı eğimli (Up)  
        Egzersiz sırasında ST segmenti yukarı eğimlidir. Bu genellikle **normal** kabul edilir ve **kalp hastalığı riski düşüktür**.
        """)

        
        # Veri hazırlama
        df_temp = df.copy()
        st_slope_mapping = {0: 'Down', 1: 'Flat', 2: 'Up'}
        df_temp['ST_Eğimi_Label'] = df_temp['ST_Eğimi'].map(st_slope_mapping)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # ST Eğimi dağılımı
            st_slope_count = df_temp['ST_Eğimi_Label'].value_counts()
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(st_slope_count, labels=st_slope_count.index, autopct='%1.1f%%', startangle=90, 
                  colors=['#99ff99', '#ffcc99', '#ff9999'])
            ax.set_title("ST Eğimi Dağılımı")
            st.pyplot(fig)
            
            # ST Eğimi sayıları
            for slope, count in st_slope_count.items():
                st.write(f"**{slope}:** {count} kişi ({count/len(df)*100:.1f}%)")
        
        with col2:
            # ST Depresyonu dağılımı
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data=df, x='STDepresyonu', bins=20, kde=True, ax=ax)
            ax.set_title("ST Depresyonu Dağılımı")
            ax.set_xlabel("ST Depresyonu")
            ax.set_ylabel("Frekans")
            st.pyplot(fig)
            
            # ST Depresyonu istatistikleri
            st.write(f"**Ortalama ST Depresyonu:** {df['STDepresyonu'].mean():.2f}")
            st.write(f"**Minimum ST Depresyonu:** {df['STDepresyonu'].min():.2f}")
            st.write(f"**Maksimum ST Depresyonu:** {df['STDepresyonu'].max():.2f}")
        
        # ST Eğimi ve kalp hastalığı ilişkisi
        st.subheader("ST Eğimi ve Kalp Hastalığı İlişkisi")
        
        st_slope_heart_disease = df_temp.groupby(['ST_Eğimi_Label', 'KalpHastalığı']).size().unstack()
        st_slope_heart_disease_percent = st_slope_heart_disease.div(st_slope_heart_disease.sum(axis=1), axis=0) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("ST Eğimine Göre Kalp Hastalığı Sayıları")
            st.dataframe(st_slope_heart_disease)
        
        with col2:
            st.write("ST Eğimine Göre Kalp Hastalığı Oranları (%)")
            st.dataframe(st_slope_heart_disease_percent.round(1))
        
        # ST Eğimine göre kalp hastalığı oranı grafiği
        fig, ax = plt.subplots(figsize=(10, 6))
        st_slope_heart_disease_percent[1].plot(kind='bar', ax=ax, color='coral')
        ax.set_title("ST Eğimine Göre Kalp Hastalığı Oranı (%)")
        ax.set_xlabel("ST Eğimi")
        ax.set_ylabel("Kalp Hastalığı Oranı (%)")
        ax.set_ylim(0, 100)
        
        # Değerleri çubukların üzerine ekleme
        for i, v in enumerate(st_slope_heart_disease_percent[1]):
            ax.text(i, v + 2, f"{v:.1f}%", ha='center')
            
        st.pyplot(fig)
# İlişki Analizleri
elif visualization_category == "İlişki Analizleri":
    st.header("İlişki Analizleri")
    
    # Alt kategori seçimi
    relation_option = st.selectbox(
        "Görselleştirme Türü Seçin",
        ["Korelasyon Matrisi", "Özellik Önem Analizi", "Çoklu Değişken Analizi"]
    )
    
    if relation_option == "Korelasyon Matrisi":
        st.subheader("Özellikler Arası Korelasyon Matrisi")
        
        # Kategorik değişkenleri sayısallaştırma
        df_corr = df.copy()
        
        # Türkçe sütun adlarına göre düzenleme
        if 'Cinsiyet' in df_corr.columns:
            df_corr['Cinsiyet'] = df_corr['Cinsiyet'].astype(int)
        
        if 'GöğüsAğrısıTürü' in df_corr.columns:
            df_corr['GöğüsAğrısıTürü'] = df_corr['GöğüsAğrısıTürü'].astype(int)
        
        if 'İstirahatEKG' in df_corr.columns:
            df_corr['İstirahatEKG'] = df_corr['İstirahatEKG'].astype(int)
        
        if 'EgzersizAnginası' in df_corr.columns:
            df_corr['EgzersizAnginası'] = df_corr['EgzersizAnginası'].astype(int)
        
        if 'ST_Eğimi' in df_corr.columns:
            df_corr['ST_Eğimi'] = df_corr['ST_Eğimi'].astype(int)
        
        # Sayısal sütunları seçme
        numeric_df = df_corr.select_dtypes(include=[np.number])
        
        # Korelasyon matrisini hesaplama
        corr = numeric_df.corr()
        
        # Korelasyon matrisini görselleştirme
        fig, ax = plt.subplots(figsize=(12, 10))
        mask = np.triu(np.ones_like(corr, dtype=bool))
        cmap = sns.diverging_palette(230, 20, as_cmap=True)
        sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                    square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True, fmt=".2f")
        ax.set_title("Özellikler Arası Korelasyon Matrisi")
        st.pyplot(fig)
        
        st.markdown("""
        **Korelasyon Matrisi Yorumu:**
        
        Korelasyon matrisi, veri setindeki sayısal özellikler arasındaki ilişkiyi gösterir. 
        1'e yakın değerler güçlü pozitif korelasyonu, -1'e yakın değerler güçlü negatif korelasyonu, 
        0'a yakın değerler ise zayıf veya hiç korelasyon olmadığını gösterir.
        
        **Önemli Korelasyonlar:**
        - **Yaş ve Maksimum Kalp Hızı**: Negatif korelasyon - Yaş arttıkça maksimum kalp hızı düşme eğilimindedir.
        - **ST Depresyonu ve ST Eğimi**: Yüksek korelasyon - ST eğimi ile ST Depresyonu değeri arasında güçlü bir ilişki vardır.
        - **Egzersiz Angina ve Kalp Hastalığı**: Pozitif korelasyon - Egzersiz sırasında angina yaşayanların kalp hastalığı riski daha yüksektir.
        """)
    
    elif relation_option == "Özellik Önem Analizi":
        st.subheader("Özellik Önem Analizi")
        
        st.write("""
        Bu analiz, hangi özelliklerin kalp hastalığı tahmini için daha önemli olduğunu gösterir.
        Özellik önem analizi için basit bir lojistik regresyon modeli kullanılmıştır.
        """)
        
        # Veri setini hazırlama
        df_model = df.copy()
        
        # Bağımsız değişkenler ve hedef değişken
        if 'KalpHastalığı' in df_model.columns:
            X = df_model.drop('KalpHastalığı', axis=1)
            y = df_model['KalpHastalığı']
        else:
            st.error("KalpHastalığı sütunu bulunamadı!")
            st.stop()
        
        # Lojistik regresyon modeli
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        
        # Verileri ölçeklendirme
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Modeli eğitme
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_scaled, y)
        
        # Özellik önemlerini hesaplama
        feature_importance = pd.DataFrame({
            'Feature': X.columns,
            'Importance': np.abs(model.coef_[0])
        })
        
        # Özellik önemlerini sıralama
        feature_importance = feature_importance.sort_values('Importance', ascending=False)
        
        # Özellik önemlerini görselleştirme
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.barplot(data=feature_importance, x='Importance', y='Feature', ax=ax)
        ax.set_title("Özellik Önem Analizi")
        ax.set_xlabel("Önem Derecesi")
        ax.set_ylabel("Özellik")
        st.pyplot(fig)
        
        st.markdown("""
        **Özellik Önem Analizi Yorumu:**
        
        Bu grafik, her bir özelliğin kalp hastalığı tahmini üzerindeki etkisini göstermektedir. 
        Çubuk ne kadar uzunsa, o özelliğin modeldeki önemi o kadar fazladır.
        
        **En Önemli Özellikler:**
        - Göğüs ağrısı tipi
        - ST eğimi
        - Egzersiz angina
        - Maksimum kalp hızı
        - ST depresyonu
        
        Bu özellikler, kalp hastalığı riskini değerlendirirken daha fazla dikkat edilmesi gereken faktörlerdir.
        """)
    
    elif relation_option == "Çoklu Değişken Analizi":
        st.subheader("Çoklu Değişken Analizi")
        
        # Analiz türü seçimi
        multi_var_option = st.selectbox(
            "Analiz Türü Seçin",
            ["Yaş, Cinsiyet ve Kalp Hastalığı", "Göğüs Ağrısı, Egzersiz Angina ve Kalp Hastalığı", 
             "Kolesterol, Kan Basıncı ve Kalp Hastalığı", "Yaş, Maksimum Kalp Hızı ve Kalp Hastalığı"]
        )
        
        if multi_var_option == "Yaş, Cinsiyet ve Kalp Hastalığı":
            st.write("Bu analiz, yaş ve cinsiyet faktörlerinin kalp hastalığı riski üzerindeki etkisini gösterir.")
            
            # Yaş grupları oluşturma
            df['YaşGrubu'] = pd.cut(df['Yaş'], bins=[20, 30, 40, 50, 60, 70, 80], 
                                   labels=['20-30', '30-40', '40-50', '50-60', '60-70', '70-80'])
            
            # Cinsiyet etiketleri
            df['CinsiyetLabel'] = df['Cinsiyet'].map({1: 'Erkek', 0: 'Kadın'})
            
            # Yaş grupları, cinsiyet ve kalp hastalığı dağılımı
            age_sex_heart = pd.crosstab([df['YaşGrubu'], df['CinsiyetLabel']], df['KalpHastalığı'])
            age_sex_heart_percent = age_sex_heart.div(age_sex_heart.sum(axis=1), axis=0) * 100
            
            # Grafik
            fig, ax = plt.subplots(figsize=(14, 8))
            age_sex_heart_percent[1].unstack().plot(kind='bar', ax=ax)
            ax.set_title("Yaş Grupları ve Cinsiyete Göre Kalp Hastalığı Oranı (%)")
            ax.set_xlabel("Yaş Grubu ve Cinsiyet")
            ax.set_ylabel("Kalp Hastalığı Oranı (%)")
            ax.set_ylim(0, 100)
            ax.legend(title="Cinsiyet")
            plt.xticks(rotation=45)
            
            st.pyplot(fig)
            
            st.markdown("""
            **Analiz Yorumu:**
            
            Bu grafik, farklı yaş grupları ve cinsiyetlere göre kalp hastalığı oranını göstermektedir. 
            Genel olarak, yaş arttıkça kalp hastalığı riski artmaktadır. Ayrıca, erkeklerde kalp hastalığı riski 
            kadınlara göre daha yüksektir, özellikle orta yaş gruplarında bu fark daha belirgindir.
            """)
        
        elif multi_var_option == "Göğüs Ağrısı, Egzersiz Angina ve Kalp Hastalığı":
            st.write("Bu analiz, göğüs ağrısı tipi ve egzersiz angina faktörlerinin kalp hastalığı riski üzerindeki etkisini gösterir.")
            
            # Göğüs ağrısı tipi etiketleri
            chest_pain_labels = {0: 'Tip 0', 1: 'Tip 1', 2: 'Tip 2', 3: 'Tip 3'}
            df['GöğüsAğrısıLabel'] = df['GöğüsAğrısıTürü'].map(chest_pain_labels)
            
            # Egzersiz angina etiketleri
            df['EgzersizAnginasıLabel'] = df['EgzersizAnginası'].map({1: 'Evet', 0: 'Hayır'})
            
            # Göğüs ağrısı tipi, egzersiz angina ve kalp hastalığı dağılımı
            chest_angina_heart = pd.crosstab([df['GöğüsAğrısıLabel'], df['EgzersizAnginasıLabel']], df['KalpHastalığı'])
            chest_angina_heart_percent = chest_angina_heart.div(chest_angina_heart.sum(axis=1), axis=0) * 100
            
            # Grafik
            fig, ax = plt.subplots(figsize=(14, 8))
            chest_angina_heart_percent[1].unstack().plot(kind='bar', ax=ax)
            ax.set_title("Göğüs Ağrısı Tipi ve Egzersiz Anginaya Göre Kalp Hastalığı Oranı (%)")
            ax.set_xlabel("Göğüs Ağrısı Tipi ve Egzersiz Angina")
            ax.set_ylabel("Kalp Hastalığı Oranı (%)")
            ax.set_ylim(0, 100)
            ax.legend(title="Egzersiz Angina")
            plt.xticks(rotation=45)
            
            st.pyplot(fig)
            
            st.markdown("""
            **Analiz Yorumu:**
            
            Bu grafik, farklı göğüs ağrısı tipleri ve egzersiz angina durumlarına göre kalp hastalığı oranını göstermektedir. 
            Egzersiz sırasında angina yaşayanların kalp hastalığı riski belirgin şekilde daha yüksektir.
            """)
        
        elif multi_var_option == "Kolesterol, Kan Basıncı ve Kalp Hastalığı":
            st.write("Bu analiz, kolesterol ve kan basıncı faktörlerinin kalp hastalığı riski üzerindeki etkisini gösterir.")
            
            # Kolesterol grupları oluşturma
            df['KolesterolGrubu'] = pd.cut(df['Kolesterol'], 
                                          bins=[0, 200, 240, 600], 
                                          labels=['Normal (<200)', 'Sınırda (200-240)', 'Yüksek (>240)'])
            
            # Kan basıncı grupları oluşturma
            df['KanBasıncıGrubu'] = pd.cut(df['İstirahatKanBasıncı'], 
                                          bins=[0, 120, 140, 200], 
                                          labels=['Normal (<120)', 'Prehipertansiyon (120-140)', 'Hipertansiyon (>140)'])
            
            # Kolesterol, kan basıncı ve kalp hastalığı dağılımı
            chol_bp_heart = pd.crosstab([df['KolesterolGrubu'], df['KanBasıncıGrubu']], df['KalpHastalığı'])
            chol_bp_heart_percent = chol_bp_heart.div(chol_bp_heart.sum(axis=1), axis=0) * 100
            
            # Grafik
            fig, ax = plt.subplots(figsize=(14, 8))
            chol_bp_heart_percent[1].unstack().plot(kind='bar', ax=ax)
            ax.set_title("Kolesterol ve Kan Basıncı Gruplarına Göre Kalp Hastalığı Oranı (%)")
            ax.set_xlabel("Kolesterol ve Kan Basıncı Grupları")
            ax.set_ylabel("Kalp Hastalığı Oranı (%)")
            ax.set_ylim(0, 100)
            ax.legend(title="Kan Basıncı")
            plt.xticks(rotation=45)
            
            st.pyplot(fig)
            
            st.markdown("""
            **Analiz Yorumu:**
            
            Bu grafik, farklı kolesterol ve kan basıncı gruplarına göre kalp hastalığı oranını göstermektedir. 
            Yüksek kolesterol ve hipertansiyon, kalp hastalığı riskini artıran faktörlerdir. Özellikle her iki 
            faktörün de yüksek olduğu durumlarda kalp hastalığı riski daha da artmaktadır.
            """)
        
        elif multi_var_option == "Yaş, Maksimum Kalp Hızı ve Kalp Hastalığı":
            st.write("Bu analiz, yaş ve maksimum kalp hızı faktörlerinin kalp hastalığı riski üzerindeki etkisini gösterir.")
            
            # Yaş grupları oluşturma
            df['YaşGrubu'] = pd.cut(df['Yaş'], bins=[20, 40, 60, 80], 
                                   labels=['Genç (20-40)', 'Orta Yaş (40-60)', 'Yaşlı (60-80)'])
            
            # Maksimum kalp hızı grupları oluşturma
            df['KalpHızıGrubu'] = pd.cut(df['MaksimumKalpHızı'], 
                                        bins=[0, 120, 150, 220], 
                                        labels=['Düşük (<120)', 'Normal (120-150)', 'Yüksek (>150)'])
            
            # Yaş, maksimum kalp hızı ve kalp hastalığı dağılımı
            age_hr_heart = pd.crosstab([df['YaşGrubu'], df['KalpHızıGrubu']], df['KalpHastalığı'])
            age_hr_heart_percent = age_hr_heart.div(age_hr_heart.sum(axis=1), axis=0) * 100
            
            # Grafik
            fig, ax = plt.subplots(figsize=(14, 8))
            age_hr_heart_percent[1].unstack().plot(kind='bar', ax=ax)
            ax.set_title("Yaş ve Maksimum Kalp Hızı Gruplarına Göre Kalp Hastalığı Oranı (%)")
            ax.set_xlabel("Yaş ve Maksimum Kalp Hızı Grupları")
            ax.set_ylabel("Kalp Hastalığı Oranı (%)")
            ax.set_ylim(0, 100)
            ax.legend(title="Maksimum Kalp Hızı")
            plt.xticks(rotation=45)
            
            st.pyplot(fig)
            
            # Yaş ve maksimum kalp hızı ilişkisi
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(data=df, x='Yaş', y='MaksimumKalpHızı', hue='KalpHastalığı', ax=ax)
            ax.set_title("Yaş ve Maksimum Kalp Hızı İlişkisi")
            ax.set_xlabel("Yaş")
            ax.set_ylabel("Maksimum Kalp Hızı")
            st.pyplot(fig)
            
            st.markdown("""
            **Analiz Yorumu:**
            
            Bu grafik, farklı yaş grupları ve maksimum kalp hızı gruplarına göre kalp hastalığı oranını göstermektedir. 
            Yaş arttıkça ve maksimum kalp hızı düştükçe kalp hastalığı riski artma eğilimindedir. Özellikle yaşlı 
            grupta ve düşük maksimum kalp hızına sahip kişilerde kalp hastalığı riski daha yüksektir.
            
            Ayrıca, yaş ve maksimum kalp hızı arasında negatif bir korelasyon vardır, yani yaş arttıkça maksimum 
            kalp hızı düşme eğilimindedir.
            """)

# Footer
st.markdown("---")
st.markdown("© 2025 Kalp Hastalığı Analiz Platformu | Streamlit ile geliştirilmiştir.")
