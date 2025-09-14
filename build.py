#!/usr/bin/env python3
"""
Anomali Tespit Uygulaması - Build Script
Bu script uygulamayı executable dosyaya çevirir.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Gerekli paketlerin kurulu olup olmadığını kontrol eder."""
    try:
        import PyInstaller
        print("✅ PyInstaller bulundu")
        return True
    except ImportError:
        print("❌ PyInstaller bulunamadı. Kuruluyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0.0"])
        return True

def clean_build():
    """Önceki build dosyalarını temizler."""
    print("🧹 Önceki build dosyaları temizleniyor...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   - {dir_name} klasörü silindi")
    
    # .pyc dosyalarını temizle
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def build_executable():
    """Executable dosyayı oluşturur."""
    print("🔨 Executable dosya oluşturuluyor...")
    
    # PyInstaller komutunu çalıştır
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Tek dosya olarak
        "--windowed",  # GUI uygulaması (console penceresi açılmasın)
        "--name=AnomaliTespitUygulamasi",  # Executable adı
        "--add-data=data:data",  # Veri klasörünü ekle
        "--add-data=config:config",  # Config klasörünü ekle
        "--add-data=models:models",  # Models klasörünü ekle
        "--add-data=services:services",  # Services klasörünü ekle
        "--add-data=utils:utils",  # Utils klasörünü ekle
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=matplotlib.backends.backend_tkagg",
        "--hidden-import=sklearn.ensemble",
        "--hidden-import=sklearn.svm",
        "--hidden-import=sklearn.preprocessing",
        "--hidden-import=sklearn.model_selection",
        "--hidden-import=sklearn.metrics",
        "--hidden-import=sklearn.decomposition",
        "main.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable başarıyla oluşturuldu!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build hatası: {e}")
        return False

def create_release_package():
    """Release paketi oluşturur."""
    print("📦 Release paketi oluşturuluyor...")
    
    # Release klasörü oluştur
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    release_dir.mkdir()
    
    # Executable'ı kopyala
    exe_name = "AnomaliTespitUygulamasi"
    if sys.platform == "win32":
        exe_name += ".exe"
    
    exe_path = Path("dist") / exe_name
    if exe_path.exists():
        shutil.copy2(exe_path, release_dir / exe_name)
        print(f"✅ {exe_name} kopyalandı")
    else:
        print(f"❌ {exe_name} bulunamadı!")
        return False
    
    # README dosyası oluştur
    readme_content = """# Anomali Tespit Uygulaması

Bu uygulama Kadir Can Felek tarafından geliştirilmiştir.

## Kullanım

1. `AnomaliTespitUygulamasi.exe` (Windows) veya `AnomaliTespitUygulamasi` (Mac/Linux) dosyasını çalıştırın
2. Uygulama otomatik olarak örnek veri seti oluşturacak
3. Modeller eğitilecek ve sonuçlar sekmeler halinde gösterilecek

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
"""
    
    with open(release_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README.txt oluşturuldu")
    
    # Veri klasörünü kopyala (boş olsa bile)
    data_dir = release_dir / "data"
    data_dir.mkdir()
    print("✅ data klasörü oluşturuldu")
    
    print(f"\n🎉 Release paketi hazır: {release_dir.absolute()}")
    return True

def main():
    """Ana build fonksiyonu."""
    print("=" * 60)
    print("ANOMALİ TESPİT UYGULAMASI - BUILD SCRIPT")
    print("=" * 60)
    
    # Gereksinimleri kontrol et
    if not check_requirements():
        print("❌ Gereksinimler karşılanamadı!")
        return False
    
    # Temizlik yap
    clean_build()
    
    # Executable oluştur
    if not build_executable():
        print("❌ Build başarısız!")
        return False
    
    # Release paketi oluştur
    if not create_release_package():
        print("❌ Release paketi oluşturulamadı!")
        return False
    
    print("\n" + "=" * 60)
    print("✅ BUILD TAMAMLANDI!")
    print("=" * 60)
    print("Executable dosya: release/AnomaliTespitUygulamasi")
    print("Uygulamayı çalıştırmak için release klasöründeki dosyayı kullanın.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
