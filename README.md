# Kalp Hastalığı Analiz Platformu

Bu platform, kalp hastalığı veri setini analiz etmenize, görselleştirmenize ve tahmin modelleri oluşturmanıza olanak tanıyan çok sayfalı bir Streamlit web uygulamasıdır.

## Özellikler

### Ana Sayfa (Home.py)
- Platform tanıtımı ve genel bakış
- Veri seti önizlemesi ve temel istatistikler
- Kalp hastalığı dağılımı grafiği
- Diğer sayfalara hızlı erişim kartları
- Veri seti özellikleri hakkında detaylı bilgiler

### Veri Görselleştirme (1_Veri_Görselleştirme.py)
- **Demografik Analizler:**
  - Yaş dağılımı ve kalp hastalığı ilişkisi
  - Cinsiyet dağılımı ve kalp hastalığı ilişkisi
- **Sağlık Parametreleri Analizleri:**
  - Göğüs ağrısı tipi ve kalp hastalığı ilişkisi
  - Kolesterol seviyesi analizi
  - Kan basıncı analizi
  - Maksimum kalp hızı analizi
  - Egzersiz angina analizi
  - ST eğimi analizi
  - Oldpeak analizi
- **İlişki Analizleri:**
  - Özellikler arası korelasyon matrisi
  - Özellik önemi analizi
  - Çok değişkenli analizler
  - Yaş ve maksimum kalp hızı ilişkisi

### Tahmin Modeli (2_Tahmin_Modeli.py)
- **Makine Öğrenmesi Modelleri:**
  - Lojistik Regresyon
  - Rastgele Orman
  - Destek Vektör Makinesi (SVM)
  - K-En Yakın Komşu (KNN)
  - Karar Ağacı
- **Model Performans Metrikleri:**
  - Doğruluk (Accuracy)
  - Precision, Recall ve F1-Score
  - Karmaşıklık Matrisi (Confusion Matrix)
  - Özellik Önemleri (Rastgele Orman için)
- **Kişisel Risk Tahmini:**
  - Kullanıcı verilerine dayalı kalp hastalığı risk tahmini
  - Risk olasılığı görselleştirmesi

### Tanıtım (3_Tanıtım.py)
- **Kalp Hastalıkları Bilgileri:**
  - Kalp hastalığı türleri
  - Belirtiler ve tanı yöntemleri
- **Risk Faktörleri:**
  - Değiştirilebilir ve değiştirilemez risk faktörleri
  - Risk faktörlerinin kalp hastalığı üzerindeki etkisi
- **Korunma Yöntemleri:**
  - Beslenme önerileri
  - Fiziksel aktivite önerileri
  - Diğer yaşam tarzı değişiklikleri
  - Korunma yöntemlerinin etkinliği
- **Veri Seti Bilgileri:**
  - Veri seti özellikleri açıklaması
  - Veri seti istatistikleri
  - Veri seti görselleştirmeleri

## Kurulum

1. Gerekli kütüphaneleri yükleyin:

```bash
pip install -r requirements.txt
```

2. Uygulamayı çalıştırın:

```bash
streamlit run Home.py
```

3. Tarayıcınızda otomatik olarak açılacak olan `http://localhost:8501` adresine gidin.

## Veri Seti

Uygulama, `heart.csv` veri setini kullanmaktadır. Bu veri seti, çeşitli sağlık parametrelerine göre kalp hastalığı riskini değerlendirmektedir.

Veri seti özellikleri:

- **Age**: Yaş
- **Sex**: Cinsiyet (M: Erkek, F: Kadın)
- **ChestPainType**: Göğüs ağrısı tipi (TA: Tipik Angina, ATA: Atipik Angina, NAP: Non-Anginal Ağrı, ASY: Asemptomatik)
- **RestingBP**: İstirahat kan basıncı (mm Hg)
- **Cholesterol**: Kolesterol (mg/dl)
- **FastingBS**: Açlık kan şekeri (1: >120 mg/dl, 0: <=120 mg/dl)
- **RestingECG**: İstirahat elektrokardiyogram sonuçları (Normal, ST: ST-T dalga anormalliği, LVH: Sol ventrikül hipertrofisi)
- **MaxHR**: Maksimum kalp hızı
- **ExerciseAngina**: Egzersiz kaynaklı angina (Y: Evet, N: Hayır)
- **Oldpeak**: Oldpeak = ST (Egzersiz ile indüklenen ST depresyonu)
- **ST_Slope**: ST eğiminin eğimi (Up: Yukarı, Flat: Düz, Down: Aşağı)
- **HeartDisease**: Kalp hastalığı (1: Kalp hastalığı var, 0: Kalp hastalığı yok)

## Proje Yapısı

```
├── Home.py                    # Ana sayfa
├── pages/
│   ├── 1_Veri_Görselleştirme.py  # Veri görselleştirme sayfası
│   ├── 2_Tahmin_Modeli.py        # Tahmin modeli sayfası
│   └── 3_Tanıtım.py              # Tanıtım sayfası
├── heart.csv                  # Veri seti
├── requirements.txt           # Gerekli kütüphaneler
└── README.md                  # Bu dosya
```

## Gereksinimler

- Python 3.7+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- NumPy
- Scikit-learn

## Geliştirici

Bu uygulama, Streamlit kullanılarak geliştirilmiştir.

## Lisans

Kulanılan veri seti

```bash
https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction
```

Bu proje açık kaynaklıdır ve eğitim amaçlı kullanılabilir.

