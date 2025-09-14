"""
One-Class SVM Model sınıfı
"""
from sklearn.svm import OneClassSVM
import numpy as np


class OneClassSVMModel:
    """One-Class SVM anomali tespit modeli"""
    
    def __init__(self, **params):
        """
        One-Class SVM modelini başlatır
        
        Args:
            **params: Model parametreleri
        """
        self.model = OneClassSVM(**params)
        self.is_trained = False
    
    def fit(self, X):
        """
        Modeli eğitir (sadece normal verilerle)
        
        Args:
            X: Eğitim verisi (sadece normal veriler)
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
        # One-Class SVM -1 (anomali) ve 1 (normal) döner, biz 1 (anomali) ve 0 (normal) istiyoruz
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
