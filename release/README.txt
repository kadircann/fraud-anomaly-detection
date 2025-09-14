# Anomali Tespit Uygulaması

Bu uygulama Kadir Can Felek tarafından geliştirilmiştir.

## Kullanım

### macOS:
```bash
# Yöntem 1 - Uygulama olarak (ÖNERİLEN)
open AnomaliTespitUygulamasi.app
# veya Finder'da çift tıklayın

# Yöntem 2 - Terminal'den
./AnomaliTespitUygulamasi

# Yöntem 3 - Launcher script ile
./run.sh
```

### Linux:
```bash
# Yöntem 1 - Direkt çalıştırma
./AnomaliTespitUygulamasi

# Yöntem 2 - Launcher script ile
./run.sh
```

### Windows:
```cmd
AnomaliTespitUygulamasi.exe
```

### Adımlar:
1. Executable dosyasını çalıştırın
2. Uygulama otomatik olarak örnek veri seti oluşturacak
3. Modeller eğitilecek ve sonuçlar sekmeler halinde gösterilecek
4. Hiç popup pencere açılmayacak - sadece ana uygulama penceresi

## Özellikler

- 📊 Performans Metrikleri Karşılaştırması
- 📈 ROC Eğrileri
- 📉 Precision-Recall Eğrileri
- 🔢 Confusion Matrix'ler
- 🌲 Isolation Forest Anomali Dağılımı
- 🤖 One-Class SVM Anomali Dağılımı

## Sistem Gereksinimleri

- Windows 10/11, macOS 10.14+, veya Linux
- En az 4GB RAM
- 100MB boş disk alanı

## Not

Uygulama ilk çalıştırıldığında örnek veri seti oluşturur.
Gerçek veri seti kullanmak için `data/creditcard.csv` dosyasını ekleyin.
