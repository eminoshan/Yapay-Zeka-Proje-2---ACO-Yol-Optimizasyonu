# 🐜 Karınca Kolonisi Algoritması (ACO)

"""
Travelling Salesman Problem (TSP) çözmek için ACO Algoritması.
Ring seferi: Başlangıç noktasından başlayıp aynı noktaya dönüş.
"""

import numpy as np
import streamlit as st


class AntColonyOptimizer:
    """
    Karınca Kolonisi Algoritması (Ant Colony Optimization)
    
    Algoritma İşleyişi:
        1. İniciyalizasyon: Feromon matrisi başlatılır
        2. Her İterasyon:
            - Her karınca tüm düğümleri ziyaret eder (TSP)
            - Seçim: Feromon^α × (1/Mesafe)^β
            - Rulet tekerleği (Roulette Wheel) seçimi
        3. Feromon Güncelleme: En iyi çözümü bulanlar feromon bırakır
        4. Buharlaşma: Eski feromonlar azalır
        5. Sonlandırma: Belirtilen iterasyon tamamlandığında
    
    Referans:
        Dorigo & Stützle (2004). Ant Colony Optimization
    """
    
    def __init__(self, distance_matrix, n_ants=30, n_iterations=100,
                 alpha=1.0, beta=2.0, evaporation=0.3, pheromone_init=0.5):
        """
        ACO Optimizer'ı başlat.
        
        Args:
            distance_matrix (np.array): n×n mesafe matrisi
            n_ants (int): Karınca sayısı
            n_iterations (int): İterasyon sayısı
            alpha (float): Feromon ağırlığı (0.5-5.0)
            beta (float): Mesafe ağırlığı (0.5-5.0)
            evaporation (float): Feromon buharlaşma (0.1-0.9)
            pheromone_init (float): Başlangıç feromon
        """
        self.distance_matrix = distance_matrix
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation = evaporation
        
        self.n_points = len(distance_matrix)
        self.pheromone = np.ones((self.n_points, self.n_points)) * pheromone_init
        
        self.best_path = None
        self.best_distance = float('inf')
        self.best_distances = []
        self.avg_distances = []
    
    def _calculate_probabilities(self, current_node, unvisited):
        """
        Rulet tekerleği için seçim olasılıklarını hesapla.
        
        Formül: P(i,j) = (τ^α × η^β) / Σ(τ^α × η^β)
        où: τ = feromon, η = 1/mesafe
        
        Args:
            current_node (int): Şu anki düğüm
            unvisited (set): Ziyaret edilmemiş düğümler
        
        Returns:
            tuple: (olasılıklar, seçilebilir_düğümler)
        """
        probabilities = []
        possible_next = list(unvisited)
        
        for next_node in possible_next:
            # Feromon etkisi
            tau = self.pheromone[current_node][next_node] ** self.alpha
            
            # Mesafe etkisi (ters orantılı)
            dist = self.distance_matrix[current_node][next_node]
            if dist > 0:
                eta = (100.0 / dist) ** self.beta
            else:
                eta = 1.0
            
            probabilities.append(tau * eta)
        
        # Normalize et
        probs_array = np.array(probabilities)
        probs_sum = probs_array.sum()
        
        if probs_sum > 0:
            probs_array = probs_array / probs_sum
        else:
            probs_array = np.ones(len(probs_array)) / len(probs_array)
        
        return probs_array, possible_next
    
    def _build_path(self, start_node):
        """
        Tek bir karıncanın rotasını oluştur.
        
        Args:
            start_node (int): Başlangıç düğümü (ring seferi)
        
        Returns:
            tuple: (path, total_distance)
        """
        path = [start_node]
        visited = {start_node}
        current = start_node
        
        # Tüm düğümleri ziyaret et
        while len(visited) < self.n_points:
            unvisited = set(range(self.n_points)) - visited
            
            # Seçim olasılıklarını hesapla
            probs, possible_next = self._calculate_probabilities(current, unvisited)
            
            if len(possible_next) == 0:
                break
            
            # Rulet tekerleği ile seç
            next_node = np.random.choice(possible_next, p=probs)
            path.append(next_node)
            visited.add(next_node)
            current = next_node
        
        # Ring seferi: Başlangıca dönüş
        path.append(start_node)
        
        # Mesafeyi hesapla
        total_dist = sum([
            self.distance_matrix[path[i]][path[i+1]]
            for i in range(len(path)-1)
        ])
        
        return path, total_dist
    
    def solve(self, start_node=0, progress_callback=None):
        """
        ACO ile en kısa rotayı bul.
        
        Args:
            start_node (int): Ring seferinin başlayacağı düğüm
            progress_callback (func): Progress güncelleme fonksiyonu
        
        Returns:
            tuple: (best_path, best_distance, best_distances, avg_distances)
        """
        for iteration in range(self.n_iterations):
            all_paths = []
            all_distances = []
            
            # Tüm karıncalar rota oluştur
            for _ in range(self.n_ants):
                path, distance = self._build_path(start_node)
                all_paths.append(path)
                all_distances.append(distance)
                
                # En iyi yolu güncelle
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_path = path.copy()
            
            # İstatistikler
            self.best_distances.append(min(all_distances))
            self.avg_distances.append(np.mean(all_distances))
            
            # Feromon buharlaşması
            self.pheromone *= (1 - self.evaporation)
            
            # Feromon güncelleme
            for path, distance in zip(all_paths, all_distances):
                pheromone_increase = 1.0 / distance
                for i in range(len(path) - 1):
                    self.pheromone[path[i]][path[i+1]] += pheromone_increase
            
            # Progress
            if progress_callback:
                progress_callback(iteration + 1, self.n_iterations, self.best_distance)
        
        return self.best_path, self.best_distance, self.best_distances, self.avg_distances
