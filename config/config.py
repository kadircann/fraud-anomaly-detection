"""
Konfigürasyon dosyası
"""
import os

# Veri seti yolu
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'creditcard.csv')

# Model parametreleri
ISOLATION_FOREST_PARAMS = {
    'random_state': 42,
    'contamination': 0.1
}

ONE_CLASS_SVM_PARAMS = {
    'nu': 0.1,
    'kernel': 'rbf'
}

# Eğitim parametreleri
TRAIN_TEST_SPLIT = {
    'test_size': 0.3,
    'random_state': 42,
    'stratify': True
}

# Görselleştirme parametreleri
PLOT_PARAMS = {
    'figsize': (10, 6),
    'dpi': 100
}
