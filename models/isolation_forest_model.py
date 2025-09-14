"""
Isolation Forest Model sınıfı
"""
from sklearn.ensemble import IsolationForest
import numpy as np


class IsolationForestModel:
    """Isolation Forest anomali tespit modeli"""
    
    def __init__(self, **params):
        """
        Isolation Forest modelini başlatır
        
        Args:
            **params: Model parametreleri
        """
        self.model = IsolationForest(**params)
        self.is_trained = False
    
    def fit(self, X):
        """
        Modeli eğitir
        
        Args:
            X: Eğitim verisi
        """
        self.model.fit(X)
        self.is_trained = True
    
    def predict(self, X):
        """
        Anomali tahminleri yapar
        
        Args:
            X: Test verisi
            
        Returns:
            numpy.ndarray: Tahmin edilen etiketler (1: anomali, 0: normal)
        """
        if not self.is_trained:
            raise ValueError("Model henüz eğitilmemiş. Önce fit() metodunu çağırın.")
        
        predictions = self.model.predict(X)
        # Isolation Forest -1 (anomali) ve 1 (normal) döner, biz 1 (anomali) ve 0 (normal) istiyoruz
        return np.where(predictions == -1, 1, 0)
    
    def decision_function(self, X):
        """
        Anomali skorlarını döner
        
        Args:
            X: Test verisi
            
        Returns:
            numpy.ndarray: Anomali skorları
        """
        if not self.is_trained:
            raise ValueError("Model henüz eğitilmemiş. Önce fit() metodunu çağırın.")
        
        return self.model.decision_function(X)
    
    def get_params(self):
        """Model parametrelerini döner"""
        return self.model.get_params()
