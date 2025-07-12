import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# Sayfa yapılandırması
st.set_page_config(
    page_title="Tahmin Modeli - Kalp Yetmezliği Analiz Platformu",
    page_icon="🔮",
    layout="wide"
)

# Sayfa başlığı
st.title("🔮 Kalp Yetmezliği Tahmin Modeli")
st.markdown("Bu sayfada kalp hastalığı riskini tahmin etmek için makine öğrenmesi modelleri kullanabilirsiniz.")

# Veri setini yükleme
@st.cache_data
def load_data():
    data = pd.read_csv('heart_cleaned.csv')
    return data

df = load_data()

# Sidebar oluşturma
st.sidebar.header("Model Seçenekleri")

# Model seçimi
model_option = st.sidebar.selectbox(
    "Tahmin Modeli Seçin",
    ["Lojistik Regresyon", "Rastgele Orman", "Destek Vektör Makinesi"]
)

# Test veri seti boyutu ve random state değerleri
test_size = 0.20
random_state = 40

# Veri ön işleme fonksiyonu - VERİ SETİNİZLE UYUMLU HALE GETİRİLDİ
def preprocess_data(df, is_training=True, reference_columns=None):
    """
    Veri ön işleme fonksiyonu
    """
    df_processed = df.copy()
    
    # Cinsiyet dönüşümü (1: Erkek, 0: Kadın)
    if 'Cinsiyet' in df_processed.columns:
        # Zaten sayısal format, sadece eksik değerleri kontrol et
        if df_processed['Cinsiyet'].isnull().any():
            df_processed['Cinsiyet'] = df_processed['Cinsiyet'].fillna(1)
    
    # Göğüs ağrısı tipi dönüşümü
    if 'GöğüsAğrısıTürü' in df_processed.columns:
        # Eksik değerleri doldurma
        if df_processed['GöğüsAğrısıTürü'].isnull().any():
            df_processed['GöğüsAğrısıTürü'] = df_processed['GöğüsAğrısıTürü'].fillna(0)
        
        # One-hot encoding
        chest_pain_dummies = pd.get_dummies(df_processed['GöğüsAğrısıTürü'], prefix='GöğüsAğrısıTürü')
        df_processed = pd.concat([df_processed, chest_pain_dummies], axis=1)
        df_processed = df_processed.drop('GöğüsAğrısıTürü', axis=1)
    
    # İstirahat EKG dönüşümü
    if 'İstirahatEKG' in df_processed.columns:
        # Eksik değerleri doldurma
        if df_processed['İstirahatEKG'].isnull().any():
            df_processed['İstirahatEKG'] = df_processed['İstirahatEKG'].fillna(0)
        
        # One-hot encoding
        ecg_dummies = pd.get_dummies(df_processed['İstirahatEKG'], prefix='İstirahatEKG')
        df_processed = pd.concat([df_processed, ecg_dummies], axis=1)
        df_processed = df_processed.drop('İstirahatEKG', axis=1)
    
    # Egzersiz angina dönüşümü (1: Var, 0: Yok)
    if 'EgzersizAnginası' in df_processed.columns:
        if df_processed['EgzersizAnginası'].isnull().any():
            df_processed['EgzersizAnginası'] = df_processed['EgzersizAnginası'].fillna(0)
    
    # ST eğimi dönüşümü
    if 'ST_Eğimi' in df_processed.columns:
        # Eksik değerleri doldurma
        if df_processed['ST_Eğimi'].isnull().any():
            df_processed['ST_Eğimi'] = df_processed['ST_Eğimi'].fillna(1)
        
        # One-hot encoding
        st_slope_dummies = pd.get_dummies(df_processed['ST_Eğimi'], prefix='ST_Eğimi')
        df_processed = pd.concat([df_processed, st_slope_dummies], axis=1)
        df_processed = df_processed.drop('ST_Eğimi', axis=1)
    
    # Sayısal değişkenlerdeki eksik değerleri doldurma
    numeric_cols = ['Yaş', 'İstirahatKanBasıncı', 'Kolesterol', 'AçlıkKanŞekeri', 'MaksimumKalpHızı', 'STDepresyonu']
    for col in numeric_cols:
        if col in df_processed.columns and df_processed[col].isnull().any():
            df_processed[col] = df_processed[col].fillna(df_processed[col].mean() if len(df_processed) > 1 else 0)
    
    # Eğitim verisi değilse, referans sütunlara göre düzenleme
    if not is_training and reference_columns is not None:
        # Eksik sütunları ekle
        for col in reference_columns:
            if col not in df_processed.columns:
                df_processed[col] = 0
        
        # Sütun sırasını düzenle
        df_processed = df_processed[reference_columns]
    
    return df_processed

