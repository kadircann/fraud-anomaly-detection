"""
Görselleştirme yardımcı fonksiyonları
"""
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend kullan - popup açmaz
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import roc_curve, precision_recall_curve
from sklearn.decomposition import PCA
from config.config import PLOT_PARAMS

# Matplotlib ayarları
plt.ioff()  # Interactive mode'u kapat - popup açmaz


def plot_performance_comparison(metrics_iso, metrics_svm, ax=None):
    """
    Modellerin performans metriklerini karşılaştıran bar grafiği oluşturur.
    
    Args:
        metrics_iso: Isolation Forest metrikleri
        metrics_svm: One-Class SVM metrikleri
        ax: Matplotlib axis (subplot için)
    """
    # Karşılaştırma için DataFrame oluştur
    metrics_df = pd.DataFrame({
        'Model': ['Isolation Forest', 'One-Class SVM'],
        'Doğruluk': [metrics_iso[0], metrics_svm[0]],
        'Kesinlik': [metrics_iso[1], metrics_svm[1]],
        'Duyarlılık': [metrics_iso[2], metrics_svm[2]],
        'F1 Skoru': [metrics_iso[3], metrics_svm[3]]
    })
    
    # DataFrame'i melt et
    metrics_df_melted = metrics_df.melt('Model', var_name='Metrik', value_name='Değer')
    
    # Grafik oluştur
    if ax is None:
        fig = plt.figure(figsize=PLOT_PARAMS['figsize'], dpi=PLOT_PARAMS['dpi'])
        ax = fig.add_subplot(111)
        # Figure'ı gizle ki popup olarak açılmasın
        plt.close(fig)
    
    sns.barplot(x='Metrik', y='Değer', hue='Model', data=metrics_df_melted, palette='viridis', ax=ax)
    ax.set_title('Modellerin Performans Metrikleri Karşılaştırması', fontsize=12, fontweight='bold')
    ax.set_ylabel('Değer', fontsize=10)
    ax.set_xlabel('Metrik', fontsize=10)
    ax.set_ylim(0, 1)
    ax.legend(title='Model', title_fontsize=10, fontsize=9)
    ax.grid(axis='y', linestyle='--', alpha=0.7)


def plot_roc_curves(y_test, y_pred_iso_scores, y_pred_svm_scores, auc_iso, auc_svm, ax=None):
    """
    ROC eğrilerini çizer.
    
    Args:
        y_test: Test etiketleri
        y_pred_iso_scores: Isolation Forest skorları
        y_pred_svm_scores: One-Class SVM skorları
        auc_iso: Isolation Forest AUC skoru
        auc_svm: One-Class SVM AUC skoru
        ax: Matplotlib axis (subplot için)
    """
    # ROC eğrilerini hesapla
    fpr_iso, tpr_iso, _ = roc_curve(y_test, -y_pred_iso_scores)
    fpr_svm, tpr_svm, _ = roc_curve(y_test, -y_pred_svm_scores)
    
    # Grafik oluştur
    if ax is None:
        fig = plt.figure(figsize=PLOT_PARAMS['figsize'], dpi=PLOT_PARAMS['dpi'])
        ax = fig.add_subplot(111)
        # Figure'ı gizle ki popup olarak açılmasın
        plt.close(fig)
    
    ax.plot(fpr_iso, tpr_iso, label=f'Isolation Forest (AUC = {auc_iso:.3f})', linewidth=2)
    ax.plot(fpr_svm, tpr_svm, label=f'One-Class SVM (AUC = {auc_svm:.3f})', linewidth=2)
    ax.plot([0, 1], [0, 1], 'k--', label='Rastgele Tahmin', alpha=0.7)
    ax.set_xlabel('Yanlış Pozitif Oranı (FPR)', fontsize=10)
    ax.set_ylabel('Doğru Pozitif Oranı (TPR)', fontsize=10)
    ax.set_title('Modellerin ROC Eğrisi Karşılaştırması', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)


