# 📐 Haversine Formülü - Mesafe Hesaplama

"""
Haversine formülü ile iki koordinat arasındaki kuş uçuşu mesafesini hesapla.
Kullanım: Google Maps API olmadığında fallback olarak kullanılır.
"""

import numpy as np
from config import HAVERSINE_MULTIPLIER

def haversine_distance(coord1, coord2):
    """
    Haversine formülü ile iki koordinat arasındaki mesafeyi hesapla.
    
    Formül: d = 2R * arcsin(sqrt(sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)))
    
    Args:
        coord1 (list): [Enlem, Boylam] - İlk koordinat
        coord2 (list): [Enlem, Boylam] - İkinci koordinat
    
    Returns:
        float: Mesafe (metre cinsinden, kampüs içi taşıt mesafesi)
    
    Örnek:
        >>> coord1 = [37.8290, 30.5165]  # Rektörlük
        >>> coord2 = [37.8350, 30.5290]  # Mühendislik
        >>> distance = haversine_distance(coord1, coord2)
        >>> print(f"{distance:.2f} metre")
        894.23 metre
    """
    
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Dünya'nın yarıçapı (metre)
    R = 6371000
    
    # Açıları radyana çevir
    lat1_rad = np.radians(lat1)
    lat2_rad = np.radians(lat2)
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    
    # Haversine formülü
    a = np.sin(dlat/2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Mesafe (kuş uçuşu)
    straight_distance = R * c
    
    # Kampüs içi taşıt mesafesi (kuş uçuşu × 1.35)
    return straight_distance * HAVERSINE_MULTIPLIER


def calculate_distance_matrix(locations):
    """
    Tüm duraklar arasındaki mesafe matrisini hesapla (Haversine).
    
    Args:
        locations (dict): {Durak Adı: [Lat, Lon], ...}
    
    Returns:
        tuple: (distance_matrix, stop_names, coordinates_array)
            - distance_matrix: n×n mesafe matrisi (numpy array)
            - stop_names: Durak adları (list)
            - coordinates: Tüm koordinatlar (numpy array)
    
    Örnek:
        >>> locations = {
        ...     "Rektörlük": [37.8290, 30.5165],
        ...     "Kütüphane": [37.8315, 30.5320]
        ... }
        >>> matrix, names, coords = calculate_distance_matrix(locations)
        >>> print(matrix.shape)  # (2, 2)
        >>> print(matrix[0, 1])  # Rektörlük -> Kütüphane
    """
    
    names = list(locations.keys())
    coords = np.array(list(locations.values()))
    n = len(names)
    
    # Mesafe matrisini başlat (simetrik)
    matrix = np.zeros((n, n))
    
    # Matrisi doldur
    for i in range(n):
        for j in range(i + 1, n):
            dist = haversine_distance(coords[i], coords[j])
            matrix[i, j] = dist
            matrix[j, i] = dist  # Simetrik
    
    return matrix, names, coords