# Veri setini ön işleme
df_processed = preprocess_data(df, is_training=True)

# Bağımsız değişkenler ve hedef değişken
X = df_processed.drop('KalpHastalığı', axis=1)
feature_names = X.columns.tolist()
y = df_processed['KalpHastalığı']

# Veri setini eğitim ve test olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

# Veri ölçeklendirme
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model seçimi ve eğitimi
def train_model(model_option, X_train, y_train):
    if model_option == "Lojistik Regresyon":
        model = LogisticRegression(max_iter=1000, random_state=random_state)
    elif model_option == "Rastgele Orman":
        model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    elif model_option == "Destek Vektör Makinesi":
        model = SVC(probability=True, random_state=random_state)
    
    model.fit(X_train, y_train)
    return model

# Modeli eğitme
model = train_model(model_option, X_train_scaled, y_train)

# Model performansını değerlendirme
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred, output_dict=True)

# Model sonuçlarını gösterme
st.header("Model Performansı")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Model Bilgileri")
    st.write(f"**Seçilen Model:** {model_option}")
    st.write(f"**Eğitim Veri Seti Boyutu:** {len(X_train)} örnek ({(1-test_size)*100:.0f}%)")
    st.write(f"**Test Veri Seti Boyutu:** {len(X_test)} örnek ({test_size*100:.0f}%)")
    st.write(f"**Doğruluk (Accuracy):** {accuracy:.4f} ({accuracy*100:.2f}%)")
    
    # Sınıflandırma raporu
    st.subheader("Sınıflandırma Raporu")
    
    # Precision, Recall ve F1-Score değerlerini gösterme
    precision_0 = class_report['0']['precision']
    recall_0 = class_report['0']['recall']
    f1_0 = class_report['0']['f1-score']
    
    precision_1 = class_report['1']['precision']
    recall_1 = class_report['1']['recall']
    f1_1 = class_report['1']['f1-score']
    
    st.write(f"**Kalp Hastalığı Yok (0):**")
    st.write(f"- Precision: {precision_0:.4f}")
    st.write(f"- Recall: {recall_0:.4f}")
    st.write(f"- F1-Score: {f1_0:.4f}")
    
    st.write(f"**Kalp Hastalığı Var (1):**")
    st.write(f"- Precision: {precision_1:.4f}")
    st.write(f"- Recall: {recall_1:.4f}")
    st.write(f"- F1-Score: {f1_1:.4f}")

with col2:
    # Karmaşıklık matrisi
    st.subheader("Karmaşıklık Matrisi (Confusion Matrix)")
    
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Tahmin Edilen Sınıf')
    ax.set_ylabel('Gerçek Sınıf')
    ax.set_title('Karmaşıklık Matrisi')
    ax.set_xticklabels(['Kalp Hastalığı Yok (0)', 'Kalp Hastalığı Var (1)'])
    ax.set_yticklabels(['Kalp Hastalığı Yok (0)', 'Kalp Hastalığı Var (1)'])
    st.pyplot(fig)
    
    # Özellik önemleri (Rastgele Orman için)
    if model_option == "Rastgele Orman":
        st.subheader("Özellik Önemleri")
        
        feature_importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            'Özellik': feature_names,
            'Önem': feature_importances
        }).sort_values('Önem', ascending=False)
        
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.barplot(data=feature_importance_df, x='Önem', y='Özellik', ax=ax)
        ax.set_title("Özellik Önemleri (Rastgele Orman)")
        ax.set_xlabel("Önem Derecesi")
        ax.set_ylabel("Özellik")
        st.pyplot(fig)

# Tahmin bölümü
st.header("Kalp Hastalığı Riski Tahmini")
st.markdown("Kendi sağlık verilerinizi girerek kalp hastalığı riskinizi tahmin edebilirsiniz.")