def plot_precision_recall_curves(y_test, y_pred_iso_scores, y_pred_svm_scores, ax=None):
    """
    Precision-Recall eğrilerini çizer.
    
    Args:
        y_test: Test etiketleri
        y_pred_iso_scores: Isolation Forest skorları
        y_pred_svm_scores: One-Class SVM skorları
        ax: Matplotlib axis (subplot için)
    """
    # Precision-Recall eğrilerini hesapla
    precision_iso, recall_iso, _ = precision_recall_curve(y_test, -y_pred_iso_scores)
    precision_svm, recall_svm, _ = precision_recall_curve(y_test, -y_pred_svm_scores)
    
    # Grafik oluştur
    if ax is None:
        fig = plt.figure(figsize=PLOT_PARAMS['figsize'], dpi=PLOT_PARAMS['dpi'])
        ax = fig.add_subplot(111)
        # Figure'ı gizle ki popup olarak açılmasın
        plt.close(fig)
    
    ax.plot(recall_iso, precision_iso, label='Isolation Forest', linewidth=2)
    ax.plot(recall_svm, precision_svm, label='One-Class SVM', linewidth=2)
    ax.set_xlabel('Duyarlılık (Recall)', fontsize=10)
    ax.set_ylabel('Kesinlik (Precision)', fontsize=10)
    ax.set_title('Modellerin Precision-Recall Eğrisi Karşılaştırması', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)


def plot_anomaly_distribution(X_test, y_pred, model_name):
    """
    Anomali noktalarının dağılımını 2D olarak gösterir (PCA ile).
    
    Args:
        X_test: Test verisi
        y_pred: Tahmin edilen etiketler
        model_name: Model adı
    """
    # PCA ile 2 boyuta indir
    pca = PCA(n_components=2)
    X_test_pca = pca.fit_transform(X_test)
    
    # Grafik oluştur
    fig = plt.figure(figsize=PLOT_PARAMS['figsize'], dpi=PLOT_PARAMS['dpi'])
    ax = fig.add_subplot(111)
    scatter = ax.scatter(X_test_pca[:, 0], X_test_pca[:, 1], c=y_pred, cmap='coolwarm', s=20, alpha=0.7)
    ax.set_xlabel('Ana Bileşen 1', fontsize=12)
    ax.set_ylabel('Ana Bileşen 2', fontsize=12)
    plt.colorbar(scatter, ax=ax, label='Anomali (1) / Normal (0)')
    ax.grid(True, alpha=0.3)
    # Figure'ı gizle ki popup olarak açılmasın
    plt.close(fig)


def plot_confusion_matrices(y_test, y_pred_iso, y_pred_svm, ax1=None, ax2=None):
    """
    Confusion matrix'leri yan yana gösterir.
    
    Args:
        y_test: Test etiketleri
        y_pred_iso: Isolation Forest tahminleri
        y_pred_svm: One-Class SVM tahminleri
        ax1: İlk confusion matrix için axis
        ax2: İkinci confusion matrix için axis
    """
    from sklearn.metrics import confusion_matrix
    
    # Confusion matrix'leri hesapla
    cm_iso = confusion_matrix(y_test, y_pred_iso)
    cm_svm = confusion_matrix(y_test, y_pred_svm)
    
    # Grafik oluştur
    if ax1 is None or ax2 is None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=PLOT_PARAMS['dpi'])
        # Figure'ı gizle ki popup olarak açılmasın
        plt.close(fig)
    
    # Isolation Forest confusion matrix
    sns.heatmap(cm_iso, annot=True, fmt='d', cmap='Blues', ax=ax1)
    ax1.set_title('Isolation Forest Confusion Matrix', fontweight='bold', fontsize=10)
    ax1.set_xlabel('Tahmin Edilen', fontsize=9)
    ax1.set_ylabel('Gerçek', fontsize=9)
    
    # One-Class SVM confusion matrix
    sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Blues', ax=ax2)
    ax2.set_title('One-Class SVM Confusion Matrix', fontweight='bold', fontsize=10)
    ax2.set_xlabel('Tahmin Edilen', fontsize=9)
    ax2.set_ylabel('Gerçek', fontsize=9)


