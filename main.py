"""
 SDÜ Kampüs Ring Seferi Optimizasyonu - Streamlit Uygulaması

Karınca Kolonisi Algoritması (ACO) ile Isparta Uygulamalı Bilimler Üniversitesi
kampüsü içindeki 10 durakta ring seferi yapan otobüsün rotasını optimize eder.

Öğrenci: Muhammed Emin Oshan (2212729007)
Senaryo: 7
Tarih: Aralık 2025
"""

import streamlit as st
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Modülleri import et
from config import PROJECT_INFO, ACO_RANGES
from data.coordinates import CAMPUS_STOPS
from core.matrix_utils import get_distance_matrix
from core.ant_algorithm import AntColonyOptimizer
from visual.plotting import plot_convergence, plot_route, generate_kml

# ============================================
# SAYFA AYARLARI
# ============================================
st.set_page_config(
    page_title="SDÜ Ring Optimizasyonu",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# SOL PANEL - BİLGİLER
# ============================================
st.sidebar.title(" Proje Bilgileri")
st.sidebar.info(
    f"**Adı Soyadı:** {PROJECT_INFO['student_name']}\n\n"
    f"**Okul No:** {PROJECT_INFO['student_id']}\n\n"
    f"**Senaryo:** {PROJECT_INFO['scenario']}\n\n"
    f"**Üniversite:** {PROJECT_INFO['university']}"
)

st.sidebar.markdown("---")
st.sidebar.markdown("###  API Ayarları")

# Secrets'ten API Key'i oku (yoksa input'tan)
try:
    default_api_key = st.secrets["google_maps_api_key"]
except:
    default_api_key = ""

api_key = st.sidebar.text_input(
    "Google Maps API Key",
    type="password",
    value=default_api_key,
    help="Distance Matrix API etkinleştirilmiş olmalıdır"
)
st.sidebar.markdown("""
**API Key Nasıl Alınır?**
1. [Google Cloud Console](https://console.cloud.google.com/) sayfasına gidin
2. **Distance Matrix API** etkinleştirin
3. API Key oluşturun ve buraya yapıştırın
""")
st.sidebar.markdown("---")

# ============================================
# ANA SAYFA - BAŞLIK VE AÇIKLAMA
# ============================================
st.title(PROJECT_INFO['title'])
st.markdown(PROJECT_INFO['description'])
st.markdown("---")

# ============================================
# DURAK VERİLERİ
# ============================================
duraklar = CAMPUS_STOPS

# DataFrame oluştur
df_duraklar = pd.DataFrame.from_dict(duraklar, orient='index', columns=['lat', 'lon'])
df_duraklar['isim'] = list(duraklar.keys())

st.sidebar.success(f"Toplam Durak Sayısı: {len(duraklar)}")

# ============================================
# KONTROLLER - PARAMETRELER
# ============================================
st.markdown("### ⚙️ ACO Algoritması Parametreleri")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Algoritma Parametreleri**")
    n_ants = st.slider(
        "🐜 Karınca Sayısı",
        min_value=10,
        max_value=100,
        value=30,
        step=5,
        help="Daha çok karınca = daha iyi sonuç (yavaş)"
    )
    n_iter = st.slider(
        "🔄 İterasyon Sayısı",
        min_value=10,
        max_value=300,
        value=100,
        step=10,
        help="Daha çok iterasyon = daha optimize"
    )
    alpha = st.slider(
        "📍 Alpha (Feromon Ağırlığı)",
        min_value=0.5,
        max_value=5.0,
        value=1.0,
        step=0.1,
        help="Fermona ne kadar önem ver?"
    )

with col2:
    st.markdown("**Optimizasyon Ayarları**")
    beta = st.slider(
        "📏 Beta (Mesafe Ağırlığı)",
        min_value=0.5,
        max_value=5.0,
        value=2.0,
        step=0.1,
        help="Mesafeye ne kadar önem ver?"
    )
    evap = st.slider(
        "💨 Feromon Buharlaşma",
        min_value=0.1,
        max_value=0.9,
        value=0.3,
        step=0.05,
        help="Eski feromon ne kadar yok olsun?"
    )
    start_stop = st.selectbox(
        "📍 Başlangıç Durakı (Ring Merkezi)",
        options=list(duraklar.keys()),
        index=0
    )

with col3:
    st.markdown("**Harita**")
    st.map(df_duraklar, size=100, color='#FF0000')

st.markdown("---")

# ============================================
# BUTONLAR
# ============================================
col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])

with col_btn1:
    calculate_btn = st.button(" Rotayı Hesapla", use_container_width=True)

with col_btn2:
    clear_btn = st.button(" Temizle", use_container_width=True)

with col_btn3:
    download_btn = st.button(" Sonuçları İndir", use_container_width=True)

