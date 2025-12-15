# ⚙️ ACO Algoritması Konfigürasyon Dosyası

"""
Karınca Kolonisi Algoritması (ACO) parametreleri ve sabitler
"""

# ACO Algoritması Varsayılan Parametreleri
ACO_PARAMS = {
    "n_ants": 30,           # Karınca sayısı
    "n_iterations": 100,    # İterasyon sayısı
    "alpha": 1.0,           # Feromon ağırlığı
    "beta": 2.0,            # Mesafe ağırlığı
    "evaporation": 0.3,     # Feromon buharlaşma oranı
    "pheromone_init": 0.5,  # Başlangıç feromon değeri
}

# ACO Parametreleri Aralıkları (UI Slider için)
ACO_RANGES = {
    "n_ants": {"min": 10, "max": 100, "step": 5},
    "n_iterations": {"min": 10, "max": 300, "step": 10},
    "alpha": {"min": 0.5, "max": 5.0, "step": 0.1},
    "beta": {"min": 0.5, "max": 5.0, "step": 0.1},
    "evaporation": {"min": 0.1, "max": 0.9, "step": 0.05},
}

# Proje Bilgileri
PROJECT_INFO = {
    "title": "🚌 Senaryo 7: Kampüs Ring Seferi Optimizasyonu",
    "student_name": "Muhammed Emin Oshan",
    "student_id": "2212729007",
    "university": "Isparta Uygulamalı Bilimler Üniversitesi (SDÜ)",
    "scenario": 7,
    "description": "Karınca Kolonisi Algoritması (ACO) kullanarak Isparta Uygulamalı Bilimler Üniversitesi kampüsünde otobüs rotasını optimize etme"
}

# Haversine Formülü Katsayı (Kampüs içi)
HAVERSINE_MULTIPLIER = 1.35  # Kuş uçuşu × 1.35 = Taşıt mesafesi

# Koordinat Sistemi
COORDINATE_SYSTEM = {
    "format": "[Latitude, Longitude]",
    "example": "[37.8290, 30.5165]",
}

# Google Maps API
GOOGLE_MAPS_CONFIG = {
    "mode": "driving",      # Trafik modu
    "units": "metric",      # Metrik sistem (km)
    "timeout": 10,          # API timeout (saniye)
}
