# 🔧 Mesafe Matrisi Utility Fonksiyonları

"""
Google Maps API ve Haversine fallback ile mesafe matrisi oluştur.
"""

import numpy as np
import googlemaps
import streamlit as st
from core.haversine import calculate_distance_matrix as haversine_matrix


def get_distance_matrix(locations, api_key=None):
    """
    Google Maps Distance Matrix API veya Haversine ile mesafe matrisi oluştur.
    
    Args:
        locations (dict): {Durak Adı: [Lat, Lon], ...}
        api_key (str): Google Maps API Key (optional)
    
    Returns:
        tuple: (distance_matrix, stop_names, coordinates_array)
    
    Açıklama:
        1. API Key varsa: Google Maps Distance Matrix API (gerçek sürüş mesafesi)
        2. API Key yoksa: Haversine formülü (kuş uçuşu × 1.35)
    """
    
    names = list(locations.keys())
    coords = np.array(list(locations.values()))
    n = len(names)
    matrix = np.zeros((n, n))
    api_connected = False

    # Google Maps API Denemesi
    if api_key:
        try:
            gmaps = googlemaps.Client(key=api_key)
            
            # API test et
            _ = gmaps.distance_matrix(
                origins=[(coords[0][0], coords[0][1])],
                destinations=[(coords[1][0], coords[1][1])],
                mode='driving',
                units='metric'
            )
            api_connected = True
            st.sidebar.success("✅ Google Maps API Bağlantısı Aktif")
            
            # Mesafe matrisini API ile doldur
            progress = st.progress(0)
            for i in range(n):
                for j in range(n):
                    if i == j:
                        matrix[i][j] = 0
                    elif matrix[j][i] > 0:
                        matrix[i][j] = matrix[j][i]
                    else:
                        try:
                            result = gmaps.distance_matrix(
                                origins=[(coords[i][0], coords[i][1])],
                                destinations=[(coords[j][0], coords[j][1])],
                                mode='driving',
                                units='metric'
                            )
                            if result['status'] == 'OK':
                                dist_meters = result['rows'][0]['elements'][0]['distance']['value']
                                matrix[i][j] = dist_meters
                            else:
                                # Fallback
                                from core.haversine import haversine_distance
                                matrix[i][j] = haversine_distance(coords[i], coords[j])
                        except:
                            from core.haversine import haversine_distance
                            matrix[i][j] = haversine_distance(coords[i], coords[j])
                progress.progress((i + 1) / n)
                
        except Exception as e:
            st.sidebar.warning(f"⚠️ API Hata: {str(e)}")
            st.sidebar.info("📍 Haversine formülü kullanılıyor...")
            api_key = None

    # Haversine Fallback
    if not api_connected:
        matrix, names, coords = haversine_matrix(locations)

    return matrix, names, coords
