"""
Veri ön işleme servisi
"""
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from config.config import DATA_PATH, TRAIN_TEST_SPLIT


class DataPreprocessingService:
    """Veri ön işleme işlemlerini yöneten servis"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def load_data(self, data_path=None):
        """
        Veri setini yükler
        
        Args:
            data_path (str, optional): Veri dosyası yolu. Varsayılan olarak config'den alınır.
            
        Returns:
            pandas.DataFrame: Yüklenen veri seti
        """
        if data_path is None:
            data_path = DATA_PATH
        
        try:
            df = pd.read_csv(data_path)
            print("Veri seti başarıyla yüklendi.")
            return df
        except FileNotFoundError:
            print(f"Hata: '{data_path}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
            raise
    
    def preprocess_data(self, df):
        """
        Veriyi ön işler
        
        Args:
            df (pandas.DataFrame): Ham veri seti
            
        Returns:
            tuple: (X, y) - Özellikler ve hedef değişken
        """
        # 'Class' etiketini ayırma
        X = df.drop('Class', axis=1)
        y = df['Class']
        
        # 'Time' sütununu atma (anomali tespiti için gerekli değil)
        if 'Time' in X.columns:
            X = X.drop('Time', axis=1)
        
        return X, y
    
    def scale_features(self, X_train, X_test=None):
        """
        Özellikleri normalleştirir
        
        Args:
            X_train (pandas.DataFrame): Eğitim verisi
            X_test (pandas.DataFrame, optional): Test verisi
            
        Returns:
            tuple: (X_train_scaled, X_test_scaled) veya (X_train_scaled, None)
        """
        # Eğitim verisini fit et ve dönüştür
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns)
        self.is_fitted = True
        
        # Test verisi varsa dönüştür
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled, None
    
    def split_data(self, X, y, **split_params):
        """
        Veriyi eğitim ve test setlerine ayırır
        
        Args:
            X (pandas.DataFrame): Özellikler
            y (pandas.Series): Hedef değişken
            **split_params: train_test_split parametreleri
            
        Returns:
            tuple: (X_train, X_test, y_train, y_test)
        """
        # Varsayılan parametreleri kullan
        params = TRAIN_TEST_SPLIT.copy()
        params.update(split_params)
        
        # stratify parametresini kontrol et
        if params.get('stratify') is True:
            params['stratify'] = y
        
        return train_test_split(X, y, **params)
    
    def get_scaler(self):
        """Fitted scaler'ı döner"""
        if not self.is_fitted:
            raise ValueError("Scaler henüz fit edilmemiş.")
        return self.scaler
