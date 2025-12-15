# 🚌 Senaryo 7: Kampüs Ring Seferi Optimizasyonu

## 📌 Proje Özeti

Isparta Uygulamalı Bilimler Üniversitesi (SDÜ) kampüsü içinde, otobüs seferinin 10 durakta durarak **en kısa sürede tur atması** hedeflenmiştir. Bu amaçla **Karınca Kolonisi Algoritması (ACO)** kullanılarak rota optimize edilmiş ve **Google Maps API** ile gerçek mesafeler hesaplanmıştır.

---

## 🎯 Amaç

- **Karınca Kolonisi Algoritması (ACO)** ile Travelling Salesman Problem (TSP) çözümü
- **Google Maps Distance Matrix API** ile gerçek sürüş mesafeleri
- **Streamlit** ile interaktif kullanıcı arayüzü
- **10 Durak Ring Seferi** optimizasyonu

---

## � Proje Yapısı

```
Proje2_Karinca/
├── main.py                    # ⭐ Streamlit ana uygulaması
├── config.py                  # ACO parametreleri ve konfigürasyon
├── requirements.txt           # Python paket bağımlılıkları
├── README.md                  # Bu dosya
├── .gitignore                 # Git'e yüklenmeyen dosyalar
├── .env.example               # Ortam değişkenleri örneği
│
├── data/
│   └── coordinates.py         # 📍 SDÜ Kampüsü 10 durak koordinatları
│
├── core/
│   ├── ant_algorithm.py       # 🐜 ACO Algoritması (AntColonyOptimizer sınıfı)
│   ├── haversine.py           # 📐 Haversine formülü ile mesafe hesaplama
│   └── matrix_utils.py        # 🔧 Distance Matrix API entegrasyonu
│
├── visual/
│   └── plotting.py            # 📊 Grafik ve KML görselleştirmesi
│
├── .streamlit/
│   └── secrets.example.toml   # Streamlit API Key yapısı
│
└── figure/  (opsiyonel)
    ├── rota.png               # Rota haritası (örnek)
    └── convergence.png        # Yakınsama grafiği (örnek)
```

---

## 🛠️ Gereksinimler

- Python 3.8+
- Streamlit 1.28+
- Google Maps API Key (Distance Matrix API etkinleştirilmiş)

### Paketleri Yükleyin:
```bash
pip install -r requirements.txt
```

---

## 🚀 Uygulamayı Çalıştırma

```bash
# Proje klasörüne git
cd Proje2_Karinca

# Paketleri yükle
pip install -r requirements.txt

# Streamlit uygulamasını başlat
streamlit run main.py
```

**Tarayıcı otomatik olarak `http://localhost:8501` adresine açılacak.**

---

## 🔑 Google Maps API Key Alma