# Başlangıç düğümünü seç
start_node = list(duraklar.keys()).index(start_stop)

# ============================================
# HESAPLAMA
# ============================================
if calculate_btn:
    # Mesafeleri hesapla
    with st.spinner("📊 Mesafe Matrisi Hesaplanıyor..."):
        dist_matrix, names, coords = get_distance_matrix(duraklar, api_key)
    
    # Durakları kontrol et
    if len(duraklar) != 10:
        st.warning(f" Uyarı: {len(duraklar)} durak var, 10 olması gerekiyor!")
    
    # ACO Optimizer'ı oluştur
    optimizer = AntColonyOptimizer(
        distance_matrix=dist_matrix,
        n_ants=n_ants,
        n_iterations=n_iter,
        alpha=alpha,
        beta=beta,
        evaporation=evap
    )
    
    # Progress bar için callback
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def progress_callback(current, total, best_dist):
        progress_bar.progress(current / total)
        status_text.text(f"İterasyon {current}/{total} - En İyi: {best_dist/1000:.2f} km")
    
    # Algoritma çalış
    with st.spinner(" Karınca Kolonisi Algoritması Çalışıyor..."):
        path_indices, min_dist, best_distances, avg_distances = optimizer.solve(
            start_node=start_node,
            progress_callback=progress_callback
        )
    
    #  BAŞARILI SONUÇ
    st.success(f" Optimum Rota Bulundu!")
    
    #  Ana Metrikler
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    
    with col_metric1:
        st.metric(" Toplam Mesafe", f"{min_dist/1000:.2f} km", f"{min_dist:.0f} m")
    
    with col_metric2:
        num_stops = len([x for x in path_indices if x != path_indices[0]])
        st.metric(" Durak Sayısı", num_stops, f"{len(duraklar)} hepsini ziyaret")
    
    with col_metric3:
        avg_stop_dist = (min_dist / num_stops) if num_stops > 0 else 0
        st.metric(" Ort. Durak Arası", f"{avg_stop_dist/1000:.2f} km", f"{avg_stop_dist:.0f} m")
    
    with col_metric4:
        st.metric(" Çalışan Algoritma", "ACO", f"{n_ants} karınca")
    
    st.markdown("---")
    
    #  Grafikler
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        st.write("### Yakınsama Analizi")
        fig1 = plot_convergence(best_distances, avg_distances)
        st.pyplot(fig1, use_container_width=True)
    
    with col_graph2:
        st.write("###  Optimum Rota Haritası")
        fig2 = plot_route(names, path_indices, coords)
        st.pyplot(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # 📋 Detaylı Rota Tablosu
    st.write("###  Detaylı Rota Tablosu")
    
    rota_data = []
    for idx, node_idx in enumerate(path_indices):
        durak_adi = names[node_idx]
        lat, lon = coords[node_idx]
        
        if idx < len(path_indices) - 1:
            next_idx = path_indices[idx + 1]
            mesafe = dist_matrix[node_idx][next_idx]
        else:
            mesafe = 0
        
        rota_data.append({
            "Sıra": idx,
            "Durak": durak_adi,
            "Enlem": f"{lat:.6f}",
            "Boylam": f"{lon:.6f}",
            "Sonraki Duraktan Mesafe": f"{mesafe/1000:.2f} km" if mesafe > 0 else "-"
        })
    
    df_rota = pd.DataFrame(rota_data)
    st.dataframe(df_rota, use_container_width=True, hide_index=True)
    
    # Rota Özeti
    st.write("###  Rota Özeti")
    rota_str = " → ".join([f"[{idx+1}] {names[i].split('. ')[1]}" for idx, i in enumerate(path_indices)])
    
    st.info(f"**Takip Edilecek Rota (Sırasıyla):**\n\n{rota_str}")
    
    st.markdown("---")
    
    #  İndir Seçenekleri
    st.write("###  Sonuçları İndir")
    
    col_down1, col_down2 = st.columns(2)
    
    with col_down1:
        # CSV İndir
        csv_data = df_rota.to_csv(index=False, encoding='utf-8')
        st.download_button(
            label=" Rotayı CSV Olarak İndir",
            data=csv_data,
            file_name="kampus_ring_seferi_rota.csv",
            mime="text/csv"
        )
    
    with col_down2:
        # KML İndir
        kml_data = generate_kml(names, path_indices, coords)
        st.download_button(
            label=" Rotayı KML Olarak İndir (Google Earth)",
            data=kml_data,
            file_name="kampus_ring_seferi_rota.kml",
            mime="application/vnd.google-earth.kml+xml"
        )

elif clear_btn:
    st.info(" Sonuçlar temizlendi. Tekrar hesaplamak için 'Rotayı Hesapla' butonuna basın.")