def plot_all_visualizations(y_test, y_pred_iso, y_pred_svm, y_pred_iso_scores, y_pred_svm_scores, 
                           metrics_iso, metrics_svm, X_test_scaled):
    """
    Tüm görselleştirmeleri tek bir uygulama penceresinde sekmeler halinde gösterir.
    
    Args:
        y_test: Test etiketleri
        y_pred_iso: Isolation Forest tahminleri
        y_pred_svm: One-Class SVM tahminleri
        y_pred_iso_scores: Isolation Forest skorları
        y_pred_svm_scores: One-Class SVM skorları
        metrics_iso: Isolation Forest metrikleri
        metrics_svm: One-Class SVM metrikleri
        X_test_scaled: Test verisi (anomali dağılımı için)
    """
    try:
        # Tkinter için TkAgg backend'ini kullan
        import matplotlib
        matplotlib.use('TkAgg')
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        import tkinter as tk
        from tkinter import ttk
    except ImportError:
        print("Tkinter bulunamadı. Basit matplotlib penceresi kullanılıyor...")
        plot_simple_visualizations(y_test, y_pred_iso, y_pred_svm, y_pred_iso_scores, y_pred_svm_scores, 
                                  metrics_iso, metrics_svm, X_test_scaled)
        return
    
    print("\n" + "="*60)
    print("ANOMALİ TESPİT UYGULAMASI AÇILIYOR")
    print("="*60)
    print("Grafikler sekmeler halinde gösterilecek.")
    print("Sekmeler arasında geçiş yapabilirsiniz.")
    print("="*60)
    
    # Ana pencere oluştur
    root = tk.Tk()
    root.title("Anomali Tespit Modelleri - Analiz Uygulaması")
    root.geometry("1400x900")
    root.configure(bg='#f0f0f0')
    
    # Notebook (sekmeler) oluştur
    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Sekme 1: Performans Metrikleri
    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text="📊 Performans Metrikleri")
    
    fig1 = plt.figure(figsize=(12, 8), dpi=100)
    ax1 = fig1.add_subplot(111)
    plot_performance_comparison(metrics_iso, metrics_svm, ax1)
    ax1.set_title('Performans Metrikleri Karşılaştırması', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    canvas1 = FigureCanvasTkAgg(fig1, frame1)
    canvas1.draw()
    canvas1.get_tk_widget().pack(fill='both', expand=True)
    
    toolbar1 = NavigationToolbar2Tk(canvas1, frame1)
    toolbar1.update()
    
    # Sekme 2: ROC Eğrileri
    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text="📈 ROC Eğrileri")
    
    fig2 = plt.figure(figsize=(12, 8), dpi=100)
    ax2 = fig2.add_subplot(111)
    plot_roc_curves(y_test, y_pred_iso_scores, y_pred_svm_scores, 
                   metrics_iso[4], metrics_svm[4], ax2)
    ax2.set_title('ROC Eğrileri Karşılaştırması', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    canvas2 = FigureCanvasTkAgg(fig2, frame2)
    canvas2.draw()
    canvas2.get_tk_widget().pack(fill='both', expand=True)
    
    toolbar2 = NavigationToolbar2Tk(canvas2, frame2)
    toolbar2.update()
    
    # Sekme 3: Precision-Recall Eğrileri
    frame3 = ttk.Frame(notebook)
    notebook.add(frame3, text="📉 Precision-Recall")
    
    fig3 = plt.figure(figsize=(12, 8), dpi=100)
    ax3 = fig3.add_subplot(111)
    plot_precision_recall_curves(y_test, y_pred_iso_scores, y_pred_svm_scores, ax3)
    ax3.set_title('Precision-Recall Eğrileri Karşılaştırması', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    canvas3 = FigureCanvasTkAgg(fig3, frame3)
    canvas3.draw()
    canvas3.get_tk_widget().pack(fill='both', expand=True)
    
    toolbar3 = NavigationToolbar2Tk(canvas3, frame3)
    toolbar3.update()
    
    # Sekme 4: Confusion Matrix'ler
    frame4 = ttk.Frame(notebook)
    notebook.add(frame4, text="🔢 Confusion Matrix")
    
    fig4, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), dpi=100)
    plot_confusion_matrices(y_test, y_pred_iso, y_pred_svm, ax1, ax2)
    plt.suptitle('Confusion Matrix Karşılaştırması', fontsize=16, fontweight='bold', y=0.95)
    plt.tight_layout()
    
    canvas4 = FigureCanvasTkAgg(fig4, frame4)
    canvas4.draw()
    canvas4.get_tk_widget().pack(fill='both', expand=True)
    
    toolbar4 = NavigationToolbar2Tk(canvas4, frame4)
    toolbar4.update()
    
    # Sekme 5: Isolation Forest Anomali Dağılımı
    frame5 = ttk.Frame(notebook)
    notebook.add(frame5, text="🌲 Isolation Forest")
    
    fig5 = plt.figure(figsize=(12, 8), dpi=100)
    ax5 = fig5.add_subplot(111)
    plot_anomaly_distribution_subplot(X_test_scaled, y_pred_iso, "Isolation Forest", ax5)
    ax5.set_title('Isolation Forest - Anomali Dağılımı (PCA)', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    canvas5 = FigureCanvasTkAgg(fig5, frame5)
    canvas5.draw()
    canvas5.get_tk_widget().pack(fill='both', expand=True)
    
    toolbar5 = NavigationToolbar2Tk(canvas5, frame5)
    toolbar5.update()
    
    # Sekme 6: One-Class SVM Anomali Dağılımı
    frame6 = ttk.Frame(notebook)
    notebook.add(frame6, text="🤖 One-Class SVM")
    
    fig6 = plt.figure(figsize=(12, 8), dpi=100)
    ax6 = fig6.add_subplot(111)
    plot_anomaly_distribution_subplot(X_test_scaled, y_pred_svm, "One-Class SVM", ax6)
    ax6.set_title('One-Class SVM - Anomali Dağılımı (PCA)', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    
    canvas6 = FigureCanvasTkAgg(fig6, frame6)
    canvas6.draw()
    canvas6.get_tk_widget().pack(fill='both', expand=True)
    
    toolbar6 = NavigationToolbar2Tk(canvas6, frame6)
    toolbar6.update()
    
    # Alt bilgi paneli
    info_frame = ttk.Frame(root)
    info_frame.pack(fill='x', padx=10, pady=5)
    
    info_label = ttk.Label(info_frame, text="Anomali Tespit Modelleri - Analiz Uygulaması | Her sekmede farklı bir analiz görüntülenir", 
                          font=('Arial', 10))
    info_label.pack(side='left')
    
    # Uygulamayı başlat
    print("Uygulama penceresi açıldı. Sekmeler arasında geçiş yapabilirsiniz.")
    root.mainloop()


def plot_simple_visualizations(y_test, y_pred_iso, y_pred_svm, y_pred_iso_scores, y_pred_svm_scores, 
                              metrics_iso, metrics_svm, X_test_scaled):
    """
    Tkinter yoksa basit matplotlib pencereleri gösterir.
    """
    print("\nTkinter bulunamadı. Grafikler gösterilemiyor.")
    print("Lütfen tkinter kurulumunu kontrol edin veya uygulamayı farklı bir ortamda çalıştırın.")
    print("\nModel sonuçları:")
    print(f"Isolation Forest - F1 Skoru: {metrics_iso[3]:.4f}")
    print(f"One-Class SVM - F1 Skoru: {metrics_svm[3]:.4f}")
    print("En iyi model:", "Isolation Forest" if metrics_iso[3] > metrics_svm[3] else "One-Class SVM")


def plot_anomaly_distribution_subplot(X_test, y_pred, model_name, ax):
    """
    Anomali dağılımını subplot olarak çizer.
    
    Args:
        X_test: Test verisi
        y_pred: Tahmin edilen etiketler
        model_name: Model adı
        ax: Matplotlib axis
    """
    # PCA ile 2 boyuta indir
    pca = PCA(n_components=2)
    X_test_pca = pca.fit_transform(X_test)
    
    # Grafik oluştur
    scatter = ax.scatter(X_test_pca[:, 0], X_test_pca[:, 1], c=y_pred, cmap='coolwarm', s=20, alpha=0.7)
    ax.set_xlabel('Ana Bileşen 1', fontsize=12)
    ax.set_ylabel('Ana Bileşen 2', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Colorbar ekle
    plt.colorbar(scatter, ax=ax, label='Anomali (1) / Normal (0)')


def plot_feature_importance(model, feature_names, top_n=10):
    """
    Özellik önemini gösterir (sadece Isolation Forest için).
    
    Args:
        model: Eğitilmiş model
        feature_names: Özellik isimleri
        top_n: Gösterilecek en önemli özellik sayısı
    """
    if hasattr(model.model, 'feature_importances_'):
        importances = model.model.feature_importances_
        
        # En önemli özellikleri seç
        indices = np.argsort(importances)[::-1][:top_n]
        
        # Grafik oluştur
        plt.figure(figsize=(10, 8), dpi=PLOT_PARAMS['dpi'])
        plt.barh(range(top_n), importances[indices])
        plt.yticks(range(top_n), [feature_names[i] for i in indices])
        plt.xlabel('Özellik Önemi', fontsize=12)
        plt.title(f'En Önemli {top_n} Özellik', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        # Figure'ı gizle ki popup olarak açılmasın
        plt.close()
    else:
        print("Bu model özellik önemini desteklemiyor.")