1. [Google Cloud Console](https://console.cloud.google.com/) sayfasına gidin
2. Yeni proje oluşturun
3. **Distance Matrix API** ve **Maps API** etkinleştirin
4. API Key oluşturun
5. Streamlit uygulamasının sol panelinde "🔑 Google Maps API Key" alanına yapıştırın

**Not:** API Key olmadan da çalışır, ancak mesafeler **Haversine formülü** (kuş uçuşu) ile hesaplanır.

---

## 📍 Duraklar

SDÜ Kampüsü'ndeki 10 durak:

1. **Rektörlük** - Kampüsün yönetim merkezi
2. **Mühendislik Fakültesi** - Doğu tarafında
3. **Fen-Edebiyat Fakültesi** - Merkez bölgede
4. **Tıp Fakültesi** - Doğu uçta
5. **Merkez Yemekhane** - Merkez alımı
6. **KYK Yurtları** - Batı tarafında
7. **Spor Bilimleri Fakültesi** - Orta bölgede
8. **Teknokent** - Batı uçta
9. **Mediko-Sosyal** - Sağlık merkezi
10. **Kütüphane** - Merkez bölgede

---

## 🐜 Karınca Kolonisi Algoritması (ACO)

### Algoritma İşleyişi:

1. **İniciyalizasyon:** Feromon matrisi (0.5 başlangıç değeri)
2. **Her İterasyon:**
   - Her karınca rastgele başlayarak tüm durakları ziyaret etmektedir
   - **Rulet Tekerleği (Roulette Wheel)** seçimi ile bir sonraki durak seçilir
   - Seçim olasılığı = (Feromon^α) × (1/Mesafe^β)
3. **Feromon Güncellemesi:** En iyi çözümü bulan karıncalar feromon bırakır
4. **Buharlaşma:** Eski feromonlar azalır (Evaporation)
5. **Sonlandırma:** Belirtilen iterasyon sayısı tamamlandığında en iyi rota döndürülür

### Parametreler:

| Parameter | Açıklama | Aralık | Default |
|-----------|----------|--------|---------|
| **Karınca Sayısı** | Çalışacak karınca sayısı | 10-100 | 30 |
| **İterasyon** | Algoritmanın kaç kez çalışacağı | 10-300 | 100 |
| **Alpha (α)** | Feromon ağırlığı | 0.5-5.0 | 1.0 |
| **Beta (β)** | Mesafe ağırlığı | 0.5-5.0 | 2.0 |
| **Buharlaşma** | Feromon kaybı oranı | 0.1-0.9 | 0.3 |

---

## 📊 Çıktılar

### 1. Metrikler
- **📏 Toplam Mesafe** - Optimum rotanın toplam km'si
- **🚏 Durak Sayısı** - Ziyaret edilen durak sayısı (her zaman 10)
- **📍 Ortalama Durak Arası** - Duraks arasındaki ortalama mesafe
- **🐜 Çalışan Algoritma** - ACO + karınca sayısı

### 2. Yakınsama Grafiği
- **En İyi Mesafe:** Her iterasyondan sonra bulunan en iyi rota
- **Ortalama Mesafe:** O iterasyondaki tüm karıncaların ortalama mesafesi
- Algoritmanın iyileşme eğilimi görülür

### 3. Rota Haritası
- Durakların coğrafik konumları
- Optimum rotanın vizüel gösterimi
- Başlangıç/Bitiş noktası işaretlenmesi
- Durakların ziyaret sırası numarandırılmış

### 4. Detaylı Rota Tablosu
- Ziyaret sırası
- Durak adı
- Enlem/Boylam koordinatları
- Sonraki duraka kadar mesafe

---

## 💾 İndir Seçenekleri

### CSV Formatı
- Rotayı Excel/Google Sheets'te açılabilir formatta indir
- Koordinat ve mesafe bilgileri içerir

### KML Formatı
- Google Earth ile açılabilir format
- Rota haritası üzerinde görüntülenebilir
- GPS cihazlarında kullanılabilir

---

## 🔧 Teknik Detaylar

### Mesafe Hesaplama

**Google Maps API Kullanıldığında:**
- `Distance Matrix API` ile gerçek sürüş mesafeleri
- Trafik durumu dikkate alınmaz (statik mesafeler)
- Metre cinsinden sonuç

**API Olmadığında (Fallback):**
- **Haversine Formülü:** İki koordinat arasındaki kuş uçuşu mesafesi
- Katsayı: 1.35x (kampüs içi taşıt mesafesi ≈ kuş uçuşu × 1.35)

### Koordinat Sistemi
- **Format:** [Enlem, Boylam]
- **Örnek:** [37.8290, 30.5165]
- **Visualizasyon:** Matplotlib (Longitude × Latitude)

---

## 🎓 Öğrenme Çıktıları

1. ✅ **ACO Algoritması Anlaması** - Metaheuristik optimizasyon
2. ✅ **TSP Problemi** - Travelling Salesman Problem çözümü
3. ✅ **API Entegrasyonu** - Google Maps Distance Matrix API
4. ✅ **Streamlit UI** - İnteraktif web arayüzü
5. ✅ **Veri Visualizasyonu** - Grafik ve harita gösterimi
6. ✅ **Python Programlama** - NumPy, Pandas, Matplotlib

---

## 📌 Notlar

- Algoritma her çalıştırıldığında farklı sonuçlar verebilir (stokastik)
- Daha çok iterasyon = daha optimize sonuç (zaman artar)
- API Key'siz kullanıldığında mesafeler yaklaşık değerdir
- Ring seferi: Otobüs aynı noktadan başlar ve aynı noktaya döner

---

## 👨‍💼 Öğrenci Bilgileri

- **Adı Soyadı:** Muhammed Emin Oshan
- **Okul Numarası:** 2212729007
- **Üniversite:** Isparta Uygulamalı Bilimler Üniversitesi (SDÜ)
- **Senaryo:** 7
- **Tarih:** Aralık 2025

---

## 📚 Kaynaklar

- [Karınca Kolonisi Algoritması](https://en.wikipedia.org/wiki/Ant_colony_optimization)
- [Google Maps API Dokümantasyonu](https://developers.google.com/maps/documentation/distance-matrix)
- [Streamlit Dokümantasyonu](https://docs.streamlit.io/)
- [Travelling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem)

---

## 📝 Lisans

Bu proje eğitim amacıyla oluşturulmuştur.
