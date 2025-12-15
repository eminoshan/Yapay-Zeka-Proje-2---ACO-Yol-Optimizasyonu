# 📊 Görselleştirme Fonksiyonları

"""
ACO Algoritması sonuçlarının görselleştirilmesi.
- Yakınsama grafiği (Convergence plot)
- Rota haritası (Route map)
- KML dosyası oluşturma
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_convergence(best_distances, avg_distances):
    """
    Algoritmanın yakınsama eğrilerini çiz.
    
    Args:
        best_distances (list): Her iterasyondaki en iyi mesafe
        avg_distances (list): Her iterasyondaki ortalama mesafe
    
    Returns:
        matplotlib.figure.Figure: Grafik figürü
    
    Açıklama:
        - En İyi Mesafe: Bulunan en kısa rota
        - Ortalama Mesafe: Tüm karıncaların ortalama mesafesi
        - Aralarındaki alan: Algoritmanın iyileşme potansiyeli
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    iterations = range(len(best_distances))
    
    # Çizgileri çiz
    ax.plot(best_distances, label="En İyi Mesafe", linewidth=2, 
            color='#FF6B6B', marker='o', markersize=3)
    ax.plot(avg_distances, label="Ortalama Mesafe", linewidth=2, 
            color='#4ECDC4', alpha=0.7, marker='s', markersize=2)
    
    # Alan doldur
    ax.fill_between(iterations, best_distances, avg_distances, alpha=0.2)
    
    # Etiketler ve başlık
    ax.set_xlabel("İterasyon", fontsize=11, fontweight='bold')
    ax.set_ylabel("Mesafe (meter)", fontsize=11, fontweight='bold')
    ax.set_title("Algoritma Performansı - Yakınsama Analizi", fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    return fig


def plot_route(names, path_indices, coords):
    """
    Optimum rotayı harita üzerinde göster.
    
    Args:
        names (list): Durak adları
        path_indices (list): Ziyaret sırası (düğüm indeksleri)
        coords (np.array): Koordinatlar (n×2)
    
    Returns:
        matplotlib.figure.Figure: Harita figürü
    
    Görselleştirilecekler:
        - Kırmızı noktalar: Duraklar
        - Mavi çizgiler: Rota
        - Yeşil yıldız: Başlangıç/Bitiş
        - Sarı etiketler: Durak isimleri
        - Numaralar: Ziyaret sırası
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Durakları çiz
    ax.scatter(coords[:, 1], coords[:, 0], c='#FF6B6B', s=300, 
               zorder=5, edgecolors='black', linewidth=2, label='Duraklar')
    
    # Ziyaret sırasını numalandır
    for i, node_idx in enumerate(path_indices):
        order = i + 1
        # Sıra numarası
        ax.annotate(f"{order}", (coords[node_idx, 1], coords[node_idx, 0]), 
                   fontsize=9, fontweight='bold', ha='center', va='center',
                   color='white', bbox=dict(boxstyle='circle', facecolor='#2C3E50', alpha=0.8))
        
        # Durak adı
        ax.annotate(names[node_idx], (coords[node_idx, 1], coords[node_idx, 0]), 
                   xytext=(5, 5), textcoords='offset points',
                   fontsize=8, bbox=dict(boxstyle='round,pad=0.3', 
                                        facecolor='yellow', alpha=0.5))
    
    # Rotayı çiz
    path_coords = coords[path_indices]
    ax.plot(path_coords[:, 1], path_coords[:, 0], 'b--', alpha=0.6, 
            linewidth=2, label='Rota', zorder=3)
    
    # Başlangıç/Bitiş
    ax.plot(coords[path_indices[0], 1], coords[path_indices[0], 0], 
            'g*', markersize=20, label='Başlangıç/Bitiş', zorder=6)
    
    # Format
    ax.set_xlabel("Boylam (Longitude)", fontsize=11, fontweight='bold')
    ax.set_ylabel("Enlem (Latitude)", fontsize=11, fontweight='bold')
    ax.set_title("Kampüs Ring Seferi Rotası", fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal', adjustable='box')
    
    return fig


def generate_kml(names, path_indices, coords):
    """
    Google Earth uyumlu KML dosyası oluştur.
    
    Args:
        names (list): Durak adları
        path_indices (list): Ziyaret sırası
        coords (np.array): Koordinatlar
    
    Returns:
        str: KML formatında XML
    
    KML Formatı:
        - Placemark: Her durak için point
        - LineString: Rota çizgisi
        - Google Earth'te görüntülenebilir
    """
    kml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    kml += '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
    kml += '<Document>\n'
    kml += '<name>SDÜ Kampüs Ring Seferi Rotası</name>\n'
    kml += '<description>Karınca Kolonisi Algoritması ile optimize edilmiş rota</description>\n'
    
    # Her durak için placemark
    for idx, node_idx in enumerate(path_indices):
        kml += '<Placemark>\n'
        kml += f'<name>{idx}: {names[node_idx]}</name>\n'
        kml += f'<description>Ziyaret sırası: {idx}</description>\n'
        kml += '<Point>\n'
        kml += f'<coordinates>{coords[node_idx][1]},{coords[node_idx][0]},0</coordinates>\n'
        kml += '</Point>\n'
        kml += '</Placemark>\n'
    
    # Rota çizgisi
    kml += '<Placemark>\n'
    kml += '<name>Optimum Rota</name>\n'
    kml += '<LineString>\n'
    kml += '<coordinates>\n'
    for node_idx in path_indices:
        kml += f'{coords[node_idx][1]},{coords[node_idx][0]},0\n'
    kml += '</coordinates>\n'
    kml += '</LineString>\n'
    kml += '</Placemark>\n'
    
    kml += '</Document>\n'
    kml += '</kml>'
    
    return kml
