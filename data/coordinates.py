# 📍 SDÜ Kampüs Durak Koordinatları

"""
Isparta Uygulamalı Bilimler Üniversitesi kampüsü'ndeki 10 durak.
Koordinatlar: [Enlem, Boylam] formatında
Kaynak: Google Maps - SDÜ Kampüsü
"""

CAMPUS_STOPS = {
    "1. Rektörlük": [37.8290, 30.5165],
    "2. Mühendislik Fakültesi": [37.8350, 30.5290],
    "3. Fen-Edebiyat Fakültesi": [37.8320, 30.5320],
    "4. Tıp Fakültesi": [37.8260, 30.5395],
    "5. Merkez Yemekhane": [37.8300, 30.5330],
    "6. KYK Yurtları": [37.8220, 30.5350],
    "7. Spor Bilimleri Fakültesi": [37.8280, 30.5345],
    "8. Teknokent": [37.8360, 30.5140],
    "9. Mediko-Sosyal": [37.8295, 30.5310],
    "10. Kütüphane": [37.8315, 30.5320],
}

def get_stops():
    """
    Kampüs duraklarını döndür
    
    Returns:
        dict: Durak adı -> Koordinatlar
    """
    return CAMPUS_STOPS

def get_stop_count():
    """
    Toplam durak sayısını döndür
    
    Returns:
        int: 10 (zorunlu ring seferi)
    """
    return len(CAMPUS_STOPS)

def get_stop_names():
    """
    Tüm durak adlarını listele
    
    Returns:
        list: Durak adları
    """
    return list(CAMPUS_STOPS.keys())
