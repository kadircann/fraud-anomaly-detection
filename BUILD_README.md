# Anomali Tespit Uygulaması - Executable Build

Bu proje Kadir Can Felek tarafından geliştirilmiştir.

## 🚀 Executable Oluşturma

### macOS için:
```bash
python3 build.py
```

### Windows için:
```cmd
build_windows.bat
```

## 📁 Çıktı Dosyaları

Build işlemi tamamlandıktan sonra `release/` klasöründe şu dosyalar oluşur:

- **AnomaliTespitUygulamasi** (macOS/Linux)
- **AnomaliTespitUygulamasi.exe** (Windows)
- **README.txt** - Kullanım kılavuzu
- **data/** - Veri klasörü

## 🎯 Özellikler

### Uygulama Özellikleri:
- **Tek Pencere**: Tkinter tabanlı modern arayüz
- **Sekmeli Yapı**: 6 farklı analiz sekmesi
- **Interactive Toolbar**: Zoom, pan, kaydetme araçları
- **Cross-Platform**: macOS, Windows ve Linux desteği

### Analiz Sekmeleri:
1. **📊 Performans Metrikleri** - Bar chart karşılaştırması
2. **📈 ROC Eğrileri** - ROC eğrileri karşılaştırması
3. **📉 Precision-Recall** - Precision-Recall eğrileri
4. **🔢 Confusion Matrix** - Yan yana confusion matrix'ler
5. **🌲 Isolation Forest** - Anomali dağılımı (PCA)
6. **🤖 One-Class SVM** - Anomali dağılımı (PCA)

## 💻 Sistem Gereksinimleri

### Minimum Gereksinimler:
- **macOS**: 10.14+ (Mojave)
- **Windows**: 10/11
- **Linux**: Ubuntu 18.04+ veya eşdeğer
- **RAM**: 4GB
- **Disk**: 100MB boş alan

### Önerilen Gereksinimler:
- **RAM**: 8GB+
- **Disk**: 500MB+ boş alan
- **İşlemci**: 4+ çekirdek

## 🔧 Kurulum

1. **Release klasörünü indirin**
2. **Executable dosyayı çalıştırın**:
   - macOS/Linux: `./AnomaliTespitUygulamasi`
   - Windows: `AnomaliTespitUygulamasi.exe`

## 📊 Veri Seti

Uygulama ilk çalıştırıldığında otomatik olarak örnek veri seti oluşturur.

### Gerçek Veri Seti Kullanımı:
1. `data/creditcard.csv` dosyasını indirin
2. Dosyayı `release/data/` klasörüne kopyalayın
3. Uygulamayı yeniden başlatın

## 🐛 Sorun Giderme

### Uygulama Açılmıyor:
- Dosya izinlerini kontrol edin
- Antivirus yazılımını geçici olarak devre dışı bırakın
- Yönetici olarak çalıştırmayı deneyin

### Grafikler Görünmüyor:
- Tkinter kurulumunu kontrol edin
- Sistem Python sürümünü kontrol edin

### Performans Sorunları:
- Daha fazla RAM kullanın
- Diğer uygulamaları kapatın
- SSD kullanın

## 📞 Destek

Sorunlar için:
- GitHub Issues kullanın
- E-posta: [email protected]
- Proje sahibi: Kadir Can Felek

## 📄 Lisans

Bu proje eğitim amaçlı oluşturulmuştır.

---

**Not**: Bu executable dosyası PyInstaller ile oluşturulmuştur ve tüm Python bağımlılıklarını içerir.
