"""
Model değerlendirme yardımcı fonksiyonları
"""
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def evaluate_model(y_true, y_pred, y_scores, model_name):
    """
    Model performans metriklerini hesaplar ve yazdırır.
    
    Args:
        y_true: Gerçek etiketler
        y_pred: Tahmin edilen etiketler
        y_scores: Anomali skorları
        model_name: Model adı
        
    Returns:
        list: [accuracy, precision, recall, f1, roc_auc] metrikleri
    """
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_true, -y_scores)
    
    print(f"--- {model_name} Performansı ---")
    print(f"Doğruluk: {accuracy:.4f}")
    print(f"Kesinlik (Precision): {precision:.4f}")
    print(f"Duyarlılık (Recall): {recall:.4f}")
    print(f"F1 Skoru: {f1:.4f}")
    print(f"ROC AUC Skoru: {roc_auc:.4f}")
    print()
    
    return [accuracy, precision, recall, f1, roc_auc]


def calculate_confusion_matrix_metrics(y_true, y_pred):
    """
    Confusion matrix metriklerini hesaplar.
    
    Args:
        y_true: Gerçek etiketler
        y_pred: Tahmin edilen etiketler
        
    Returns:
        dict: Confusion matrix metrikleri
    """
    from sklearn.metrics import confusion_matrix
    
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    metrics = {
        'true_negatives': tn,
        'false_positives': fp,
        'false_negatives': fn,
        'true_positives': tp,
        'specificity': tn / (tn + fp) if (tn + fp) > 0 else 0,
        'sensitivity': tp / (tp + fn) if (tp + fn) > 0 else 0
    }
    
    return metrics


def print_model_summary(metrics_list, model_names):
    """
    Modellerin özet performansını yazdırır.
    
    Args:
        metrics_list: Her model için metrik listesi
        model_names: Model isimleri listesi
    """
    print("\n" + "="*60)
    print("MODEL PERFORMANS ÖZETİ")
    print("="*60)
    
    # Metrik isimleri
    metric_names = ['Doğruluk', 'Kesinlik', 'Duyarlılık', 'F1 Skoru', 'ROC AUC']
    
    # Tablo başlığı
    print(f"{'Model':<20}", end="")
    for name in metric_names:
        print(f"{name:<12}", end="")
    print()
    
    print("-" * 60)
    
    # Her model için metrikleri yazdır
    for i, (metrics, name) in enumerate(zip(metrics_list, model_names)):
        print(f"{name:<20}", end="")
        for metric in metrics:
            print(f"{metric:<12.4f}", end="")
        print()
    
    print("="*60)
