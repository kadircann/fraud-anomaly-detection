import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve, precision_recall_curve
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend kullan - popup açmaz
import matplotlib.pyplot as plt
import seaborn as sns

# Matplotlib ayarları
plt.rcParams['figure.max_open_warning'] = 0  # Çoklu figure uyarısını kapat
plt.ioff()  # Interactive mode'u kapat - popup açmaz

# Proje modüllerini içe aktar
from services.data_preprocessing_service import DataPreprocessingService
from services.model_trainer_service import ModelTrainerService
from config.config import PLOT_PARAMS
from utils.visualization_utils import plot_all_visualizations


def main():
    """Ana uygulama fonksiyonu"""
    print("=== Anomali Tespit Projesi ===")
    print("Bu proje Kadir Can Felek tarafından tamamlanmıştır.\n")
    
    # Veri ön işleme servisini başlat
    data_service = DataPreprocessingService()
    
    # Veri setini yükle
    print("Veri seti yükleniyor...")
    try:
        df = data_service.load_data()
        print(f"Veri seti boyutu: {df.shape}")
        print(f"Anomali oranı: {df['Class'].mean():.4f}")
    except FileNotFoundError:
        print("Hata: Veri seti bulunamadı. Lütfen 'data/creditcard.csv' dosyasını ekleyin.")
        print("Veri setini indirmek için 'download_data.py' scriptini çalıştırabilirsiniz.")
        return
    
    # Veriyi ön işle
    print("\nVeri ön işleme yapılıyor...")
    X, y = data_service.preprocess_data(df)
    print(f"Özellik sayısı: {X.shape[1]}")
    
    # Veriyi eğitim ve test setlerine ayır
    X_train, X_test, y_train, y_test = data_service.split_data(X, y)
    print(f"Eğitim seti boyutu: {X_train.shape}")
    print(f"Test seti boyutu: {X_test.shape}")
    
    # Özellikleri normalleştir
    print("\nÖzellikler normalleştiriliyor...")
    X_train_scaled, X_test_scaled = data_service.scale_features(X_train, X_test)
    
    # Model eğitimi servisini başlat
    model_trainer = ModelTrainerService()
    
    # Modelleri eğit ve değerlendir
    results = model_trainer.train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Sonuçları al
    iso_results = results['isolation_forest']
    svm_results = results['one_class_svm']
    
    y_pred_iso = iso_results['predictions']
    y_pred_iso_scores = iso_results['scores']
    metrics_iso = iso_results['metrics']
    
    y_pred_svm = svm_results['predictions']
    y_pred_svm_scores = svm_results['scores']
    metrics_svm = svm_results['metrics']
    
    # Görselleştirmeler
    print("\nTüm grafikler tek bir çıktıda oluşturuluyor...")
    
    # Tüm görselleştirmeleri tek bir figure'da göster
    plot_all_visualizations(y_test, y_pred_iso, y_pred_svm, y_pred_iso_scores, y_pred_svm_scores, 
                           metrics_iso, metrics_svm, X_test_scaled)
    
    # En iyi modeli göster
    best_model_name, best_model_results = model_trainer.get_best_model()
    print(f"\nEn iyi performans gösteren model: {best_model_name.replace('_', ' ').title()}")
    print(f"F1 Skoru: {best_model_results['metrics'][3]:.4f}")
    
    # Performans özetini göster
    performance_df = model_trainer.get_model_performance_summary()
    print("\nPerformans Özeti:")
    print(performance_df.to_string(index=False))
    
    print("\n=== Analiz Tamamlandı ===")
    print("Tüm grafikler gösterildi. Program sonlandırılıyor...")


if __name__ == "__main__":
    main()