# Form oluşturma
st.subheader("Veri Girişi")

# Yatay düzende form elemanları için container oluşturma
form_container = st.container()

# İlk satır - Yaş ve Cinsiyet
row1_col1, row1_col2 = form_container.columns(2)
with row1_col1:
    st.markdown("**Yaş**")
    age = st.number_input("Yaş giriniz", min_value=20, max_value=80, value=45, step=1, key="age")

with row1_col2:
    st.markdown("**Cinsiyet**")
    sex_option = st.selectbox("Cinsiyetinizi seçiniz", options=["Erkek", "Kadın"], key="sex")
    sex_value = 1 if sex_option == "Erkek" else 0

# İkinci satır - Göğüs Ağrısı Tipi ve İstirahat Kan Basıncı
row2_col1, row2_col2 = form_container.columns(2)
with row2_col1:
    st.markdown("**Göğüs Ağrısı Tipi**")
    chest_pain_options = {"Tipik Angina (0)": 0, "Atipik Angina (1)": 1, "Non-Anjinal Ağrı (2)": 2, "Asemptomatik (3)": 3}
    chest_pain_option = st.selectbox("Göğüs ağrısı tipinizi seçiniz", options=list(chest_pain_options.keys()), key="chest_pain")
    chest_pain_value = chest_pain_options[chest_pain_option]

with row2_col2:
    st.markdown("**İstirahat Kan Basıncı (mm Hg)**")
    resting_bp = st.number_input("İstirahat kan basıncınızı giriniz", min_value=80, max_value=200, value=130, step=1, key="resting_bp")

# Üçüncü satır - Kolesterol ve Açlık Kan Şekeri
row3_col1, row3_col2 = form_container.columns(2)
with row3_col1:
    st.markdown("**Kolesterol (mg/dl)**")
    cholesterol = st.number_input("Kolesterol seviyenizi giriniz", min_value=100, max_value=600, value=250, step=1, key="cholesterol")

with row3_col2:
    st.markdown("**Açlık Kan Şekeri > 120 mg/dl**")
    fasting_bs_option = st.selectbox("Açlık kan şekeriniz 120 mg/dl'den yüksek mi?", options=["Hayır (0)", "Evet (1)"], key="fasting_bs")
    fasting_bs_value = 1 if "Evet" in fasting_bs_option else 0

# Dördüncü satır - İstirahat EKG ve Maksimum Kalp Hızı
row4_col1, row4_col2 = form_container.columns(2)
with row4_col1:
    st.markdown("**İstirahat EKG**")
    resting_ecg_options = {"Normal (0)": 0, "ST (1)": 1, "LVH (2)": 2}
    resting_ecg_option = st.selectbox("İstirahat EKG sonucunuzu seçiniz", options=list(resting_ecg_options.keys()), key="resting_ecg")
    resting_ecg_value = resting_ecg_options[resting_ecg_option]

with row4_col2:
    st.markdown("**Maksimum Kalp Hızı**")
    max_hr = st.number_input("Maksimum kalp hızınızı giriniz", min_value=60, max_value=220, value=150, step=1, key="max_hr")

# Beşinci satır - Egzersiz Angina ve ST Depresyonu
row5_col1, row5_col2 = form_container.columns(2)
with row5_col1:
    st.markdown("**Egzersiz Kaynaklı Angina**")
    exercise_angina_option = st.selectbox("Egzersiz sırasında angina yaşıyor musunuz?", options=["Hayır (0)", "Evet (1)"], key="exercise_angina")
    exercise_angina_value = 1 if "Evet" in exercise_angina_option else 0

with row5_col2:
    st.markdown("**ST Depresyonu**")
    st_depression = st.number_input("ST depresyon değerini giriniz", min_value=0.0, max_value=6.0, value=1.0, step=0.1, key="st_depression")

# Altıncı satır - ST Eğimi
row6_col1, _ = form_container.columns(2)
with row6_col1:
    st.markdown("**ST Eğimi**")
    st_slope_options = {"Düşük (0)": 0, "Düz (1)": 1, "Yüksek (2)": 2}
    st_slope_option = st.selectbox("ST eğimini seçiniz", options=list(st_slope_options.keys()), key="st_slope")
    st_slope_value = st_slope_options[st_slope_option]

