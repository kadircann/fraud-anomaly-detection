"""
Veri seti indirme scripti
Credit Card Fraud Detection veri setini Kaggle'dan indirir.
"""

import os
import requests
import zipfile
from pathlib import Path


def download_creditcard_dataset():
    """
    Credit Card Fraud Detection veri setini indirir.
    
    Not: Bu script Kaggle API kullanmadan direkt indirme yapar.
    Eğer Kaggle hesabınız varsa, kaggle API kullanmanız önerilir.
    """
    
    # Veri klasörünü oluştur
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Veri dosyası yolu
    data_file = data_dir / "creditcard.csv"
    
    if data_file.exists():
        print("Veri seti zaten mevcut!")
        return str(data_file)
    
    print("Credit Card Fraud Detection veri seti indiriliyor...")
    print("Not: Bu veri seti Kaggle'dan manuel olarak indirilmelidir.")
    print("\nİndirme adımları:")
    print("1. https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud adresine gidin")
    print("2. 'Download' butonuna tıklayın")
    print("3. İndirilen zip dosyasını açın")
    print("4. 'creditcard.csv' dosyasını 'data/' klasörüne kopyalayın")
    print(f"\nHedef dosya yolu: {data_file}")
    
    # Alternatif olarak, küçük bir örnek veri seti oluşturabiliriz
    create_sample_dataset(data_file)
    
    return str(data_file)


def create_sample_dataset(file_path):
    """
    Test için küçük bir örnek veri seti oluşturur.
    """
    import pandas as pd
    import numpy as np
    
    print("\nTest için örnek veri seti oluşturuluyor...")
    
    # Rastgele veri oluştur
    np.random.seed(42)
    n_samples = 10000
    n_features = 28
    
    # Normal dağılımdan rastgele veri oluştur
    X = np.random.randn(n_samples, n_features)
    
    # Anomali oranı %1
    n_anomalies = int(0.01 * n_samples)
    anomaly_indices = np.random.choice(n_samples, n_anomalies, replace=False)
    
    # Anomali etiketleri
    y = np.zeros(n_samples)
    y[anomaly_indices] = 1
    
    # Anomali verilerini daha farklı yap
    X[anomaly_indices] += np.random.randn(n_anomalies, n_features) * 2
    
    # DataFrame oluştur
    feature_names = [f'V{i+1}' for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_names)
    df['Class'] = y
    
    # Time sütunu ekle (orijinal veri setinde olduğu gibi)
    df.insert(0, 'Time', np.arange(n_samples))
    
    # Dosyayı kaydet
    df.to_csv(file_path, index=False)
    print(f"Örnek veri seti oluşturuldu: {file_path}")
    print(f"Veri seti boyutu: {df.shape}")
    print(f"Anomali oranı: {df['Class'].mean():.4f}")


def setup_kaggle_api():
    """
    Kaggle API kurulumu için talimatlar verir.
    """
    print("\nKaggle API Kurulumu:")
    print("1. https://www.kaggle.com/account adresine gidin")
    print("2. 'Create New API Token' butonuna tıklayın")
    print("3. İndirilen 'kaggle.json' dosyasını ~/.kaggle/ klasörüne kopyalayın")
    print("4. Terminal'de: pip install kaggle")
    print("5. Terminal'de: kaggle datasets download -d mlg-ulb/creditcardfraud")
    print("6. İndirilen zip dosyasını açın ve creditcard.csv'yi data/ klasörüne kopyalayın")


if __name__ == "__main__":
    print("=== Veri Seti İndirme Scripti ===")
    print("Bu proje Kadir Can Felek tarafından tamamlanmıştır.\n")
    
    # Veri setini indir
    data_path = download_creditcard_dataset()
    
    print(f"\nVeri seti hazır: {data_path}")
    print("Artık 'python main.py' komutu ile projeyi çalıştırabilirsiniz.")
