"""
Model eğitimi ve karşılaştırma servisi
"""
import pandas as pd
import numpy as np
from typing import Tuple, List, Dict, Any

from models.isolation_forest_model import IsolationForestModel
from models.one_class_svm_model import OneClassSVMModel
from config.config import ISOLATION_FOREST_PARAMS, ONE_CLASS_SVM_PARAMS
from utils.evaluation_utils import evaluate_model, print_model_summary


class ModelTrainerService:
    """Model eğitimi ve karşılaştırma işlemlerini yöneten servis"""
    
    def __init__(self):
        self.models = {}
        self.results = {}
    
    def train_models(self, X_train, X_test, y_train, y_test) -> Dict[str, Any]:
        """
        Tüm modelleri eğitir ve değerlendirir.
        
        Args:
            X_train: Eğitim özellikleri
            X_test: Test özellikleri
            y_train: Eğitim etiketleri
            y_test: Test etiketleri
            
        Returns:
            dict: Model sonuçları
        """
        print("Modeller eğitiliyor...")
        
        # Isolation Forest modeli
        print("Isolation Forest modeli eğitiliyor...")
        iso_model = IsolationForestModel(**ISOLATION_FOREST_PARAMS)
        iso_model.fit(X_train)
        y_pred_iso = iso_model.predict(X_test)
        y_pred_iso_scores = iso_model.decision_function(X_test)
        
        # One-Class SVM modeli
        print("One-Class SVM modeli eğitiliyor...")
        svm_model = OneClassSVMModel(**ONE_CLASS_SVM_PARAMS)
        # OCSVM normalde sadece normal verilerle eğitilir
        # DataFrame'i numpy array'e çevir
        X_train_array = X_train.values if hasattr(X_train, 'values') else X_train
        X_test_array = X_test.values if hasattr(X_test, 'values') else X_test
        y_train_array = y_train.values if hasattr(y_train, 'values') else y_train
        
        normal_indices = y_train_array == 0
        svm_model.fit(X_train_array[normal_indices])
        y_pred_svm = svm_model.predict(X_test_array)
        y_pred_svm_scores = svm_model.decision_function(X_test_array)
        
        # Modelleri sakla
        self.models = {
            'isolation_forest': iso_model,
            'one_class_svm': svm_model
        }
        
        # Model değerlendirme
        print("\nModellerin performans metrikleri hesaplanıyor...")
        metrics_iso = evaluate_model(y_test, y_pred_iso, y_pred_iso_scores, "Isolation Forest")
        metrics_svm = evaluate_model(y_test, y_pred_svm, y_pred_svm_scores, "One-Class SVM")
        
        # Sonuçları sakla
        self.results = {
            'isolation_forest': {
                'model': iso_model,
                'predictions': y_pred_iso,
                'scores': y_pred_iso_scores,
                'metrics': metrics_iso
            },
            'one_class_svm': {
                'model': svm_model,
                'predictions': y_pred_svm,
                'scores': y_pred_svm_scores,
                'metrics': metrics_svm
            }
        }
        
        # Özet yazdır
        print_model_summary([metrics_iso, metrics_svm], ['Isolation Forest', 'One-Class SVM'])
        
        return self.results
    
    def get_best_model(self) -> Tuple[str, Any]:
        """
        En iyi performans gösteren modeli döner.
        
        Returns:
            tuple: (model_name, model_results)
        """
        if not self.results:
            raise ValueError("Henüz model eğitimi yapılmamış.")
        
        # F1 skoruna göre en iyi modeli bul
        best_model_name = None
        best_f1_score = -1
        
        for model_name, results in self.results.items():
            f1_score = results['metrics'][3]  # F1 skoru 4. indekste
            if f1_score > best_f1_score:
                best_f1_score = f1_score
                best_model_name = model_name
        
        return best_model_name, self.results[best_model_name]
    
    def predict_anomalies(self, X, model_name: str = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Yeni veri için anomali tahmini yapar.
        
        Args:
            X: Tahmin edilecek veri
            model_name: Kullanılacak model adı (None ise en iyi model)
            
        Returns:
            tuple: (predictions, scores)
        """
        if not self.results:
            raise ValueError("Henüz model eğitimi yapılmamış.")
        
        if model_name is None:
            model_name, _ = self.get_best_model()
        
        if model_name not in self.results:
            raise ValueError(f"Model '{model_name}' bulunamadı.")
        
        model = self.results[model_name]['model']
        predictions = model.predict(X)
        scores = model.decision_function(X)
        
        return predictions, scores
    
    def get_model_performance_summary(self) -> pd.DataFrame:
        """
        Tüm modellerin performans özetini DataFrame olarak döner.
        
        Returns:
            pandas.DataFrame: Performans özeti
        """
        if not self.results:
            raise ValueError("Henüz model eğitimi yapılmamış.")
        
        data = []
        for model_name, results in self.results.items():
            metrics = results['metrics']
            data.append({
                'Model': model_name.replace('_', ' ').title(),
                'Accuracy': metrics[0],
                'Precision': metrics[1],
                'Recall': metrics[2],
                'F1_Score': metrics[3],
                'ROC_AUC': metrics[4]
            })
        
        return pd.DataFrame(data)
    
    def save_models(self, filepath_prefix: str = "models"):
        """
        Eğitilmiş modelleri kaydeder.
        
        Args:
            filepath_prefix: Dosya yolu öneki
        """
        if not self.models:
            raise ValueError("Kaydedilecek model bulunamadı.")
        
        import joblib
        
        for model_name, model in self.models.items():
            filename = f"{filepath_prefix}_{model_name}.joblib"
            joblib.dump(model, filename)
            print(f"Model kaydedildi: {filename}")
    
    def load_models(self, filepath_prefix: str = "models"):
        """
        Kaydedilmiş modelleri yükler.
        
        Args:
            filepath_prefix: Dosya yolu öneki
        """
        import joblib
        import os
        
        model_files = {
            'isolation_forest': f"{filepath_prefix}_isolation_forest.joblib",
            'one_class_svm': f"{filepath_prefix}_one_class_svm.joblib"
        }
        
        loaded_models = {}
        for model_name, filepath in model_files.items():
            if os.path.exists(filepath):
                model = joblib.load(filepath)
                loaded_models[model_name] = model
                print(f"Model yüklendi: {filepath}")
            else:
                print(f"Model dosyası bulunamadı: {filepath}")
        
        self.models = loaded_models
        return loaded_models