# Tahmin butonu
if st.button("🔮 Tahmin Et", key="predict_button", type="primary"):
    try:
        # Kullanıcı verilerini bir DataFrame'e dönüştürme (VERİ SETİNİZLE UYUMLU)
        user_df = pd.DataFrame({
            'Yaş': [age],
            'Cinsiyet': [sex_value],
            'GöğüsAğrısıTürü': [chest_pain_value],
            'İstirahatKanBasıncı': [resting_bp],
            'Kolesterol': [cholesterol],
            'AçlıkKanŞekeri': [fasting_bs_value],
            'İstirahatEKG': [resting_ecg_value],
            'MaksimumKalpHızı': [max_hr],
            'EgzersizAnginası': [exercise_angina_value],
            'STDepresyonu': [st_depression],
            'ST_Eğimi': [st_slope_value]
        })
        
        # Kullanıcı verilerini ön işleme (referans sütunlarla)
        user_data_processed = preprocess_data(user_df, is_training=False, reference_columns=X.columns)
        
        # Debug bilgisi
        if st.checkbox("Debug bilgilerini göster"):
            st.write("**Orijinal veri:**")
            st.dataframe(user_df)
            st.write("**İşlenmiş veri:**")
            st.dataframe(user_data_processed)
            st.write("**Beklenen sütunlar:**")
            st.write(X.columns.tolist())
            st.write("**Mevcut sütunlar:**")
            st.write(user_data_processed.columns.tolist())
        
        # Veri kontrolü
        if user_data_processed.shape[1] != X.shape[1]:
            st.error(f"Sütun sayısı uyuşmazlığı! Beklenen: {X.shape[1]}, Mevcut: {user_data_processed.shape[1]}")
            st.stop()
        
        # NaN kontrolü
        if user_data_processed.isnull().values.any():
            st.warning("Eksik değerler tespit edildi ve 0 ile dolduruldu.")
            user_data_processed = user_data_processed.fillna(0)
        
        # Verileri ölçeklendirme
        user_data_scaled = scaler.transform(user_data_processed)
        
        # Ölçeklendirme sonrası NaN kontrolü
        if np.isnan(user_data_scaled).any():
            st.warning("Ölçeklendirme sonrası NaN değerler tespit edildi ve 0 ile dolduruldu.")
            user_data_scaled = np.nan_to_num(user_data_scaled)
        
        # Tahmin yapma
        prediction = model.predict(user_data_scaled)
        prediction_proba = model.predict_proba(user_data_scaled)
        
        # Sonuçları gösterme
        st.subheader("🎯 Tahmin Sonucu")
        
        # Sonuç kartı
        prob_heart_disease = prediction_proba[0][1]
        prob_no_heart_disease = prediction_proba[0][0]
        
        # Renk kodlamalı sonuç
        if prob_heart_disease >= 0.50:
            st.error(f"🚨 **YÜKSEK RİSK** - Kalp hastalığı riski: {prob_heart_disease:.1%}")
            st.warning("Lütfen bir kardiyolog ile görüşmeyi düşünün.")
        else:
            st.success(f"✅ **DÜŞÜK RİSK** - Kalp hastalığı riski: {prob_heart_disease:.1%}")
            st.info("Risk düşük görünse de düzenli sağlık kontrollerinizi ihmal etmeyin.")
        
        # Detaylı olasılık gösterimi
        st.subheader("📊 Detaylı Risk Analizi")
        
        # Progress bar ile görsel gösterim
        st.write("**Kalp Hastalığı Riski:**")
        st.progress(float(prob_heart_disease))
        st.write(f"Risk Oranı: {prob_heart_disease:.2%}")
        
        st.write("**Sağlıklı Olma Olasılığı:**")
        st.progress(float(prob_no_heart_disease))
        st.write(f"Sağlıklı Olma Oranı: {prob_no_heart_disease:.2%}")
        
        # Olasılık grafiği
        fig, ax = plt.subplots(figsize=(10, 6))
        
        categories = ['Sağlıklı', 'Kalp Hastalığı']
        probabilities = [prob_no_heart_disease, prob_heart_disease]
        colors = ['lightgreen', 'lightcoral']
        
        bars = ax.bar(categories, probabilities, color=colors, alpha=0.7, edgecolor='black')
        
        # Değerleri çubukların üzerine yazma
        for bar, prob in zip(bars, probabilities):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{prob:.1%}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_ylabel('Olasılık')
        ax.set_title('Kalp Hastalığı Risk Analizi')
        ax.set_ylim(0, 1)
        ax.grid(axis='y', alpha=0.3)
        
        # Eşik çizgisi
        ax.axhline(y=0.5, color='red', linestyle='--', alpha=0.7, label='Risk Eşiği (%50)')
        ax.legend()
        
        st.pyplot(fig)
        
        # Risk faktörleri analizi (sadece Random Forest için)
        if model_option == "Rastgele Orman":
            st.subheader("🔍 Risk Faktörleri Analizi")
            
            # En önemli özellikleri göster
            feature_importances = model.feature_importances_
            feature_importance_df = pd.DataFrame({
                'Özellik': feature_names,
                'Önem': feature_importances
            }).sort_values('Önem', ascending=False).head(5)
            
            st.write("**En Önemli 5 Risk Faktörü:**")
            for idx, row in feature_importance_df.iterrows():
                st.write(f"• {row['Özellik']}: {row['Önem']:.3f}")
        
        # Uyarı mesajı
        st.warning("""
        ⚠️ **ÖNEMLİ UYARI:** 
        Bu tahmin sadece bilgilendirme amaçlıdır ve kesinlikle tıbbi teşhis yerine geçmez. 
        Sağlık durumunuzla ilgili herhangi bir endişeniz varsa, lütfen derhal bir sağlık uzmanına başvurun.
        """)
        
    except Exception as e:
        st.error(f"❌ Tahmin yapılırken bir hata oluştu: {str(e)}")
        st.write("**Hata detayları:**")
        st.write(f"Hata tipi: {type(e).__name__}")
        st.write("Lütfen girdiğiniz değerlerin doğru formatta olduğundan emin olun ve tekrar deneyin.")

