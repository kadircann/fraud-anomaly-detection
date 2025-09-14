@echo off
echo ============================================================
echo ANOMALI TESPIT UYGULAMASI - WINDOWS BUILD SCRIPT
echo ============================================================

echo PyInstaller kuruluyor...
pip install pyinstaller>=5.0.0

echo.
echo Eski build dosyalari temizleniyor...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__

echo.
echo Executable olusturuluyor...
pyinstaller --onefile --windowed --name=AnomaliTespitUygulamasi --add-data="data;data" --add-data="config;config" --add-data="models;models" --add-data="services;services" --add-data="utils;utils" --hidden-import=tkinter --hidden-import=tkinter.ttk --hidden-import=matplotlib.backends.backend_tkagg --hidden-import=sklearn.ensemble --hidden-import=sklearn.svm --hidden-import=sklearn.preprocessing --hidden-import=sklearn.model_selection --hidden-import=sklearn.metrics --hidden-import=sklearn.decomposition main.py

echo.
echo Release paketi olusturuluyor...
if exist release rmdir /s /q release
mkdir release

echo Executable kopyalaniyor...
copy "dist\AnomaliTespitUygulamasi.exe" "release\AnomaliTespitUygulamasi.exe"

echo README dosyasi olusturuluyor...
echo # Anomali Tespit Uygulamasi > release\README.txt
echo. >> release\README.txt
echo Bu uygulama Kadir Can Felek tarafindan gelistirilmistir. >> release\README.txt
echo. >> release\README.txt
echo ## Kullanim >> release\README.txt
echo. >> release\README.txt
echo 1. AnomaliTespitUygulamasi.exe dosyasini calistirin >> release\README.txt
echo 2. Uygulama otomatik olarak ornek veri seti olusturacak >> release\README.txt
echo 3. Modeller egitilecek ve sonuclar sekmeler halinde gosterilecek >> release\README.txt
echo. >> release\README.txt
echo ## Ozellikler >> release\README.txt
echo. >> release\README.txt
echo - Performans Metrikleri Karsilastirmasi >> release\README.txt
echo - ROC Egrileri >> release\README.txt
echo - Precision-Recall Egrileri >> release\README.txt
echo - Confusion Matrix'ler >> release\README.txt
echo - Isolation Forest Anomali Dagilimi >> release\README.txt
echo - One-Class SVM Anomali Dagilimi >> release\README.txt

echo data klasoru olusturuluyor...
mkdir release\data

echo.
echo ============================================================
echo BUILD TAMAMLANDI!
echo ============================================================
echo Executable dosya: release\AnomaliTespitUygulamasi.exe
echo Uygulamayi calistirmak icin release klasorundeki dosyayi kullanin.
echo ============================================================

pause