# Açıklama bölümü
st.header("📚 Model Hakkında Bilgi")

st.markdown("""
**Kullanılan Modeller:**

1. **Lojistik Regresyon:** Sınıflandırma problemleri için kullanılan basit ve etkili bir istatistiksel model.

2. **Rastgele Orman:** Birden fazla karar ağacının sonuçlarını birleştiren güçlü bir topluluk öğrenme algoritması.

3. **Destek Vektör Makinesi (SVM):** Veri noktaları arasındaki en iyi ayırma sınırını bulan bir algoritma.

**Değerlendirme Metrikleri:**

- **Doğruluk (Accuracy):** Doğru tahmin edilen örneklerin toplam örnek sayısına oranı.
- **Precision:** Pozitif olarak tahmin edilen örnekler arasında gerçekten pozitif olanların oranı.
- **Recall:** Gerçekte pozitif olan örnekler arasında pozitif olarak tahmin edilenlerin oranı.
- **F1-Score:** Precision ve Recall'un harmonik ortalaması.

**Veri Özellikleri:**

- **Yaş:** Yaş
- **Cinsiyet:** Cinsiyet (1: Erkek, 0: Kadın)
- **GöğüsAğrısıTürü:** Göğüs ağrısı tipi (0: Tipik Angina, 1: Atipik Angina, 2: Non-Anjinal, 3: Asemptomatik)
- **İstirahatKanBasıncı:** İstirahat kan basıncı (mm Hg)
- **Kolesterol:** Kolesterol seviyesi (mg/dl)
- **AçlıkKanŞekeri:** Açlık kan şekeri (1: >120 mg/dl, 0: ≤120 mg/dl)
- **İstirahatEKG:** İstirahat EKG (0: Normal, 1: ST, 2: LVH)
- **MaksimumKalpHızı:** Maksimum kalp hızı
- **EgzersizAnginası:** Egzersiz kaynaklı angina (1: Var, 0: Yok)
- **STDepresyonu:** ST depresyon değeri
- **ST_Eğimi:** ST eğimi (0: Düşük, 1: Düz, 2: Yüksek)
""")

# Footer
st.markdown("---")
st.markdown("© 2024 Kalp Hastalığı Analiz Platformu | Streamlit ile geliştirilmiştir.")
st.markdown("*Bu uygulama sadece eğitim ve bilgilendirme amaçlıdır.*")
